# Performance Review Coach

Transforms messy manager notes into structured, evidence-based performance reviews with SMART goals and coaching frameworks, built with Claude API.

## What it does
Manager pastes rough notes about an employee. The tool generates a complete performance review including overall rating, key achievements, development areas, competency scores, coaching framework with timelines, and SMART goals for the next period.

## Why it matters
Most performance reviews are poorly written — vague, biased, or legally risky. This tool structures any manager input into fair, consistent, evidence-based documentation.

## Tech stack
- Python
- Anthropic Claude API (claude-haiku-4-5)
- Google Colab

## Key design decision
No RAG needed — this is pure prompt engineering. The value is in the output structure, not document retrieval.

## Sample inputs tested
- Detailed manager notes → Exceeds Expectations review with full coaching plan
- Vague manager notes ("difficult attitude", "missed some stuff") → Still produces structured, actionable, legally defensible output

## Known limitations
- Output quality depends on manager input detail
- Does not integrate with HRIS systems (yet)
