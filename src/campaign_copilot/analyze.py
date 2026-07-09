from __future__ import annotations

from collections import defaultdict

from campaign_copilot.models import ContentItem, JsonDict, PublicSignal, Recommendation
from campaign_copilot.taxonomy import DESTINATIONS


WEIGHTS: dict[str, float] = {
    "news": 0.25,
    "sns": 0.20,
    "exchange_rate": 0.15,
    "holiday": 0.15,
    "weather": 0.10,
    "tourism": 0.10,
    "flight_price": 0.05,
}


def analyze_trends(
    contents: list[ContentItem],
    signals: list[PublicSignal],
    top_n: int = 3,
) -> list[Recommendation]:
    scored: list[Recommendation] = []
    for rule in DESTINATIONS:
        evidence: list[JsonDict] = []
        sns_score = score_sns(rule.destination, rule.city, contents, evidence)
        signal_score, opportunity, risk = score_public_signals(rule.region, rule.city, signals, evidence)
        base = (sns_score * WEIGHTS["sns"]) + signal_score
        final_score = clamp(base + opportunity - risk, 0.0, 100.0)
        if final_score <= 0:
            continue
        reasons = build_reasons(rule.destination, evidence, opportunity, risk)
        confidence = clamp(0.45 + min(len(evidence), 8) * 0.06, 0.45, 0.92)
        scored.append(
            Recommendation(
                destination=rule.destination,
                score=round(final_score, 1),
                confidence=round(confidence, 2),
                opportunity=round(opportunity, 1),
                risk=round(risk, 1),
                reasons=reasons,
                recommended_channels=recommend_channels(rule.destination, contents),
                evidence=evidence[:8],
            )
        )
    scored.sort(key=lambda item: item.score, reverse=True)
    return scored[:top_n]


def score_sns(
    destination: str,
    city: str,
    contents: list[ContentItem],
    evidence: list[JsonDict],
) -> float:
    mentions = [
        item
        for item in contents
        if destination in f"{item.title} {item.body}" or city.lower() in f"{item.city}".lower()
    ]
    if not mentions:
        evidence.append(
            {
                "type": "sns_gap",
                "title": f"{destination} owned-channel exposure is low",
                "detail": "최근 자사 채널 노출이 적어 캠페인 보강 여지가 있습니다.",
                "source_mode": "derived",
            }
        )
        return 18.0
    for item in mentions[:3]:
        evidence.append(
            {
                "type": "owned_channel",
                "title": item.title,
                "detail": f"{item.platform} {item.published_at}",
                "url": item.url,
                "source_mode": item.source_mode,
            }
        )
    return min(mentions_count_score(len(mentions)), 70.0)


def score_public_signals(
    region: str,
    city: str,
    signals: list[PublicSignal],
    evidence: list[JsonDict],
) -> tuple[float, float, float]:
    by_type: dict[str, list[PublicSignal]] = defaultdict(list)
    for signal in signals:
        if signal.region.lower() in {region.lower(), city.lower()}:
            by_type[signal.signal_type].append(signal)
    weighted = 0.0
    opportunity = 0.0
    risk = 0.0
    for signal_type, rows in by_type.items():
        if signal_type == "news":
            weighted += min(len(rows) * 18.0, 85.0) * WEIGHTS["news"]
            opportunity += min(len(rows) * 4.0, 18.0)
        if signal_type == "exchange_rate":
            weighted += exchange_score(rows) * WEIGHTS["exchange_rate"]
            opportunity += exchange_opportunity(rows)
        if signal_type == "holiday":
            weighted += min(sum(row.value for row in rows) * 40.0, 80.0) * WEIGHTS["holiday"]
            opportunity += 8.0
        if signal_type == "weather":
            weather_value, weather_risk = weather_scores(rows)
            weighted += weather_value * WEIGHTS["weather"]
            risk += weather_risk
        if signal_type == "flight_price":
            weighted += flight_score(rows) * WEIGHTS["flight_price"]
            opportunity += flight_opportunity(rows)
    for row in flatten_signal_rows(by_type)[:5]:
        evidence.append(signal_evidence(row))
    return weighted, min(opportunity, 35.0), min(risk, 40.0)


def mentions_count_score(count: int) -> float:
    return 24.0 + min(count * 14.0, 46.0)


def exchange_score(rows: list[PublicSignal]) -> float:
    score = 20.0
    for row in rows:
        if row.change_7d is not None and row.change_7d < 0:
            score += min(abs(row.change_7d) * 10.0, 30.0)
    return min(score, 80.0)


def exchange_opportunity(rows: list[PublicSignal]) -> float:
    return sum(min(abs(row.change_7d or 0.0) * 3.0, 10.0) for row in rows if (row.change_7d or 0) < 0)


def weather_scores(rows: list[PublicSignal]) -> tuple[float, float]:
    score = 20.0
    risk = 0.0
    for row in rows:
        metric = row.metric.lower()
        if metric in {"clear", "cloudy"}:
            score += 12.0
        if metric == "rain":
            risk += 8.0
        if metric == "storm":
            risk += 25.0
    return min(score, 80.0), min(risk, 40.0)


def flight_score(rows: list[PublicSignal]) -> float:
    score = 15.0
    for row in rows:
        if row.change_7d is not None and row.change_7d < 0:
            score += min(abs(row.change_7d) * 4.0, 35.0)
    return min(score, 70.0)


def flight_opportunity(rows: list[PublicSignal]) -> float:
    return sum(min(abs(row.change_7d or 0.0), 12.0) for row in rows if (row.change_7d or 0) < 0)


def flatten_signal_rows(by_type: dict[str, list[PublicSignal]]) -> list[PublicSignal]:
    rows: list[PublicSignal] = []
    for signal_type in ("news", "exchange_rate", "holiday", "weather", "flight_price"):
        rows.extend(by_type.get(signal_type, []))
    return rows


def signal_evidence(row: PublicSignal) -> JsonDict:
    return {
        "type": row.signal_type,
        "title": row.title,
        "detail": f"{row.metric}: {row.value}",
        "url": row.url,
        "source_mode": row.source_mode,
    }


def build_reasons(
    destination: str,
    evidence: list[JsonDict],
    opportunity: float,
    risk: float,
) -> list[str]:
    reasons = [f"{destination} 관련 공개 신호와 자사 채널 근거가 확인되었습니다."]
    if any(item.get("type") == "sns_gap" for item in evidence):
        reasons.append("최근 자사 채널 노출이 적어 신규 캠페인 여지가 있습니다.")
    if opportunity >= 10:
        reasons.append("환율, 항공권, 뉴스 중 하나 이상의 기회 신호가 있습니다.")
    if risk >= 15:
        reasons.append("날씨 리스크가 있어 메시지는 일정 유연성을 강조해야 합니다.")
    if len(reasons) < 3:
        reasons.append("추천 근거가 리포트 evidence 섹션에 연결되어 있습니다.")
    return reasons[:4]


def recommend_channels(destination: str, contents: list[ContentItem]) -> list[str]:
    recent_platforms = {
        item.platform
        for item in contents
        if destination in f"{item.title} {item.body}" or destination in f"{item.city}"
    }
    channels = ["instagram", "naver_blog"]
    if "facebook" not in recent_platforms:
        channels.append("facebook")
    return channels


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(value, upper))
