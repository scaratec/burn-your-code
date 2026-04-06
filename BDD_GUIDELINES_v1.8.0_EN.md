# AI-Driven Behavior Driven Development: Practical Guidelines for Specification-Driven Software Development

**Version: 1.8.0**

## Preamble

These guidelines describe a pragmatic BDD process for software development with AI assistance.

The central assumption is:

**Feature files in Gherkin are the Single Source of Truth for business logic.**

This means:

- Business requirements, expected behavior, and visible business rules are described in the feature file.
- Step code, test helper code, and implementation serve to execute and validate this behavior.
- Hidden business rules in glue code must be avoided.

This does not mean:

- that every technical detail must be in the feature file,
- that feature files replace architecture diagrams, type systems, or operations documentation,
- or that a green BDD test constitutes formal proof of correctness, security, or memory safety.

BDD in this document is not an ideology but a tool for increasing clarity, traceability, and technical discipline.

## 1. Core Principles

### 1.1 Single Source of Truth for Business Logic

When it comes to business logic, the feature file is authoritative.

This includes in particular:

- expected behavior of APIs, UIs, jobs, and services,
- business input data and expected results,
- business derivation rules,
- error cases and rejection rules,
- observable side effects on neighboring systems.

The feature file should not contain technical internals without business value, such as:

- specific class hierarchies,
- private helper methods,
- framework-specific internal flags,
- irrelevant refactoring details.

### 1.2 Observable Behavior Over Internal Assumptions

BDD specifies the externally observable behavior of a system.

Tests should preferably validate:

- return values,
- HTTP responses,
- generated files,
- persisted data,
- messages in queues,
- logs with business or operational relevance,
- visible UI states.

Tests should not primarily confirm:

- that a specific private method was called,
- that a specific implementation strategy was used,
- or that the test reproduces its own helper logic.

### 1.3 No Hidden Business Logic in Glue Code

Step implementations must be as simple as possible.

Their purpose is:

- to read inputs from the feature file,
- to drive the system under test,
- to capture results,
- to compare results against the specification.

Their purpose is not:

- to replicate business logic,
- to guess missing business data,
- to secretly inject default values,
- to conceal business edge cases.

## 2. Data Explicitness

### 2.1 All Business-Relevant Data Must Be Visible

A good BDD scenario is sufficiently complete in business terms to be understood without looking at the step code.

If a `Then` step expects a specific value, that value must either:

1. be explicitly contained in the `Given`, or
2. be derivable through a business rule clearly recognizable in the scenario.

### 2.2 Avoiding Requirement Gaps

A requirement gap exists when an expected value is demanded in the scenario but its origin remains invisible.

Bad example:

```gherkin
Scenario: Map Order to Marketplace
  Given an order for item "X"
  When the mapping logic is applied
  Then the output must contain:
    | field | value       |
    | iban  | DE123456789 |
    | tax   | VAT_DE      |
```

Here it remains unclear where `DE123456789` and `VAT_DE` come from.

Consequence:

- The implementation or step code will most likely hardcode the value.
- The test then confirms no general logic, only a static text comparison.

### 2.3 Anti-Hardcoding Strategy

To uncover hidden constants, three rules apply:

- Completeness: All business-relevant source data must be visible.
- Variance: For critical fields, at least two different scenarios should exist.
- Derivation rule: If values are calculated, the business rule must be recognizable.

`Scenario Outline` is often the right tool here.

### 2.4 Separation of Master Data and Transactional Data

In more complex domains, static configurations and case-specific data should be separated.

Recommendation:

- Master data explicitly as JSON or table in the `Given`.
- Transactional data separately as JSON, table, or referenced artifact.

This keeps the feature file readable without sacrificing business completeness.

## 3. Complex Data Structures

### 3.1 DocStrings for JSON and Payloads

Complex data belongs not in cryptic helper objects in the step code but visibly in the scenario.

Example:

```gherkin
Scenario: Upload a valid invoice document
  Given the client provides business metadata:
    """
    {
      "invoice_number": "INV-2026-001",
      "net_amount": 10050,
      "currency": "EUR"
    }
    """
```

The step code may parse this JSON and pass it technically to the application. However, it must not extend or repair it in business terms.

### 3.2 Making Transformation Logic Visible

Mapping logic between source and target systems is often pure business logic. It should be visible in the feature file as an example.

Example:

```gherkin
Scenario: Mapping custom fields from source to target
  Given a source order with custom fields:
    | source_code | value |
    | color-01    | blue  |
    | size-x      | 42    |
  When the mapping logic is applied
  Then the target structure should contain:
    | target_field   | value |
    | attributes.col | blue  |
    | attributes.sz  | 42    |
```

### 3.3 Artifacts Over Fabricated Data

