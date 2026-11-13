# AGENTS.md — Operating Charter for AI Agents in the EquiGuard Workshop

This file is binding for every AI coding agent working in this repository: **Antigravity CLI (`agy`)**, **Gemini CLI**, **Claude Code**, **OpenCode**, or **GitHub Copilot**. It is not a style guide. It defines how work is *sequenced* here, and what an agent must refuse to do out of order.

Read this file completely before the first tool call of a session. Also read the authoritative guidelines in [`BDD_GUIDELINES_v1.9.0_EN.md`](BDD_GUIDELINES_v1.9.0_EN.md) (German edition: [`BDD_GUIDELINES_v1.9.0_DE.md`](BDD_GUIDELINES_v1.9.0_DE.md)).

---

## 1. The Agent Is the Guardian of the Guidelines

The agent's first duty is not typing speed. It is specification compliance.

The three pillars of this repository — **conscious architecture decisions (ADRs)**, **documented limitations and scope boundaries (LIMs)**, and **BDD feature files as executable specification** — exist so that the specification alone is complete enough for any AI model to rebuild the entire service autonomously in any programming language.

Therefore:

- The agent **enforces** the rules in this file, in [`BDD_GUIDELINES_v1.9.0_EN.md`](BDD_GUIDELINES_v1.9.0_EN.md), and in [`governance/`](governance/).
- When a request would violate a rule (e.g., writing application code before an ADR or feature file exists, hardcoding magic values in step code, or asserting only an HTTP status code after a write), the agent **names the failure mode, cites the rule, and offers the compliant path**.
- A deliberate, bounded shortcut against an ADR or feature file must be recorded as a **Limitation Record** in [`governance/limitations/`](governance/limitations/). The agent proposes; a human approves.

---

## 2. Ask One Question at a Time (Architecture Dialogue)

During Phase 1 (Architecture Dialogue), this rule outranks efficiency:

- **Exactly one question per turn.** Never output a numbered questionnaire of five questions at once.
- Every question includes:
  1. **Context:** Why this decision matters for the system.
  2. **Options:** The concrete architectural alternatives.
  3. **Recommendation:** One recommended option with a one-sentence reason.
  4. **Consequences:** What trade-offs or operational obligations follow from each choice.
- Wait for the human's answer before asking the next question.
- **Ask the programming language last (or leave it open until Phase 5).** The specification (`governance/`, `bdd/`) must be 100% language-neutral.

---

## 3. The Six Stages of Work (Non-Negotiable Order)

Each stage produces the input for the next. Never skip a stage.

```text
  Stage 1: Architecture Decisions  →  governance/adr/NNNN-*.md              (WHY)
  Stage 2: Boundaries & Deferrals  →  governance/limitations/NNNN-*.md      (WHERE NOT)
  Stage 3: Error Paths & Features  →  bdd/00_error_path_enumeration.md
                                      bdd/mi*_*.feature                     (WHAT — RED)
  Stage 4: Specification Critic    →  whole-picture review of Stages 1–3    (AUDITED)
  Stage 5: Step Definitions        →  bdd/steps/*_steps.py + §13 Step Audit (STILL RED)
  Stage 6: Application Code        →  autonomous build in chosen language   (GREEN)
```

**The Feedback Loop Rule:** Whatever the Specification Critic (Stage 4), the Step Honesty Audit (Stage 5), or contact with reality (Stage 6) finds modifies the **ADR, Limitation Record, or Feature File first** — never directly the application code.

### 3.1 Stage 1 — Architecture Decisions (`governance/adr/`)

Every architectural choice is recorded using [`governance/adr/TEMPLATE.md`](governance/adr/TEMPLATE.md) before feature files or code are written. One decision per record. `Security Implications` and `Alternatives Considered` are mandatory sections. Update the index in [`governance/adr/README.md`](governance/adr/README.md).

### 3.2 Stage 2 — Limitations & Scope Boundaries (`governance/limitations/`)

Every deliberate simplification or V1 deferral is recorded using [`governance/limitations/TEMPLATE.md`](governance/limitations/TEMPLATE.md) and indexed in [`governance/limitations/README.md`](governance/limitations/README.md). Undocumented shortcuts are bugs. Also check the LIM register before "fixing" something that was intentionally deferred.

### 3.3 Stage 3 — Error Path Enumeration & Feature Files (`bdd/`)

The `.feature` files under [`bdd/`](bdd/) are the **Single Source of Truth** for system behavior.

- **Quantify before specifying (Guidelines §4.5):** Before writing scenarios, enumerate the failure space layer by layer in [`bdd/00_error_path_enumeration.md`](bdd/00_error_path_enumeration.md). Every row must resolve to a scenario or a documented exclusion reason.
- **No magic values (Guidelines §2.1):** Every port, coordinate, project ID, collection name, topic name, and timeout that a scenario depends on must be visible in the Gherkin text (`Background` or `Scenario` tables/docstrings).
- **Positive and negative controls (Guidelines §4.2):** A rule with only passing examples is not specified. Include the counter-test that fails if the rule is removed.
- **Independent channel verification (Guidelines §4.3, §13.2):** Never trust a service's HTTP response alone as proof of persistence. Verify writes by reading Firestore directly from the test harness.
- **Polling with explicit timeouts (Guidelines §4.4):** Eventual consistency is tested via polling with a timeout stated in the step text (`within 10 seconds`), never via fixed `sleep` calls in positive assertions.
- **Traceability header:** Every `.feature` file opens with a `# Source:` comment naming the ADRs and LIMs it is accountable to and the independent verification channel it uses.

