# Phase 2 Prompt — Error Path Enumeration & Gherkin Feature Files

Run this prompt in **Antigravity CLI (`agy`)** with Gemini after completing Phase 1 (or after `make checkpoint-adrs`):

```text
Read AGENTS.md, ../BDD_GUIDELINES_v1.9.0_EN.md (especially §2, §3, §4, and §4.5), and all records in governance/adr/ and governance/limitations/.

Follow Stage 3 of AGENTS.md strictly:
1. First, create `bdd/00_error_path_enumeration.md` following BDD Guidelines §4.5: enumerate the failure and boundary space layer by layer (Geometry & Boundary Evaluation, Payload & Input Validation, State & Persistence Behavior, Container & Cloud Runtime) and summarize the counts in a table.
2. Propose the first feature file `bdd/mi1_geofence_library.feature` (`@library @geofence @mi1`) using the polygon coordinates from `geofence.kml` (`HomePasture` convex polygon and `ComplexPasture` concave polygon) with `Scenario Outline` and `Examples` tables for inside and outside points. Include a `# Source:` header citing the governing ADRs/LIMs and the independent verification channel.
3. Pause so I can review and approve the shape of `mi1_geofence_library.feature`.
4. Once approved, write:
   - `bdd/mi2_geofence_processor.feature` (`@processor @infrastructure @mi2`): local service with explicit `Background` config table (port 8081, firestore-emulator-host localhost:8082, pubsub-emulator-host localhost:8085, firestore-project-id equiguard-test), `HomePasture` seeded in Firestore `geofences`, positive outside-ping scenario for "Lilly" (`GEOFENCE_VIOLATION` within 10s), and negative control inside-ping scenario for "Honey" (no alert within 2s).
   - `bdd/mi3_geofence_processor_image.feature` (`@image @infrastructure @mi3`): OCI container image `equiguard/geofence-processor:test`, `GET /health` within 10s, port 8081 check, behavioral equivalence with MI2 ("Lilly" and "Honey"), plus a `Scenario Outline` rejecting malformed payloads (missing lon/lat, missing zone, empty body) with HTTP 400 and an empty `alerts` collection.
   - `bdd/mi4_cloud_run.feature` (`@cloud @live @mi4`): live GCP Cloud Run deployment provisioned with Terraform (`project_id` in Background table as single source of truth), `GET /health` within 30s, and real Pub/Sub topic `equiguard-telemetry` scenarios for "Lilly" and "Honey".

Do NOT write any Python step files or application code yet.
```
