# Test Scenarios — AI Resume Job Apply Bot
## TS-JOBBOT-001 — Valid Resume Parsing
Parse supported formats (PDF / DOCX / TXT) and produce a populated profile.
_Requirements_: REQ-JOBBOT-001
_Test cases_: TC-JOBBOT-001, TC-JOBBOT-002, TC-JOBBOT-003
## TS-JOBBOT-002 — Invalid Resume File Handling
Reject or degrade safely on empty files, wrong extensions, oversized files, and corrupted content.
_Requirements_: REQ-JOBBOT-002
_Test cases_: TC-JOBBOT-004, TC-JOBBOT-005, TC-JOBBOT-006
## TS-JOBBOT-003 — Structured Profile Generation
LLM output must validate against the profile JSON schema; missing fields are marked `null` not fabricated.
_Requirements_: REQ-JOBBOT-003
_Test cases_: TC-JOBBOT-007, TC-JOBBOT-008
## TS-JOBBOT-004 — Field Detection on Forms
Detect common form inputs across a fixture page set (text, email, tel, select, radio, checkbox, file).
_Requirements_: REQ-JOBBOT-004
_Test cases_: TC-JOBBOT-009, TC-JOBBOT-010
## TS-JOBBOT-005 — Mapping Candidate Data → Fields
Map profile keys onto detected fields with a confidence score; exact match > fuzzy match > fallback.
_Requirements_: REQ-JOBBOT-005
_Test cases_: TC-JOBBOT-011, TC-JOBBOT-012
## TS-JOBBOT-006 — Autofill Validation
Typed values are echoed back by the DOM; selects set the correct option; file upload input holds a path.
_Requirements_: REQ-JOBBOT-006
_Test cases_: TC-JOBBOT-013, TC-JOBBOT-014
## TS-JOBBOT-007 — Low-Confidence Mapping Gate
When any mapped field is below the configured threshold, safe-submit blocks until reviewed.
_Requirements_: REQ-JOBBOT-007
_Test cases_: TC-JOBBOT-015, TC-JOBBOT-016
## TS-JOBBOT-008 — Missing Required Fields
Form-level required attribute missing from the profile → submission blocked with clear reason.
_Requirements_: REQ-JOBBOT-008
_Test cases_: TC-JOBBOT-017
## TS-JOBBOT-009 — File Upload Behavior
Upload a resume to the application form; verify filename in the DOM and server request.
_Requirements_: REQ-JOBBOT-009
_Test cases_: TC-JOBBOT-018
## TS-JOBBOT-010 — Safe-Submit Behavior
Submit never fires without user confirmation when `--dry-run` is set, regardless of confidence.
_Requirements_: REQ-JOBBOT-010
_Test cases_: TC-JOBBOT-019
## TS-JOBBOT-011 — Screenshot Generation
Pre-submit and post-submit screenshots are captured with file names including timestamp and job ID.
_Requirements_: REQ-JOBBOT-011
_Test cases_: TC-JOBBOT-020
## TS-JOBBOT-012 — Logging Behavior
Logs are JSON structured; emails, phone numbers, and tokens are masked.
_Requirements_: REQ-JOBBOT-012
_Test cases_: TC-JOBBOT-021
## TS-JOBBOT-013 — Malformed AI Response Handling
LLM response that is not valid JSON / fails schema → retry once, then surface an actionable error (no silent bad data).
_Requirements_: REQ-JOBBOT-013
_Test cases_: TC-JOBBOT-022
## TS-JOBBOT-014 — Browser Interaction Edge Cases
Handle dynamic fields (appear after scroll), iframes, disabled fields, CAPTCHA detection (abort gracefully).
_Requirements_: REQ-JOBBOT-014
_Test cases_: TC-JOBBOT-023, TC-JOBBOT-024
