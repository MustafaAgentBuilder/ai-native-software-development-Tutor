<!-- Claude is Work to Build this Project -->
---
original_path: 01-Introducing-AI-Driven-Development/03-billion-dollar-ai/04-vertical-intelligence.md
chapter: 01-Introducing-AI-Driven-Development
difficulty: intermediate
read_time: 2.5 minutes
generated: 2025-11-15
---

# Summary

The paradigm shift from code reuse to intelligence reuse fundamentally changes software architecture. Traditional DRY (Don't Repeat Yourself) principles emphasized writing code once and reusing everywhere, requiring heavy upfront investment in reusable libraries. In the AI era, code becomes disposable—AI agents generate 10,000 lines of specialized code in seconds, making code maintenance across applications more expensive than generating fresh code per application. The new principle: reuse intelligence, not code.

A reusable subagent comprises five components arranged from generic to domain-specific: (1) System Prompt defining persona, knowledge, and constraints (e.g., "You are a senior portfolio manager with 20 years equity experience"), (2) Horizontal Skills covering infrastructure (Docker, Kubernetes, cloud APIs, authentication), (3) Vertical Skills containing domain expertise (Bloomberg API knowledge, portfolio models, FHIR standards, ICD-10 codes), (4) MCP Horizontal Connections to generic tools (GitHub, Docker registries, CI/CD pipelines), and (5) MCP Vertical Connections to industry APIs (Bloomberg, Epic Systems, PubMed)—the defensible moat.

The five components create different value sources than traditional code reuse. Traditional libraries were long-lived (used for years), centrally maintained (one library, many users), and limited in scalability (updates risked breaking changes). Intelligence reuse uses disposable code (regenerated per application), distributed maintenance (each application owns its copy), unlimited scalability (new apps get fresh code), and derives value from domain expertise and integrations rather than code logic.

A concrete example: traditional accounting libraries maintain Chart of Accounts, General Ledger, and Tax reporting across five products, updating once when tax code changes but supporting every feature of every app (complex). AI-driven accounting subagents define expert accountant personas, maintain updated tax knowledge via MCP, integrate with QuickBooks/Xero/Freshbooks/Wave, and encode GAAP standards—generating tailored code per customer while reusing intelligence permanently.

## Key Concepts

- Code is disposable when AI generates quickly; intelligence (prompts, skills, integrations) is permanent
- Five reusable subagent components: system prompt, horizontal skills, vertical skills, horizontal MCPs, vertical MCPs
- Vertical MCP connections (industry API integrations) create defensibility competitors must rebuild
- Traditional code reuse (long-lived, centralized) vs. intelligence reuse (disposable, distributed, unlimited scalability)
- Domain expertise and integrations replace code logic as primary value source
