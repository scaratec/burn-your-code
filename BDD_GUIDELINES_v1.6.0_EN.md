# AI-Driven Behavior Driven Development: Practical Guidelines for Specification-Driven Software Engineering

**Version: 1.6.0**

## Preamble

These guidelines describe a pragmatic BDD process for software development
with AI assistance.

The central premise is:

**Feature files written in Gherkin are the single source of truth for
business behaviour.**

This means:

- Business requirements, expected behaviour, and visible business rules are
  described in the feature file.
- Step code, test helper code, and the implementation serve to execute and
  validate that behaviour.
- Hidden business rules in glue code are to be avoided.

This does not mean:

- that every technical detail must appear in the feature file,
- that feature files replace architecture diagrams, type systems, or
  operational documentation,
- or that a green BDD test constitutes a formal proof of correctness,
  security, or memory safety.

In this document BDD is not an ideology but a tool for increasing clarity,
traceability, and technical discipline.

## 1. Core Principles

### 1.1 Business Single Source of Truth

When it comes to business behaviour, the feature file is authoritative.

This covers in particular:

- expected behaviour of APIs, UIs, jobs, and services,
- business input data and expected results,
- business derivation rules,
- error cases and rejection rules,
- observable side effects on neighbouring systems.

The feature file is not the place for technical internals without business
value, such as:

- concrete class hierarchies,
- private helper methods,
- framework-specific internal flags,
- irrelevant refactoring details.

### 1.2 Observable Behaviour Over Internal Assumption

BDD specifies the externally observable behaviour of a system.

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

Step implementations must be as dumb as possible.

Their job is to:

- read inputs from the feature file,
- drive the system under test,
- capture results,
- compare results against the specification.

Their job is not to:

- re-implement business logic,
- guess missing business data,
- silently inject default values,
- conceal business edge cases.

## 2. Data Explicitness

### 2.1 All Business-Relevant Data Must Be Visible

A good BDD scenario is sufficiently complete from a business perspective to
be understood without looking at the step code.

If a `Then` step expects a concrete value, that value must either:

1. be explicitly present in the `Given`, or
2. be derivable from a business rule that is clearly identifiable in the
   scenario.

### 2.2 Avoid Requirement Gaps

A requirement gap exists when an expected value is demanded by the scenario
but its origin remains invisible.

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

- The implementation or step code will in all likelihood hardcode the value.
- The test then confirms not a general rule but only a static string match.

### 2.3 Anti-Hardcoding Strategy

To surface hidden constants, three rules apply:

- Completeness: all business-relevant source data must be visible.
- Variance: for critical fields at least two different scenarios should exist.
- Derivation rule: when values are computed, the business rule must be
  recognisable.

`Scenario Outline` is often the right tool here.

### 2.4 Separation of Master Data and Transactional Data

In more complex domains, static configuration and case-specific data should
be kept separate.

Recommendation:

- Master data explicitly as JSON or a table in the `Given`.
- Transactional data separately as JSON, a table, or a referenced artefact.

This keeps the feature file readable without sacrificing business completeness.

## 3. Complex Data Structures

### 3.1 DocStrings for JSON and Payloads

Complex data belongs visibly in the scenario, not in cryptic helper objects
inside step code.

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

Step code may parse this JSON and pass it technically to the application.
It must not, however, extend or repair it for business reasons.

### 3.2 Make Transformation Logic Visible

Mapping logic between source and target systems is frequently pure business
logic. It should be visible in the feature file as an example.

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

### 3.3 Artefacts Instead of Invented Data

Where sensible, real or realistic artefacts should be used:

- JSON files,
- XML payloads,
- invoices,
- log output,
- example messages,
- mail messages,
- CSV files.

This reduces the risk of optimising only for an artificial test world.

## 4. Test Design

### 4.1 The Prohibition of Circular Logic

A test must not re-implement the business logic itself.

Bad:

- The test calculates the same gross price in the Python step as the
  application does.
- The test builds the same mapping table internally as the implementation.

Good:

- The test supplies inputs.
- The application produces a result.
- The test compares the visible result against the specification.

### 4.2 Positive and Negative Paths

For important business cases both success and failure paths must always be
present.

At a minimum the following must be covered:

- happy path,
- validation errors,
- business rejections,
- technical errors with business impact,
- relevant edge cases.

### 4.3 Explicitly Test for Silent Failures

A test must not rely solely on status codes or success messages.

When the system signals success, critical processes must also have their
target state validated, for example:

- record was actually saved,
- message was actually published,
- object was actually created,
- mail was actually stored,
- UI does not merely show success but reflects the new state.

### 4.4 Handle Eventual Consistency Cleanly

In distributed systems a single immediate `assert` must not be used
prematurely.

Instead:

- polling with a clearly defined timeout,
- comprehensible error messages,
- no infinite sleeps without justification,
- no flakiness accepted as a normal condition.

## 5. Step Implementations

