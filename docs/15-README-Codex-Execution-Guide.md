# 15. README (Codex Execution Guide)

# MyRealTrip Weekly Campaign Copilot

> AX Hackathon Codex Plugin

## Read First

You are implementing a production-ready Codex Plugin.

Read every document under `/docs` in numeric order before writing code.

Do not redesign the architecture.

---

# Mission

Automate the weekly campaign planning workflow for MyRealTrip's Marketing Team and MD Team.

Outputs:

- Weekly HTML Report
- Recommendation JSON
- Campaign JSON
- Instagram Draft
- Facebook Draft
- Naver Blog Draft
- Image Prompt

---

# Target Users

- Marketing Team
- MD
- Product Managers
- Content Managers

This plugin is NOT for travelers.

---

# Workflow

Collect Public Data
→ Normalize
→ Analyze Trends
→ Generate Recommendations
→ Build Campaign
→ Generate Contents
→ Build HTML Dashboard

---

# Public Data

Use only public sources by default.

Supported:

- MyRealTrip Instagram
- MyRealTrip Facebook
- MyRealTrip Naver Blog
- News
- Exchange Rates
- Weather
- Holidays
- Tourism Statistics

API Keys are optional.

The plugin MUST work without them.

---

# Coding Rules

- Python 3.12+
- Type hints required
- Dataclasses preferred
- No TODO
- No pass
- Every module testable
- Maximum ~200 lines per file when practical

---

# Project Layout

Do not modify:

src/
docs/
tests/
templates/
data/
outputs/
logs/

---

# Data Rules

Keep:

raw/
normalized/
reports/

Never overwrite raw data.

---

# Prompt Rules

Responses must:

- cite evidence
- avoid hallucinations
- follow JSON schema
- follow markdown templates

---

# HTML Rules

Generate:

index.html
style.css
app.js
data.json

Must run without Node.js or internet.

---

# Error Handling

Collector failures must not stop the workflow.

Continue with remaining collectors.

---

# Logging

Never log:

- API Keys
- Tokens
- Passwords
- Secrets

---

# Validation

Required:

- Unit Tests
- Integration Tests
- End-to-End Test

---

# Definition of Done

The project is complete only if:

python -m campaign_copilot.cli run-weekly

generates:

- HTML Report
- Markdown Report
- Campaign JSON
- Recommendation JSON
- Instagram Draft
- Facebook Draft
- Naver Blog Draft
- Image Prompt
- submission.zip

---

# AGENT CHECKLIST

Before marking complete verify:

[ ] All docs implemented
[ ] Tests passing
[ ] HTML opens locally
[ ] Outputs generated
[ ] No TODOs
[ ] No placeholder code
[ ] Submission structure valid

Always prefer maintainability, readability and extensibility over shortcuts.
