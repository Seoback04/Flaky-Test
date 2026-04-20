# Test Data — AI Resume Job Apply Bot
## Valid Inputs
- `sample_resume.pdf` — 2-page PDF with standard sections: Summary, Experience, Education, Skills.
- `sample_resume.docx` — same content, docx format.
- `sample_resume.txt` — same content, plain text with heading lines in uppercase.
- Profile JSON schema (happy):
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "+1 555-123-4567",
  "title": "Senior SDET",
  "experience_years": 7,
  "skills": ["Python", "pytest", "Selenium"]
}
```
- Confidence thresholds: `0.7` (permissive), `0.8` (default), `0.9` (strict).
## Invalid Inputs
- `empty.pdf` — 0 bytes.
- `fake.pdf` — HTML masquerading as PDF.
- `huge.pdf` — 20 MB PDF (above 5 MB limit).
- `resume.rtf` — unsupported format.
- Malformed LLM reply: `"I cannot do that, sorry."`.
- LLM reply with wrong schema: `{"email": 123}`.
## Edge Inputs
- Resume with only one section (no Experience).
- Resume with 50+ skills (stress the skills array serialization).
- Resume with emoji in name: `"Jane 🚀 Doe"`.
- Unicode name: `"张三"`.
- Very long email: `"jane.doe.the.automation.engineer.senior@a-very-long-subdomain.example.com"`.
- Phone in various formats: `"+1 555.123.4567"`, `"(555) 123-4567"`, `"5551234567"`.
## Boundary Inputs
- File sizes: 1 byte (rejected), 5 MB exactly (accepted), 5 MB + 1 byte (rejected).
- Confidence: `0.0`, `0.7999...`, `0.8`, `0.8001`, `1.0`, `1.01` (invalid).
- Experience years: `0`, `50`, `99` (accepted), `-1` (invalid).
## Special-Case Values
- LLM returns fields not in schema → dropped with warning log.
- Profile with all fields null → safe-submit blocks immediately with "no usable profile data".
- Form with duplicate required names (`email` twice) → mapping warns and picks the first; tested.
- File upload with space in filename (`sample resume.pdf`) → handled.
## Fixture Pages (self-hosted HTML fixtures)
- `simple-form.html` — text, email, tel, select, checkbox.
- `upload-form.html` — text + file input.
- `lazy-form.html` — fields rendered on scroll via JS.
- `iframe-form.html` — form nested inside an iframe.
- `recaptcha-form.html` — reCAPTCHA widget embedded.
- `tel-fax-first.html` — fax field first, phone field second (BUG-JOBBOT-001 regression).
## Assumptions
- LLM provider is available in staging; mocked in CI.
- Fixture HTML pages served via a local static server on `127.0.0.1`.
- Test runs never target real job boards without explicit `--live` flag.
