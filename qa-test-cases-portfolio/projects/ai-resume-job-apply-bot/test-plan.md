# Test Plan — AI Resume Job Apply Bot
_Version_: 1.0 &nbsp;|&nbsp; _Owner_: QA Portfolio
## 1. Introduction
Validate the bot's end-to-end flow: resume ingestion → LLM-extracted profile → form-field detection → mapping → safe submit. The primary quality risk is **data correctness under LLM non-determinism**; the primary safety risk is **accidental submission of wrong or partial data**.
## 2. Objectives
- Prove resume parsing handles common formats and degrades safely on invalid files.
- Prove the mapping engine respects the configured confidence threshold.
- Validate safe-submit gate blocks submissions with missing required fields or low confidence.
- Verify logs contain no unmasked PII.
- Verify screenshots are captured and paired with each submission attempt.
## 3. Scope
**In scope**
- Resume ingestion (PDF, DOCX, TXT).
- Profile extraction from LLM (schema-validated).
- Field detection on representative HTML forms.
- Mapping engine (exact match, fuzzy match, fallback).
- Autofill on text / select / file / radio / checkbox.
- Safe-submit gate behavior.
- Logging and screenshot artifacts.
- CLI argument validation.
**Out of scope**
- Bypassing CAPTCHA / bot detection.
- Sites requiring OAuth flows beyond username/password.
- LLM provider availability / billing.
## 4. Test Approach
| Dimension | Approach |
|---|---|
| Functional | Positive happy paths per site type. |
| Negative | Malformed resumes, broken LLM responses, hostile field names. |
| Boundary | Max resume size, min profile, many fields, unicode. |
| Safety | Safe-submit gate cases dominate High-risk coverage. |
| Non-functional | Performance, reliability, privacy, observability. |
## 5. Test Design Techniques
- **Decision tables** for the safe-submit gate.
- **State transition** for the form-fill state machine.
- **Equivalence partitioning** for resume formats.
- **Negative / error guessing** for hostile field names and LLM drift.
## 6. Deliverables
Same 10-file contract as the other projects.
## 7. Environments
- **Dev / CI**: real browser under Playwright in headless mode against a fixture set of static HTML pages.
- **Staging**: real browser against public demo job boards.
- **LLM**: mocked in unit tests; real (low temperature) in staging smoke.
## 8. Entry / Exit Criteria
Entry: bot installs cleanly, fixture site reachable, LLM key available for staging.
Exit: all High-risk cases Pass; 0 open S1/S2; safe-submit blocks all under-threshold cases in evidence.
## 9. Risks
See `risk-analysis.md`.
