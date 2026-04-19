# Project Overview — Visual Regression Engine
## What It Is
A Python CLI that compares a **target** screenshot against a **baseline** screenshot pixel-by-pixel (with optional anti-aliasing tolerance and ignored regions), produces a **diff image** with highlighted changed regions, and returns a pass/fail decision based on a configurable difference threshold.
## Why It Matters
UI regressions sneak past functional tests all the time — a misaligned button, a color change, a font swap. Visual regression catches these without relying on brittle selectors.
## User Personas
- **Frontend engineer** — runs the tool in CI after every PR.
- **QA engineer** — curates baselines and tunes thresholds per page.
- **Designer** — reviews diff images for intent vs regression.
## Core Surfaces Under Test
1. **Image loader** — supports PNG / JPG / WebP.
2. **Alignment / resize** — matches dimensions between baseline and target.
3. **Diff engine** — per-pixel comparison with anti-aliasing tolerance.
4. **Ignored regions** — rectangle masks applied before comparison.
5. **Threshold decision** — ratio of changed pixels vs total pixels.
6. **Diff renderer** — output image highlighting changed regions.
7. **Batch runner** — compare many pairs via a manifest file.
8. **CLI** — `compare`, `batch`, `approve-baseline` commands.
## Inputs / Outputs
- **Inputs**: `baseline.png`, `target.png`, `--threshold`, `--ignore-regions`, `--anti-alias` tolerance.
- **Outputs**: `diff.png`, `report.json` (decision + stats), exit code reflecting pass/fail.
## Key Contracts
- `threshold = 0.0` → exact match required.
- `threshold = 1.0` → any diff accepted (pass always).
- Ignored regions are applied to **both** images before diffing.
- Missing baseline is an error, not a silent pass.
## Known Constraints
- Not designed for video frame comparison.
- Anti-aliasing tolerance is heuristic; not a color-managed comparison.
- Huge images (>50 MP) may exhaust memory on constrained CI.
## Testability Notes
- Diff engine is pure (image1, image2 → stats) — trivially fixture-testable.
- CLI is a thin wrapper; most tests target the diff engine.
- Golden diff images are committed alongside fixtures.
