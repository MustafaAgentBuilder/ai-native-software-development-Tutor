<!-- Claude is Work to Build this Project -->
---
original_path: docs/02-AI-Tool-Landscape/05-claude-code-features-and-workflows/05-subagents-and-orchestration.md
chapter: 02-AI-Tool-Landscape
difficulty: intermediate
read_time: 6-8 min
generated: 2025-11-15
---

# Summary

Subagents solve the context clutter problem where complex multi-step tasks fill Claude Code's conversation context with research notes, explanations, and intermediate results, making later interactions messy and less focused. A subagent is a specialized AI assistant with its own instructions and isolated context window, functioning as an expert at one specific type of task. Claude Code acts as project manager coordinating specialized team members, with the built-in Plan subagent researching codebases and creating multi-step plans, plus support for custom subagents handling content planning, research synthesis, document structuring, or any domain-specific needs.

The execution model follows a critical one-task, one-completion pattern: main Claude Code recognizes a task needing specialist attention, launches the subagent with a specific goal, the subagent works independently in isolated context, completes its task and returns results, then control returns to main Claude Code for user interaction. Subagents don't persist across conversations—they're invoked once for focused work, complete their assignment, return findings, and hand control back. This orchestration enables main Claude Code to coordinate multiple specialists toward complex goals without cluttering its primary context.

The built-in Plan subagent automatically activates for complex multi-step tasks like "Add user authentication to this project," researching current codebase structure, creating phased plans (database schema, auth logic, integration, testing), and presenting strategies for approval before any code changes. This prevents jumping straight to code without understanding project structure, avoiding missed dependencies or conflicts through research-first strategic planning.

Creating custom subagents uses the simple `/agents` workflow: launch agent creation, choose project or personal location, select AI-generated configuration, describe what the agent should do and when to use it, then Claude generates the agent with appropriate name, instructions, tool permissions, and saves to `.claude/agents/`. Subagents are stored as Markdown files with YAML frontmatter and can be invoked explicitly ("Use the [name] subagent to...") or automatically when Claude recognizes matching task patterns. Example use cases include startup planning (competitor research, business model analysis), blog writing (topic research, outlines, headlines), learning guides (structured plans, resources, exercises), and meeting notes organization (action items, decisions, follow-ups).

## Key Concepts

- Context isolation benefit: Each subagent operates with clean, focused context preventing main conversation pollution from specialized tasks
- One-task execution model: Subagents complete single focused assignment, return results to main Claude, then control returns without persistence
- Automatic Plan subagent: Built-in specialist activates for complex requests, researches codebase, creates multi-phase strategies before execution
- Custom subagent creation: Simple `/agents` workflow with AI-generated configuration based on plain-language task descriptions
- Orchestration pattern: Main Claude coordinates specialist subagents like project manager directing team experts toward complex goals
