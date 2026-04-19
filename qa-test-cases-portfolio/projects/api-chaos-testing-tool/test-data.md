# Test Data — API Chaos Testing Tool
## Valid Inputs
- `specs/valid.yaml` — 3 endpoints (GET /users, POST /users, DELETE /users/{id}).
- `auth.json` — `{ "type":"bearer", "token":"TEST_TOKEN" }` (fixture only).
- Concurrency values: `1`, `4`, `8`, `16`.
- Duration: `10s`, `60s`.
- Seed: any non-negative integer (default `42`).
## Invalid Inputs
- `specs/broken.yaml` — missing `paths` key.
- `specs/nonopenapi.yaml` — arbitrary YAML not conforming to OpenAPI.
- `auth.json` with missing `token`.
- Concurrency `0`, `-1`, `"abc"`.
- Duration `-1`, `0`.
- Invalid URL: `not-a-url`, `http://`, `ftp://host`.
## Edge Inputs
- OpenAPI with **recursive schema** references (`$ref` cycles) → generator caps depth.
- Empty string in required string field.
- Unicode in names / values: `"name":"李雷"`.
- Maximum JSON nesting depth of 16.
- Numeric types at int32 / int64 limits.
## Boundary Inputs
- `minLength`/`maxLength` strings at exact boundary and ±1.
- `minimum`/`maximum` numeric at exact boundary and ±1.
- `arrays` with 0 / 1 / max items.
- Request body: 1 KB, 1 MB, 10 MB, 100 MB (expect 413 above server limit).
## Injection Corpus
- `';DROP TABLE users;--`
- `<script>alert(1)</script>`
- `$where: "sleep(1000)"`
- `../../../etc/passwd`
- `%00` null byte
- `{"$gt":""}`
- Long Unicode escape sequences
## Special-Case Values
- Zero-length response body.
- Chunked transfer-encoding response.
- Response with `Content-Encoding: gzip` but non-gzipped body (mismatch).
- Response with `Content-Length` lying about actual body size.
## Assumptions
- Stub API implements all endpoints in the spec.
- Staging environment is isolated from production.
- Time synchronization is adequate for 10 ms measurement accuracy (± clock drift disclaimers).
