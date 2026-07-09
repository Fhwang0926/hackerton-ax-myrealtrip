from __future__ import annotations

from campaign_copilot.models import Campaign, Recommendation


def plan_campaign(week: str, recommendations: list[Recommendation]) -> Campaign:
    if not recommendations:
        raise ValueError("At least one recommendation is required to build a campaign")
    top = recommendations[0]
    target = target_for(top.destination)
    cta = cta_for(top)
    return Campaign(
        campaign_id=f"{week}-001",
        theme=f"{top.destination} 근거 기반 주간 캠페인",
        target=target,
        destination=top.destination,
        objective="예약 전환",
        channels=top.recommended_channels,
        cta=cta,
        evidence=top.reasons,
    )


def target_for(destination: str) -> str:
    if destination in {"다낭", "세부/보홀", "제주"}:
        return "가족 여행과 첫 자유여행을 준비하는 20~40대"
    if destination in {"후쿠오카", "오사카"}:
        return "짧은 휴가로 해외여행을 떠나려는 20~30대 자유여행객"
    return "테마가 분명한 여행을 찾는 20~40대 고객"


def cta_for(recommendation: Recommendation) -> str:
    if recommendation.opportunity >= 12:
        return "이번 주 특가 보기"
    return "추천 일정 확인하기"
