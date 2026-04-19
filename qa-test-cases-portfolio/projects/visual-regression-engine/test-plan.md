# Test Plan — Visual Regression Engine
_Version_: 1.0 &nbsp;|&nbsp; _Owner_: QA Portfolio
## 1. Introduction
Validate the visual-diff engine and CLI. The central quality concern is that the tool **does not produce false negatives** (i.e. fails to detect real regressions) — that is worse than a false positive.
## 2. Objectives
- Prove the diff engine detects changes at and above the configured threshold.
- Prove ignored regions are excluded from the diff calculation.
- Prove missing-file / unsupported-format paths fail cleanly.
- Produce a deterministic diff image and report artifact per comparison.
## 3. Scope
**In scope**
- Image loading (PNG / JPG / WebP).
- Size mismatch handling (resize policy).
- Pixel diff with anti-aliasing tolerance.
- Ignored regions.
- Threshold decision logic.
- Diff image rendering.
- Batch manifest runner.
- CLI argument validation.
**Out of scope**
- Perceptual similarity (SSIM) metrics (future enhancement).
- Cross-browser screenshot capture (assumed done by caller).
- Video / animated GIF comparison.
## 4. Test Approach
| Dimension | Approach |
|---|---|
| Functional | Identical pair pass, single-pixel diff fail, region-masked diff pass. |
| Boundary | Threshold at 0.0, 0.5, 1.0; image size 1×1; 1-byte diff. |
| Negative | Missing baseline, corrupt file, unsupported format. |
| Non-functional | Performance on 4K images; memory bound. |
## 5. Test Design Techniques
- **BVA** on threshold; **EP** on image formats.
- **Decision tables** for size-mismatch policy (crop / pad / reject).
- **Error guessing**: stripped metadata, ICC profile mismatch, grayscale vs RGB.
## 6. Deliverables
Same 10-file contract.
## 7. Environments
- Dev (Linux / Windows / macOS).
- CI (Linux container).
## 8. Entry / Exit
Entry: package installs; fixture images load; baseline manifest parses.
Exit: all High-risk cases Pass; CI pipeline exits non-zero on any real regression in the golden set.
## 9. Risks
See `risk-analysis.md`.