### 5.1 Responsibilities of Steps

Step files are adapters between specification and system.

They should:

- read data from Gherkin,
- start or drive the system,
- configure mocks,
- store results,
- execute standardised assertions.

They should not:

- contain business logic,
- silently mutate test data,
- supply implicit defaults,
- hide complex calculations.

### 5.2 Modularisation

As complexity grows, steps must be cleanly structured.

Recommended layout:

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

Helpers, fixtures, and mocks are necessary, but they are not the business
source of truth.

If there is a conflict between the feature file and test helper code, the
feature file is authoritative for business behaviour.

## 6. Isolation and Runtime Environment

### 6.1 Isolated Test Environment

BDD tests should run in an isolated runtime environment.

Goals:

- reproducible dependencies,
- no mixing with the local developer environment,
- controlled versions,
- clean starting conditions.

Depending on the stack this can mean:

- `.venv`,
- container,
- dedicated test database,
- separate browser context,
- isolated queue or bucket.

### 6.2 Housekeeping Before Test Start

Before tests begin the environment must be clean.

Examples:

- no leftover containers,
- no ghost processes on test ports,
- no stale sessions or browser states,
- no contaminated temp directories,
- a defined test data baseline.

## 7. External Dependencies

### 7.1 Deterministic Mocks Instead of Uncontrolled Live Dependencies

External systems should be replaced by controlled mocks for most tests.

Suitable options include:

- HTTP mock servers,
- queue fakes,
- test databases,
- filesystem sandboxes,
- local SMTP, IMAP, or DNS test systems.

Live systems belong in a small number of targeted integration or smoke tests.

### 7.2 Mocks Must Simulate Behaviour, Not Wishful Thinking

A mock is only useful if it realistically represents relevant behaviour for
the case under test.

Examples:

- HTTP 429 with retry,
- timeouts,
- 403 and 500 errors,
- delayed service startup,
- partial data,
- idempotent repetitions.

## 8. Architecture and BDD

### 8.1 BDD Should Promote Good Interfaces

BDD often leads naturally to better architecture because testable systems
require explicit interfaces.

Typical positive effects:

- better separation of core and infrastructure,
- testable adapters,
- clearer input and output models,
- fewer hidden side effects.

### 8.2 BDD Does Not Replace Architecture Work

BDD helps to sharpen architecture. It does not replace:

- architectural decisions,
- load tests,
- security reviews,
- static analysis,
- type checking,
- formal verification,
- code reviews.

A green BDD test means only:

- The tested behaviour works for the tested cases.

Nothing more, nothing less.

## 9. Systems-Level Languages and Memory Errors

BDD can also be useful for C, C++, Rust, or other systems-level components.

Practical use cases:

- checking the API behaviour of small native libraries,
- making error paths reproducible,
- making crashes visible in known scenarios,
- hardening integration behaviour against the host system.

Important caveats:

- The absence of a crash is not proof of memory safety.
- A successful `ctypes` test replaces neither sanitisers nor Valgrind nor
  fuzzing.
- BDD can complement these tools but cannot replace formal or specialised
  tooling.

## 10. UI Testing

### 10.1 Test User Intent

UI scenarios should describe user intent, not DOM internals.

Example:

```gherkin
Scenario: Candidate selection in data grid
  When the user selects the candidate "Max Mustermann" in the data grid
```

Step code may encapsulate the technical selection. The feature file describes
the intent.

### 10.2 No Fragile Browser Manipulation

Real user interactions or realistic simulations are preferred:

- typing,
- clicking,
- focusing,
- choosing,
- submitting.

Directly setting values without triggering relevant events is a fallback only
and must be a conscious choice.

### 10.3 Browser Isolation

UI tests should run in isolated browser contexts to avoid cache, cookie, and
session leaks.

## 11. Iterative Process

The development cycle stays simple:

1. Describe the business behaviour in the feature file.
2. Test fails.
3. Add implementation and step code.
4. Test turns green.
5. Refactoring without changing the business behaviour.

The key is:

- clarify behaviour first,
- then implement,
- then clean up technically.

## 12. Quality Criteria for Good Feature Files

A good feature file is:

- business-clear,
- readable without hidden rules,
- data-explicit,
- not redundant,
- not technically overloaded,
- robust against trivial hardcoding,
- relevant to observable behaviour.

A bad feature file is:

- full of magic values,
- business-incomplete,
- only understandable with a look into the glue code,
- technically obfuscated,
- so generic that it asserts nothing concrete,
- or so detail-obsessed that it unnecessarily obstructs refactoring.

## Closing Remarks

These guidelines are not meant to create dogma but to foster better
development practice.

The core remains:

- **Feature files are the single source of truth for business behaviour.**
- Glue code and implementation are there to serve that business behaviour.
- Good BDD practice creates clarity, reduces hidden assumptions, and improves
  testability.
- BDD is a powerful tool, but not a substitute for professional engineering
  outside of the tested behaviour.
