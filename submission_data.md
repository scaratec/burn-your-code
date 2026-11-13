# Conference & Workshop Submission Data

## Rethought Title Options

### 1. Recommended Primary Title (Keeps the "Burn Your Code" Brand + Sharpens the Autonomous Spec-First Promise)
- **EN:** **Burn Your Code: Specification-First Engineering for Autonomous AI Agents**
- **Subtitle (Workshop):** *From ADRs and Gherkin to Autonomous Polyglot Cloud Run Services with Gemini and Antigravity CLI*
- **DE:** **Burn Your Code: Spezifikationsgetriebenes Engineering für autonome KI-Agenten**

### 2. Alternative Title Options (Depending on Event Track / Focus)
- **Option B (Focus on the Spec as Code):** *The Spec Is the Source Code: Building Autonomous Polyglot Services with ADRs, BDD, and Gemini*
- **Option C (Focus on Vibe Coding vs. Engineering):** *From House of Cards to Foundation: How ADRs, BDD, and a Critic Agent Make AI Development Reproducible*
- **Option D (Hands-On Workshop Focus):** *Zero Lines of Hand-Written Code: Hands-On Specification Engineering with Antigravity CLI, Gemini, and Google Cloud*
- **Option E (Original Classic Title):** *Burn Your Code: Feature Files as the Ultimate AI Agent Prompt*

---

## Elevator Pitch (max. 300 chars)

AI writes code faster than teams make decisions, turning "Vibe Coding" into a fragile house of cards. In this hands-on workshop, we engineer ADRs, Limitation Records, and Gherkin tests with Antigravity CLI so tight that Gemini builds and deploys the service autonomously in any language on GCP.

---

## Short Abstract — Hands-On Workshop (EN, max. 600 chars)

Ad-hoc prompting ("Vibe Coding") produces plausible code in minutes and unmaintainable debt in hours. What if you never touched application code at all? In this hands-on workshop, we use Antigravity CLI and Gemini to build a complete specification triad: Architecture Decision Records (Why), Limitation Records (Where Not), and Gherkin Feature Files (What). After an independent Critic Agent audits the specification and our black-box steps turn cleanly RED, Gemini autonomously generates the entire service in your language of choice and deploys it to Google Cloud Run.

---

## Full Abstract — Hands-On Workshop (EN)

AI coding agents write code faster than we make decisions. When teams rely on ad-hoc chat prompting ("Vibe Coding"), every generated file leans on unwritten assumptions. Because agents have no memory across sessions, anything not captured in the repository is re-negotiated or hallucinated on the next prompt — building a house of cards.

The solution is a radical shift in where we spend our engineering effort: **95% understanding, defining, and validating the problem; 5% implementing with AI.** When the specification is complete, application code becomes a disposable, replaceable build artifact.

We kick off this hands-on workshop by watching a recorded run where an agent builds a complete event-driven service from zero lines of code against a read-only specification. Then, working hands-on with **Antigravity CLI (`agy`)** and **Google Gemini**, we walk through the five phases that make autonomous development work in practice — building **EquiGuard**, a real-time GPS pasture geofencing system on Google Cloud:

1. **Phase 1 — Architecture Dialogue (ADRs & LIMs):** Starting from a naive prompt, the agent asks one architectural question at a time (with options, recommendations, and consequences — leaving the programming language open). We record our decisions in **ADRs** (*Why*) and our deliberate V1 shortcuts in **Limitation Records** (*Where Not*, telling future agents what *not* to "fix").
2. **Phase 2 — Error Path Enumeration & Gherkin Feature Files:** Before writing scenarios, we systematically count the failure paths layer by layer. Then we write executable Gherkin `.feature` files with explicit configuration tables (zero magic values) and both positive and negative controls.
3. **Phase 3 — The Specification Critic (`bdd-critic`):** Because ADRs, LIMs, and Feature Files all live in Markdown and Gherkin, an independent Critic Agent audits the entire specification in a single context window *before* a single line of code exists — catching contradictions between records and uncovered rules, and feeding every finding back into the specification.
4. **Phase 4 — Language-Neutral Black-Box Steps & Honesty Audit:** We create Python `behave` step definitions that test the system strictly from the outside (CLI `stdin`/`stdout`, HTTP, Docker, and direct Firestore verification) and audit them against LLM test-cheating patterns (circular reasoning, self-reporting HTTP 200 stubs, hidden data injection) until the suite fails **cleanly RED**.
5. **Phase 5 — Autonomous Polyglot Code Generation & Cloud Run Rollout:** With the specification locked, you pick **any programming language you want** (Go, Python, Rust, TypeScript, Java…) and let Gemini autonomously implement the service until all local emulator milestones pass twice in a row — and finally roll it out live to **Google Cloud Run**, **Pub/Sub**, and **Firestore** via Terraform.

---

## Full Abstract — Hands-On Workshop (DE)

