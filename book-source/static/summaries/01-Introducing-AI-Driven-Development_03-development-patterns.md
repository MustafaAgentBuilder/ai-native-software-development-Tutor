<!-- Claude is Work to Build this Project -->
---
original_path: docs/01-Introducing-AI-Driven-Development/02-ai-turning-point/03-development-patterns.md
chapter: 01 - Introducing AI-Driven Development
difficulty: intermediate
read_time: 25
generated: 2025-11-15
---

# Summary

This lesson distinguishes two fundamental development approaches—vibe coding (intuition-led) and spec-driven development (specification-led)—and explains when each works and why discipline matters more with AI tools. Vibe coding excels for learning (immediate feedback), exploration and discovery (faster than rigid planning), low-stakes solo work (affordable rework), and creative flow states. However, it has predictable failure modes when stakes increase: ambiguous requirements create team misalignment, missing tests skip edge cases that break in production, and architecture drift makes code resist extensibility as features accumulate.

Spec-Driven Development (SDD) inverts the order with a 7-step workflow: Specify (clear requirements and edge cases), Plan (break into implementable tasks), Tasks (concrete acceptance criteria), Implement with Red-Green TDD (write failing tests, then code to pass), Refactor (clean up while keeping tests passing), Explain (document decisions and trade-offs), and Record/Share (capture ADRs and create PRs with context). The concrete comparison shows Team A (vibe coding) shipping in 10 hours but requiring 24 hours of rework when requirements change (34 total), versus Team B (spec-driven) investing 10 hours upfront and adding extensions in 2 hours with no rework (12 total)—sustainable velocity through planning.

The lesson emphasizes that vibe coding and SDD are both powerful for different contexts: learning new technology favors vibe coding, shipping to production requires SDD; solo low-stakes projects fit vibe coding, team features need SDD; exploration works best with vibe coding, extended maintenance benefits from specifications. The critical insight is that AI amplifies whatever practice you bring—vibe coding with AI ships fast but encounters staging surprises with AI-generated code no one understands, while SDD with AI becomes a force multiplier where AI helps write clear specs, generate tests from specs, and implement against those tests.

The constitutional principle emerges: "Specs are the new syntax." In traditional programming, value came from typing correct syntax fast. In AI-native development, value comes from articulating intent clearly so AI can execute flawlessly. Specification quality directly determines output quality, making the 7-step SDD workflow essential training for systematic thinking before typing and validation before shipping—the foundation of AI-native development.

## Key Concepts

- Vibe coding strengths: learning, exploration, low-stakes solo work, creative flow—but predictable failures at scale (ambiguity, missing tests, architecture drift)
- Spec-Driven Development 7-step workflow: Specify → Plan → Tasks → Red-Green Implement → Refactor → Explain → Record/Share (integrating TDD and knowledge capture)
- Real cost comparison: vibe coding 34 hours (10 initial + 24 rework) versus spec-driven 12 hours (10 upfront + 2 extension) for sustainable velocity
- AI as amplifier: magnifies both good practices (specs, tests, discipline) and bad practices (speed without quality, ambiguous requirements, missing edge cases)
- Constitutional principle: "Specs are the new syntax"—specification writing IS the primary AI-era skill, replacing syntax-typing as core developer value
