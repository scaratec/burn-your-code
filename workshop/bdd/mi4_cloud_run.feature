@cloud @live @mi4
Feature: Geofence Processor on Cloud Run (Live GCP)
  As the EquiGuard system in production
  The geofence-processor service must operate identically on Cloud Run
  as it does locally — using real Firestore, real Pub/Sub, and a real
  Artifact Registry

  # ============================================================
  # WARNING: THIS MILESTONE USES REAL GCP RESOURCES.
  #
  # PARTICIPANT SETUP — one edit required:
  #   Change project_id in the Background table below to your
  #   GCP project ID. That value is the single source of truth:
  #   the Makefile reads it from here and passes it to Terraform
  #   and Docker automatically. No other file needs to be changed.
  #
  # Prerequisites:
  #   - GCP project with billing enabled
  #   - gcloud CLI authenticated: gcloud auth application-default login
  #   - Docker authenticated: make auth-registry PROJECT=<project_id>
  #   - Terraform installed: >= 1.7
  #
  # Before running:
  #   make tf-apply   # provision all GCP resources via Terraform
  #
  # After the workshop:
  #   make teardown-mi4   # destroy all GCP resources (stops billing)
  # ============================================================

  Background:
    # project_id is the single source of truth for the GCP project.
    # The Makefile reads this value via awk and derives the Artifact
    # Registry image URL and all Terraform -var flags from it — no
    # other file needs to be edited. All values explicit (Guideline 2.1).
    Given the Cloud Run deployment is configured with:
      | key                 | value                        |
      | project_id          | randy-gupta-poc              |
      | region              | europe-west3                 |
      | service_name        | geofence-processor           |
      | pubsub_topic        | equiguard-telemetry          |
      | pubsub_subscription | equiguard-telemetry-push-sub |

    # Terraform provisions Artifact Registry, Cloud Run, Pub/Sub topic
    # and push subscription in one idempotent apply
    And the infrastructure is provisioned with Terraform

    # Master data: geofence polygon from KML, written to real Firestore
    # before each scenario (Guideline 2.3)
    And the Firestore collection "geofences" contains the document "HomePasture":
      """
      {
        "polygon": [
          {"lon": 9.6096319, "lat": 53.2278606},
          {"lon": 9.6147013, "lat": 53.2273050},
          {"lon": 9.6147281, "lat": 53.2282170},
          {"lon": 9.6120513, "lat": 53.2285285},
          {"lon": 9.6096319, "lat": 53.2278606}
        ]
      }
      """

  Scenario: Service is reachable and healthy on Cloud Run
    # Cloud Run may have a cold start — allow up to 30 seconds (Guideline 6.4)
    Then the Cloud Run service health endpoint "GET /health" should respond with status 200 within 30 seconds

  Scenario: Alert when a horse leaves the pasture via real Pub/Sub
    # Identical payload to MI2/MI3 — the spec does not change with the
    # execution environment (Guideline 1.2)
    When a Pub/Sub message is published to topic "equiguard-telemetry" for "Lilly":
      """
      {
        "device": "Lilly",
        "lon": 9.6116704,
        "lat": 53.2275266,
        "timestamp": "2026-02-25T14:00:00Z",
        "zone": "HomePasture"
      }
      """
    Then the Firestore collection "alerts" should eventually contain a record for "Lilly" within 30 seconds:
      | field | value              |
      | type  | GEOFENCE_VIOLATION |
      | zone  | HomePasture        |

  Scenario: No alert when a horse remains inside the pasture
    When a Pub/Sub message is published to topic "equiguard-telemetry" for "Honey":
      """
      {
        "device": "Honey",
        "lon": 9.6113700,
        "lat": 53.2280821,
        "timestamp": "2026-02-25T14:05:00Z",
        "zone": "HomePasture"
      }
      """
    # Longer wait than MI3 — real Pub/Sub latency is higher than local
    Then the Firestore collection "alerts" should not contain a record for "Honey" within 10 seconds