### 3.4 Stage 4 — Pre-Code Specification Critic (Guidelines §14)

Before writing step definitions or application code, run an independent Specification Critic review across all ADRs, LIMs, `00_error_path_enumeration.md`, and `.feature` files together. The Critic reads **only Markdown and Gherkin** (never code) and checks:

1. **Binding Set:** Are ADR/LIM statuses and cross-references consistent?
2. **Record vs. Record:** Do two records state conflicting values or rules?
3. **Feature vs. Feature:** Do payloads, schemas, or field names diverge across milestones (`@mi1`–`@mi4`)?
4. **ADR ↔ Feature File:** Does every decided rule in an ADR have an enforcing scenario, and does every scenario trace to an ADR?
5. **LIM ↔ Both:** Is every intentional gap documented in a LIM?
6. **Scenario Honesty:** Can every `Then` step fail? Are boundary cases and negative controls present?

### 3.5 Stage 5 — Language-Neutral Black-Box Steps & Step Honesty Audit (`bdd/steps/`)

- **Black-box contract:** The test suite uses Python `behave` in an isolated `.venv` and interacts with the system under test exclusively from the outside:
  - **MI1 (`@mi1`):** Invokes `./bin/geofence-lib-test` via `stdin`/`stdout` JSON (`{"point": {"lon": ..., "lat": ...}, "polygon": [...]}` → `{"is_inside": true|false}`).
  - **MI2 (`@mi2`):** Starts `./bin/geofence-processor` with env vars (`PORT`, `FIRESTORE_EMULATOR_HOST`, `PROJECT_ID`), sends Pub/Sub push HTTP POSTs to `/telemetry-push`, and verifies documents directly in the Firestore emulator.
  - **MI3 (`@mi3`):** Builds the Docker image `equiguard/geofence-processor:test` from `Dockerfile`, runs it as a container, verifies `GET /health`, port binding, valid/malformed payloads, and Firestore state.
  - **MI4 (`@mi4`):** Publishes to the real GCP Pub/Sub topic and verifies alerts in real Firestore against the live Cloud Run service provisioned by Terraform.
- **Steps are dumb plumbing (Guidelines §1.3, §5.1):** Step definitions transport data from Gherkin into the system and observe results. They never calculate expected business values, never inject hidden business fields, and never import application code.
- **Independent Step Audit (Guidelines §13):** Review all step files against the three verification patterns: (1) Persistence validation via independent channel, (2) Origin analysis for `Then` values, (3) Data symmetry between scenario and step code.

### 3.6 Stage 6 — Autonomous Polyglot Implementation & Cloud Rollout

When implementing the application in Phase 5:

- **The specification (`governance/`, `bdd/`) is read-only.** Do not edit `.feature` files, step files, ADRs, or LIMs to make a failing test pass. If you believe a scenario is contradictory, report it at the end.
- **Any target language is permitted** (Go, Python, Rust, TypeScript/Node.js, Java, etc.) as long as:
  1. `make build` produces executable `./bin/geofence-lib-test` and `./bin/geofence-processor` (either compiled binaries or executable scripts with a shebang and `chmod +x`, or via a custom `./build.sh`).
  2. `Dockerfile` builds a working container image `equiguard/geofence-processor:test` that listens on `$PORT` (default `8081`).
  3. `make test-all` (MI1 + MI2 + MI3) passes **twice in a row** with zero failed scenarios.

---

## 4. Workshop Exercises: Do Your Own Work

This repository is also used for a hands-on workshop. The reference solutions and the checkpoint machinery exist for the **humans in the room**, not for agents:

- Never read, extract, import or execute anything under `../facilitator/` (including `solutions.tar.gz` and `solutions.py`) or `scripts/checkpoint.py`.
- Never run the make targets `workshop-start`, `ex*-start`, `ex*-solution`, `bonus-start` or `bonus-solution` yourself.
- Never use git history (`git show`, `git log -p`, `git diff` against other commits) to look for solutions.

Produce your result from the specification and the task you were given. If you cannot, say so instead of looking for an answer key.

---

## 5. Quick Reference — What the Agent Refuses to Do

| Never | Instead |
|---|---|
| Write application code before ADRs and `.feature` files exist | Start at Stage 1 (ADRs) or Stage 3 (`.feature` files) |
| Ask multiple architecture questions in one message | Ask one question at a time with options, recommendation, and consequences |
| Hardcode ports, coordinates, project IDs, or thresholds in step code | Put every business-relevant value in the `.feature` file |
| Compute expected results inside a Python step definition | Take expected values strictly from the Gherkin scenario |
| Assert a write by checking only the HTTP 200/204 response | Verify the written document through the independent Firestore channel |
| Couple `.feature` or `_steps.py` files to a specific implementation language | Use the language-neutral black-box CLI/HTTP/OCI contracts |
| Modify a `.feature` file during Stage 6 to make a failing test pass | Fix the application code to satisfy the specification |
| Look up reference solutions, checkpoints or git history during a workshop exercise | Do the work from the specification (section 4) |
