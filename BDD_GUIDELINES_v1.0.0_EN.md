# AI-Driven Behavior Driven Development: A Technical Guide for Software Development

**Version: 1.0.0**

## Preamble

These guidelines define the standardized process for software development. They mark a paradigm shift from classical programming to specification-driven development, where Artificial Intelligence acts as the executive tool. In this model, the Feature File, formulated in Gherkin syntax, is the sole source of truth ("Single Source of Truth").

## 1. The Nature of the Executable Contract

The fundamental premise of our approach is that a software solution is fully defined by its externally observable behavior. The Feature File serves as a binding contract between the business requirement and the technical implementation. We enforce a strict synchronization: The Feature File is the deterministic prompt for the AI agent.

## 2. Explicitness and Data Transparency (Single Source of Truth)

A critical quality characteristic of this process is the complete transparency of data and configurations. A common anti-pattern in traditional BDD practice is hiding parameters within step implementations ("Glue Code"). This leads to "magic values" that are invisible in the Gherkin text and undermines the value of the specification.

### 2.1 Case Study: Avoiding Implicit Configuration (Reference: DDNS Service)

Let's consider a **Dynamic DNS Service** that needs to listen on a specific network port and communicate with an external API. In a robust architecture, these parameters must not be hardcoded in the program code. They must be explicitly stated in the scenario so that the behavior is understandable even without looking into the code.

**Positive Example (Explicit Configuration):**
Here, the Feature File serves as the sole configuration source. The code becomes a generic layer that merely applies data from the table.

*Feature File:*
```gherkin
Given the ddns-service is configured with:
  | key                  | value                 |
  | listen-port          | 8080                  |
  | autodns-api-base-url | http://localhost:8081 |
```

**Technical Implementation (From Gherkin to CLI Call):**
The Python step reads this table and dynamically constructs the arguments for starting the service. There is no "hidden truth" in the Python code; all runtime parameters come directly from the Feature File.

```python
@given("the ddns-service is configured with")
def step_impl(context):
    if not hasattr(context, 'ddns_config'):
        context.ddns_config = {}

    for row in context.table:
        context.ddns_config[row['key']] = row['value']

@given("the ddns-service is listening")
def start_service(context):
    cmd = ["./bin/ddns-service"]
    # Generate CLI flags dynamically: 
    # From {'listen-port': '8080'} becomes ["--listen-port=8080"]
    for key, value in context.ddns_config.items():
        cmd.append(f"--{key}={value}")
    
    # Resulting command:
    # ./bin/ddns-service --listen-port=8080 --autodns-api-base-url=http://localhost:8081
    context.process = subprocess.Popen(cmd)
```

**Consequence & Conclusion:**
The tests enforce that the application is fully configurable via the command line. There are no hardcoded constants for ports or URLs in the code, otherwise the test would not work. The **CLI interface is defined by the test**.

### 2.2 The Danger of Data Gaps (Requirement Gaps)

A critical failure in test design occurs when data is required in the expected outcome (`Then`) that is not included in the data basis (`Given`). This creates a logical gap that corrupts the technical implementation: The developer (or the AI agent) is forced to hardcode "magic values" to pass the test. 

A valid BDD test must represent a **pure transformation** (Pure Function). Every value validated in the `Then` step must either:
1.  Come directly from the `Given` step.
2.  Be derived from input data through a business rule explicitly described in the Feature File.

**Anti-Pattern (Data Gap):**
The scenario expects a specific IBAN and tax codes in the result but does not provide them in the input.

*Bad Feature File:*
```gherkin
Scenario: Map Order to Marketplace
    Given an order for item "X"
    When the mapping logic is applied
    Then the output must contain:
      | field | value       |
      | iban  | DE123456789 |  <-- Where does this value come from?
      | tax   | VAT_DE      |  <-- "Magic" knowledge
```

**Consequence:**
The resulting code will hardwire this value (`const IBAN = "DE123456789"`). The test is thus worthless as it checks no general logic, only the match of two static texts.

**Best Practice (Anti-Hardcoding Strategy):**
1.  **Completeness:** Supplement the `Given` block with all necessary source data.
2.  **Variance (The "Bob Test"):** Always create at least two scenarios (e.g., using `Scenario Outline`) with different values for the same fields. If the implementation has hardcoded a value, the second scenario will inevitably fail. Only this proves that the logic actually works **generically**.

