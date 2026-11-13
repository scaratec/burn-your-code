# ADR 0004: Language-neutral black-box BDD test harness across four milestones

- **Status:** Accepted
- **Date:** 2026-11-10
- **Deciders:** EquiGuard Architecture Team

## Context

The core goal of this project is to prove that a complete specification (ADRs + LIMs + Gherkin feature files + black-box step definitions) allows an AI agent to implement the service autonomously in **any programming language** (Go, Python, Rust, TypeScript, Java, etc.) without changing a single line of the specification or test suite.

## Decision

We implement the BDD test suite in **Python `behave`** (running in `.venv/`) using strictly language-neutral, black-box interfaces across four progressive milestones:

| Milestone | Tag | Interface Under Test | Independent Verification Channel |
|---|---|---|---|
| **MI1** | `@mi1` | Executable `./bin/geofence-lib-test` reading JSON `{"point": {"lon": <float>, "lat": <float>}, "polygon": [{"lon": <float>, "lat": <float>}, ...]}` from `stdin` and writing `{"is_inside": <bool>}` to `stdout` (exit code 0) | Process `stdout` JSON |
| **MI2** | `@mi2` | Executable `./bin/geofence-processor` started as a background OS process configured via env vars (`PORT`, `FIRESTORE_EMULATOR_HOST`, `PROJECT_ID`); Pub/Sub push deliveries are simulated as HTTP POSTs, so no Pub/Sub emulator is needed | Firestore Emulator (`localhost:8082`) & HTTP `GET /health` |
| **MI3** | `@mi3` | OCI Container image built from `Dockerfile` with tag `equiguard/geofence-processor:test` | Firestore Emulator (`localhost:8082`), HTTP `GET /health`, HTTP status code (`400`), & socket/port inspection |
| **MI4** | `@mi4` | Live Cloud Run service deployed via Terraform (`terraform/`), receiving real Pub/Sub messages | Real GCP Firestore in `project_id` (read from `bdd/mi4_cloud_run.feature`) |

The `Makefile` `build` target supports any implementation language:
- If a custom `./build.sh` script exists in `workshop/`, `make build` executes `./build.sh`.
- Otherwise, it uses executables already placed in `bin/geofence-lib-test` and `bin/geofence-processor` (e.g., Python or Node.js scripts with a shebang and `chmod +x`), and builds the Go reference implementation from `go.mod` for whatever is still missing.
- Every other language (Rust, Java, TypeScript, …) provides `./build.sh`; this is the route the workshop's exercise 4 prescribes.

## Consequences

### Positive

- Complete decoupling between specification (`governance/`, `bdd/`) and application language.
- Deleting the implementation (`make burn`) and asking an AI agent to re-implement in Go, Python, Rust, or TypeScript requires zero changes to `bdd/` or `governance/`.
- Progressive verification: algorithmic bugs fail in MI1 (milliseconds), integration bugs fail in MI2 (seconds), packaging bugs fail in MI3, and cloud IAM/networking bugs fail in MI4.

### Negative

- Implementing languages must provide the lightweight CLI adapter `./bin/geofence-lib-test` in addition to the HTTP server `./bin/geofence-processor`.

### Neutral

- The `project_id` in `bdd/mi4_cloud_run.feature` serves as the single source of truth for `Makefile`, Docker, and Terraform in MI4.

## Security Implications

The test harness never imports application modules in-process and never shares memory with the system under test. Local tests (`@mi1`–`@mi3`) run hermetically against local emulators without cloud credentials.

## Alternatives Considered

- **In-process unit/integration tests in the target language (e.g., `go test`, `pytest`, `jest`).** Rejected because tests written in the application's language must be rewritten whenever the implementation language changes, violating the single-specification principle.
- **Testing only via Docker (`@mi3`) and skipping `@mi1`/`@mi2`.** Rejected because fast inner-loop feedback (`@mi1` runs in < 0.2s without Docker or emulators) drastically reduces AI agent iteration time and token cost.

## References

- Enforced by: [`bdd/mi1_geofence_library.feature`](../../bdd/mi1_geofence_library.feature), [`bdd/mi2_geofence_processor.feature`](../../bdd/mi2_geofence_processor.feature), [`bdd/mi3_geofence_processor_image.feature`](../../bdd/mi3_geofence_processor_image.feature), [`bdd/mi4_cloud_run.feature`](../../bdd/mi4_cloud_run.feature)
