@cloud @live @mi4
Feature: Geofence Processor on Cloud Run (Live GCP)
  As the EquiGuard system in production
  The geofence-processor service must operate identically on Cloud Run
  as it does locally — using real Firestore, real Pub/Sub, and a real
  Artifact Registry

  # ============================================================
  # WARNING: THIS MILESTONE USES REAL GCP RESOURCES.
  #
  # Prerequisites:
  #   - GCP project: randy-gupta-poc (billing enabled)
  #   - gcloud CLI authenticated: gcloud auth application-default login
  #   - Docker authenticated: make auth-registry
  #   - Terraform installed: >= 1.7
  #
  # Before running:
  #   make push-image     # tag and push the container image
  #   make tf-apply       # provision all GCP resources via Terraform
  #
  # After the workshop:
  #   make teardown-mi4   # destroy all GCP resources (stops billing)
  # ============================================================

  Background:
    # All values explicit — no magic defaults (Guideline 2.1).
    # These must match terraform/terraform.tfvars.
    Given the Cloud Run deployment is configured with:
      | key                 | value                                                                        |
      | project_id          | randy-gupta-poc                                                              |
      | region              | europe-west3                                                                 |
      | service_name        | geofence-processor                                                           |
      | registry_image      | europe-west3-docker.pkg.dev/randy-gupta-poc/equiguard/geofence-processor:v1 |
      | local_image         | equiguard/geofence-processor:test                                            |
      | pubsub_topic        | equiguard-telemetry                                                          |
      | pubsub_subscription | equiguard-telemetry-push-sub                                                 |

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
    # Pub/Sub → Cloud Run → Firestore is fully async — allow 30 seconds
    Then the Firestore collection "alerts" should eventually contain a record for "Lilly":
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
