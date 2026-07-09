from __future__ import annotations

from campaign_copilot.models import Campaign, GeneratedAssets, Recommendation
from campaign_copilot.utils import truncate


CHANNEL_IMAGE_ASSETS = {
    "instagram": {
        "path": "assets/instagram-campaign.png",
        "label": "인스타그램 캠페인 이미지",
    },
    "facebook": {
        "path": "assets/facebook-campaign.png",
        "label": "페이스북 캠페인 이미지",
    },
    "naver_blog": {
        "path": "assets/naver-blog-campaign.png",
        "label": "네이버 블로그 대표 이미지",
    },
}


def generate_assets(campaign: Campaign, recommendations: list[Recommendation]) -> GeneratedAssets:
    top = recommendations[0]
    evidence_lines = "\n".join(f"- {reason}" for reason in top.reasons)
    instagram_prompt = render_channel_image_prompt(campaign, "instagram")
    facebook_prompt = render_channel_image_prompt(campaign, "facebook")
    naver_blog_prompt = render_channel_image_prompt(campaign, "naver_blog")
    instagram = render_instagram(campaign, top, instagram_prompt)
    facebook = render_facebook(campaign, top, evidence_lines, facebook_prompt)
    naver_blog = render_naver_blog(campaign, top, evidence_lines, naver_blog_prompt)
    image_prompt = render_image_prompt(campaign)
    landing_summary = render_landing_summary(campaign, top)
    assets = {
        "campaign_id": campaign.campaign_id,
        "destination": campaign.destination,
        "channels": campaign.channels,
        "cta": campaign.cta,
        "image_prompts": {
            "instagram": instagram_prompt,
            "facebook": facebook_prompt,
            "naver_blog": naver_blog_prompt,
        },
        "image_outputs": {
            channel: data["path"] for channel, data in CHANNEL_IMAGE_ASSETS.items()
        },
        "formats": ["instagram.md", "facebook.md", "naver_blog.md", "image_prompt.md"],
    }
    return GeneratedAssets(
        instagram=instagram,
        facebook=facebook,
        naver_blog=naver_blog,
        image_prompt=image_prompt,
        landing_summary=landing_summary,
        assets=assets,
    )


def render_instagram(
    campaign: Campaign,
    recommendation: Recommendation,
    image_prompt: str,
) -> str:
    hook = truncate(f"이번 주 {campaign.destination} 여행", 25)
    tags = hashtags_for(campaign.destination)
    evidence_note = short_evidence_note(recommendation)
    return (
        f"# {hook}\n\n"
        f"{render_image_attachment('instagram')}"
        "## 복사 영역\n\n"
        "```text\n"
        f"이번 주 짧게 떠날 여행지를 찾고 있다면 {campaign.destination}를 먼저 확인해보세요.\n\n"
        f"{campaign.destination}는 먹거리, 쇼핑, 근교 일정까지 한 번에 잡기 좋아 "
        "첫 해외여행부터 재방문 여행까지 부담 없이 고르기 좋은 도시입니다.\n"
        f"이번 주 공개 여행 신호와 마이리얼트립 공개 채널 반응을 함께 봤을 때도 {campaign.destination} 관련 관심이 확인됐어요.\n\n"
        "추천 일정은 이렇게 잡아보세요.\n"
        f"- 1일차: {campaign.destination} 도착 후 중심가 산책과 로컬 맛집\n"
        "- 2일차: 대표 명소와 쇼핑 코스\n"
        "- 3일차: 근교 또는 여유 일정 후 귀국\n\n"
        f"여행 준비는 복잡하게 미루지 말고, {campaign.cta}.\n\n"
        f"{tags}\n"
        "```\n\n"
        f"{render_image_prompt_block('instagram', image_prompt)}"
        "## 운영 메모\n\n"
        f"- 추천 근거: {evidence_note}\n"
        "- 권장 소재: 피드 4:5 이미지 1장, 스토리 9:16 버전 1장\n"
        "- 본문은 위 `복사 영역`만 그대로 복사해서 사용하면 됩니다.\n"
    )


