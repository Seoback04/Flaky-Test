# Risk Analysis — Visual Regression Engine
## Functional Risks
| ID | Risk | L | I | Rating | Mitigation |
|---|---|---|---|---|---|
| R-F1 | False negative: real regression passes silently | L | H | **High** | Missing-file paths are hard errors; threshold BVA covered; golden-diff regressions in test suite. |
| R-F2 | False positive: spurious diff on unchanged page | M | M | **Medium** | Anti-aliasing tolerance; ignored regions for known noisy zones. |
| R-F3 | Ignored-region boundary bug (BUG-VISREG-001) | L | M | **Low** | Regression test added; inclusive-bounds contract documented. |
| R-F4 | EXIF rotation ignored (BUG-VISREG-002) | M | H | **High** | Fix via `ImageOps.exif_transpose`; README guidance to prefer PNG/WebP. |
## Integration Risks
| ID | Risk | L | I | Rating | Mitigation |
|---|---|---|---|---|---|
| R-I1 | Different browsers render same page with subpixel variance | M | M | **Medium** | Per-team threshold tuning; anti-alias tolerance flag. |
| R-I2 | Headless vs headed Chromium differ on fonts | M | M | **Medium** | Tests run only in headless mode; document otherwise. |
## Data Risks
| ID | Risk | L | I | Rating | Mitigation |
|---|---|---|---|---|---|
| R-D1 | Baseline corruption (e.g. git LFS misfetched) | L | H | **Medium** | Hash check in batch mode; fail loud. |
| R-D2 | Image dimensions drift after UI redesign | M | M | **Medium** | Size-mismatch policy defaults to reject (explicit approval required). |
## Usability Risks
| ID | Risk | L | I | Rating | Mitigation |
|---|---|---|---|---|---|
| R-U1 | Diff PNG unclear when many tiny changes | M | L | **Low** | Heatmap mode (future). |
| R-U2 | Users don't know about EXIF traps | M | M | **Medium** | README callout; recommend PNG/WebP. |
## Reliability Risks
| ID | Risk | L | I | Rating | Mitigation |
|---|---|---|---|---|---|
| R-R1 | OOM on 4K × 4K images | M | M | **Medium** | Streaming tile-based diff path (future). |
## Automation Risks
| ID | Risk | L | I | Rating | Mitigation |
|---|---|---|---|---|---|
| R-A1 | CI OS differs from screenshot capture OS | H | M | **High** | Capture and diff on the same OS; documented contract. |
## Priority Ranking
1. R-F1 — false negatives (the tool's central safety claim).
2. R-F4 — EXIF rotation.
3. R-A1 — cross-OS capture/diff skew.
4. R-F2 — anti-alias false positives.
5. Everything else.