Where appropriate, real or realistic artifacts should be used:

- JSON files,
- XML payloads,
- invoices,
- log outputs,
- example messages,
- email messages,
- CSV files.

This reduces the risk of optimizing only for an artificial test world.

## 4. Test Design

### 4.1 The Prohibition of Circular Reasoning

The test must not replicate the business logic itself.

Bad:

- The test calculates the same gross price in a Python step as the application.
- The test internally produces the same mapping table as the implementation.

Good:

- The test provides inputs.
- The application produces a result.
- The test compares the visible result against the specification.

### 4.2 Positive and Negative Paths

For important business cases, both success and failure paths must always be present.

At minimum, the following should be covered:

- Happy path,
- Validation errors,
- Business rejections,
- Technical errors with business impact,
- Relevant edge cases.

### 4.3 Explicitly Testing for Silent Failures

A test must not rely solely on status codes or success messages.

When the system signals success, the target state must also be validated for critical processes, for example:

- Record was actually saved,
- Message was actually published,
- Object was actually created,
- Email was actually stored,
- UI shows not just success but reflects the new state.

### 4.4 Handling Eventual Consistency Properly

In distributed systems, a single `assert` must not be used prematurely.

Instead, the following applies:

- Polling with a clearly defined timeout,
- Comprehensible error messages,
- No endless sleeps without justification,
- No flakiness accepted as normal.

### 4.5 Systematic Identification of Failure Paths

Section 4.2 names which categories of failure paths to cover. This section describes how the complete set of failure paths for a given system is methodically identified.

#### The Principle: Quantification Before Specification

Before individual failure scenarios are described, the total number of possible failure paths must be determined. The question is not "which errors come to mind?" but "how many failure paths exist in this system?".

The difference is essential:

- "Which errors come to mind?" produces an incomplete list, limited by experience and attention.
- "How many are there?" forces a systematic decomposition of the system and makes gaps visible.

The number does not need to be exact. It must be justifiable. If the derivation is traceable, it covers all relevant cases with high probability.

#### The Method: Layer-by-Layer Enumeration

The system is decomposed along its processing chain into layers. For each layer, the possible error sources are enumerated. The sum across all layers yields the total count.

**Step 1: Identify layers.**

Every system that accepts inputs, communicates externally, and delivers results has at least these layers:

| Layer | Error Source | Typical Question |
|---|---|---|
| Input validation | Missing, empty, incorrectly formatted, wrong-typed, duplicate values | What can the caller pass incorrectly? |
| External communication | Network, HTTP status, timeouts, DNS, TLS | What can go wrong between the system and the remote endpoint? |
| Response processing | Format, schema, unexpected content, missing fields | What can the remote endpoint return that does not match the expected format? |
| Data integrity | Value ranges, business consistency, degenerate structures | What can be factually wrong with the received data? |
| Protocol / Interface | Unknown methods, incorrect message formats | What can go wrong at the transport level? |

Not every system has all layers. A pure algorithm without external dependencies has only input validation and data integrity. An API gateway has all five.

**Step 2: Enumerate per layer.**

For each identified layer, the specific failure cases are listed. The following rules apply:

- Each failure case must have its own distinguishable cause.
- Variants of the same cause (e.g., HTTP 400 vs. HTTP 403 vs. HTTP 500) count individually if the system must respond differently.
- Variants to which the system responds identically can be grouped together.

Example for the "Input validation" layer of a system with four required fields:

- 4 fields x "missing" = 4 failure cases
- 4 fields x "empty" = 4 failure cases (if "empty" is handled differently from "missing")
- 2 fields x "wrong format" = 2 failure cases
- 1 special case "duplicates" = 1 failure case
- 1 structural error "wrong type" = 1 failure case
- Layer total: 12 failure cases

**Step 3: Sum up and present in tabular form.**

The layers and their failure counts are summarized in an overview table:

```text
| Layer                  | Count  | Already covered   |
|------------------------|--------|-------------------|
| Input validation       | 12     | 4                 |
| External communication | 8      | 1                 |
| Response processing    | 5      | 0                 |
| Data integrity         | 4      | 0                 |
| Protocol               | 3      | 1                 |
| Total                  | 32     | 6                 |
| New scenarios          | 26     |                   |
```

The "Already covered" column prevents duplicate work when failure paths are already specified in other feature files.

**Step 4: Derive scenarios.**

Only after quantification are the individual scenarios written. For failure cases with the same pattern but different inputs, `Scenario Outline` is suitable (Guideline 2.3). For failure cases with different behavior, separate scenarios are created.

#### Scope

