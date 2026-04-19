# Project Overview — AI Resume Job Apply Bot
## What It Is
A Python + browser-automation tool that ingests a candidate's resume (PDF/DOCX), produces a structured profile via an LLM, opens target job-application pages, detects form fields, **maps profile → fields with confidence scores**, previews the mapping, and (with explicit user consent) submits the application.
## Why It Matters
Manual job applications are time-consuming and repetitive. Automated applications at scale risk submitting bad data. This tool exists to make the process both **fast and safe** — safety comes from visible mapping confidence, dry-run previews, screenshot evidence, and a hard "review before submit" gate for low-confidence cases.
## User Personas
- **Job seeker** — the primary operator.
- **Privacy-conscious user** — expects resume data not to leak; expects clear consent.
- **Debugging developer** — needs observable logs and screenshot trails.
## Core Surfaces Under Test
1. **Resume ingestion** — PDF / DOCX / TXT parsing.
2. **Profile extraction** — LLM call → structured profile (name, email, phone, experience, etc.).
3. **Browser automation** — navigate, wait, locate fields, handle dynamic pages.
4. **Field detection** — CSS/XPath/semantic detection of inputs / selects / file uploads.
5. **Mapping engine** — profile keys → form fields with confidence scores.
6. **Autofill execution** — typed input, selects, radio/checkbox, file upload.
7. **Safe-submit gate** — confirmation step for low-confidence or missing required fields.
8. **Screenshot capture** — pre-submit and post-submit artifacts.
9. **Logging** — structured JSON logs; no resume PII leakage.
10. **Error recovery** — captcha, bot-check, timeouts, element-not-found retries.
## Inputs / Outputs
- **Inputs**: resume file, list of job URLs, optional profile overrides, confidence threshold.
- **Outputs**: per-job `mapping.json`, `submission.json`, pre/post screenshots, structured log.
## Key Contracts
- No submission fires below the configured confidence threshold without explicit user approval.
- Resume content in logs is masked (email → `***@***.tld`).
- Missing required fields abort submission with a clear reason.
## Known Constraints
- LLM non-determinism — temperature should be low; responses validated against a JSON schema.
- Sites with CAPTCHA / WAF challenges are out of scope.
- Only tested against forms using common HTML inputs; heavy canvas-based forms are unsupported.
## Testability Notes
- Mapping engine is pure logic on top of LLM output — easy to unit-test with fixtures.
- Browser layer should be wrapped behind an interface so tests can use a Playwright / Selenium stub.
- LLM responses must be fixture-able for deterministic test runs.
