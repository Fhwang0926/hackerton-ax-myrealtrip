# AGENTS.md

# Master Agent Instructions

This repository is an AX Hackathon submission.

Every coding agent (Codex, Claude Code, Cursor, GPT) MUST follow this document.

---

# Primary Goal

Build a production-quality Codex Plugin.

Do not build a prototype.

Do not simplify the architecture.

---

# Priority

P0
- Working Plugin
- Repeatable workflow
- HTML dashboard
- Submission structure

P1
- Code quality
- Maintainability
- Tests

P2
- Extra optimizations

---

# Non-Negotiable Rules

- Never leave TODO.
- Never leave `pass`.
- Never return pseudo-code.
- Every module must compile.
- Every public function must include type hints.
- Prefer dataclasses.
- Separate business logic from I/O.

---

# Architecture Lock

Never change this flow:

Collector
→ Normalizer
→ Trend Engine
→ Campaign Planner
→ Content Generator
→ HTML Report

---

# Coding Standards

- Python 3.12+
- Ruff/Black compatible
- Small functions
- Clear names
- Dependency injection where practical

---

# Evidence Policy

Recommendations MUST include evidence.

Never claim trends without supporting signals.

---

# Data Policy

Keep directories isolated:

data/raw
data/normalized
data/reports

Never overwrite raw data.

---

# LLM Policy

Outputs must:

- Follow schema
- Cite evidence
- Avoid hallucinations
- Produce deterministic markdown

---

# Testing Policy

Every feature requires:

- Unit Test
- Integration Test (when applicable)

End-to-end workflow:

python -m campaign_copilot.cli run-weekly

must succeed.

---

# Git Rules

Suggested commits:

feat:
fix:
refactor:
docs:
test:

Small logical commits only.

---

# Forbidden

- Secrets in logs
- Hardcoded API keys
- Hidden dependencies
- Breaking project layout

---

# Definition of Done

The project is complete only when:

- Plugin executes
- HTML report renders
- Markdown assets generated
- recommendation.json generated
- campaign.json generated
- Tests pass
- submission.zip is ready

Always optimize for maintainability, readability and extensibility.
