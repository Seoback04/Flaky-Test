# Test Data — Flaky Test Detector
## Valid Inputs
### `--runs`
- Minimum useful: `5`
- Typical: `10`, `20`, `50`
- Large: `200`
### `--delay`
- `0.0`, `0.5`, `2.0`
### `-k` filter
- `"flaky"`, `"infra"`, `"not slow"`
### `-m` marker
- `"smoke"`, `"regression"`
### pytest-json-report payloads (well-formed)
```json
{
  "created": 1700000000.0,
  "duration": 1.23,
  "exitcode": 1,
  "tests": [
    {"nodeid": "demo/test_flaky.py::test_random_50_50", "outcome": "passed", "duration": 0.01},
    {"nodeid": "demo/test_flaky.py::test_random_50_50", "outcome": "failed", "duration": 0.02,
     "call": {"outcome": "failed", "longrepr": "AssertionError: coin-flip"}}
  ]
}
```
## Invalid Inputs
### `--runs`
- `0` → reject.
- `-1` → reject.
- `"abc"` → reject.
### `--delay`
- `-0.1` → reject.
- `"NaN"` → reject.
### JSON payloads
- `{not json` — corrupt.
- `[]` — wrong top-level type.
- `null` — null payload.
- Missing `tests` key → treated as empty.
- `tests` value not a list → reject / empty.
## Edge Inputs
- pytest exit code 5 (no tests collected) with empty `tests` array → analyzer produces an empty summary, not a crash.
- Single test only → reports produced with one-row CSVs.
- 1 run only → analyze runs; flakiness_score always 0.0 (can't have mixed outcomes with N=1).
- Test whose nodeid contains unicode: `"tests/test_emoji.py::test_π_pi"` → must survive CSV + HTML.
- Test whose duration is 0.0 across all runs → avg=0, stddev=0, no false high-variance flag.
- Runs where the same nodeid is sometimes skipped → skipped outcomes excluded from executed_runs.
## Boundary Inputs
- `--runs 1` → smallest legal.
- `--runs 10000` → largest legal (documented cap).
- Flakiness score = 0.0 (all pass), 0.5 (perfect mix), exactly 0.5 at 1 pass + 1 fail.
- Transitions: 0 (monotonic), N-1 (fully alternating).
- Longest streak length = total executed runs.
## Special-Case Values
- All-skipped test (executed_runs = 0) → category = `unknown`.
- Single `xpassed` outcome — counts as pass (per `Outcome.is_pass`).
- Single `xfailed` outcome — not counted as executed.
- Error messages mixing infra + non-infra keywords — infra dominance computed on per-failure basis.
## Assumptions
- Test nodeids are stable across runs (same test → same ID).
- Durations are in seconds, non-negative floats.
- JSON timestamps are Unix seconds.
- The runner runs on the same host for all N runs (no distributed execution).
