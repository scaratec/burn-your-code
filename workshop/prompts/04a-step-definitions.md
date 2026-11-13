# Phase 4a Prompt — Language-Neutral Black-Box Step Definitions (`bdd/steps/`)

Run this prompt in **Antigravity CLI (`agy`)** with Gemini after the Specification Critic approves the specification (or after `make checkpoint-features`):

```text
Read AGENTS.md (§3.5), BDD_GUIDELINES_v1.9.0_EN.md (§1.3, §4, §5, §6, §13), governance/adr/0004-language-neutral-black-box-test-harness.md, and all feature files in `bdd/*.feature`.

Implement the Python `behave` test harness (`bdd/environment.py`) and step definitions (`bdd/steps/geofence_steps.py`, `bdd/steps/processor_steps.py`, `bdd/steps/image_steps.py`, `bdd/steps/cloud_steps.py`) following these rules strictly:

1. **100% Language-Neutral Black-Box Contract:**
   - Never import application code or assume a specific programming language.
   - MI1 (`geofence_steps.py`): invoke `./bin/geofence-lib-test` passing JSON `{"point": point_data, "polygon": polygon}` on `stdin` and reading `{"is_inside": true|false}` from `stdout`. If `./bin/geofence-lib-test` is missing, fail cleanly with an `AssertionError` explaining that the scenario is RED.
   - MI2 (`processor_steps.py`): start `./bin/geofence-processor` with `PORT`, `FIRESTORE_EMULATOR_HOST`, and `PROJECT_ID` from the Gherkin `Background` table; poll `GET /health` until HTTP 200 (within 10s); seed `geofences` in Firestore; post base64-encoded Pub/Sub push envelopes to `/telemetry-push`; poll Firestore `alerts` collection directly as the independent verification channel.
   - MI3 (`image_steps.py`): build Docker image `equiguard/geofence-processor:test`, run container with env vars from Gherkin table, verify `GET /health`, port listening, valid/malformed push events, HTTP 400 status, and empty `alerts` collection.
   - MI4 (`cloud_steps.py`): read `cloud_run_url` and `topic_path` from `terraform output -json` (without running `terraform apply` inside a Given step!), authenticate health checks with `gcloud auth print-identity-token`, publish to real Pub/Sub, and reuse the Firestore assertion steps against real Firestore.
2. **Dumb Steps (Zero Business Logic):**
   - Never compute point-in-polygon in Python, never hardcode coordinates or ports, and never inject hidden business fields.
3. **Test Isolation (`bdd/environment.py`):**
   - Stop any started process or Docker container and clear the `alerts` and `geofences` collections in Firestore after every scenario.
4. Run `make test-mi1` and confirm that the suite executes and fails **cleanly RED** because the service executables in `./bin/` do not exist yet.
```
