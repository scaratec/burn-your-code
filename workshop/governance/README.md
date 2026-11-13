# EquiGuard Governance: ADR + LIM + BDD Specification Triad

This directory holds the architectural decisions and bounded limitations for **EquiGuard**, forming the specification triad alongside [`../bdd/`](../bdd/):

| Register | Path | Question Answered |
|---|---|---|
| **ADRs** | [`adr/`](adr/) | *Why is the system built this way?* |
| **LIMs** | [`limitations/`](limitations/) | *Where do we knowingly fall short in V1?* |
| **Feature Files** | [`../bdd/`](../bdd/) | *What does the system do (observably)?* |

All three registers are written in Markdown and Gherkin so that:
1. An independent **Specification Critic (`bdd-critic`)** can audit them together as a single consistent specification *before* any step code or application code is written ([BDD Guidelines v1.9.0 §14](../../BDD_GUIDELINES_v1.9.0_EN.md)).
2. An AI coding agent (**Gemini** via **Antigravity CLI**) can implement the entire service autonomously in *any* programming language without re-litigating architectural choices or "fixing" intentional V1 deferrals.
