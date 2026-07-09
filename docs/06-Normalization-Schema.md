# 06. Normalization Schema

# 목적

모든 수집 데이터를 하나의 공통 모델로 변환한다.
Collector는 다양한 형식의 데이터를 반환하지만, Analyzer는 하나의 스키마만 처리한다.

---

# 핵심 원칙

- Source마다 Parser는 달라도 Output Schema는 동일하다.
- 원본(raw)은 절대 수정하지 않는다.
- Normalized Item은 추론 가능한 필드만 채운다.
- 불명확한 값은 null로 둔다.

---

# ContentItem Schema

```json
{
  "id":"uuid",
  "platform":"instagram",
  "source":"owned_channel",
  "published_at":"2026-07-08",
  "title":"청도 맥주축제",
  "body":"...",
  "country":"China",
  "city":"Qingdao",
  "travel_type":"festival",
  "season":"summer",
  "campaign_type":"promotion",
  "promotion":true,
  "cta":"예약하기",
  "hashtags":["청도","맥주축제"],
  "media_type":"reel",
  "topics":["beer","festival"],
  "sentiment":null,
  "url":"..."
}
```

---

# PublicSignal Schema

```json
{
 "signal_type":"exchange_rate",
 "region":"Japan",
 "metric":"JPY_KRW",
 "value":9.1,
 "change_7d":-1.8,
 "observed_at":"2026-07-09"
}
```

지원 signal_type

- news
- trend
- exchange_rate
- weather
- holiday
- tourism
- flight_price

---

# CampaignCandidate

Analyzer 출력은 아래 구조를 따른다.

```json
{
 "destination":"Fukuoka",
 "score":87.5,
 "evidence":[
   "엔저 지속",
   "연휴 임박",
   "최근 SNS 언급 증가"
 ],
 "recommended_channels":[
   "instagram",
   "naver_blog"
 ]
}
```

---

# Entity Extraction

본문에서 추출

- 국가
- 도시
- 여행지
- 시즌
- 행사
- 할인
- CTA
- 가격
- 브랜드

규칙

추정이 아닌 명시된 정보만 저장.

---

# Taxonomy

travel_type

- city
- beach
- food
- shopping
- festival
- family
- luxury
- nature
- honeymoon

campaign_type

- event
- promotion
- guide
- review
- inspiration

media_type

- image
- reel
- short
- video
- carousel
- article

---

# Validation Rules

필수

- id
- platform
- published_at
- body

선택

- hashtags
- country
- city
- cta

---

# Pipeline

raw/*.json

↓

normalize()

↓

content_items.jsonl

↓

trend_engine()

---

# 완료조건

- 모든 Source가 ContentItem으로 변환
- JSON Schema 검증 통과
- jsonl 생성
- Unit Test 작성