def render_facebook(
    campaign: Campaign,
    recommendation: Recommendation,
    evidence_lines: str,
    image_prompt: str,
) -> str:
    return (
        f"# {campaign.theme}\n\n"
        f"{render_image_attachment('facebook')}"
        "## 복사 영역\n\n"
        "```text\n"
        f"이번 주 마이리얼트립이 추천하는 여행지는 {campaign.destination}입니다.\n\n"
        f"{campaign.target}이라면, 긴 휴가를 내지 않아도 충분히 다녀올 수 있는 여행지가 필요합니다. "
        f"{campaign.destination}는 이동 부담은 낮추고, 맛집과 쇼핑, 대표 명소, 근교 일정까지 한 번에 담기 좋은 선택지입니다.\n\n"
        "이번 추천은 단순한 감이 아니라 공개 여행 신호와 자사 공개 채널 반응을 함께 확인해 정리했습니다.\n"
        f"- {safe_reason(recommendation, 0)}\n"
        f"- {safe_reason(recommendation, 1)}\n"
        f"- {safe_reason(recommendation, 2)}\n\n"
        f"이번 주 여행 계획이 고민된다면 {campaign.destination} 상품부터 확인해보세요.\n"
        f"{campaign.cta}\n"
        "```\n\n"
        f"{render_image_prompt_block('facebook', image_prompt)}"
        "## 내부 확인용 추천 근거\n"
        f"{evidence_lines}\n\n"
        "## 운영 메모\n\n"
        "- 본문은 위 `복사 영역`만 그대로 복사해서 사용하면 됩니다.\n"
        "- 페이스북은 첫 문장에 여행지와 추천 이유가 바로 보이도록 유지하세요.\n"
    )


