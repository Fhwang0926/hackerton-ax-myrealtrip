# 04. Directory Structure

# 목적

이 문서는 Codex가 프로젝트를 생성할 때 따라야 할 디렉터리 구조와 각 파일의 책임을 정의한다.

핵심 원칙은 다음과 같다.

1. `src/` 안에 Codex Plugin 루트가 있어야 한다.
2. `src/.codex-plugin/plugin.json`은 필수다.
3. `src/skills/weekly-campaign-copilot/SKILL.md`는 핵심 실행 지침이다.
4. 데이터 수집, 정규화, 분석, 캠페인 생성, HTML 보고서 생성을 모듈별로 분리한다.
5. 모든 출력물은 `outputs/` 또는 `src/data/reports/` 아래에 생성한다.
6. 해커톤 제출 시 `submission.zip` 구조를 바로 만들 수 있어야 한다.

---

# 최종 제출 구조

```text
submission.zip
├── src/
│   ├── .codex-plugin/
│   │   └── plugin.json
│   ├── skills/
│   │   └── weekly-campaign-copilot/
│   │       └── SKILL.md
│   ├── .mcp.json
│   ├── pyproject.toml
│   ├── README.md
│   ├── collectors/
│   ├── normalizers/
│   ├── analyzers/
│   ├── planners/
│   ├── generators/
│   ├── reports/
│   ├── templates/
│   ├── data/
│   └── tests/
├── README.md
└── logs/
```

---

# 개발용 루트 구조

```text
mrt-weekly-campaign-copilot/
├── README.md
├── docs/
├── src/
├── outputs/
├── logs/
├── scripts/
├── examples/
└── submission/
```

---

# src 상세 구조

```text
src/
├── .codex-plugin/
│   └── plugin.json
│
├── skills/
│   └── weekly-campaign-copilot/
│       └── SKILL.md
│
├── .mcp.json
├── pyproject.toml
├── README.md
│
├── campaign_copilot/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── workflow.py
│   │
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── instagram.py
│   │   ├── facebook.py
│   │   ├── naver_blog.py
│   │   ├── news.py
│   │   ├── exchange_rate.py
│   │   ├── weather.py
│   │   ├── holiday.py
│   │   ├── flight_price.py
│   │   └── sample_loader.py
│   │
│   ├── normalizers/
│   │   ├── __init__.py
│   │   ├── content_normalizer.py
│   │   ├── signal_normalizer.py
│   │   └── schema.py
│   │
│   ├── analyzers/
│   │   ├── __init__.py
│   │   ├── sns_analyzer.py
│   │   ├── trend_analyzer.py
│   │   ├── opportunity_score.py
│   │   └── risk_analyzer.py
│   │
│   ├── planners/
│   │   ├── __init__.py
│   │   ├── product_planner.py
│   │   ├── campaign_planner.py
│   │   └── channel_strategy.py
│   │
│   ├── generators/
│   │   ├── __init__.py
│   │   ├── instagram_generator.py
│   │   ├── facebook_generator.py
│   │   ├── naver_blog_generator.py
│   │   ├── image_prompt_generator.py
│   │   └── markdown_generator.py
│   │
│   ├── reports/
│   │   ├── __init__.py
│   │   ├── html_report.py
│   │   ├── chart_data.py
│   │   └── assets.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── date_utils.py
│       ├── text_utils.py
│       ├── json_utils.py
│       ├── http_client.py
│       └── logging.py
│
├── templates/
│   ├── report/
│   │   ├── index.html.j2
│   │   ├── style.css
│   │   └── app.js
│   ├── campaign/
│   │   ├── instagram.md.j2
│   │   ├── facebook.md.j2
│   │   ├── naver_blog.md.j2
│   │   └── image_prompt.md.j2
│   └── prompts/
│       ├── normalize_content.md
│       ├── trend_analysis.md
│       ├── campaign_planning.md
│       └── content_generation.md
│
├── data/
│   ├── raw/
│   ├── normalized/
│   ├── snapshots/
│   ├── reports/
│   └── samples/
│
└── tests/
    ├── test_normalizer.py
    ├── test_trend_score.py
    ├── test_campaign_planner.py
    ├── test_content_generator.py
    └── test_report_generator.py
```

---

# 핵심 파일 책임

## `src/.codex-plugin/plugin.json`

Codex Plugin의 메타데이터를 정의한다.