KI-Agenten schreiben Code schneller, als wir Entscheidungen treffen. Wer sich auf Ad-hoc-Prompting („Vibe Coding“) verlässt, baut ein Kartenhaus aus ungeschriebenen Annahmen: Da Agenten kein Gedächtnis über Sessions hinweg besitzen, wird jede nicht dokumentierte Entscheidung beim nächsten Prompt neu verhandelt oder halluziniert.

Die Lösung kehrt das Verhältnis um: **95 % Problem verstehen, Entscheidungen festhalten und Prüfbarkeit herstellen – 5 % autonome Umsetzung durch KI.** Ist die Spezifikation vollständig, wird der Anwendungscode zu einem austauschbaren Build-Artefakt.

Zum Einstieg sehen wir im Zeitraffer-Video, wie ein Agent aus null Zeilen Anwendungscode und einer schreibgeschützten Spezifikation vollkommen autonom einen lauffähigen Dienst baut. Anschließend durchlaufen wir hands-on mit der **Antigravity CLI (`agy`)** und **Google Gemini** genau die fünf Entwicklungsphasen, die diese Autonomie ermöglichen – am Beispiel von **EquiGuard**, einem Event-getriebenen GPS-Geofencing-System auf Google Cloud:

1. **Phase 1 — Architektur-Dialog (ADRs & LIMs):** Ausgehend von einer einfachen Idee führt uns der Agent Frage für Frage (mit Optionen, Empfehlung und Konsequenzen – die Programmiersprache bleibt offen!) zu sauberen **Architecture Decision Records** (*Warum*) und **Limitation Records** (*Wo fallen wir bewusst zurück?*).
2. **Phase 2 — Fehlerpfad-Enumeration & Gherkin Feature-Files:** Wir zählen zuerst systematisch die Fehlerpfade durch und formulieren dann sprachneutrale Gherkin-Szenarien ohne Magic Values, inklusive Positivfall und Gegenprobe.
3. **Phase 3 — Der Spezifikations-Kritiker (`bdd-critic`):** Weil ADRs, LIMs und Feature-Files komplett in Markdown und Gherkin vorliegen, liest ein unabhängiger Kritiker-Agent die gesamte Spezifikation als Ganzes gegen, *bevor* eine Zeile Code existiert – und spielt jeden Befund zurück in die Spezifikation.
4. **Phase 4 — Sprachneutrale Black-Box-Steps & Ehrlichkeits-Audit:** Wir erstellen Python-`behave`-Prüfschritte gegen unabhängige Kanäle (CLI, HTTP, Docker, Firestore-Emulator) und prüfen sie per Spec-Audit darauf, dass der Test nicht schummeln kann, bis die Suite **sauber ROT** ist.
5. **Phase 5 — Autonome Polyglotte Code-Generierung & GCP Rollout:** Zum Schluss wählen die Teilnehmenden **eine beliebige Programmiersprache** (Go, Python, Rust, TypeScript, Java …), lassen Gemini die Software vollkommen autonom implementieren, bis alle lokalen Meilensteine grün sind, und rollen den Dienst per Terraform live auf **Google Cloud Run** aus.

---

## Key Takeaways (3 items, max. 150 chars each)

1. Combine ADRs (Why), LIMs (Where Not), and Gherkin (What) into one readable specification that fits in a single agent context window.
2. Audit your specification with an independent Critic Agent before writing code — every finding becomes a permanent scenario, ADR, or LIM.
3. Use black-box steps and independent-channel assertions so Gemini can autonomously build or replace your service in any programming language.

---

## Target Audience and Prerequisites

Software engineers and architects who want to move beyond ad-hoc "Vibe Coding" to reproducible, specification-driven AI engineering. Bring a laptop (macOS, Linux or Windows with WSL2) with git, make, Python 3.11+ and the Antigravity CLI (`agy`) signed in with a Google account. No Docker and no cloud account needed for the exercises.

---

## Workshop Outline (90 min)

| Duration | Block | Activity |
|---:|---|---|
| 18 min | **Kickoff & video** | From House of Cards to Foundation (95/5 shift), video of an autonomous rebuild (Gemini 3.8 Flash, 525 scenarios, zero lines of code), EquiGuard, `make check` |
| 15 min | **Exercise 1: Decide the fence** | Architecture dialogue with Antigravity CLI (`agy`), one question at a time → ADR-0005 and LIM-0004 |
| 16 min | **Exercise 2: Make it red** | Error paths first (§4.5), then boundary scenarios in Gherkin → RED |
| 17 min | **Exercise 3: Let the critic find the bugs** | The specification critic (§14) audits ADRs, LIMs, error paths and features and hunts five hidden defects |
| 18 min | **Exercise 4: Burn your code** | All code deleted; Gemini rebuilds the geofence library in any language until every scenario is GREEN |
| 6 min | **Wrap-up** | Take-aways, going further: full five-phase cycle, milestones 2–4 up to Google Cloud Run |

Longer formats (120–180 min) add the bonus step honesty audit (§13) and the full five-phase cycle; milestones 2–4 run as instructor demo or hands-on with a GCP project.

