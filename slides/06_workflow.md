# The 5-Phase Specification-First Cycle

1. **Phase 1 — Dialogue & Decisions (`governance/adr/`, `limitations/`):** Guided architecture dialogue (one question at a time) → **ADRs** (*Why*) & **LIMs** (*Where Not*).
2. **Phase 2 — Error Paths & Features (`bdd/`):** Quantify failure paths layer by layer (§4.5), then write Gherkin `.feature` files (*What*) → **RED**.
3. **Phase 3 — Specification Critic (`bdd-critic`):** Whole-picture pre-code audit across ADRs, LIMs, Error Paths, and Feature Files (Markdown & Gherkin only) → **AUDITED**.
4. **Phase 4 — Black-Box Steps & Honesty Audit (`bdd/steps/`):** Language-neutral Python `behave` steps + §13 Step Honesty Audit (Independent Channel, Value Provenance, Data Symmetry) → **STILL RED**.
5. **Phase 5 — Autonomous Polyglot Code & Cloud Rollout:** Gemini (via Antigravity CLI) implements the service in **any language** until all scenarios pass twice in a row → **GREEN** (local & GCP Cloud Run).

**Feedback Loop Rule:** Whatever the Critic (3), the Step Audit (4), or Reality (5) finds modifies the **ADR, LIM, or Feature File FIRST** — never directly the code.
