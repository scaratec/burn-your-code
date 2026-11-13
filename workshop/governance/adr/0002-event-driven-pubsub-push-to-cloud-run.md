# ADR 0002: Event-driven telemetry ingestion via Pub/Sub push to Cloud Run

- **Status:** Accepted
- **Date:** 2026-11-10
- **Deciders:** EquiGuard Architecture Team

## Context

GPS collars emit telemetry events asynchronously. EquiGuard needs an ingestion and processing architecture that scales to zero when no pings arrive, runs identically in local container tests and on Google Cloud, and decouples telemetry producers from geofence evaluation.

## Decision

We implement `geofence-processor` as a stateless HTTP service deployed on **Google Cloud Run**, triggered via a **Google Cloud Pub/Sub push subscription**:

1. **Runtime Configuration (Environment Variables):**
   - `PORT`: HTTP listening port (default `8081` in local/container runs).
   - `PROJECT_ID`: Google Cloud / Firestore project ID (e.g., `equiguard-test` locally, `randy-gupta-poc` in GCP).
   - `FIRESTORE_EMULATOR_HOST`: Optional host:port (`localhost:8082`) for local emulator runs; unset in live Cloud Run.
2. **Endpoints:**
   - `GET /health`: Returns HTTP `200 OK` as soon as the HTTP server is ready to accept requests.
   - `POST /telemetry-push`: Accepts a standard Google Cloud Pub/Sub push envelope:
     ```json
     {
       "message": {
         "data": "<base64-encoded JSON telemetry payload>",
         "messageId": "<string>"
       }
     }
     ```
3. **Telemetry Payload Contract & Input Validation:**
   - Decoded `message.data` JSON must contain mandatory fields: non-empty `zone` (string) and numeric `lon` and `lat` coordinates, plus `device` (string) and `timestamp` (RFC3339 string).
   - If the request body is invalid JSON, `message.data` is missing/invalid base64, or mandatory fields (`lon`, `lat`, `zone`) are missing, `POST /telemetry-push` **must reject the request with HTTP `400 Bad Request`** and must not write any document to Firestore.
   - Valid events are evaluated against the polygon stored in Firestore (`geofences/<zone>`). If the point is outside the polygon, an alert is persisted ([ADR-0003](0003-firestore-persistence-and-alert-schema.md)) and the endpoint returns HTTP `200` (or `204`).

## Consequences

### Positive

- Identical HTTP push interface across local process runs (`@mi2`), local Docker container runs (`@mi3`), and live Cloud Run (`@mi4`).
- Scales to zero on Cloud Run; Terraform provisions the topic (`equiguard-telemetry`), Cloud Run service (`geofence-processor`), and push subscription (`equiguard-telemetry-push-sub`).

### Negative

- Pub/Sub push uses at-least-once delivery; combined with stateless per-ping evaluation ([LIM-0002](../limitations/0002-stateless-per-ping-evaluation-without-deduplication.md)), duplicate or consecutive outside pings produce multiple alert documents.

### Neutral

- Returning HTTP `400` on malformed payloads is observable in direct HTTP tests (`@mi3`).

## Security Implications

- **Authentication on Cloud Run (`@mi4`):** The Cloud Run service requires authenticated OIDC invocation (`roles/run.invoker`). The Pub/Sub push subscription authenticates using a dedicated service account, and the BDD test harness authenticates `GET /health` using `gcloud auth print-identity-token`.
- **Boundary validation:** Every incoming push request is strictly validated before Firestore is queried or written. Malformed payloads fail closed with HTTP `400` and leave the `alerts` collection untouched.

## Alternatives Considered

- **Pub/Sub pull worker.** Rejected because a continuous pull loop prevents Cloud Run from scaling to zero when idle and complicates local HTTP black-box testing.
- **Direct HTTP ingestion from collars without Pub/Sub.** Rejected because buffering and retry semantics belong in a managed message broker rather than on low-power IoT devices.

## References

- Enforced by: [`bdd/mi2_geofence_processor.feature`](../../bdd/mi2_geofence_processor.feature), [`bdd/mi3_geofence_processor_image.feature`](../../bdd/mi3_geofence_processor_image.feature), [`bdd/mi4_cloud_run.feature`](../../bdd/mi4_cloud_run.feature)
- Error paths: [`bdd/00_error_path_enumeration.md`](../../bdd/00_error_path_enumeration.md)
