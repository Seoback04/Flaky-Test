# Test Execution Summary — Visual Regression Engine — 1.2.0
_Owner_: QA Portfolio &nbsp;|&nbsp; _Generated_: 2026-04-10 &nbsp;|&nbsp; _Build_: 1.2.0
## 1. Scope Tested
- Image loading (PNG/JPG/WebP).
- Pixel diff engine.
- Threshold decision at boundaries (0.0, 1.0).
- Ignored region handling (single + multi-rect).
- Batch manifest run.
- CLI arg validation.
## 2. Summary
| Metric | Count |
|---|---|
| Total test cases | 20 |
| Passed | 19 |
| Failed | 0 |
| Blocked | 1 (BUG-VISREG-002 pending fix for EXIF rotation) |
| Not Run | 0 |
| Pass % (of executed) | 100% |
## 3. Coverage by Type
| Type | Planned | Executed | Passed | Failed |
|---|---|---|---|---|
| functional | 11 | 11 | 11 | 0 |
| boundary | 3 | 3 | 3 | 0 |
| negative | 6 | 5 | 5 | 0 |
## 4. Coverage by Risk
| Risk | Planned | Executed | % Executed |
|---|---|---|---|
| High | 14 | 13 | 93% |
| Medium | 6 | 6 | 100% |
## 5. Key Defects
| Bug ID | Title | Severity | Priority | Status |
|---|---|---|---|---|
| BUG-VISREG-001 | Boundary pixel counted in diff despite ignored rect | S2 | P1 | Fixed |
| BUG-VISREG-002 | JPG EXIF orientation ignored → false diff | S1 | P1 | Triaged |
| BUG-VISREG-003 | Malformed `--ignore` silently accepted | S3 | P2 | Fixed |
## 6. Top Risks Still Open
- BUG-VISREG-002 — false positives on EXIF-rotated JPGs.
- No perceptual-similarity fallback; anti-aliasing differences between renderers can still trigger false fails.
## 7. Deviations From Plan
- Performance tests on 4K images punted to a follow-up (CI VM memory constraints).
## 8. Release Recommendation
**Conditional Go.**
**Rationale**: All non-blocked High-risk cases pass. The JPG EXIF issue is deterministic and documented.
**Conditions**:
- Merge `ImageOps.exif_transpose` fix.
- Add README note: "prefer PNG/WebP; JPG requires EXIF-aware loader".
## 9. Known Limitations
- No SSIM / perceptual metrics.
- Size-mismatch policy is "reject" by default; crop/pad modes are documented but not CI-gated.
- Large (>50 MP) images may OOM in constrained CI runners.
## 10. Sign-off
| Role | Name | Date |
|---|---|---|
| QA Owner | QA Portfolio | 2026-04-10 |
| Tech Lead | — | Pending BUG-VISREG-002 merge |