## 3. Complex Data Structures and Payloads

For enterprise applications, passing simple key-value pairs is often insufficient. Complex business objects, JSON payloads, or database schemas must be mapped directly in the scenario using **DocStrings** (Triple-Quotes). This ensures that even complex validation logic remains readable for domain experts.

### 3.1 Case Study: Business Objects (Reference: PaperSink DMS)

Instead of burying validation logic for mandatory fields like `net_amount` or `currency` in the code, the expected data object is defined as JSON in Gherkin.

*Feature File:*
```gherkin
Scenario: Upload a valid Invoice document
    And the client provides business metadata:
      """
      {
        "invoice_number": "INV-2025-001",
        "net_amount": 10050,
        "currency": "EUR"
      }
      """
```

**Technical Implementation (DocString Parsing):**
The step code parses the DocString and uses it directly for the API request.

```python
@given("the client provides business metadata")
def step_impl(context):
    try:
        # Validation that the DocString is valid JSON
        metadata = json.loads(context.text)
        context.request_payload = metadata
    except json.JSONDecodeError as e:
        raise AssertionError(f"Invalid JSON in Feature File: {e}")

@when("the client sends the document")
def send_document(context):
    # The JSON from the Feature File is sent 1:1 to the API
    requests.post(url, json=context.request_payload)
```

**Consequence & Conclusion:**
The Feature File becomes a **schema reference**. There are no implicit default values in the test code. This forces the API to correctly handle missing mandatory fields (e.g., if `currency` is omitted in Gherkin) (e.g., 400 Bad Request), instead of the test code secretly filling them in.

### 3.2 Case Study: Transformation Logic (Reference: Enterprise Integration)

In complex integration scenarios, the core task is often to map data from a source system (e.g., Shop API) to a target system (e.g., ERP). These mappings are pure business logic and must not be hidden deep in Java or Go code.

*Feature File:*
```gherkin
Scenario: Mapping of custom fields from Source System to Target System
  # Definition of input data (Source System)
  Given a source order with custom fields:
    | source_code | value      |
    | color-01    | blue       |
    | size-x      | 42         |
  
  When the order mapping logic is applied
  
  # Definition of expected output data (Target System)
  Then the target system structure should contain:
    | target_field   | value |
    | attributes.col | blue  |
    | attributes.sz  | 42    |
```

**Technical Implementation (Unit-Level BDD):**
Here, no HTTP request is sent; instead, the application's mapping function is called directly.

```python
@when("the order mapping logic is applied")
def step_impl(context):
    from src.logic import mapper
    context.target_order = mapper.transform(context.source_order)

@then("the target system structure should contain")
def step_impl(context):
    for row in context.table:
        actual = get_value(context.target_order, row['target_field'])
        assert actual == row['value']
```

**Consequence & Conclusion:**
Business logic becomes **readable and validatable** for domain experts. Complex mappings are no longer hidden in Java Streams or Go loops but stand explicitly as examples in Gherkin. This prevents "Lost in Translation" errors between Business and IT.

### 3.3 Case Study: Observability & Logging (Reference: DDNS Service)

Often, the internal state of a system is difficult to view from the outside.

*Feature File:*
```gherkin
Scenario: Successful update produces a structured JSON log
    And the service should log the following structured JSON message:
      """
      {
        "level": "info",
        "message": "Successfully updated DNS record",
        "service": "ddns-service",
        "context": {
          "dns_name": "gupta.ddns.scaratec.com",
          "update_ip": "127.0.0.1"
        }
      }
      """
```

**Technical Implementation (Log Capture):**
The step code reads the `stdout` of the subprocess and parses each line as JSON.

```python
@then("the service should log the following structured JSON message")
def step_impl(context):
    expected_log = json.loads(context.text)
    logs = get_captured_logs(context)
    assert any(is_subset(expected_log, log) for log in logs)
```

**Consequence & Conclusion:**
Logging becomes a **First-Class Feature**. The test enforces that the application writes structured, machine-readable logs (JSON) instead of unstructured text deserts. This guarantees integrability into monitoring systems (ELK, Splunk) from day 1.

