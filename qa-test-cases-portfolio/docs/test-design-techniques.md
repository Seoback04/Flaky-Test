# Test Design Techniques
## Why Techniques Matter
Ad-hoc tests produce ad-hoc coverage. Named techniques force us to think in structured partitions so we can demonstrate *why* a set of test cases is sufficient, not just long.
The projects in this portfolio apply the techniques below. Each test case in every `test-cases.csv` is tagged with a **Type** column that maps back here.
## 1. Equivalence Partitioning (EP)
Group inputs into classes where all members are expected to be treated identically; test one representative per class.
**Example — Flaky Test Detector, `--runs N`:**
- Invalid class: N ≤ 0 → reject with error.
- Valid small class: 1 ≤ N ≤ 9 → warn about weak signal, proceed.
- Valid typical class: 10 ≤ N ≤ 100 → accept.
- Valid large class: 100 < N ≤ 10 000 → accept with warning.
- Invalid class: N > 10 000 → reject (resource-protection cap).
One test per class = 5 cases instead of a random N.
## 2. Boundary Value Analysis (BVA)
Bugs cluster at edges. For each valid partition, test just-inside and just-outside its boundaries.
**Example — Visual Regression, pixel diff threshold (0.0 – 1.0):**
- 0.0 (exact match required), 0.0001 (just above min), 0.9999 (just below max), 1.0 (any diff accepted), -0.01 (invalid), 1.01 (invalid).
## 3. Negative Testing
Actively try to break the system with malformed, missing, or malicious inputs.
**Examples:**
- Corrupt JSON report fed to the Flaky Test Detector parser.
- Resume PDF that is actually an HTML file with a .pdf extension (AI Resume Bot).
- API payload with deeply nested recursive JSON (Chaos Tool).
- PNG declared as JPEG via content-type header mismatch (Visual Regression).
## 4. Error Guessing
Experience-driven. Target places historically flaky in similar systems.
**Hot spots used in this portfolio:**
- File paths with spaces / unicode / trailing separators.
- DST transitions and non-UTC timezones in timestamps.
- Concurrent runs writing to the same output directory.
- Network mid-request timeouts vs connect timeouts.
- Off-by-one in 0-indexed vs 1-indexed run counters.
## 5. Decision Tables
Use when the output depends on combinations of conditions. Each rule = one row.
**Example — Flaky Test Detector classifier:**
| pass? | fail? | infra-dominant? | executed>0? | Category |
|---|---|---|---|---|
| all | 0 | N/A | yes | stable_pass |
| 0 | all | no | yes | stable_fail |
| 0 | all | yes | yes | infra_suspect |
| mix | mix | no | yes | flaky |
| mix | mix | yes | yes | infra_suspect |
| 0 | 0 | N/A | no | unknown |
Each rule becomes one test case.
## 6. State Transition Testing
Use when the system has discrete states and illegal transitions matter.
**Example — AI Resume Bot form-fill state machine:**
- States: idle → form_loaded → mapping → previewing → submitting → submitted / aborted.
- Test: submit while in `mapping` (illegal) — should raise, not silently submit.
- Test: go back to `form_loaded` from `previewing` — mappings preserved.
## 7. Risk-Based Prioritization
For each requirement, assign:
- **Likelihood** — how often will users hit this? (H/M/L)
- **Impact** — how bad is failure? (H/M/L)
- Risk = likelihood × impact → H / M / L.
High-risk cases are executed first and must pass for a release to ship.
**Example — API Chaos Tool:**
- Data-corrupting requests (H × H = H) → blocking.
- Response time measurement accuracy (M × M = M) → non-blocking.
- Color of rate-limit log line (L × L = L) → sampled.
## 8. Pairwise / Combinatorial (Lightweight)
Some test cases have too many parameter combinations to enumerate. Use pairwise when a single parameter doesn't independently drive behavior.
**Example — Visual Regression Engine:**
- Parameters: image format × threshold × ignored regions × anti-aliasing.
- Full matrix = 3×3×2×2 = 36 combinations; pairwise ≈ 9–12 covering all pairs.
## 9. Positive + Negative + Edge Triangulation
Every feature gets, at minimum, one of each:
- **Positive** — happy path, valid input, expected output.
- **Negative** — invalid/hostile input, expected clean rejection.
- **Edge** — boundary, empty, max, min, unicode, whitespace, duplicate.
If a feature has fewer than 3 cases, it's under-tested.
## 10. Charter-Based Exploratory
Time-boxed sessions with a written charter, recorded notes, and a debrief. Never "just click around."
See `templates/exploratory-testing-template.md`.
## Tagging Convention
Each test case carries a `Type` tag from this set:
`functional | regression | negative | boundary | edge | error-path | usability | reliability | performance | security | exploratory`
This lets execution reports slice coverage by type (e.g., "we executed 90% functional but only 40% boundary — gap in BVA coverage").
