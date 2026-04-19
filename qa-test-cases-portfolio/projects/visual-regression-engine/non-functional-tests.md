# Non-Functional Tests — Visual Regression Engine
## Performance
- **1024×768 diff**: < 200 ms on a modern laptop.
- **3840×2160 diff**: < 2 s on a modern laptop.
- **Batch of 50 pairs**: < 15 s cumulative.
- Measured with `time.perf_counter`.
## Reliability
- Re-run the same compare 50 times → identical `report.json`.
- Batch with one corrupt pair → other pairs still produce reports; exit code reflects failure.
## Robustness
- Unsupported formats: clean rejection.
- EXIF orientation quirks (BUG-VISREG-002 regression).
- Files with stripped metadata.
- Transparent PNGs vs opaque RGB.
## Usability
- `diff.png` is visibly interpretable (changed pixels highlighted in red or heatmap style).
- `report.json` is human-readable.
- CLI errors identify the offending flag + value.
## Observability
- Logs include baseline path, target path, threshold, changed_ratio, decision, duration_ms.
- Exit codes: 0 pass, 1 fail, 2 invalid args, 3 missing file.
## Maintainability
- Diff engine is a single pure function with 100% unit coverage.
- Fixtures kept small (<5 MB) to keep repository lean.
## Not Covered (Explicit)
- Video / animated GIF comparison.
- Color-managed / ICC-aware comparison.
- Full-page multi-browser matrix.