def render_naver_blog(
    campaign: Campaign,
    recommendation: Recommendation,
    evidence_lines: str,
    image_prompt: str,
) -> str:
    return (
        f"# {campaign.destination} 여행 추천: 이번 주 떠나기 좋은 이유와 2박 3일 코스\n\n"
        f"{render_image_attachment('naver_blog')}"
        "## 복사 영역\n\n"
        "```markdown\n"
        f"# {campaign.destination} 여행 추천: 이번 주 떠나기 좋은 이유와 2박 3일 코스\n\n"
        f"이번 주 해외여행을 고민하고 있다면 {campaign.destination}를 먼저 살펴보세요. "
        f"{campaign.destination}는 짧은 일정에도 맛집, 쇼핑, 대표 명소, 근교 여행을 고르게 담을 수 있어 "
        "처음 가는 분도, 다시 찾는 분도 만족도가 높은 여행지입니다.\n\n"
        "마이리얼트립은 이번 주 공개 여행 신호와 자사 공개 채널 반응을 함께 확인해 "
        f"{campaign.destination}를 캠페인 추천 여행지로 선정했습니다.\n\n"
        "## 왜 지금 가기 좋을까요?\n\n"
        f"첫째, {safe_reason(recommendation, 0)}\n\n"
        f"둘째, {safe_reason(recommendation, 1)}\n\n"
        f"셋째, {safe_reason(recommendation, 2)}\n\n"
        "즉흥적으로 떠나기보다는 항공, 숙소, 현지 투어를 한 번에 비교하면서 "
        "일정에 맞는 상품을 고르는 것이 좋습니다.\n\n"
        "## 이런 분께 추천합니다\n\n"
        f"- {campaign.target}\n"
        "- 맛집과 쇼핑을 함께 즐기고 싶은 분\n"
        "- 2박 3일 또는 3박 4일로 알차게 다녀오고 싶은 분\n"
        "- 자유여행은 하고 싶지만 예약과 동선 준비는 간단히 끝내고 싶은 분\n\n"
        "## 2박 3일 추천 일정\n\n"
        f"### 1일차: {campaign.destination} 도착 후 중심가 산책\n\n"
        "도착 첫날은 무리한 이동보다 숙소 주변과 중심가를 천천히 둘러보는 일정이 좋습니다. "
        "저녁에는 현지 분위기를 느낄 수 있는 맛집이나 야경 코스를 넣어보세요.\n\n"
        "### 2일차: 대표 명소와 쇼핑 코스\n\n"
        "둘째 날은 가장 보고 싶은 명소를 오전에 먼저 다녀오고, 오후에는 쇼핑이나 카페 일정을 넣으면 좋습니다. "
        "이동 시간이 길어지지 않도록 교통권이나 패스를 미리 확인해두면 일정이 훨씬 편해집니다.\n\n"
        "### 3일차: 근교 또는 여유 일정\n\n"
        "마지막 날은 근교 반나절 코스나 여유로운 브런치 일정으로 마무리해보세요. "
        "비행 시간에 맞춰 짐 보관, 공항 이동 시간도 함께 체크하는 것이 좋습니다.\n\n"
        "## 예약 전 체크 포인트\n\n"
        "- 항공권과 숙소 가격은 일정에 따라 차이가 크니 여러 날짜를 비교해보세요.\n"
        "- 현지 투어나 입장권은 매진될 수 있어 인기 일정은 미리 예약하는 편이 좋습니다.\n"
        "- 날씨와 이동 동선을 함께 확인하면 현지에서 버리는 시간을 줄일 수 있습니다.\n\n"
        f"이번 주 여행 준비를 시작한다면, 마이리얼트립에서 {campaign.destination} 상품을 먼저 확인해보세요.\n\n"
        f"{campaign.cta}\n"
        "```\n\n"
        f"{render_image_prompt_block('naver_blog', image_prompt)}"
        "## 내부 확인용 추천 근거\n"
        f"{evidence_lines}\n\n"
        "## FAQ 후보\n"
        f"- Q. 왜 {campaign.destination}인가요?\n"
        f"  A. {safe_reason(recommendation, 0)}\n"
        "- Q. 블로그에 그대로 올려도 되나요?\n"
        "  A. 위 `복사 영역`을 붙여넣은 뒤 상품 링크와 실제 가격만 운영자가 확인해 넣으면 됩니다.\n"
    )


def render_image_prompt(campaign: Campaign) -> str:
    return (
        "공통 이미지 제작 방향\n\n"
        f"- 주제: {campaign.destination} 여행 캠페인 광고 이미지\n"
        "- 분위기: 여름 시즌, 밝고 신뢰감 있는 색감, 실제 여행자가 자연스럽게 걷는 장면\n"
        "- 스타일: 여행 플랫폼 브랜드 광고 사진, 과한 보정 없는 현실적인 라이프스타일 사진\n"
        "- 금지 요소: 로고, 워터마크, 읽기 어려운 텍스트, 과장된 랜드마크 합성\n\n"
        f"Instagram 4:5\n- 저장 경로: reports/{CHANNEL_IMAGE_ASSETS['instagram']['path']}\n"
        f"{render_channel_image_prompt(campaign, 'instagram')}\n\n"
        f"Facebook 1.91:1\n- 저장 경로: reports/{CHANNEL_IMAGE_ASSETS['facebook']['path']}\n"
        f"{render_channel_image_prompt(campaign, 'facebook')}\n\n"
        f"Naver Blog 16:9\n- 저장 경로: reports/{CHANNEL_IMAGE_ASSETS['naver_blog']['path']}\n"
        f"{render_channel_image_prompt(campaign, 'naver_blog')}\n"
    )


def render_landing_summary(campaign: Campaign, recommendation: Recommendation) -> str:
    return (
        f"# {campaign.destination} 주간 캠페인 랜딩 요약\n\n"
        f"Subtitle: {campaign.target}를 위한 근거 기반 여행 제안\n\n"
        "Highlights:\n"
        + "\n".join(f"- {reason}" for reason in recommendation.reasons)
        + f"\n\nCTA: {campaign.cta}\n"
    )


