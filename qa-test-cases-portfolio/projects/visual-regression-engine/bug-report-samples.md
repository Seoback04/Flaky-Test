# Bug Report Samples — Visual Regression Engine
---
## BUG-VISREG-001 — [Ignored Regions] Changes touching the ignored-rect boundary counted as diff
| Field | Value |
|---|---|
| **Bug ID** | BUG-VISREG-001 |
| **Severity** | S2 |
| **Priority** | P1 |
| **Frequency** | Always |
| **Status** | Fixed |
| **Linked Test Case** | TC-VISREG-011 |
| **Linked Requirement** | REQ-VISREG-005 |
### Preconditions
- baseline + target differ by one pixel at coordinate `(100, 100)`.
- Ignored region specified as `100,100,110,110`.
### Steps to Reproduce
1. `python -m visreg compare --baseline b.png --target t.png --ignore 100,100,110,110`.
2. Inspect `report.json`.
### Expected Result
`changed_ratio = 0`, decision `pass` (the differing pixel sits on the rectangle boundary).
### Actual Result
`changed_ratio = 1/N`, decision `fail`.
### Impact
Teams specifying tight ignored rects get false fails. Workaround is to over-allocate the rect by 1 pixel on each side — but that's footgun behavior.
### Root Cause Hypothesis
Rectangle boundary test used `<` on upper bounds instead of `<=`, so the boundary pixel wasn't inside the mask.
### Notes
- Fix: clarify rectangle semantics in README (inclusive on both ends) and align code.
- Regression test: TC-VISREG-011.
---
## BUG-VISREG-002 — [Loader] JPG metadata rotation ignored; images compared in wrong orientation
| Field | Value |
|---|---|
| **Bug ID** | BUG-VISREG-002 |
| **Severity** | S1 |
| **Priority** | P1 |
| **Frequency** | Always for JPGs with EXIF orientation |
| **Status** | Triaged |
| **Linked Test Case** | TC-VISREG-002 |
| **Linked Requirement** | REQ-VISREG-001 |
### Preconditions
- Baseline and target are the same visual image, but the target carries EXIF orientation metadata (rotated 90°).
### Steps to Reproduce
1. Capture screenshot A and screenshot B (same content) where B was taken with a camera / tool that sets `Orientation=6` EXIF tag.
2. Run `compare`.
### Expected Result
Images are auto-rotated per EXIF orientation before diff; diff ratio ≈ 0.
### Actual Result
Images are compared as raw pixel buffers. Orientation difference yields a massive diff, decision `fail`.
### Impact
Produces a large volume of false positives whenever screenshots come through camera-derived or mobile-capture pipelines.
### Root Cause Hypothesis
Loader uses `PIL.Image.open` without `ImageOps.exif_transpose`.
### Notes
- Fix candidate: add `ImageOps.exif_transpose` by default; add `--no-exif-transpose` opt-out.
- Will also document that WebP/PNG are preferred formats for visual regression to avoid metadata traps.
---
## BUG-VISREG-003 — [CLI] `--ignore` accepts malformed rectangle silently
| Field | Value |
|---|---|
| **Bug ID** | BUG-VISREG-003 |
| **Severity** | S3 |
| **Priority** | P2 |
| **Frequency** | Always when rect string is malformed |
| **Status** | Fixed |
| **Linked Test Case** | TC-VISREG-012 |
| **Linked Requirement** | REQ-VISREG-005 |
### Preconditions
- Provide `--ignore '100,abc,110,110'`.
### Steps to Reproduce
1. Run `compare --ignore 100,abc,110,110`.
### Expected Result
Exit non-zero; error: `Invalid --ignore rectangle: '100,abc,110,110' (expected 4 integers)`.
### Actual Result
Tool silently treats malformed rect as "no mask" and compares the entire image; user sees a pass they didn't expect.
### Impact
Silent failure of a safety-relevant flag.
### Root Cause Hypothesis
Argparse custom type catches `ValueError` too broadly and returns `None` instead of raising.
### Notes
- Fix: raise `argparse.ArgumentTypeError` with a precise message.
