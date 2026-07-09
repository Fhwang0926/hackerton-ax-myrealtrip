from __future__ import annotations

import json
import ssl
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from campaign_copilot.models import CollectContext, CollectorResult, JsonDict
from campaign_copilot.utils import iso_now, load_json, parse_date, strip_html


class CollectorError(Exception):
    """Base collector exception."""


class NetworkError(CollectorError):
    """Raised when a public endpoint cannot be reached."""


@dataclass(frozen=True)
class HttpResponse:
    url: str
    body: str
    tls_verified: bool | None
    tls_policy: str


class BaseCollector:
    name: str = "base"

    def __init__(self, sample_dir: Path) -> None:
        self.sample_dir = sample_dir

    def collect(self, context: CollectContext) -> CollectorResult:
        raise NotImplementedError(f"{self.__class__.__name__} must implement collect")

    def sample_items(self) -> list[JsonDict]:
        path = self.sample_dir / f"{self.name}_sample.json"
        data = load_json(path)
        if not isinstance(data, list):
            raise CollectorError(f"Sample file must contain a list: {path}")
        return [dict(item) for item in data]

    def sample_result(self, error: str | None = None) -> CollectorResult:
        return CollectorResult(
            source=self.name,
            ok=True,
            collected_at=iso_now(),
            items=self.sample_items(),
            error=error,
            meta={
                "source_mode": "sample",
                "public_url": public_url_for(self.name),
                "note": sample_note_for(self.name),
            },
        )


class InstagramCollector(BaseCollector):
    name = "instagram"

    def collect(self, context: CollectContext) -> CollectorResult:
        return self.sample_result(
            "인스타그램 공개 페이지는 소유 계정 내보내기 파일이나 공식 API 없이는 게시글 단위 데이터를 안정적으로 제공하지 않습니다."
        )


class FacebookCollector(BaseCollector):
    name = "facebook"

    def collect(self, context: CollectContext) -> CollectorResult:
        return self.sample_result(
            "페이스북 공개 페이지는 소유 계정 내보내기 파일이나 공식 API 없이는 게시글 단위 데이터를 안정적으로 제공하지 않습니다."
        )


class NaverBlogCollector(BaseCollector):
    name = "naver_blog"
    rss_url = "https://rss.blog.naver.com/myrealtrip.xml"

    def collect(self, context: CollectContext) -> CollectorResult:
        if context.use_live:
            try:
                response = fetch_text(self.rss_url)
                items = parse_naver_blog_rss(response.body)
                if items:
                    return CollectorResult(
                        source=self.name,
                        ok=True,
                        collected_at=iso_now(),
                        items=items[: context.max_items_per_source],
                        meta={
                            "source_mode": "live",
                            "public_url": self.rss_url,
                            "tls_verified": response.tls_verified,
                            "tls_policy": response.tls_policy,
                        },
                    )
            except (CollectorError, ET.ParseError) as exc:
                if context.use_sample:
                    return self.sample_result(str(exc))
                return failed_result(self.name, str(exc))
        return self.sample_result()


class NewsCollector(BaseCollector):
    name = "news"
    keywords = ("일본 여행", "동남아 여행", "여름휴가", "항공권", "마이리얼트립")

    def collect(self, context: CollectContext) -> CollectorResult:
        if context.use_live:
            try:
                items: list[JsonDict] = []
                tls_verified = True
                for keyword in self.keywords:
                    query = urllib.parse.quote(keyword)
                    url = (
                        "https://news.google.com/rss/search?"
                        f"q={query}&hl=ko&gl=KR&ceid=KR:ko"
                    )
                    response = fetch_text(url)
                    tls_verified = tls_verified and response.tls_verified
                    for item in parse_news_rss(response.body, keyword):
                        items.append(item)
                    if len(items) >= context.max_items_per_source:
                        break
                if items:
                    return CollectorResult(
                        source=self.name,
                        ok=True,
                        collected_at=iso_now(),
                        items=items[: context.max_items_per_source],
                        meta={
                            "source_mode": "live",
                            "public_url": "https://news.google.com/rss",
                            "tls_verified": tls_verified,
                            "tls_policy": "certificate_verification_disabled",
                        },
                    )
            except (CollectorError, ET.ParseError) as exc:
                if context.use_sample:
                    return self.sample_result(str(exc))
                return failed_result(self.name, str(exc))
        return self.sample_result()


