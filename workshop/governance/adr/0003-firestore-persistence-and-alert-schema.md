# ADR 0003: Firestore persistence and alert schema

- **Status:** Accepted
- **Date:** 2026-11-10
- **Deciders:** EquiGuard Architecture Team

## Context

`geofence-processor` needs a cloud-native store to read pasture boundary definitions (`geofences`) and persist violation alerts (`alerts`). Furthermore, our BDD Guidelines (§4.3, §13.2) require an **independent verification channel**: the test suite must verify state changes by reading the backing store directly rather than trusting the HTTP response of `POST /telemetry-push`.

## Decision

We use **Google Cloud Firestore (Native Mode)** in the `(default)` database with two collections:

1. **Master Data Collection `geofences`:**
   - Document ID: `<zone>` (e.g., `"HomePasture"`).
   - Document Schema:
     ```json
     {
       "polygon": [
         {"lon": 9.6096319, "lat": 53.2278606},
         {"lon": 9.6147013, "lat": 53.2273050},
         {"lon": 9.6147281, "lat": 53.2282170},
         {"lon": 9.6120513, "lat": 53.2285285},
         {"lon": 9.6096319, "lat": 53.2278606}
       ]
     }
     ```
2. **Transactional Output Collection `alerts`:**
   - When a valid telemetry ping for `device` in `zone` evaluates to **outside** (`is_inside == false`) per [ADR-0001](0001-point-in-polygon-ray-casting.md), the service writes a new document to `alerts` containing at minimum:
     ```json
     {
       "device": "<device_id>",
       "type": "GEOFENCE_VIOLATION",
       "zone": "<zone>",
       "lon": 9.6116704,
       "lat": 53.2275266,
       "timestamp": "2026-02-25T14:00:00Z"
     }
     ```
   - When a valid telemetry ping evaluates to **inside** (`is_inside == true`), the service writes **nothing** to `alerts`.

## Consequences

### Positive

- Serverless, zero-maintenance operational store on GCP with an official local emulator (`firebase-tools` Firestore emulator on `localhost:8082`) that behaves identically to production.
- Provides a clean independent channel for BDD `Given` setup (seeding `geofences`) and `Then` assertions (polling `alerts` by `device`).

### Negative

- Firestore queries in `Then` steps must account for eventual consistency across Pub/Sub and Cloud Run using bounded polling (`within 10 seconds` locally, `within 30 seconds` on GCP).

### Neutral

- Test isolation is guaranteed by wiping `alerts` and `geofences` between scenarios in [`bdd/environment.py`](../../bdd/environment.py).

## Security Implications

In GCP (`@mi4`), Firestore access is governed by IAM using Application Default Credentials / Cloud Run service account identity (`roles/datastore.user`); no static API keys or credentials are stored in the repository.

## Alternatives Considered

- **Cloud SQL (PostgreSQL).** Rejected because relational schema migrations and always-on instance costs are disproportionate for a two-collection document store in a serverless workshop.
- **In-memory pasture config (KML baked into the container image).** Rejected because BDD Guideline §2.3 requires strict separation of master data (`Given` in Firestore) from application code, and operators must be able to update pasture boundaries without rebuilding the container.

## References

- Enforced by: [`bdd/mi2_geofence_processor.feature`](../../bdd/mi2_geofence_processor.feature), [`bdd/mi3_geofence_processor_image.feature`](../../bdd/mi3_geofence_processor_image.feature), [`bdd/mi4_cloud_run.feature`](../../bdd/mi4_cloud_run.feature)
- Bounded by: [LIM-0001](../limitations/0001-single-static-polygon-per-pasture.md), [LIM-0002](../limitations/0002-stateless-per-ping-evaluation-without-deduplication.md)
