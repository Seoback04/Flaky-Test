# Bug Report Samples — AI Resume Job Apply Bot
---
## BUG-JOBBOT-001 — [Mapping] Phone mapped into 'Fax' field when `Fax` label appears first
| Field | Value |
|---|---|
| **Bug ID** | BUG-JOBBOT-001 |
| **Severity** | S1 |
| **Priority** | P1 |
| **Frequency** | Always on affected layout |
| **Status** | Fixed |
| **Linked Test Case** | TC-JOBBOT-011 |
| **Linked Requirement** | REQ-JOBBOT-005 |
### Preconditions
- Form page with two tel-type inputs: the first labeled "Fax Number" and the second labeled "Phone Number".
- Profile contains only `phone`, no `fax`.
### Steps to Reproduce
1. Load fixture `tel-fax-first.html`.
2. Run `map_profile_to_fields(profile, fields)`.
3. Inspect the mapping for the Fax field.
### Expected Result
Fax field is unmapped (or mapped at very low confidence); Phone is mapped to `profile.phone` at high confidence.
### Actual Result
Fax field is mapped to `profile.phone` at confidence 0.72 (fuzzy on "number"); Phone is also mapped to the same value.
### Impact
Candidate's phone number leaks into a Fax field on the applied form — visible to the recruiter and wrong.
### Root Cause Hypothesis
Fuzzy matcher scored "Fax Number" vs "phone" via shared token "Number" without a type-compatibility penalty.
### Notes
- Fix: require `aria-label`/`name` semantic match before fuzzy; exclude "fax" tokens from phone mapping via a stop-list.
- Regression test added.
---
## BUG-JOBBOT-002 — [Logging] Resume text echoed in DEBUG logs in plaintext
| Field | Value |
|---|---|
| **Bug ID** | BUG-JOBBOT-002 |
| **Severity** | S1 |
| **Priority** | P1 |
| **Frequency** | Always when log level is DEBUG |
| **Status** | Fixed |
| **Linked Test Case** | TC-JOBBOT-021 |
| **Linked Requirement** | REQ-JOBBOT-012 |
### Preconditions
- `--log-level=DEBUG` set.
### Steps to Reproduce
1. Run `apply --log-level=DEBUG --dry-run`.
2. Tail `bot.log`.
### Expected Result
Log contains masked identifiers only (email → `***@***.***`, phone → `***-***-****`).
### Actual Result
Log contains the raw resume text verbatim including full name, email, and phone number.
### Impact
PII leakage if logs are uploaded to a shared issue tracker or bug report.
### Root Cause Hypothesis
PII-masking filter is only applied to INFO+ levels; DEBUG path bypasses the filter to emit raw LLM inputs.
### Notes
- Fix: apply the redaction filter at the logger root, not per level.
- Added `test_logging_pii_mask_on_all_levels`.
---
## BUG-JOBBOT-003 — [Safe-Submit] `--dry-run` flag ignored when job URL contains query parameters
| Field | Value |
|---|---|
| **Bug ID** | BUG-JOBBOT-003 |
| **Severity** | S1 |
| **Priority** | P1 |
| **Frequency** | Always on URLs with `?` |
| **Status** | Triaged |
| **Linked Test Case** | TC-JOBBOT-019 |
| **Linked Requirement** | REQ-JOBBOT-010 |
### Preconditions
- Job URL: `https://jobs.example.com/apply?ref=abc&jid=123`.
- `--dry-run` passed on CLI.
### Steps to Reproduce
1. `python -m bot apply --url "https://jobs.example.com/apply?ref=abc&jid=123" --dry-run`.
2. Watch network traffic for submission POST.
### Expected Result
No submission POST issued; dry-run report printed.
### Actual Result
Submission POST **is** issued; application submitted to the site.
### Impact
Catastrophic: live submissions when the user explicitly asked for dry-run. Breaks the safety contract.
### Root Cause Hypothesis
CLI config-merging logic parses the URL with `urlsplit` and on URLs with query strings clobbers `dry_run=True` with defaults from the URL-derived config loader.
### Notes
- Workaround until fix: pass `--url` with no query string, move query params to `--site-params`.
- Must ship as hotfix before next release.
