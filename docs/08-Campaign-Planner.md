# 08. Campaign Planner

# 목적

Campaign Planner는 Trend Engine의 결과를 실제 실행 가능한 마케팅 캠페인으로 변환한다.

입력:
- recommendation.json
- content_items.jsonl
- public_signals.jsonl

출력:
- campaign.json
- instagram.md
- facebook.md
- naver_blog.md
- image_prompt.md

---

# Workflow

Trend Recommendation
↓
상품 후보 선정
↓
타겟 고객 정의
↓
채널 전략 선택
↓
캠페인 메시지 생성
↓
콘텐츠 초안 생성

---

# Campaign Schema

```json
{
  "campaign_id":"2026-W28-001",
  "theme":"엔저 일본 여행",
  "target":"20~30대 자유여행",
  "destination":"후쿠오카",
  "objective":"예약 전환",
  "channels":["instagram","facebook","naver_blog"],
  "cta":"지금 예약하기"
}
```

---

# 상품 선정 규칙

우선순위

1. Trend Score
2. Opportunity Score
3. Risk Score
4. 최근 SNS 노출 빈도
5. 시즌 적합성

동일 목적지 연속 추천 시 Diversity Penalty 적용.

---

# 채널 전략

## Instagram
- 감성 중심
- 짧은 Hook
- Reel 우선
- 해시태그 포함

## Facebook
- 이벤트/프로모션
- 공유 유도
- CTA 강조

## Naver Blog
- SEO 제목
- 상세 여행 정보
- 예약 링크 삽입
- FAQ 포함

---

# CTA 생성 규칙

허용 예시
- 지금 예약하기
- 얼리버드 혜택 확인
- 이번 주 특가 보기

금지
- 과장 광고
- 근거 없는 최저가 표현

---

# 이미지 프롬프트

출력은 이미지 자체가 아니라 생성 프롬프트.

예시

```text
여름 후쿠오카 거리 풍경,
20대 여행객,
따뜻한 색감,
SNS 광고 스타일,
16:9
```

---

# 산출물

reports/
├── campaign.json
├── instagram.md
├── facebook.md
├── naver_blog.md
├── image_prompt.md

---

# Prompt Template

입력

- 여행지
- 시즌
- 타겟
- 프로모션
- CTA

출력

- 제목
- 본문
- 해시태그
- 예약 유도 문구

---

# Validation

생성 결과는

- 채널별 형식 준수
- CTA 포함
- 추천 근거 연결
- 금칙어 검사

---

# 완료 조건

- campaign.json 생성
- 플랫폼별 Markdown 생성
- image_prompt.md 생성
- Validation 통과
