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

  @mi1 @complex
  Scenario Outline: Validate complex concave geofence with interior exclusions
    Given the geofence "ComplexPasture" is defined by the following polygon:
      | longitude | latitude   |
      | 9.6014131 | 53.2288678 |
      | 9.5975078 | 53.2283026 |
      | 9.5933879 | 53.2265043 |
      | 9.5929588 | 53.2239351 |
      | 9.5960058 | 53.2209803 |
      | 9.6009410 | 53.2190531 |
      | 9.6083225 | 53.2191559 |
      | 9.6116269 | 53.2219566 |
      | 9.6120132 | 53.2246288 |
      | 9.6111978 | 53.2267098 |
      | 9.6077216 | 53.2279943 |
      | 9.6035589 | 53.2286880 |
      | 9.6034301 | 53.2262217 |
      | 9.6051467 | 53.2260161 |
      | 9.6089233 | 53.2249371 |
      | 9.6091378 | 53.2230101 |
      | 9.6080650 | 53.2213914 |
      | 9.6026576 | 53.2208775 |
      | 9.5976795 | 53.2225476 |
      | 9.5960058 | 53.2245774 |
      | 9.5976795 | 53.2263501 |
      | 9.6016277 | 53.2261960 |
      | 9.6014131 | 53.2288678 |

    When I run the geofence library test "is-point-inside" with:
      | parameter | value                                    |
      | point     | {"lon": <longitude>, "lat": <latitude>} |
      | polygon   | ComplexPasture                           |
    Then the library result should be "<is_inside>"

    # Data points from alt_scenario.csv
    Examples:
      | point_id         | longitude | latitude   | is_inside |
      | telemetry_in_01  | 9.5981086 | 53.2280457 | true      |
      | telemetry_in_02  | 9.5996106 | 53.2267098 | true      |
      | telemetry_in_03  | 9.6105970 | 53.2233698 | true      |
      | telemetry_in_04  | 9.6066058 | 53.2274035 | true      |
      | telemetry_in_05  | 9.6000398 | 53.2209803 | true      |
      | telemetry_in_06  | 9.6055759 | 53.2205948 | true      |
      | telemetry_out_01 | 9.6005119 | 53.2248600 | false     |
      | telemetry_out_02 | 9.6042026 | 53.2238580 | false     |
      | telemetry_out_03 | 9.6131719 | 53.2205948 | false     |
      | telemetry_out_04 | 9.5945037 | 53.2280457 | false     |
