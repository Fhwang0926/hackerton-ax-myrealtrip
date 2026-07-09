# 제출용 플러그인 안내

이 저장소의 실제 실행 가능한 플러그인 소스는 아래 폴더에 있습니다.

```text
src
```

`outputs/`, `logs/`, `.local-codex-marketplace/`, `submission.zip`은 로컬 실행과 제출 패키징 과정에서 생기는 결과물이므로 Git에는 올리지 않습니다.
최종 제출용 압축 파일은 로컬에서 생성한 `outputs/myrealtrip-weekly-campaign-copilot-plugin/submission.zip`을 사용했습니다.

## Codex에 등록해서 설치하기

로컬에서 이 저장소를 받은 뒤 저장소 루트에서 아래 순서로 등록하고 설치합니다.

```bash
codex plugin marketplace add marketplace
codex plugin add myrealtrip-weekly-campaign-copilot@hackathon-local
```

설치 여부는 아래 명령으로 확인합니다.

```bash
codex plugin list
```

목록에 `myrealtrip-weekly-campaign-copilot@hackathon-local`이 `installed, enabled`로 보이면 설치가 완료된 것입니다.

## Codex에서 사용하는 예시

설치 후 새 Codex 스레드에서 플러그인 이름을 붙여 자연어로 요청하면 됩니다.

```text
MyRealTrip Weekly Campaign Copilot 마이리얼트립 주간 캠페인 리포트 생성해줘.
공개 데이터와 자사 공개 채널 신호를 보고 이번 주 추천 여행지, 추천 근거,
인스타그램/페이스북/네이버 블로그 초안을 만들어줘.
```

Codex는 플러그인 스킬을 읽고 이 저장소의 정해진 리포트 생성 흐름에 맞춰 공개 신호 수집부터 HTML 리포트와 채널별 초안 생성까지 진행합니다.

결과는 `reports/result.md` 요약과 `reports/index.html` 리포트를 먼저 보면 됩니다. `data.json`, `recommendation.json`, `campaign.json`은 개발자나 심사자가 상세 검증할 때 쓰는 파일이라 일반 사용자는 열지 않아도 됩니다.

![Codex에서 플러그인 사용 예시](docs/assets/codex-plugin-usage-example.png)

## 직접 실행하기

```bash
cd src
python3 -m campaign_copilot.cli run-weekly
```

실행하면 터미널에는 사용자용 요약이 바로 출력됩니다. 더 자세히 보려면 아래 파일을 열어 결과를 확인합니다.

```text
src/reports/result.md
src/reports/index.html
```

SNS 초안 파일에는 바로 붙여넣을 수 있는 `복사 영역`, 채널별 `이미지 생성 프롬프트`, `이미지 표시 영역`이 함께 들어갑니다.

Codex에 이미지 생성 권한이 있는 경우 각 프롬프트로 이미지를 생성해 아래 경로에 저장하면, SNS 파일 안에서 이미지가 바로 표시됩니다.

- `src/reports/assets/instagram-campaign.png`
- `src/reports/assets/facebook-campaign.png`
- `src/reports/assets/naver-blog-campaign.png`

개발/검증용 JSON 출력이 필요할 때만 아래처럼 실행합니다.

```bash
python3 -m campaign_copilot.cli run-weekly --json
```

## 검증하기

```bash
cd src
python3 -m unittest discover -s tests
python3 -m campaign_copilot.cli run-weekly
python3 -m zipfile -t submission.zip
```

프론트엔드 빌드는 필요하지 않습니다. 리포트는 정적 HTML 파일입니다.

## 플러그인은 어떻게 작동하나요?

플러그인은 Codex에서 자연어 요청을 받으면 `python3 -m campaign_copilot.cli run-weekly` 흐름을 실행합니다.

전체 구조는 아래 순서를 따릅니다.

```text
Collector
-> Normalizer
-> Trend Engine
-> Campaign Planner
-> Content Generator
-> HTML Report
```

Collector는 네이버 블로그 RSS, Google News RSS, 환율, 날씨 데이터를 수집합니다.
인스타그램과 페이스북처럼 공개 페이지만으로 안정적인 게시글 단위 수집이 어려운 채널은 샘플로 대체하고, 그 사유를 리포트에 표시합니다.

Normalizer는 수집 데이터를 콘텐츠와 공개 신호로 정규화합니다.
Trend Engine은 여행지별 점수를 계산하고, Campaign Planner는 추천 여행지와 캠페인 방향을 만듭니다.
Content Generator는 인스타그램, 페이스북, 네이버 블로그 초안과 이미지 프롬프트를 생성합니다.
마지막으로 HTML 리포트, `result.md`, 검증용 JSON, 제출용 zip을 생성합니다.

