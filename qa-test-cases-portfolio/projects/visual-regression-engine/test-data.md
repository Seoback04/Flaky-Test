# Test Data — Visual Regression Engine
## Valid Inputs
- `fixtures/baseline_1024x768.png` — clean PNG baseline.
- `fixtures/target_identical.png` — pixel-identical copy.
- `fixtures/target_1px_diff.png` — one pixel differs at (100, 100).
- `fixtures/target_20pct_diff.png` — 20% of pixels changed in center region.
- `fixtures/baseline.jpg`, `fixtures/baseline.webp` — same content in other formats.
- Thresholds: `0.0`, `0.001`, `0.01`, `0.1`, `0.5`, `1.0`.
- Ignored regions: `100,100,110,110`, `0,0,50,50;100,100,150,150`.
## Invalid Inputs
- `fixtures/missing.png` — does not exist.
- `fixtures/corrupt.png` — truncated file.
- `fixtures/empty.png` — 0 bytes.
- `fixtures/diagram.svg` — unsupported format.
- `fixtures/diagram.tiff` — unsupported format.
- Ignored region: `100,abc,110,110` (non-integer).
- Threshold: `-0.1`, `1.5`, `"abc"`.
## Edge Inputs
- `fixtures/baseline_1x1.png` — 1×1 pixel image (smoke).
- `fixtures/baseline_4k.png` — 3840×2160 stress.
- `fixtures/baseline_jpg_with_exif.jpg` — EXIF orientation 6 (BUG-VISREG-002 fixture).
- Grayscale PNG vs RGB PNG (decision table case: accept with channel coercion, reject with flag).
- PNG with alpha channel vs opaque RGB.
## Boundary Inputs
- threshold = `0.0` (exact), `1.0` (always pass), and just inside/outside each.
- Image size mismatch by 1 pixel in width / height.
- Ignored rectangle exactly covering the differing pixel.
- Ignored rectangle one pixel short on each side.
## Special-Case Values
- Identical images → changed_ratio = 0.0 exactly.
- Fully different images (all pixels different) → changed_ratio = 1.0.
- Transparent PNG over different background.
- ICC color profile differences between baseline and target (documented as ignored; surface as S3).
## Assumptions
- Screenshots are captured on the same OS / browser / DPR as baseline.
- File paths are local; no remote fetching.
- Fixtures are small enough to run in CI (<5 MB each).
