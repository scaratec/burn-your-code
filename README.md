# Burn Your Code: Feature Files as the Ultimate AI Agent Prompt

This repository contains the structure and content for a presentation on the radical shift in software development: **AI-Driven Behavior-Driven Development (BDD)**.

## The Core Concept

In modern software engineering, the implementation (code) is becoming a commodity. However, as **"Vibe Coding"** (ad-hoc coding via chat) gains popularity, we face a critical challenge: teams often prompt an agent with a rough goal, get back plausible code, but retain little control over why it works and what is protected against regression.

This talk explores a workflow where human-written **Gherkin Feature Files** serve as the primary "Single Source of Truth" for business behavior and as a highly reliable prompt for AI agents. We address the **"Speed Paradox"**: showing how the strict structure of BDD, which once slowed humans down, now acts as a practical guardrail, enabling AI to deliver higher-quality code with better reproducibility.
It also emphasizes a non-delegable human responsibility: reviewing step implementations for test honesty, because a green suite is meaningless if the glue code smuggles business logic into the test.

## Repository Structure

- **/slides**: Contains 19 Markdown files, each representing a slide. They are numbered to maintain the logical flow of the presentation.
- **submission_data.md**: Contains the final title and abstracts (full and concise versions) for conference submissions.

## Presentation Flow

1.  **Introduction**: The new paradigm.
2.  **Single Source of Truth**: Feature files as the primary contract for business behavior.
3.  **Communication**: Bridging the gap to stakeholders.
4.  **The Experiment**: Exploring how much of the system can be recovered from the specification.
5.  **The Workflow**: AI-driven Red/Green cycle.
6.  **Vibe Coding vs. Engineering**: Contrasting reproducible specs with ad-hoc chat chaos.
7.  **Guardrails**: Preventing AI hallucinations.
8.  **Speed Paradox**: Why "slow" BDD is now the fastest way to build.
9.  **Language Agnosticism**: Technology choice as a minor detail.
10. **Forensic Engineering**: Reproducing bugs and validating real outcomes.
11. **Testing the Test**: Keeping glue code honest and behavior-focused.
12. **Test Honesty**: Human review as the final guardrail against cheating tests.
13. **Code as a Commodity**: Focusing on value, not syntax.
14. **Longevity**: Solving onboarding and legacy code issues.
15. **The Human Role**: The shift from coder to architect.
16. **Conclusion**: A more industrialized approach to software development.

## How to Use

The slides are designed to be concise. They provide a clear visual statement while allowing the speaker to talk freely about the underlying concepts and real-world project experiences (e.g., `papersink`, `trellio`, `ddns`).