class ExchangeRateCollector(BaseCollector):
    name = "exchange"
    url = "https://api.frankfurter.app/latest?from=KRW&to=JPY,USD,EUR,THB,PHP,VND,CNY"

    def collect(self, context: CollectContext) -> CollectorResult:
        if context.use_live:
            try:
                response = fetch_text(self.url)
                payload = json.loads(response.body)
                items = parse_exchange(payload)
                if items:
                    return CollectorResult(
                        source=self.name,
                        ok=True,
                        collected_at=iso_now(),
                        items=items,
                        meta={
                            "source_mode": "live",
                            "public_url": self.url,
                            "tls_verified": response.tls_verified,
                            "tls_policy": response.tls_policy,
                        },
                    )
            except (CollectorError, json.JSONDecodeError) as exc:
                if context.use_sample:
                    return self.sample_result(str(exc))
                return failed_result(self.name, str(exc))
        return self.sample_result()


class WeatherCollector(BaseCollector):
    name = "weather"
    cities: dict[str, tuple[float, float, str]] = {
        "Fukuoka": (33.5902, 130.4017, "JP"),
        "Osaka": (34.6937, 135.5023, "JP"),
        "Da Nang": (16.0471, 108.2068, "VN"),
        "Cebu": (10.3157, 123.8854, "PH"),
        "Jeju": (33.4996, 126.5312, "KR"),
        "Phuket": (7.8804, 98.3923, "TH"),
    }

    def collect(self, context: CollectContext) -> CollectorResult:
        if context.use_live:
            try:
                items: list[JsonDict] = []
                tls_verified = True
                for city, (lat, lon, country) in self.cities.items():
                    url = (
                        "https://api.open-meteo.com/v1/forecast?"
                        f"latitude={lat}&longitude={lon}"
                        "&daily=weather_code,temperature_2m_max"
                        "&forecast_days=3&timezone=Asia%2FSeoul"
                    )
                    response = fetch_text(url)
                    tls_verified = tls_verified and response.tls_verified
                    items.extend(parse_weather(city, country, response.body))
                if items:
                    return CollectorResult(
                        source=self.name,
                        ok=True,
                        collected_at=iso_now(),
                        items=items[: context.max_items_per_source],
                        meta={
                            "source_mode": "live",
                            "public_url": "https://open-meteo.com/",
                            "tls_verified": tls_verified,
                            "tls_policy": "certificate_verification_disabled",
                        },
                    )
            except (CollectorError, json.JSONDecodeError) as exc:
                if context.use_sample:
                    return self.sample_result(str(exc))
                return failed_result(self.name, str(exc))
        return self.sample_result()


class HolidayCollector(BaseCollector):
    name = "holiday"

    def collect(self, context: CollectContext) -> CollectorResult:
        return self.sample_result("휴일 수집기는 현재 정적 공개 캘린더 샘플을 사용합니다.")


class FlightPriceCollector(BaseCollector):
    name = "flight_price"

    def collect(self, context: CollectContext) -> CollectorResult:
        return self.sample_result("항공권 가격 실데이터 수집에는 제휴 데이터나 사용자 업로드 파일이 필요합니다.")


def public_url_for(source: str) -> str:
    urls = {
        "instagram": "https://www.instagram.com/myrealtrip",
        "facebook": "https://www.facebook.com/myRealTrip",
        "naver_blog": "https://rss.blog.naver.com/myrealtrip.xml",
        "news": "https://news.google.com/rss",
        "exchange": "https://api.frankfurter.app/",
        "weather": "https://open-meteo.com/",
        "holiday": "public holiday calendar sample",
        "flight_price": "user or partner export sample",
    }
    return urls.get(source, "unknown")


def sample_note_for(source: str) -> str:
    if source in {"instagram", "facebook"}:
        return "게시글 단위 실데이터 수집에는 소유 계정 내보내기 파일이나 공식 API 권한이 필요합니다."
    return "공개 데이터 수집이 불가능할 때 사용하는 샘플 대체 데이터입니다."


def failed_result(source: str, error: str) -> CollectorResult:
    return CollectorResult(source=source, ok=False, collected_at=iso_now(), items=[], error=error)


