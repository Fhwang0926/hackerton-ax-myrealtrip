# 09. Content Generator

# 목적

Content Generator는 Campaign Planner의 결과를 실제 게시 가능한 콘텐츠 초안으로 변환한다.

출력 대상

- Instagram
- Facebook
- Naver Blog
- Image Prompt
- Landing Page Summary

---

# 입력

campaign.json

recommendation.json

content_items.jsonl

---

# 출력

reports/

├── instagram.md
├── facebook.md
├── naver_blog.md
├── image_prompt.md
├── landing_summary.md
└── assets.json

---

# Generator 인터페이스

```python
class ContentGenerator:
    def generate(campaign: Campaign)->GeneratedAssets:
        ...
```

---

# Instagram 규칙

구조

1. Hook (1줄)
2. 본문
3. CTA
4. 해시태그

길이

- Hook 25자 이내
- 본문 800자 이하

예시

```md
# 이번 주 후쿠오카가 가장 저렴합니다 ✈️

엔저와 연휴가 겹치는 지금,
후쿠오카 자유여행을 추천합니다.

👉 지금 예약하기

#후쿠오카 #일본여행 #마이리얼트립
```

---

# Facebook 규칙

구조

- 제목
- 설명
- 이벤트/혜택
- CTA

공유 유도 문장을 포함한다.

---

# Naver Blog 규칙

구조

- SEO 제목
- 목차
- 여행 소개
- 추천 코스
- FAQ
- 예약 CTA

본문은 1,500~3,000자를 목표로 한다.

---

# Landing Summary

랜딩페이지 제작에 사용할 핵심 문구.

```md
Title

Subtitle

Highlights

CTA

Keywords
```

---

# Image Prompt

이미지 자체가 아니라 생성 프롬프트를 만든다.

구성

- 장소
- 계절
- 시간
- 인물
- 분위기
- 카메라
- 비율

예시

```text
후쿠오카 야타이 거리,
여름 저녁,
20대 여행객,
따뜻한 조명,
광고 사진,
16:9
```

---

# Tone & Voice

브랜드 톤

- 신뢰감
- 여행 기대감
- 과장 금지
- 정보 중심

금지

- 근거 없는 최저가
- 허위 긴급성
- 과도한 이모지

---

# Prompt Template

System

당신은 MyRealTrip 콘텐츠 마케터이다.

User

Campaign JSON을 읽고
채널별 콘텐츠를 생성하라.

반드시

- CTA
- 예약 유도
- 브랜드 톤

을 유지한다.

---

# Output Validation

생성 결과는

- 빈 제목 금지
- CTA 포함
- 추천 근거와 일치
- 채널 형식 준수
- Markdown 문법 유효

---

# 완료 조건

□ instagram.md 생성

□ facebook.md 생성

□ naver_blog.md 생성

□ image_prompt.md 생성

□ landing_summary.md 생성

□ assets.json 생성
