@image @infrastructure @mi3
Feature: Geofence Processor OCI Image
  As a production deployment of the EquiGuard system
  The geofence-processor container image must be buildable,
  start correctly with explicit configuration, and handle
  telemetry events identically to the uncontainerized service

  Background:
    # Explicit image and runtime configuration (Guideline 2.1)
    # No magic values: all ports, tags and env vars are visible here
    Given the geofence-processor image is built from "." with tag "equiguard/geofence-processor:test"
    And the container is started with the following configuration:
      | key                     | value          |
      | host_port               | 9081           |
      | container_port          | 8081           |
      | FIRESTORE_EMULATOR_HOST | localhost:8082 |
      | PUBSUB_EMULATOR_HOST    | localhost:8085 |
      | PROJECT_ID              | equiguard-test |
      | network                 | host           |

    # Master data written to the emulator before each scenario (Guideline 2.3)
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

  Scenario: Container starts and becomes healthy
    # Observable behaviour: the health endpoint must respond
    # within a defined timeout — not just "eventually" (Guideline 6.4)
    Then the container health endpoint "GET /health" should respond with status 200 within 10 seconds

  Scenario: Container image exposes the correct port
    # The image must not silently bind to a different port
    Then the container should listen on port 8081

  Scenario: Alert when a horse leaves the pasture
    # Identical payload to MI2 — behaviour must be equivalent
    # regardless of the execution environment (Guideline 1.2)
    When the containerized service receives a Pub/Sub push event on "/telemetry-push" for "Lilly":
      """
      {
        "lon": 9.6116704,
        "lat": 53.2275266,
        "timestamp": "2026-02-25T14:00:00Z",
        "zone": "HomePasture"
      }
      """
    Then the Firestore collection "alerts" should eventually contain a record for "Lilly":
      | field | value              |
      | type  | GEOFENCE_VIOLATION |
      | zone  | HomePasture        |

  Scenario: No alert when a horse remains inside the pasture
    When the containerized service receives a Pub/Sub push event on "/telemetry-push" for "Honey":
      """
      {
        "lon": 9.6113700,
        "lat": 53.2280821,
        "timestamp": "2026-02-25T14:05:00Z",
        "zone": "HomePasture"
      }
      """
    Then the Firestore collection "alerts" should not contain a record for "Honey" within 2 seconds

  Scenario Outline: Container rejects requests with missing mandatory fields
    # Validate that the image enforces the input contract (Guideline 1.1)
    When the containerized service receives a malformed push event on "/telemetry-push":
      """
      <payload>
      """
    Then the response status should be <status>
    And the Firestore collection "alerts" should remain empty

    Examples:
      | description     | payload                                   | status |
      | missing lon/lat | {"zone": "HomePasture"}                   | 400    |
      | missing zone    | {"lon": 9.6116704, "lat": 53.2275266}     | 400    |
      | empty body      | {}                                        | 400    |
