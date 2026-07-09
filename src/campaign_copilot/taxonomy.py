from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DestinationRule:
    destination: str
    country: str
    city: str
    region: str
    travel_type: str
    keywords: tuple[str, ...]


DESTINATIONS: tuple[DestinationRule, ...] = (
    DestinationRule("후쿠오카", "Japan", "Fukuoka", "Japan", "food", ("후쿠오카", "fukuoka", "야타이")),
    DestinationRule("오사카", "Japan", "Osaka", "Japan", "city", ("오사카", "osaka", "교토", "고베")),
    DestinationRule("다낭", "Vietnam", "Da Nang", "Vietnam", "family", ("다낭", "da nang", "바나힐")),
    DestinationRule("세부/보홀", "Philippines", "Cebu", "Philippines", "beach", ("세부", "보홀", "cebu", "bohol")),
    DestinationRule("푸켓", "Thailand", "Phuket", "Thailand", "beach", ("푸켓", "phuket", "피피섬", "라차섬")),
    DestinationRule("치앙마이", "Thailand", "Chiang Mai", "Thailand", "nature", ("치앙마이", "chiang mai", "도이수텝", "코끼리")),
    DestinationRule("제주", "Korea", "Jeju", "Korea", "family", ("제주", "jeju")),
    DestinationRule("하와이", "United States", "Honolulu", "United States", "luxury", ("하와이", "hawaii", "호놀룰루", "hnl")),
    DestinationRule("시안", "China", "Xian", "China", "culture", ("시안", "서안", "xian", "병마용", "차카염호")),
    DestinationRule("몽골", "Mongolia", "Ulaanbaatar", "Mongolia", "nature", ("몽골", "mongolia", "고비", "홉스골")),
)

CURRENCY_REGION: dict[str, str] = {
    "JPY": "Japan",
    "VND": "Vietnam",
    "PHP": "Philippines",
    "THB": "Thailand",
    "USD": "United States",
    "CNY": "China",
    "KRW": "Korea",
}

AIRPORT_REGION: dict[str, str] = {
    "FUK": "Japan",
    "KIX": "Japan",
    "DAD": "Vietnam",
    "CEB": "Philippines",
    "CJU": "Korea",
    "HNL": "United States",
}


def detect_destination(text: str) -> DestinationRule | None:
    lowered = text.lower()
    for rule in DESTINATIONS:
        if any(keyword.lower() in lowered for keyword in rule.keywords):
            return rule
    return None


def destination_by_region(region: str) -> list[DestinationRule]:
    return [rule for rule in DESTINATIONS if rule.region.lower() == region.lower()]


def season_for_month(month: int) -> str:
    if month in {3, 4, 5}:
        return "spring"
    if month in {6, 7, 8}:
        return "summer"
    if month in {9, 10, 11}:
        return "autumn"
    return "winter"


def extract_cta(text: str) -> str | None:
    candidates = ("예약", "특가", "할인", "혜택", "확인", "보기")
    if any(candidate in text for candidate in candidates):
        return "이번 주 특가 보기"
    return None


def detect_campaign_type(text: str) -> str:
    if any(word in text for word in ("할인", "특가", "혜택", "이벤트")):
        return "promotion"
    if any(word in text for word in ("코스", "정리", "추천", "비교")):
        return "guide"
    return "inspiration"
