# 13. Test Plan

# 목적

본 문서는 MyRealTrip Weekly Campaign Copilot의 테스트 전략을 정의한다.

목표는

- 정상 동작
- 재현 가능성
- 해커톤 시연 안정성

을 확보하는 것이다.

---

# Test Strategy

테스트는 아래 4단계로 구성한다.

1. Unit Test
2. Integration Test
3. End-to-End Test
4. Acceptance Test

---

# Unit Test

각 Module은 독립적으로 테스트 가능해야 한다.

대상

- Collectors
- Normalizers
- Trend Engine
- Campaign Planner
- Content Generator
- HTML Report

---

# Collector Tests

## Instagram

입력

sample_instagram.json

검증

- 게시글 개수
- 날짜
- Body
- Hashtag

---

## Facebook

검증

- 이벤트 추출
- CTA 추출

---

## Naver Blog

검증

- 제목
- 본문
- URL
- 날짜

---

## News

검증

RSS Parsing

---

## Exchange

검증

환율 값

---

## Weather

검증

날씨 데이터

---

# Normalizer Tests

입력

Raw JSON

↓

출력

ContentItem

검증

✓ Schema

✓ Required Field

✓ Null 처리

---

# Trend Engine Tests

Scenario 1

엔저

↓

Japan Score 증가

Scenario 2

태풍

↓

Risk 증가

Scenario 3

공휴일

↓

근거리 여행 증가

Scenario 4

뉴스 증가

↓

Trend Score 증가

---

# Campaign Planner Tests

입력

Recommendation JSON

↓

출력

Campaign JSON

검증

- 여행지
- 타겟
- CTA
- 채널

---

# Content Generator Tests

생성

Instagram.md

Facebook.md

NaverBlog.md

ImagePrompt.md

검증

- Markdown 문법
- CTA 존재
- 제목 존재
- Body 존재

---

# HTML Report Tests

생성

index.html

style.css

app.js

data.json

검증

Chrome

Safari

Edge

에서 정상 실행

---

# Integration Test

Collector

↓

Normalizer

↓

Analyzer

↓

Campaign

↓

Content

↓

Report

전체 Pipeline 테스트

---

# End-to-End Test

명령

python -m campaign_copilot.cli run-weekly

성공 조건

reports 생성

campaign.json 생성

recommendation.json 생성

HTML 생성

Markdown 생성

---

# Error Test

Instagram 실패

↓

Workflow 계속

News 실패

↓

Workflow 계속

Weather 실패

↓

Workflow 계속

---

# Performance

목표

Collect

<60초

Normalize

<20초

Analyze

<10초

Generate

<30초

전체

<5분

---

# Output Validation

reports/

index.html

report.md

campaign.json

recommendation.json

instagram.md

facebook.md

naver_blog.md

image_prompt.md

모두 생성

---

# Definition of Done

✓ Unit Test Pass

✓ Integration Pass

✓ End-to-End Pass

✓ HTML Open Success

✓ Markdown Generated

✓ JSON Valid

✓ submission.zip Ready