Layer-by-layer enumeration does not replace business judgment. Not every identified failure path necessarily requires its own scenario. Some failure cases (e.g., DNS resolution, TLS certificate errors) are purely operational and have no business impact. The decision about which failure paths are specified as scenarios lies with the human.

The value of this method lies not in the number itself but in the fact that the number forces a complete analysis. Someone who identifies 32 failure paths and consciously decides to specify 26 of them has traceable coverage. Someone who lists "the most important failure cases" has a hope.

## 5. Step Implementations

### 5.1 Responsibilities of Steps

Step files are adapters between specification and system.

They should:

- read data from Gherkin,
- start or drive the system,
- configure mocks,
- store results,
- execute standardized assertions.

They should not:

- contain business logic,
- secretly mutate test data,
- silently add implicit defaults,
- hide complex calculations.

### 5.2 Modularization

With increasing complexity, steps must be cleanly separated.

Recommended structure:

```text
bdd/steps/
├── ingress_steps.py
├── logic_steps.py
├── persistence_steps.py
├── ui_steps.py
└── cloud_steps.py
```

Each step file should have a clear area of responsibility.

### 5.3 Test Helper Code Is Infrastructure, Not Truth

Helpers, fixtures, and mocks are necessary, but they are not the authoritative source of business truth.

If a conflict exists between the feature file and test helper code, the feature file is authoritative for business logic.

## 6. Isolation and Runtime Environment

### 6.1 Isolated Test Environment

BDD tests should run in an isolated runtime environment.

Goals:

- reproducible dependencies,
- no mixing with local developer environment,
- controlled versions,
- clear starting conditions.

Depending on the stack, this can mean:

- `.venv`,
- containers,
- dedicated test database,
- separate browser context,
- isolated queue or bucket.

### 6.2 Housekeeping Before Test Start

Before test execution, the environment must be clean.

Examples:

- no old containers,
- no ghost processes on test ports,
- no old sessions or browser states,
- no contaminated temp directories,
- defined test data baseline.

## 7. External Dependencies

### 7.1 Deterministic Mocks Over Uncontrolled Live Dependencies

External systems should be replaced by controlled mocks for most tests.

Suitable options include:

- HTTP mock servers,
- queue fakes,
- test databases,
- filesystem sandboxes,
- local SMTP, IMAP, or DNS test systems.

Live systems have their place in a few targeted integration or smoke tests.

### 7.2 Mocks Must Simulate Behavior, Not Wishful Thinking

A mock is only useful if it realistically represents behavior relevant to the case being tested.

Examples:

- HTTP 429 with retry,
- timeouts,
- 403 and 500 errors,
- delayed service startup,
- partial data,
- idempotent retries.

## 8. Architecture and BDD

### 8.1 BDD Should Promote Good Interfaces

BDD often naturally leads to better architecture because testable systems require explicit interfaces.

Typical positive effects:

- better separation of core and infrastructure,
- testable adapters,
- clearer input and output models,
- fewer hidden side effects.

### 8.2 BDD Does Not Replace Architecture Work

BDD helps sharpen architecture. However, it does not replace:

- architecture decisions,
- load tests,
- security reviews,
- static analysis,
- type checking,
- formal verification,
- code reviews.

A green BDD test only means:

- The tested behavior works for the tested cases.

Nothing more and nothing less.

## 9. System-Level Languages and Memory Errors

BDD can also be useful for C, C++, Rust, or other system-level components.

Practical use cases:

- testing API behavior of small native libraries,
- making failure paths reproducible,
- making crashes visible in known scenarios,
- securing integration behavior against the host system.

However, it is important to note:

- An absent crash is not proof of memory safety.
- A successful `ctypes` test replaces neither sanitizers nor Valgrind nor fuzzing.
- BDD can supplement here but cannot replace formal or specialized tools.

## 10. UI Testing

### 10.1 Testing User Intent

UI scenarios should describe user intent, not DOM internals.

Example:

```gherkin
Scenario: Candidate selection in data grid
  When the user selects the candidate "Max Mustermann" in the data grid
```

The step code may encapsulate the technical selection. The feature file describes the intent.

### 10.2 No Fragile Browser Manipulation

Prefer real user interactions or realistic simulations:

- typing,
- clicking,
- focusing,
- selecting,
- submitting.

Directly setting values without relevant events is only a fallback and must be done deliberately.

### 10.3 Browser Isolation

UI tests should run in isolated browser contexts to avoid cache, cookie, and session leaks.

## 11. Iterative Process

The development cycle remains simple:

1. Describe business behavior in the feature file.
2. Test fails.
3. Add implementation and step code.
4. Test goes green.
5. Refactor without changing business logic.

What matters is:

- first clarify behavior,
- then implement,
- then clean up technically.

## 12. Quality Criteria for Good Feature Files

A good feature file is:

