# 10. HTML Interactive Report

# 목적

평가자가 ZIP을 압축 해제한 뒤 `index.html` 하나만 열어도
이번 주 캠페인 결과를 이해할 수 있는 정적(Static) 대시보드를 생성한다.

---

# 기술 원칙

- 순수 HTML/CSS/JavaScript
- 빌드 도구 없이 실행
- 인터넷 연결 없이 동작
- data.json 기반 렌더링

---

# 출력 구조

```text
reports/
└── 2026-W28/
    ├── index.html
    ├── style.css
    ├── app.js
    ├── data.json
    ├── report.md
    └── campaign/
```

---

# data.json Schema

```json
{
  "week":"2026-W28",
  "summary":{
    "top_destination":"후쿠오카",
    "trend_score":87.5
  },
  "signals":[],
  "recommendations":[],
  "campaigns":[],
  "evidence":[]
}
```

---

# 화면 구성

## 1. Executive Summary

- 추천 여행지
- Trend Score
- Opportunity
- Risk
- 추천 이유

---

## 2. Public Signals

카드 형태

- 뉴스
- 환율
- 날씨
- 공휴일
- 관광통계

---

## 3. SNS 분석

플랫폼별

- Instagram
- Facebook
- Naver Blog

표시 항목

- 게시 수
- 주요 여행지
- CTA
- 프로모션

---

## 4. 이번 주 추천 캠페인

카드

- 여행지
- 타겟
- 채널
- CTA
- 예상 근거

---

## 5. 생성 결과

다운로드 가능한 링크

- instagram.md
- facebook.md
- naver_blog.md
- image_prompt.md

---

## 6. Evidence

추천 근거를 그대로 출력한다.

예시

- 엔저 지속
- 여름 휴가
- 최근 일본 여행 뉴스 증가

AI의 추상적 설명은 금지한다.

---

# UI 규칙

- 반응형
- 다크모드 자동 지원
- 카드 레이아웃
- 스크롤 최소화

---

# JavaScript

app.js 책임

1. data.json 로드
2. 카드 생성
3. 테이블 렌더링
4. Evidence 출력
5. 다운로드 링크 연결

---

# CSS

style.css

- Grid Layout
- Card
- Badge
- Table
- Timeline
- Responsive

---

# Validation

index.html 단독 실행 가능

브라우저

- Chrome
- Edge
- Safari

에서 확인

---

# 완료 조건

□ index.html 생성
□ style.css 생성
□ app.js 생성
□ data.json 생성
□ report.md 연결
□ 정적 실행 성공