def hashtags_for(destination: str) -> str:
    base = ["#마이리얼트립", "#여행추천", "#해외여행", "#자유여행", "#이번주여행"]
    destination_tag = "#" + destination.replace("/", "").replace(" ", "")
    return " ".join([destination_tag, *base])


def render_channel_image_prompt(campaign: Campaign, channel: str) -> str:
    prompts = {
        "instagram": (
            f"{campaign.destination} 여행 광고용 세로형 이미지, 4:5 비율, "
            "20~30대 자유여행객 2명이 현지 골목을 걷는 자연스러운 장면, "
            "따뜻한 오후 햇빛, 맛집과 쇼핑을 암시하는 배경, 밝고 선명한 색감, "
            "프리미엄 여행 플랫폼 캠페인 사진, 텍스트와 로고 없이"
        ),
        "facebook": (
            f"{campaign.destination} 여행 캠페인용 가로형 이미지, 1.91:1 비율, "
            "도시의 대표 거리와 여행자가 함께 보이는 넓은 구도, "
            "가족이나 친구와 함께 떠나는 주말 해외여행 분위기, "
            "신뢰감 있는 브랜드 광고 사진, 과장된 합성 없이, 텍스트와 로고 없이"
        ),
        "naver_blog": (
            f"{campaign.destination} 여행 블로그 대표 이미지, 16:9 비율, "
            "도시 풍경과 여행자의 뒷모습이 함께 보이는 자연스러운 사진, "
            "일정 소개 글에 어울리는 깨끗한 구도, 밝은 하늘과 현지 거리감, "
            "정보형 여행 콘텐츠 썸네일, 텍스트와 로고 없이"
        ),
    }
    return prompts[channel]


def render_image_prompt_block(channel: str, image_prompt: str) -> str:
    asset = CHANNEL_IMAGE_ASSETS[channel]
    return (
        "## 이미지 생성 프롬프트\n\n"
        f"```text\n{image_prompt}\n```\n\n"
        "## 이미지 표시 영역\n\n"
        "Codex에 이미지 생성 권한이 있으면 위 프롬프트로 이미지를 생성한 뒤 "
        f"`reports/{asset['path']}`에 저장합니다. 저장된 파일은 아래에 바로 표시됩니다.\n\n"
        f"![{asset['label']}](./{asset['path']})\n\n"
    )


def render_image_attachment(channel: str) -> str:
    asset = CHANNEL_IMAGE_ASSETS[channel]
    return (
        "## 첨부 이미지\n\n"
        f"![{asset['label']}](./{asset['path']})\n\n"
        f"- 이미지 파일: `reports/{asset['path']}`\n\n"
    )


def safe_reason(recommendation: Recommendation, index: int) -> str:
    if index < len(recommendation.reasons):
        return public_reason(recommendation.destination, recommendation.reasons[index])
    return "여행 관심 신호와 콘텐츠 반응을 함께 봤을 때 이번 주 캠페인 우선순위가 높게 잡혔습니다."


def public_reason(destination: str, text: str) -> str:
    if "공개 신호와 자사 채널" in text:
        return f"최근 여행 관심과 마이리얼트립 공개 콘텐츠 반응에서 {destination} 관련 흐름이 확인됐습니다."
    if "환율, 항공권, 뉴스" in text:
        return "여행 준비에 영향을 주는 가격, 뉴스, 일정 관련 신호도 함께 참고했습니다."
    if "evidence 섹션" in text:
        return "여러 근거를 종합했을 때 이번 주 캠페인 우선순위가 높게 산정됐습니다."
    return text


def short_evidence_note(recommendation: Recommendation) -> str:
    titles = [
        str(item["title"])
        for item in recommendation.evidence
        if item.get("source_mode") == "live" and item.get("title")
    ]
    if not titles:
        return safe_reason(recommendation, 0)
    return truncate(", ".join(titles[:2]), 120)