- clear in business terms,
- readable without hidden rules,
- data-explicit,
- not redundant,
- not technically overloaded,
- robust against trivial hardcoding,
- relevant to observable behavior.

A bad feature file is:

- full of magic values,
- incomplete in business terms,
- only understandable by looking at the glue code,
- technically cryptic,
- so generic that it secures nothing concrete,
- or so detail-obsessed that it unnecessarily complicates refactoring.

## 13. Spec Audit: Verification of Implementation Fidelity

### 13.1 The Problem

LLM-generated step code and production code can formally pass a BDD suite without honestly fulfilling the specification. This is not an edge case but an expected behavior in AI-assisted implementation.

Typical patterns:

- The system reports success but has internally done nothing (stub with status code).
- Test and implementation confirm each other through identical hardcoded values without any real business rule existing.
- Step code injects business data not visible in the scenario, thereby distorting the test reality.

A green test run alone is therefore not sufficient evidence of implementation fidelity. It must be supplemented by an independent review.

### 13.2 Three Verification Patterns

The following three checks operationalize existing principles of this document. They can be systematically applied against every scenario.

#### Check 1: Persistence Validation (operationalizes 4.3)

For every scenario with a write operation (POST, PUT, DELETE, file creation, message sending):

> Does a subsequent verification step exist that validates the target state through a second, independent channel?

An independent channel is, for example:

- a direct database query,
- reading a generated file,
- querying a queue or event log,
- a separate GET request that returns the written data.

The API response of the write operation itself is not an independent channel. It is the system's self-report and therefore insufficient.

**Finding**, if: the scenario only checks the status code or response of the write operation without independently verifying the target state.

#### Check 2: Origin Analysis for Then Values (operationalizes 2.2)

For every concrete value in a `Then` step:

> Is this value either (a) literally contained in a `Given` or `When` of the scenario, or (b) derivable through a business rule recognizable in the scenario from the visible data?

Example of a finding:

```gherkin
Given current harvest volume is 1500 kg
When the prediction is requested
Then yieldPrediction must be 19662
```

The value 19662 appears neither in the inputs nor is a derivation rule visible. This opens the possibility that implementation and test use the same hardcoded value without any real calculation taking place.

Example without finding:

```gherkin
Given net amount is 100 EUR and tax rate is 19%
When the invoice is calculated
Then gross amount must be 119 EUR
```

119 = 100 * 1.19. The derivation rule is recognizable in the scenario.

**Finding**, if: an expected value is neither explicitly present in the inputs nor derivable from visible data and a named rule.

#### Check 3: Data Symmetry Between Scenario and Step Code (operationalizes 1.3)

For every `Given` step that prepares test data:

> Does the step code use exclusively data visible in the scenario, or does it add its own business values?

Example of a finding:

```gherkin
Given climate data exists for cultivation zone 303
```

The step code inserts `calendar_week=41, light_j=1200.5, temperature_day=20.2` into the database. None of these values are visible in the scenario. If a later `Then` step checks against these values, the verification is not traceable.

Technical infrastructure data (foreign keys, IDs for referential integrity, database connections) are exempt from this check. They are not business data.

**Finding**, if: the step code injects business values that do not appear in the scenario and that could later be relevant for assertions.

### 13.3 Execution

The spec audit is performed as a separate verification step after implementation, not as part of the regular test run.

Recommended workflow:

1. The implementing LLM writes production code and step code.
2. The BDD tests run green.
3. An independent audit agent checks the three patterns against all scenarios.
4. The human evaluates the findings and decides on corrective action.

Two rules for the audit agent:

**Role separation.** The audit agent should not be the same agent that created the implementation. Not because an LLM technically cannot do both, but because independence increases the quality of insight. Those who review their own code rationalize.

**No production code.** The audit agent should preferably only read feature files and step code, not the production code. The check poses the question: Does the step code honestly validate the behavior? If the audit agent reads the production code, there is a risk that it rationalizes the implementation as correct instead of recognizing the gap between specification and verification.

### 13.4 Classification

A spec audit replaces neither code reviews nor manual tests. It is a structured verification step that specifically addresses the three most common honesty gaps in LLM-generated step code.

Not every finding requires a correction. Some scenarios deliberately test only the status code (e.g., for pure validation rejections). Some Given steps inevitably must create test data not present in the scenario. The decision about the relevance of a finding lies with the human.

## Closing Remarks

These guidelines are not meant to create dogma but to foster better development practice.

The core remains:

- **Feature files are the Single Source of Truth for business logic.**
- Glue code and implementation serve this business logic.
- Good BDD practice creates clarity, reduces hidden assumptions, and improves testability.
- BDD is a powerful tool but no substitute for professional engineering beyond the tested behavior.
