# 11. Codex Implementation Tasks

# 목적

이 문서는 Codex가 사람의 추가 지시 없이 순차적으로 구현할 수 있도록 작업(Task)을 정의한다.

---

# 구현 규칙

- TODO를 남기지 않는다.
- Stub이라도 컴파일 가능한 상태를 유지한다.
- Task 완료 후 테스트를 작성한다.
- 실패해도 다음 Task를 진행할 수 있도록 모듈을 분리한다.

---

# 우선순위

- P0: 반드시 구현
- P1: 핵심 기능
- P2: 개선 기능

---

# Phase 1 - 프로젝트 초기화

## T001 (P0)
프로젝트 디렉터리 생성

완료조건
- src 생성
- docs 생성
- tests 생성

## T002 (P0)
plugin.json 생성

완료조건
- JSON 문법 통과

## T003 (P0)
SKILL.md 작성

완료조건
- 실행 절차 포함

## T004 (P0)
pyproject.toml 생성

---

# Phase 2 - 데이터 모델

## T010
ContentItem dataclass

## T011
PublicSignal dataclass

## T012
Campaign dataclass

## T013
Recommendation dataclass

완료조건
- 타입 힌트
- 직렬화 가능

---

# Phase 3 - Collectors

T020 Instagram Collector

T021 Facebook Collector

T022 Naver Blog Collector

T023 News Collector

T024 Exchange Collector

T025 Weather Collector

T026 Holiday Collector

T027 Flight Price Collector

완료조건
- BaseCollector 상속
- 샘플 데이터 지원
- raw JSON 저장

---

# Phase 4 - Normalizer

T030 Content Normalizer

T031 Signal Normalizer

T032 JSONL Writer

완료조건
- content_items.jsonl 생성

---

# Phase 5 - Analyzer

T040 Trend Score

T041 Opportunity Score

T042 Risk Score

T043 Recommendation

T044 Evidence 생성

완료조건
- recommendation.json 생성

---

# Phase 6 - Campaign Planner

T050 상품 선정

T051 채널 전략

T052 CTA 생성

T053 campaign.json 생성

---

# Phase 7 - Content Generator

T060 Instagram Markdown

T061 Facebook Markdown

T062 Naver Blog Markdown

T063 Image Prompt

T064 Landing Summary

---

# Phase 8 - HTML Report

T070 index.html

T071 style.css

T072 app.js

T073 data.json

완료조건
- 브라우저 단독 실행

---

# Phase 9 - CLI

T080 collect

T081 normalize

T082 analyze

T083 generate

T084 run-weekly

---

# Phase 10 - Tests

T090 Unit Tests

T091 Integration Test

T092 End-to-End Test

---

# 최종 산출물

submission.zip

reports/index.html

instagram.md

facebook.md

naver_blog.md

image_prompt.md

campaign.json

recommendation.json

---

# Done Definition

프로젝트는 아래 명령으로 실행되어야 한다.

```bash
python -m campaign_copilot.cli run-weekly
```

성공 시

- reports 생성
- HTML 생성
- Markdown 생성
- JSON 생성
- 테스트 통과