---

# MyRealTrip Weekly Campaign Copilot

> AX Hackathon - Codex Plugin
>
> You are implementing a production-quality Codex Plugin.
>
> Read this document first.
>
> Then read every document under `/docs` in numerical order.
>
> Do NOT skip documents.
>
> Do NOT create your own architecture.
>
> Follow this specification exactly.

---

# Mission

Your mission is NOT to build a demo.

Your mission is to build a working Codex Plugin that helps MyRealTrip's Marketing Team and MD Team decide

> "What travel products should we promote this week?"

using publicly available signals.

The final output must generate:

- Weekly Campaign Report
- HTML Dashboard
- Instagram Draft
- Facebook Draft
- Naver Blog Draft
- Image Prompt
- Recommendation Evidence

---

# Target Users

This plugin is NOT for travelers.

Target users are

- Marketing Team
- MD
- Product Managers
- Content Managers

Do not optimize UX for travelers.

Optimize workflow for internal business users.

---

# Business Problem

Current weekly workflow

↓

Collect News

↓

Analyze SNS

↓

Analyze Public Signals

↓

Select Products

↓

Create Campaign

↓

Create Report

↓

Publish

This workflow is currently manual.

The plugin must automate it.

---

# Project Goal

Build a Weekly Campaign Copilot.

The plugin must

1.

Collect public data

2.

Normalize

3.

Analyze Trends

4.

Recommend Products

5.

Generate Campaign

6.

Generate Report

7.

Generate HTML Dashboard

---

# Public Data

You may use

- MyRealTrip Instagram
- MyRealTrip Facebook
- MyRealTrip Naver Blog
- Public News
- Google Trends
- Exchange Rate
- Holidays
- Weather
- Tourism Statistics

Do NOT require private internal databases.

API Keys are OPTIONAL.

The plugin must still work without them.

---

# Architecture

Never redesign the architecture.

Always follow

Collector

↓

Normalizer

↓

Trend Engine

↓

Campaign Planner

↓

Content Generator

↓

HTML Report

↓

Output

---

# Required Output

reports/

```
index.html
style.css
app.js
data.json

report.md

campaign.json

recommendation.json

instagram.md

facebook.md

naver_blog.md

image_prompt.md
```

---

# Required Project Structure

```
src/

docs/

tests/

templates/

data/

outputs/

logs/
```

Never change this layout.

---

# Coding Rules

Python 3.12+

Type Hints Required

Dataclass Preferred

No duplicated code.

No giant functions.

Maximum

200 lines per file

30 lines per function

---

# Implementation Rules

Implement incrementally.

Every module must be executable independently.

Every module must include

- Unit Test

- Type Hints

- Logging

- Error Handling

Do NOT leave TODO.

Do NOT leave PASS.

If implementation is impossible,

implement a Stub with documentation.

---

# Data Rules

Never overwrite raw data.

Always create

raw/

normalized/

reports/

separately.

Everything must be reproducible.

---

# Prompt Rules

LLM outputs must

- cite evidence

- never hallucinate

- follow JSON Schema

- follow Markdown Template

Never output unsupported claims.

---

# HTML Rules

The HTML report must work

without

Node

npm

React

Vue

Internet

Use

HTML

CSS

Vanilla JS

only.

---

# Error Rules

Collector failure

must NOT stop

the entire workflow.

Always continue.

---

# Logging Rules

All workflow steps

must be logged.

Never log

API Keys

Secrets

Passwords

Tokens

---

# Validation Rules

Every implementation must pass

1.

Unit Test

2.

Integration Test

3.

End-to-End Test

---

# Development Order

Read

docs/00

↓

docs/01

↓

docs/02

↓

...

↓

docs/15

Implement

one document at a time.

Never jump ahead.

---

# Completion Definition

Project is complete only when

```
python -m campaign_copilot.cli run-weekly
```

successfully generates

✓ HTML Report

✓ Markdown Report

✓ Campaign

✓ Recommendation

✓ Instagram Draft

✓ Facebook Draft

✓ Naver Blog Draft

✓ Image Prompt

✓ Tests Pass

✓ submission.zip

---

# Important

This repository is an AX Hackathon submission.

Code quality is more important than implementation speed.

Prioritize

Maintainability

Readability

Extensibility

Testability

over shortcuts.

Always produce production-quality code.

Never produce pseudo-code.

Never stop after creating templates.

Finish implementation.
