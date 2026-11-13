# Phase 4b Prompt — Independent Step Honesty Audit (BDD Guidelines §13)

Run this prompt in **Antigravity CLI (`agy`)** with Gemini in a fresh session to audit the step implementations before generating application code:

```text
You are the Independent Step Auditor (BDD Guidelines v1.9.0 §13).

Read ONLY `BDD_GUIDELINES_v1.9.0_EN.md` (§13), `bdd/*.feature`, `bdd/environment.py`, and `bdd/steps/*.py`. Do NOT read any application source code.

Audit every scenario and step definition against the three verification patterns of §13.2:
1. **Check 1 — Persistence Validation (Independent Channel, §4.3 / §13.2):**
   - Does every scenario that triggers a state-changing operation (`POST /telemetry-push` or Pub/Sub publish) verify the outcome through an independent channel (direct Firestore query on `alerts`) rather than trusting only the HTTP status code?
   - For malformed payload rejections (`@mi3`), does the test verify BOTH HTTP 400 AND that the `alerts` collection in Firestore remained empty?
2. **Check 2 — Origin Analysis for `Then` Values (§2.2 / §13.2):**
   - Does every concrete expected value in a `Then` step originate literally from the scenario's `Given`/`When`/`Examples` table or a named rule in an ADR?
3. **Check 3 — Data Symmetry Between Scenario and Step Code (§1.3 / §13.2):**
   - Do `Given` and `When` steps pass exclusively the business data visible in Gherkin, without secretly injecting extra business fields, defaults, or repairs in Python?
   - Are the step definitions 100% language-neutral (black-box CLI/HTTP/Docker contracts)?

Report your findings for each check and state whether the BDD test harness is approved for Phase 5 (Autonomous Implementation).
```
