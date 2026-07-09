# 07. Trend Engine Specification

# 목적

Trend Engine은 공개 데이터를 점수화하여
'이번 주 어떤 상품을 홍보해야 하는가?'를 결정한다.

분석이 아니라 의사결정을 만드는 엔진이다.

---

# 입력

1. ContentItem(JSONL)
2. PublicSignal(JSONL)

---

# 출력

```json
{
  "week":"2026-W28",
  "top_candidates":[
    {
      "destination":"Fukuoka",
      "score":87.4,
      "confidence":0.92,
      "reasons":[
        "엔저 지속",
        "공휴일 임박",
        "최근 일본 여행 뉴스 증가"
      ]
    }
  ]
}
```

---

# Trend Score

TrendScore는 여러 신호를 합산한다.

```text
TrendScore
=
News
+
SNS
+
Exchange
+
Holiday
+
Weather
+
Tourism
+
Flight
```

기본 가중치

| Signal | Weight |
|--------|------:|
| News | 0.25 |
| SNS | 0.20 |
| Exchange Rate | 0.15 |
| Holiday | 0.15 |
| Weather | 0.10 |
| Tourism Statistics | 0.10 |
| Flight Price | 0.05 |

가중치는 config로 변경 가능해야 한다.

---

# Opportunity Score

시장 기회를 나타낸다.

예시

- 환율 하락
- 검색량 증가
- SNS 언급 증가
- 장기 연휴

OpportunityScore는 0~100으로 정규화한다.

---

# Risk Score

리스크도 계산한다.

예시

- 태풍
- 폭염
- 여행 경보
- 항공 취소
- 환율 급등

0이 가장 안전,
100이 가장 위험.

---

# Final Campaign Score

```text
CampaignScore
=
TrendScore
+
OpportunityScore
-
RiskScore
```

상위 N개를 추천한다.

---

# Explainable Evidence

추천에는 반드시 근거가 포함되어야 한다.

좋은 예

- 최근 7일 일본 여행 뉴스 증가
- 엔화 약세
- 장기 연휴
- 자사 SNS 노출 부족

나쁜 예

- AI가 추천했습니다.

---

# 추천 규칙

동일 여행지만 반복 추천하지 않는다.

최근 2주 연속 추천된 경우
Diversity Penalty를 적용한다.

---

# Analyzer Interface

```python
class TrendAnalyzer:

    def analyze(
        self,
        contents,
        signals
    ) -> TrendAnalysis:
        ...
```

---

# Output Files

```text
reports/
├── trend.json
├── opportunity.json
├── risks.json
└── recommendation.json
```

---

# 테스트

시나리오

1.
환율 하락

↓

일본 추천 증가

2.
태풍 발생

↓

Risk 상승

↓

추천 제외

3.
연휴 증가

↓

근거리 여행 점수 상승

---

# 완료 조건

- Trend Score 계산
- Risk 계산
- Opportunity 계산
- Evidence 생성
- 추천 TOP3 생성
- recommendation.json 저장