## 4. Technical Isolation and Architecture

To ensure the integrity of the validation, strict separation between the test infrastructure and the production system is required.

### 4.1 Isolated Runtime Environment

The BDD framework operates in a completely isolated environment (`.venv`) that shares no dependencies with the production code. **This strict separation applies mandatorily even if both the application and the test suite are implemented in Python.**

### 4.2 Modularization of Steps (Reference: MOIS2)

With increasing system complexity, the structure of validation must also scale. Monolithic step files are to be avoided.

*Recommended Structure:*
```text
bdd/steps/
├── ingress_steps.py    # Handles HTTP inputs and API calls
├── logic_steps.py      # Validates internal business rules and transformations
└── cloud_steps.py      # Simulates infrastructure events (e.g., PubSub messages)
```

### 4.3 UI & End-to-End Testing (Reference: Osthues Insight Engine)

BDD is not limited to backend logic. For applications with graphical user interfaces, we specify user interactions as behavior.

*Feature File:*
```gherkin
Scenario: Candidate Selection in Data Grid
    When the user selects the candidate "Max Mustermann" in the data grid
```

**Technical Implementation (Selenium Abstraction):**
The step code encapsulates the complexity of browser automation.

```python
@when('the user selects the candidate "{name}" in the data grid')
def step_impl(context, name):
    xpath = f"//div[@role='row' and contains(., '{name}')]"
    row = context.driver.find_element(By.XPATH, xpath)
    row.click()
```

**Consequence & Conclusion:**
Tests become **resilient to layout changes**. Since Gherkin only describes the intention ("Select candidate"), only the one Python step needs to be adapted if the HTML skeleton changes (e.g., new CSS class), not hundreds of test scenarios.

## 5. Architecture by Design: Ports & Adapters

Feature Files can be used to enforce architectural encapsulation.

### 5.1 Case Study: Encapsulation of API Clients (Reference: AutoDNS Library)

By writing a Feature File that tests *only* a library (and not the entire service), we force the developer to cleanly separate this code from the rest of the application.

*Feature File (Library Test):*
```gherkin
@library @autodns
Feature: AutoDNS Library Integration
  Scenario: Library successfully authenticates
    When I run the AutoDNS library test "login" command with:
      | arg       | value |
      | user      | user  |
```

**Technical Implementation (Library Test Wrapper):**
A CLI wrapper (`main.go`) directly calls the library functions.

```go
// cmd/autodns-lib-test/main.go
func main() {
    // Calls the library directly, without HTTP Server
    client := autodns.NewClient(...)
    client.Login()
}
```

**Consequence & Conclusion:**
The test enforces a **clean code architecture**. Spaghetti code is impossible because the API client must exist as an isolated module (`pkg/autodns`) to be testable independently of the web server. The Feature File acts here as an architect.

### 5.2 Case Study: Hexagonal Architecture (Reference: PaperSink)

When we specify software that should be testable independently of its infrastructure (database, cloud provider), the path almost inevitably leads to **Hexagonal Architecture (Ports and Adapters)**. BDD naturally supports this, as the test plays the "Driver" (Primary Adapter) and Mocks replace the "Driven" (Secondary Adapters).

**Structural Proof:**
In the `papersink` project, we see this separation physically in the file system:

```text
/internal
├── core/
│   ├── domain/       # Pure business logic (Entities)
│   └── ports/        # Interfaces (What does the Core need?)
│       └── ports.go  # "type DocumentRepository interface {...}"
└── adapter/
    ├── firestore/    # Concrete implementation (Google Cloud)
    └── http/         # REST API Handler
```

**Technical Implementation (Dependency Injection):**
The Core defines only the interface (`ports.DocumentRepository`). The Adapter (`firestore.Repository`) implements this. When testing, we can now decide whether to use the real adapter or a mock.

```go
// internal/core/ports/ports.go
type DocumentRepository interface {
    Save(ctx context.Context, doc domain.Document) error
}

// internal/adapter/firestore/repository.go
func (r *FirestoreRepository) Save(...) error { ... }
```