def fetch_text(url: str, timeout: int = 12) -> HttpResponse:
    context = ssl._create_unverified_context()
    try:
        return open_text(url, timeout=timeout, context=context, tls_verified=None)
    except OSError as exc:
        raise NetworkError(f"Could not fetch {url}: {exc}") from exc


def open_text(
    url: str,
    timeout: int,
    context: ssl.SSLContext | None,
    tls_verified: bool | None,
) -> HttpResponse:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 MyRealTripWeeklyCampaignCopilot/0.1",
            "Accept": "application/rss+xml,application/json,text/html;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        body = response.read().decode(charset, errors="replace")
        return HttpResponse(
            url=url,
            body=body,
            tls_verified=tls_verified,
            tls_policy="certificate_verification_disabled",
        )


def parse_naver_blog_rss(xml_text: str) -> list[JsonDict]:
    root = ET.fromstring(xml_text)
    items: list[JsonDict] = []
    for item in root.findall("./channel/item"):
        title = text_from_xml(item, "title")
        description = text_from_xml(item, "description")
        link = text_from_xml(item, "link")
        tags = [tag.strip() for tag in text_from_xml(item, "tag").split(",") if tag.strip()]
        items.append(
            {
                "source": "naver_blog",
                "source_type": "owned_channel",
                "platform": "naver_blog",
                "title": title,
                "body": strip_html(description),
                "published_at": parse_date(text_from_xml(item, "pubDate")),
                "url": link.replace("?fromRss=true&trackingCode=rss", ""),
                "tags": tags,
                "category": text_from_xml(item, "category"),
            }
        )
    return items


def parse_news_rss(xml_text: str, keyword: str) -> list[JsonDict]:
    root = ET.fromstring(xml_text)
    rows: list[JsonDict] = []
    for item in root.findall("./channel/item"):
        rows.append(
            {
                "source": "news",
                "source_type": "public_signal",
                "title": strip_html(text_from_xml(item, "title")),
                "body": strip_html(text_from_xml(item, "description")),
                "published_at": parse_date(text_from_xml(item, "pubDate")),
                "url": text_from_xml(item, "link"),
                "keyword": keyword,
            }
        )
    return rows


def parse_exchange(payload: dict[str, Any]) -> list[JsonDict]:
    date_value = str(payload.get("date", "")) or iso_now()[:10]
    rates = payload.get("rates", {})
    rows: list[JsonDict] = []
    if not isinstance(rates, dict):
        return rows
    for currency, value in rates.items():
        numeric = float(value)
        krw_per_unit = round(1 / numeric, 4) if numeric else 0.0
        rows.append(
            {
                "source": "exchange_rate",
                "source_type": "public_signal",
                "currency": currency,
                "base": "KRW",
                "rate": krw_per_unit,
                "change_7d": None,
                "observed_at": date_value,
            }
        )
    return rows


def parse_weather(city: str, country: str, body: str) -> list[JsonDict]:
    payload = json.loads(body)
    daily = payload.get("daily", {})
    dates = daily.get("time", [])
    codes = daily.get("weather_code", [])
    temps = daily.get("temperature_2m_max", [])
    rows: list[JsonDict] = []
    for index, day in enumerate(dates):
        code = int(codes[index]) if index < len(codes) else 0
        temp = float(temps[index]) if index < len(temps) else 0.0
        rows.append(
            {
                "source": "weather",
                "source_type": "public_signal",
                "city": city,
                "country": country,
                "date": str(day),
                "condition": weather_condition(code),
                "temperature_max": temp,
            }
        )
    return rows


def weather_condition(code: int) -> str:
    if code in {0, 1}:
        return "clear"
    if code in {2, 3, 45, 48}:
        return "cloudy"
    if code in {51, 53, 55, 61, 63, 65, 80, 81, 82}:
        return "rain"
    if code in {95, 96, 99}:
        return "storm"
    return "mixed"


def text_from_xml(element: ET.Element, tag: str) -> str:
    found = element.find(tag)
    if found is None or found.text is None:
        return ""
    return found.text.strip()


def build_collectors(sample_dir: Path) -> list[BaseCollector]:
    return [
        InstagramCollector(sample_dir),
        FacebookCollector(sample_dir),
        NaverBlogCollector(sample_dir),
        NewsCollector(sample_dir),
        ExchangeRateCollector(sample_dir),
        WeatherCollector(sample_dir),
        HolidayCollector(sample_dir),
        FlightPriceCollector(sample_dir),
    ]
