# **Workshop: EquiGuard – AI-Driven Geofencing & Event-Driven Architecture**

## **About the Project**

This project serves as a practical demonstration for the presentation **"Burn Your Code: Feature Files as the Ultimate AI Agent Prompt"**. We implement a high-precision, event-driven architecture on Google Cloud, where the entire business logic and infrastructure configuration are defined exclusively through **Gherkin Feature Files**.

### **The Case: "EquiGuard Dreilingen"**

We monitor the pasture areas in Dreilingen (Heidewiese). Using GPS telemetry, the system determines in real-time whether horses (e.g., Lilly or Honey) have left the predefined geofence.

## **The Architecture**

The system is designed according to the **Ports & Adapters (Hexagonal)** principle and utilizes Google Cloud Native services for decoupling.

1. **Service A (Telemetry Ingress):** A Cloud Run service that receives GPS data via webhook (curl) and publishes it as an event to Pub/Sub.  
2. **Messaging:** Google Cloud Pub/Sub acts as an asynchronous buffer and decoupling layer.  
3. **Service B (Geofence Processor):** A Cloud Run service that reacts to events, performs geofence validation against the KML data, and persists alerts in **Firestore**.

## **Single Source of Truth: The Feature File**

In accordance with **BDD Guideline v1.2.0**, we do not use hardcoded coordinates in the program code. The polygon vertices are taken directly from the geofence.kml and are stored in the Feature File.

### **Example Specification (bdd/geofence.feature)**

Feature: Precise Geofence Monitoring

  Scenario: Alert when a horse leaves the KML-defined pasture  
    Given the geofence "HomePasture" is defined by the following polygon:  
      | longitude  | latitude   |  
      | 9.6096319  | 53.2278606 |  
      | 9.6147013  | 53.2273050 |  
      | 9.6147281  | 53.2282170 |  
      | 9.6120513  | 53.2285285 |  
      | 9.6096319  | 53.2278606 |

    When a telemetry update is received for "Lilly":  
      """  
      {  
        "lon": 9.6050000,  
        "lat": 53.2300000,  
        "timestamp": "2026-02-25T14:00:00Z"  
      }  
      """

    Then the Firestore collection "alerts" should eventually contain a record:  
      | field    | value              |  
      | device   | Lilly              |  
      | type     | GEOFENCE\_VIOLATION |  
      | zone     | HomePasture        |

## **Workshop Flow (Red/Green)**

1. **Definition:** The Human Architect writes the Feature File using the real KML coordinates.  
2. **Execution (Red):** The test run fails because neither the Ingress service nor the Processor exists yet.  
3. **AI Synthesis:** An AI agent generates the following based on the Feature File and the guidelines:  
   * Go/Python code for both Cloud Run services.  
   * Dockerfile and Cloud Build configuration.  
   * Firestore data modeling.  
4. **Validation (Green):** A curl request simulates the horse being outside the pasture; the test automatically verifies the entry in Firestore.

## **Execution & Trigger**

To manually simulate a geofence violation after deployment, use the following command:

curl \-X POST \[https://ingress-service-xyz.a.run.app/telemetry\](https://ingress-service-xyz.a.run.app/telemetry) \\  
     \-H "Content-Type: application/json" \\  
     \-d '{  
       "horse\_id": "Lilly",  
       "location": {"lat": 53.2300, "lon": 9.6050},  
       "timestamp": "2026-02-25T14:10:00Z"  
     }'

## **Guardrails Against Hallucination**

* **Technical Isolation:** Tests run in an isolated .venv.  
* **Eventual Consistency:** We use polling with a timeout (Guideline 6.4) to wait for the asynchronous Firestore entry.  
* **No Magic Values:** All validation parameters must be visible in the Gherkin text.

*Created for the presentation: Burn Your Code – Feature Files as the Ultimate Prompt.*