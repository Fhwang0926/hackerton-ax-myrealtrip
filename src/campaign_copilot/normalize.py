from __future__ import annotations

from datetime import date
from typing import Iterable

from campaign_copilot.models import CollectorResult, ContentItem, JsonDict, PublicSignal
from campaign_copilot.taxonomy import (
    AIRPORT_REGION,
    CURRENCY_REGION,
    detect_campaign_type,
    detect_destination,
    destination_by_region,
    extract_cta,
    season_for_month,
)
from campaign_copilot.utils import stable_id


OWNED_SOURCES = {"instagram", "facebook", "naver_blog"}


def normalize_results(results: Iterable[CollectorResult]) -> tuple[list[ContentItem], list[PublicSignal]]:
    contents: list[ContentItem] = []
    signals: list[PublicSignal] = []
    for result in results:
        source_mode = str(result.meta.get("source_mode", "unknown"))
        for item in result.items:
            if result.source in OWNED_SOURCES:
                contents.append(normalize_content_item(item, source_mode))
            else:
                normalized = normalize_signal_item(item, source_mode)
                if normalized:
                    signals.append(normalized)
    return contents, signals


def normalize_content_item(item: JsonDict, source_mode: str) -> ContentItem:
    body = str(item.get("body", ""))
    title = str(item.get("title", ""))
    text = f"{title} {body} {' '.join(item.get('hashtags', []))} {' '.join(item.get('tags', []))}"
    destination = detect_destination(text)
    published_at = str(item.get("published_at") or date.today().isoformat())
    month = int(published_at[5:7]) if len(published_at) >= 7 and published_at[5:7].isdigit() else 1
    hashtags = list(item.get("hashtags") or item.get("tags") or [])
    return ContentItem(
        id=stable_id(str(item.get("source", "")), published_at, title),
        platform=str(item.get("platform") or item.get("source") or "unknown"),
        source=str(item.get("source_type") or "owned_channel"),
        published_at=published_at,
        title=title,
        body=body,
        country=destination.country if destination else None,
        city=destination.city if destination else None,
        travel_type=destination.travel_type if destination else None,
        season=season_for_month(month),
        campaign_type=str(item.get("campaign_type") or detect_campaign_type(text)),
        promotion=any(word in text for word in ("할인", "특가", "혜택", "이벤트")),
        cta=extract_cta(text),
        hashtags=hashtags,
        media_type=str(item.get("media_type") or "article"),
        topics=extract_topics(text),
        sentiment=None,
        url=str(item.get("url") or ""),
        source_mode=source_mode,
    )


def normalize_signal_item(item: JsonDict, source_mode: str) -> PublicSignal | None:
    source = str(item.get("source", ""))
    if source == "news":
        return normalize_news_signal(item, source_mode)
    if source == "exchange_rate":
        return normalize_exchange_signal(item, source_mode)
    if source == "weather":
        return normalize_weather_signal(item, source_mode)
    if source == "holiday":
        return normalize_holiday_signal(item, source_mode)
    if source == "flight_price":
        return normalize_flight_signal(item, source_mode)
    return None


def normalize_news_signal(item: JsonDict, source_mode: str) -> PublicSignal:
    title = str(item.get("title") or "")
    body = str(item.get("body") or "")
    text = f"{title} {body} {item.get('keyword', '')}"
    destination = detect_destination(text)
    region = destination.region if destination else region_from_text(text)
    return PublicSignal(
        signal_type="news",
        region=region,
        metric=str(item.get("keyword") or "travel_news"),
        value=1.0,
        observed_at=str(item.get("published_at") or date.today().isoformat()),
        title=title,
        url=str(item.get("url") or ""),
        source="news",
        source_mode=source_mode,
    )


def normalize_exchange_signal(item: JsonDict, source_mode: str) -> PublicSignal:
    currency = str(item.get("currency", ""))
    return PublicSignal(
        signal_type="exchange_rate",
        region=CURRENCY_REGION.get(currency, "General"),
        metric=f"{currency}_KRW",
        value=float(item.get("rate") or 0.0),
        change_7d=optional_float(item.get("change_7d")),
        observed_at=str(item.get("observed_at") or date.today().isoformat()),
        title=f"{currency}/KRW exchange rate",
        url="https://api.frankfurter.app/",
        source="exchange_rate",
        source_mode=source_mode,
    )


