# Test Scenarios — Visual Regression Engine
## TS-VISREG-001 — Baseline Image Loading
Load supported formats (PNG / JPG / WebP) without error.
_Requirements_: REQ-VISREG-001
_Test cases_: TC-VISREG-001, TC-VISREG-002, TC-VISREG-003
## TS-VISREG-002 — Target Image Loading
Load target image; handle file-not-found cleanly.
_Requirements_: REQ-VISREG-002
_Test cases_: TC-VISREG-004, TC-VISREG-005
## TS-VISREG-003 — Image Diff Generation
Produce a diff image with changed regions highlighted.
_Requirements_: REQ-VISREG-003
_Test cases_: TC-VISREG-006, TC-VISREG-007
## TS-VISREG-004 — Threshold Behavior
Threshold 0.0 demands exact match; 0.5 allows partial; 1.0 always passes.
_Requirements_: REQ-VISREG-004
_Test cases_: TC-VISREG-008, TC-VISREG-009, TC-VISREG-010
## TS-VISREG-005 — Ignored Region Handling
Changes within an ignored rectangle are excluded from the diff.
_Requirements_: REQ-VISREG-005
_Test cases_: TC-VISREG-011, TC-VISREG-012
## TS-VISREG-006 — Changed-Region Highlighting
Diff image highlights only changed (non-ignored) regions.
_Requirements_: REQ-VISREG-006
_Test cases_: TC-VISREG-013
## TS-VISREG-007 — Pass/Fail Decision Logic
Decision reflects `changed_ratio vs threshold` exactly.
_Requirements_: REQ-VISREG-007
_Test cases_: TC-VISREG-014, TC-VISREG-015
## TS-VISREG-008 — Unsupported Format Handling
Unsupported format (BMP, TIFF, SVG) rejected with clear error.
_Requirements_: REQ-VISREG-008
_Test cases_: TC-VISREG-016
## TS-VISREG-009 — Missing File Handling
Missing baseline or target produces an actionable error, never silent pass.
_Requirements_: REQ-VISREG-009
_Test cases_: TC-VISREG-017
## TS-VISREG-010 — Batch Comparison Behavior
Manifest-driven batch run produces one report per pair.
_Requirements_: REQ-VISREG-010
_Test cases_: TC-VISREG-018
## TS-VISREG-011 — CLI Validation
Invalid threshold / missing args rejected.
_Requirements_: REQ-VISREG-011
_Test cases_: TC-VISREG-019, TC-VISREG-020
