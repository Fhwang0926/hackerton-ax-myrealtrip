# 14. Hackathon Submission Guide

# AX Hackathon Submission Guide

This document defines exactly what should be submitted.

The final deliverable must satisfy every requirement described below.

---

# Submission Structure

submission.zip

```
submission.zip

├── README.md

├── logs/

│ ├── chatgpt.md

│ ├── codex.jsonl

│ └── claude.txt

└── src/

├── .codex-plugin/

│ └── plugin.json

├── skills/

│ └── weekly-campaign-copilot/

│ └── SKILL.md

├── .mcp.json

├── campaign_copilot/

├── templates/

├── tests/

├── pyproject.toml

└── README.md

```

---

# Required Outputs

The plugin MUST generate

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

# Required Logs

logs/

```
chatgpt.md

codex.jsonl

claude.txt
```

The logs must NOT be edited.

The logs must NOT remove messages.

---

# README

README must include

Project Summary

Installation

Usage

Architecture

Output

Validation

---

# Question 1

## 무엇을 만들었나요?

MyRealTrip Weekly Campaign Copilot

A Codex Plugin that automatically generates weekly marketing campaigns from public travel signals.

Target Users

- Marketing Team

- MD

- Product Managers

---

# Question 2

## 왜 이 문제를 선택했나요?

Marketing teams spend significant time every week

- researching travel trends

- analyzing SNS

- selecting products

- creating campaign drafts

This workflow is repetitive.

The plugin automates it using publicly available data.

---

# Question 3

## 어떻게 동작하나요?

Collect

↓

Normalize

↓

Trend Analysis

↓

Campaign Planning

↓

Content Generation

↓

HTML Dashboard

↓

Output

---

# Question 4

## AI를 어떻게 활용했나요?

AI is used for

- Trend Analysis

- Campaign Planning

- Content Generation

- HTML Report Generation

Evidence-based prompting is applied.

Hallucination is minimized.

---

# Question 5

## 어떻게 검증했나요?

Validation

- Unit Tests

- Integration Tests

- End-to-End Test

Generated Outputs

- HTML

- Markdown

- JSON

Manual verification

Browser validation

---

# Demonstration Flow

Open

index.html

↓

View Dashboard

↓

Open

instagram.md

↓

Open

facebook.md

↓

Open

naver_blog.md

↓

Verify recommendation.json

↓

Finish

---

# Judge Checklist

✓ Plugin runs

✓ Public data used

✓ Problem defined

✓ Evidence included

✓ Recommendation generated

✓ HTML generated

✓ Markdown generated

✓ Project reproducible

---

# Final Checklist

README

logs

plugin.json

SKILL.md

tests

HTML

Markdown

JSON

submission.zip

Everything included.

---

# Definition of Success

A judge should be able to

1.

Download submission.zip

2.

Run

python -m campaign_copilot.cli run-weekly

3.

Open

reports/index.html

4.

Understand

Why this week's campaign was generated

without reading the source code.

That is considered success.
