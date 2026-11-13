# Phase 5 Prompt — Autonomous Polyglot Implementation

First ensure the workspace has only the specification and steps (`make burn` removes any existing application code). Then pick **any target language** you like (e.g., **Python**, **Go**, **Rust**, **TypeScript/Node.js**, **Java**) and run **Antigravity CLI (`agy`)** with Gemini using this single prompt:

```text
Implement the EquiGuard service in <YOUR_LANGUAGE_OF_CHOICE> (e.g., Python / Go / Rust / TypeScript) completely from its specification in this repository.

The specification is complete and read-only:
- Architecture Decision Records and Limitation Records under `governance/`
- Error path enumeration and Gherkin feature files under `bdd/`
- Black-box Python `behave` step definitions and test harness under `bdd/steps/` and `bdd/environment.py`
- `Makefile` and `terraform/`

Rules:
1. Do NOT modify any file under `governance/`, `bdd/`, or `terraform/`. If you believe a scenario is wrong, leave it and report it at the end.
2. Ask zero questions. Every architectural and behavioral decision is already settled in `governance/adr/` and `bdd/*.feature`.
3. Provide:
   - `./bin/geofence-lib-test`: CLI executable reading JSON `{"point": {"lon": ..., "lat": ...}, "polygon": [{"lon": ..., "lat": ...}, ...]}` from `stdin` and writing `{"is_inside": true|false}` to `stdout` (ADR-0001, ADR-0004).
   - `./bin/geofence-processor`: HTTP service listening on `$PORT` (default `8081`) implementing `GET /health` and `POST /telemetry-push` against Firestore (`$PROJECT_ID`, `$FIRESTORE_EMULATOR_HOST`) per ADR-0002 and ADR-0003.
   - `./build.sh` (if not using Go or Rust) so `make build` produces executable `./bin/geofence-lib-test` and `./bin/geofence-processor`.
   - `Dockerfile`: builds `equiguard/geofence-processor:test` and starts `geofence-processor` on port `8081`.
4. You are only done when `make test-all` (running MI1 + MI2 + MI3 against the local Firestore and Pub/Sub emulators) passes TWICE IN A ROW with 0 failed scenarios.
5. At the end, print the exact verification numbers: Features, Scenarios (passed / failed / skipped), and Steps.
```