def normalize_weather_signal(item: JsonDict, source_mode: str) -> PublicSignal:
    city = str(item.get("city") or "")
    rule = detect_destination(city)
    return PublicSignal(
        signal_type="weather",
        region=rule.region if rule else city,
        metric=str(item.get("condition") or "weather"),
        value=float(item.get("temperature_max") or 0.0),
        observed_at=str(item.get("date") or date.today().isoformat()),
        title=f"{city} weather: {item.get('condition', 'unknown')}",
        url="https://open-meteo.com/",
        source="weather",
        source_mode=source_mode,
    )


def normalize_holiday_signal(item: JsonDict, source_mode: str) -> PublicSignal:
    country = str(item.get("country") or "")
    region = {"JP": "Japan", "KR": "Korea"}.get(country, country or "General")
    return PublicSignal(
        signal_type="holiday",
        region=region,
        metric=str(item.get("name") or "holiday"),
        value=1.0 if item.get("is_long_weekend") else 0.5,
        observed_at=str(item.get("date") or date.today().isoformat()),
        title=str(item.get("name") or "Holiday"),
        url="public holiday calendar sample",
        source="holiday",
        source_mode=source_mode,
    )


def normalize_flight_signal(item: JsonDict, source_mode: str) -> PublicSignal:
    airport = str(item.get("destination") or "")
    region = AIRPORT_REGION.get(airport, "General")
    title = f"{item.get('origin', '')}-{airport} fare {item.get('price', '')}"
    return PublicSignal(
        signal_type="flight_price",
        region=region,
        metric=airport,
        value=float(item.get("price") or 0.0),
        change_7d=optional_float(item.get("change_7d")),
        observed_at=str(item.get("date_range") or date.today().isoformat()),
        title=title,
        url="user or partner export sample",
        source="flight_price",
        source_mode=source_mode,
    )


def extract_topics(text: str) -> list[str]:
    topics: list[str] = []
    topic_words = {
        "food": ("미식", "맛집", "야타이"),
        "family": ("가족", "아이", "렌터카"),
        "beach": ("호핑", "섬", "바다", "휴양"),
        "promotion": ("할인", "특가", "혜택", "이벤트"),
        "guide": ("코스", "정리", "비교", "추천"),
    }
    for topic, words in topic_words.items():
        if any(word in text for word in words):
            topics.append(topic)
    return topics


def region_from_text(text: str) -> str:
    rules = {
        "Japan": ("일본", "엔저", "도쿄", "후쿠오카", "오사카", "교토"),
        "Vietnam": ("베트남", "다낭", "나트랑"),
        "Philippines": ("필리핀", "세부", "보홀"),
        "Thailand": ("태국", "방콕", "푸켓", "치앙마이"),
        "Korea": ("제주", "국내여행", "한국"),
        "United States": ("하와이", "호놀룰루"),
        "China": ("중국", "시안", "칭다오"),
        "Mongolia": ("몽골", "고비", "홉스골"),
    }
    lowered = text.lower()
    for region, keywords in rules.items():
        if any(keyword.lower() in lowered for keyword in keywords):
            return region
    return "General"


def optional_float(value: object) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def summarize_sns(contents: list[ContentItem]) -> list[JsonDict]:
    rows: list[JsonDict] = []
    for platform in sorted({item.platform for item in contents}):
        platform_items = [item for item in contents if item.platform == platform]
        city_counts: dict[str, int] = {}
        for item in platform_items:
            if item.city:
                city_counts[item.city] = city_counts.get(item.city, 0) + 1
        top_city = max(city_counts, key=city_counts.get) if city_counts else "Unknown"
        rows.append(
            {
                "platform": platform,
                "post_count": len(platform_items),
                "top_destination": top_city,
                "promotion_count": sum(1 for item in platform_items if item.promotion),
                "source_modes": sorted({item.source_mode for item in platform_items}),
            }
        )
    return rows


def destinations_for_region(region: str) -> list[str]:
    return [rule.destination for rule in destination_by_region(region)]
