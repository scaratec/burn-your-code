@processor @infrastructure @mi2
Feature: Geofence Processor Service (Service B)
  As the core alerting component of the EquiGuard system
  The processor service must react to incoming telemetry events via Pub/Sub push
  And persist an alert in Firestore if a horse leaves its assigned pasture

  Background:
    # Explicit configuration of the service (Guideline 2.1)
    Given the geofence-processor is configured with:
      | key                       | value                     |
      | port                      | 8081                      |
      | firestore-emulator-host   | localhost:8082            |
      | pubsub-emulator-host      | localhost:8085            |
      | firestore-project-id      | equiguard-test            |

    # Separation of master data (Guideline 2.3) written directly to the mocked DB
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

  Scenario: Alert when a horse leaves the pasture (Eventual Consistency)
    # The transactional data payload received via Pub/Sub (Guideline 3.1)
    When the service receives a Pub/Sub push event on "/telemetry-push" for "Lilly":
      """
      {
        "device": "Lilly",
        "lon": 9.6116704,
        "lat": 53.2275266,
        "timestamp": "2026-02-25T14:00:00Z",
        "zone": "HomePasture"
      }
      """
    
    # Resilient testing with polling/timeout (Guideline 6.4)
    Then the Firestore collection "alerts" should eventually contain a record for "Lilly" within 10 seconds:
      | field | value              |
      | type  | GEOFENCE_VIOLATION |
      | zone  | HomePasture        |

  Scenario: No alert when a horse remains inside the pasture
    When the service receives a Pub/Sub push event on "/telemetry-push" for "Honey":
      """
      {
        "device": "Honey",
        "lon": 9.6113700,
        "lat": 53.2280821,
        "timestamp": "2026-02-25T14:05:00Z",
        "zone": "HomePasture"
      }
      """
    
    # Ensuring no false positives are generated
    Then the Firestore collection "alerts" should not contain a record for "Honey" within 2 seconds