필수 포함 항목:

```json
{
  "name": "myrealtrip-weekly-campaign-copilot",
  "version": "0.1.0",
  "description": "Generate weekly travel campaign plans from public signals and MyRealTrip social content.",
  "skills": ["weekly-campaign-copilot"]
}
```

---

## `src/skills/weekly-campaign-copilot/SKILL.md`

Codex가 이 플러그인을 사용할 때 따라야 할 지침이다.

포함해야 할 내용:

1. 언제 이 Skill을 사용할지
2. 입력 데이터가 없을 때 샘플 데이터를 사용할지
3. 수집 가능한 공개 데이터 목록
4. 실행 순서
5. 출력물 위치
6. 검증 절차

---

## `src/campaign_copilot/cli.py`

CLI 엔트리포인트다.

권장 명령어:

```bash
python -m campaign_copilot.cli run-weekly
python -m campaign_copilot.cli collect
python -m campaign_copilot.cli normalize
python -m campaign_copilot.cli analyze
python -m campaign_copilot.cli generate-campaign
python -m campaign_copilot.cli generate-report
```

---

## `src/campaign_copilot/workflow.py`

전체 파이프라인을 실행한다.

```python
def run_weekly_campaign(config: AppConfig) -> WorkflowResult:
    raw = collect_all(config)
    normalized = normalize_all(raw)
    insights = analyze_trends(normalized)
    plan = plan_campaign(insights)
    assets = generate_contents(plan)
    report = generate_html_report(plan, assets)
    return WorkflowResult(...)
```

---

# 데이터 디렉터리 규칙

## raw

수집 원본 저장.

```text
src/data/raw/
├── instagram_YYYY-MM-DD.json
├── facebook_YYYY-MM-DD.json
├── naver_blog_YYYY-MM-DD.json
├── news_YYYY-MM-DD.json
├── exchange_YYYY-MM-DD.json
└── weather_YYYY-MM-DD.json
```

## normalized

정규화 결과 저장.

```text
src/data/normalized/
├── content_items.jsonl
├── public_signals.jsonl
└── weekly_snapshot.json
```

## reports

최종 결과 저장.

```text
src/data/reports/
└── 2026-W28/
    ├── index.html
    ├── style.css
    ├── app.js
    ├── report.md
    ├── data.json
    ├── instagram.md
    ├── facebook.md
    ├── naver_blog.md
    └── image_prompt.md
```

---

# 출력물 구조

```text
outputs/
└── weekly-campaign-YYYY-WW/
    ├── index.html
    ├── report.md
    ├── data.json
    ├── campaign/
    │   ├── instagram.md
    │   ├── facebook.md
    │   ├── naver_blog.md
    │   └── image_prompt.md
    └── evidence/
        ├── sources.json
        └── normalized_content.jsonl
```

---

# import 규칙

모든 내부 import는 `campaign_copilot` 기준으로 한다.

좋은 예:

```python
from campaign_copilot.normalizers.schema import ContentItem
from campaign_copilot.analyzers.trend_analyzer import TrendAnalyzer
```

나쁜 예:

```python
from ../normalizers.schema import ContentItem
```

---

# 환경 변수

```bash
OPENAI_API_KEY=optional
MYREALTRIP_API_KEY=optional
NAVER_CLIENT_ID=optional
NAVER_CLIENT_SECRET=optional
```

주의:

- 기본 모드는 API Key 없이 실행되어야 한다.
- API Key가 없으면 샘플 데이터와 공개 RSS 기반으로 동작해야 한다.
- 비밀정보는 logs에 저장하지 않는다.

---

# Codex 구현 순서

1. 디렉터리 생성
2. `plugin.json` 생성
3. `SKILL.md` 생성
4. `pyproject.toml` 생성
5. 데이터 스키마 작성
6. 샘플 데이터 작성
7. Normalizer 구현
8. Analyzer 구현
9. Campaign Planner 구현
10. Content Generator 구현
11. HTML Report 구현
12. CLI 구현
13. 테스트 작성
14. README 작성
15. submission.zip 생성

---

# 완료 조건

- `python -m campaign_copilot.cli run-weekly` 실행 가능
- `outputs/weekly-campaign-*/index.html` 생성
- `instagram.md`, `facebook.md`, `naver_blog.md` 생성
- `sources.json` 생성
- 테스트 최소 5개 통과
- `submission.zip` 구조와 일치