**Consequence & Conclusion:**
The application becomes **independent of technologies**. We can switch the database from Firestore to Postgres without changing a line in the `core` code, as long as the new adapter serves the same port. BDD tests validate the behavior of the Core independently of the adapter used.

## 6. Strategies for External Dependencies (Mocking & Infrastructure)

Modern systems interact with complex infrastructures. In our BDD methodology, we use deterministic mocks.

### 6.1 Declarative Mocking with Mockoon (Reference: DDNS Service)

HTTP dependencies are controlled via mock servers, whose configuration is referenced in the Feature File.

*Feature File:*
```gherkin
Scenario: A client update using specific API behavior
    Given the Mockoon server is running with "bdd/mockoon_environment.json"
```

**Technical Implementation (Container Control):**
The step starts a Docker container with the spec config.

```python
subprocess.run(["docker", "run", ..., "mockoon/cli", "--data", config_file])
```

**Consequence & Conclusion:**
We test **Spec-First**. Since the mock is generated directly from the external system's OpenAPI specification, we validate that our service is compliant with the official interface description, rather than testing against hand-written, potentially incorrect mocks.

### 6.2 Infrastructure Mocking: PKI & DNS (Reference: DDNS Service)

Even system-level components like encryption (TLS) can be specified.

*Feature File:*
```gherkin
Scenario: Successful update with TLS 1.2
    Given the ddns-service is configured with:
      | key            | value                      |
      | custom-ca-cert | mock-server/pki/rootCA.crt |
```

**Technical Implementation (Envoy & Certificates):**
We use an Envoy Proxy with test certificates.

```python
# Step: Start Service with the Custom CA Certificate
# ./bin/service --custom-ca-cert=mock-server/pki/rootCA.crt
```

**Consequence & Conclusion:**
Security-relevant features become **testable**. We don't rely on "TLS just working somehow," but prove through tests that the service actively rejects insecure connections (TLS 1.0) or validates correct certificate chains.

### 6.3 AI-Accelerated Mocking: Ad-hoc System Replicas

By using AI Agents, neighboring systems can be generated **ad-hoc** as mocks.

*Feature File:*
```gherkin
Scenario: Create a new board on Trello Mock
    Given a Trello Mock Server is listening on port 3000
```

**Technical Implementation (Dynamic Python Server):**
The agent generates an `http.server` that implements *exactly* the needed endpoints.

**Consequence & Conclusion:**
**Shift-Left Testing**. We can write integration tests even before the real neighboring system is available or licensed. Dependency on external teams is eliminated.

### 6.4 Resilient Testing: Eventual Consistency Patterns

In distributed cloud systems, "immediacy" is an illusion. Operations like propagating secrets, starting containers (Cold Starts), or delivering messages (Pub/Sub) take time. Tests that check states *once* and abort immediately upon failure lead to "Flaky Tests".

**Strategy: Polling with Timeout**
Instead of a simple `assert`, we use a retry loop. The test is only considered failed if the desired state has not occurred after a defined time span (e.g., 60 seconds). If it occurs earlier, the test continues immediately.

**Example Code (Python):**
```python
max_retries = 10
success = False

for i in range(max_retries):
    try:
        # Try the action or check
        check_remote_state()
        success = True
        break
    except (AssertionError, ConnectionError):
        print(f"Waiting for consistency (Attempt {i+1}/{max_retries})...")
        time.sleep(5) # Exponential Backoff recommended

if not success:
    raise AssertionError("State not reached within timeout")
```

**Use Cases:**
1.  **Sending Traffic:** A `requests.post` to a Cloud Run Service may fail on the first attempt (Cold Start). -> Retry Loop.
2.  **Secret Validation:** A newly created secret might only be visible via API after a few seconds. -> Polling.
3.  **Asynchronous Events:** Waiting for a Pub/Sub message strictly requires polling the subscriber.

## 7. The Iterative Process (Red/Green)

Development follows a strict iterative process.

1.  **Red State:** Formulate requirement in Feature File -> `behave` fails.
2.  **Implementation:** AI generates code (App + Steps).
3.  **Green State:** `make test` passes.

## Conclusion

The quality of the software product directly correlates with the precision of the Feature Files. By lifting infrastructure, data, and architecture into the specification, we create systems that are deterministically reproducible by AI.
