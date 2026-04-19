# Bug Reporting Guidelines
## Purpose
Bad bug reports waste engineering time. Good bug reports are:
- **Reproducible** — anyone can follow the steps and see the failure.
- **Isolated** — one defect per report; no "and also…" pile-ups.
- **Attributable** — severity, priority, impact, and frequency are explicit.
- **Actionable** — the report tells the engineer where to start investigating.
## Mandatory Fields
| Field | Purpose |
|---|---|
| Bug ID | Unique, prefix-per-project (e.g., `BUG-FLAKY-007`). |
| Title | One-line summary; **what** broke and **when**. |
| Environment | OS / browser / version / build number / env (dev/staging/prod). |
| Preconditions | State the system must be in before the repro steps apply. |
| Steps to Reproduce | Numbered, deterministic, minimal. |
| Expected Result | What the spec / common sense says should happen. |
| Actual Result | What actually happened, verbatim where possible. |
| Severity | S1 / S2 / S3 / S4 (see scale below). |
| Priority | P1 / P2 / P3 / P4 (see scale below). |
| Frequency | Always / Often (≥50%) / Intermittent / Once. |
| Impact | User-facing consequence in one sentence. |
| Root Cause Hypothesis | QA's best guess; engineer may override. |
| Status | New / Triaged / In Progress / Fixed / Verified / Closed / Won't Fix. |
| Notes | Logs, screenshots, related bug IDs, workarounds. |
## Title Rules
- Start with the component or feature: `[Parser]`, `[CLI]`, `[Heatmap]`.
- Describe the symptom, not the guess: ✅ `[Classifier] Infra-suspect misclassified as flaky when all failures contain "timeout"` / ❌ `Classifier is broken`.
- Keep under ~100 characters.
## Severity Scale
| Level | Meaning |
|---|---|
| S1 | Critical — data loss / corruption / security breach / complete outage; no workaround. |
| S2 | Major — key functionality broken; workaround exists but painful. |
| S3 | Minor — non-blocking functional gap; easy workaround. |
| S4 | Cosmetic — typo, alignment, color, log-string wording. |
## Priority Scale
| Level | Meaning |
|---|---|
| P1 | Fix now — blocks release. |
| P2 | Fix this sprint. |
| P3 | Fix before the next release. |
| P4 | Backlog; fix when touched. |
## Severity vs Priority — Examples
- Data-loss in a seldom-used admin page → **S1 / P2** (bad but rarely hit).
- Brand logo incorrectly colored on landing page → **S4 / P1** (trivial but embarrassing).
- Incorrect flakiness score formula → **S2 / P1** (wrong analytics ship-blocking).
## Reproduction Steps — The Golden Rules
1. Start from a **known initial state** (cold boot, clean DB, fresh tab).
2. Use **real values** — exact config, exact input, exact file path.
3. **Numbered, imperative** — "Click X" not "clicking X seems to…".
4. One **Expected / Actual** comparison per report, not nested.
5. If the bug is **intermittent**, state the repro rate and how many times you tried.
## Evidence
Include at least one of:
- Screenshots / screen recordings.
- Console / network / server logs (filtered to the relevant window).
- A minimal repro input file (CSV, JSON, image) checked into the report folder.
## Triaging a New Bug
1. Confirm it is **not a duplicate** (search titles).
2. Confirm it is **not a misconfiguration** (re-run with a clean environment).
3. Confirm the **scope** (only browser X? only locale Y? only >10 MB files?).
4. Assign **severity first**, then **priority**.
5. Link the bug from the relevant test case (`Status: Fail` + `Linked Bug: BUG-…`).
## Re-Open Policy
- A bug marked *Fixed* is re-opened if:
  - The original repro steps produce the original Actual Result on the build that claimed the fix, OR
  - A **regression variant** of the same root cause appears.
- Re-opens carry a `re-open count`; two re-opens trigger a root-cause post-mortem.
## What NOT to Put in a Bug Report
- Blame ("the backend team's mess again"). Keep it neutral.
- Solution prescriptions ("you need to add a null check at line 112"). Leave that to the engineer — hypothesis is fine, mandate is not.
- Multi-bug dumps ("also A and B and C"). File them separately.
- PII in screenshots / logs — redact names, emails, tokens, API keys.
## Closing a Bug
A bug is closed when:
1. The original test case passes on the fixed build.
2. The regression test for the defect is added (or explicitly waived with a note).
3. The QA owner signs off in the **Notes** field.
See `templates/bug-report-template.md` for the copy/paste starting point and each project's `bug-report-samples.md` for concrete examples.
