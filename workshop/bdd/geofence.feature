@library @geofence @mi1
Feature: Geofence Library Validation
  As a core component of the EquiGuard system
  The geofence library must accurately determine if a given coordinate lies within a predefined polygon
  To ensure reliable alerting for leaving the pasture

  Background:
    # Definition of the pasture boundary (master data) directly from geofence.kml
    Given the geofence "HomePasture" is defined by the following polygon:
      | longitude  | latitude   |
      | 9.6096319  | 53.2278606 |
      | 9.6147013  | 53.2273050 |
      | 9.6147281  | 53.2282170 |
      | 9.6120513  | 53.2285285 |
      | 9.6096319  | 53.2278606 |

  Scenario Outline: Validate if a telemetry point is inside or outside the geofence
    # Stateless library call: Both the point and the polygon definition are passed as inputs
    When I run the geofence library test "is-point-inside" with:
      | parameter | value                                    |
      | point     | {"lon": <longitude>, "lat": <latitude>} |
      | polygon   | HomePasture                              |
    Then the library result should be "<is_inside>"

    # The test cases (transactional data) directly from the CSV
    Examples:
      | point_id         | longitude | latitude   | is_inside |
      | telemetry_out_01 | 9.6116704 | 53.2275266 | false     |
      | telemetry_in_01  | 9.6113700 | 53.2280821 | true      |
      | telemetry_in_02  | 9.6130383 | 53.2279794 | true      |
      | telemetry_in_03  | 9.6099377 | 53.2278959 | true      |
      | telemetry_out_02 | 9.6105653 | 53.2282106 | false     |
      | telemetry_out_03 | 9.6142453 | 53.2283615 | false     |
