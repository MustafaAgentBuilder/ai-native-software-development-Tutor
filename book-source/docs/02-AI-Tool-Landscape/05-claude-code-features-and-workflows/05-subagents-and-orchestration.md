---
sidebar_position: 5
title: "Subagents and Orchestration"
duration: "6-8 min"
---

# Subagents and Orchestration

You've installed Claude Code and tried basic commands. Now let's understand **subagents**—specialized AI assistants that help Claude Code handle complex tasks more effectively.

---

## The Problem: Context Clutter

Imagine you're working on a startup idea. You ask Claude Code to:
1. Research competitors in the market
2. Explain business model options
3. Find relevant industry reports
4. Draft a pitch deck outline

By request #4, Claude Code's conversation context is cluttered with research notes, explanations, and report summaries. The context is messy.

**Solution**: Instead of one AI trying to do everything, **specialized assistants (subagents)** handle focused tasks with clean, isolated context.

---

## What Are Subagents?

**Definition**: A subagent is a specialized AI assistant with its own instructions and isolated context window. Each subagent is an expert at one type of task.

Think of Claude Code as a project manager with a team of specialists:
- **Claude Code (main)**: Coordinates overall work
- **Plan subagent**: Researches your codebase and creates multi-step plans
- **Custom subagents**: You can create specialists for your team's specific needs (content planning, research synthesis, document structuring, etc.)

**Key benefit**: Each subagent has **clean context** (no clutter from other conversations) and **focused expertise** (specialized instructions for its task).

---

## The Plan Subagent (Built-In)

Claude Code includes a **Plan subagent** that automatically activates for complex, multi-step tasks.

### When Plan Activates

When you ask for complex work, Claude Code delegates to the Plan subagent:

**You ask**: "Add user authentication to this project"

**Plan subagent does**:
1. **Researches your codebase** to understand current structure
2. **Creates a multi-phase plan**:
   - Phase 1: Database schema (users table, sessions)
   - Phase 2: Auth logic (password hashing, login/logout)
   - Phase 3: Integration (middleware, protect routes)
   - Phase 4: Testing (unit tests, flow validation)
3. **Presents plan for your approval** before any changes

### Why This Matters

**Without Plan subagent**: Claude might jump straight to code without understanding your project structure, missing dependencies or creating conflicts.

**With Plan subagent**: Research happens first, then a strategic plan, then execution—step by step.

---

## How Subagents Work

### The Execution Model: One Task, One Completion

**Critical concept**: A subagent is invoked **once** for a specific goal, completes its work, and **returns results to main Claude Code**.

**The flow**:
1. Main Claude Code recognizes a task that needs a specialist
2. Launches the subagent with a specific goal
3. Subagent works independently in isolated context
4. Subagent completes its task and returns results
5. **Control returns to main Claude Code**
6. You interact with main Claude Code to proceed

**Think of it like this**: You send a specialist to research something. They go off, do their work, come back with a report, and then you continue the conversation with your main assistant.

### Automatic Delegation

You don't command "use the Plan subagent." Claude Code decides when to delegate based on:
- Task complexity (multi-step tasks trigger Plan)
- Your request type (code review request might trigger a review subagent if you have one)
- Subagent descriptions (Claude matches task to specialist)

**Example**:
```
You: "Help me create a content marketing strategy for my startup"
Claude Code: *recognizes complexity, delegates to Plan subagent*
Plan subagent: *researches market, creates phase breakdown, returns plan*
Claude Code: *receives plan, presents it to you*
You: *approve or modify the plan*
Claude Code: *proceeds with execution*
```

### Explicit Invocation

You can also request a specific subagent directly:

```
You: "Use the startup-planner subagent to analyze my business model"
Claude Code: *invokes startup-planner, waits for results, presents findings*
```

---

## More Subagent Ideas

Now that you've created your first subagent, here are other ideas you can try:

**Blog Writer Subagent**:
```
Help me write engaging blog posts: research topics, create outlines,
suggest headlines, and draft compelling introductions.
Use when I say "help me write a blog post" or "draft article about X."
```

**Learning Guide Subagent**:
```
Create structured learning plans for any topic: break down concepts,
suggest resources, design practice exercises, and track progress.
Use when I say "help me learn X" or "create study plan for Y."
```

**Meeting Notes Organizer Subagent**:
```
Transform messy meeting notes into structured summaries: identify action items,
extract key decisions, organize by topic, and create follow-up tasks.
Use when I say "organize these meeting notes" or "summarize this discussion."
```

**Try creating one of these** using the same `/agents` workflow you just learned!

---

## Understanding Orchestration

**Orchestration** = AI coordinating multiple specialists toward a goal

When you ask for a complex task:
1. **Claude Code (orchestrator)** analyzes your request
2. **Launches a specialist subagent** (e.g., Plan subagent) for a specific goal
3. **Subagent completes its task** (researches, creates strategy) and **returns results**
4. **Control returns to main Claude Code**, which presents the results to you
5. **You approve/modify** the strategy
6. **Main Claude Code executes** step-by-step with your oversight

**Key insight**: Subagents don't stick around. They're invoked for one task, complete it, return results, and hand control back to main Claude Code.

**This is orchestration in action**: One AI managing a team of specialist AIs to accomplish complex work—each specialist does their job and returns the baton.

---

## Hands-On: Create Your First Custom Subagent

Creating a subagent is **easy**—Claude Code has a built-in workflow. Let's create a simple startup planning subagent together.

### Step 1: Launch the Agent Creation Workflow

In Claude Code, type:

```
/agents
```

**What you'll see**:
```
│ Agents                                                                        │
│ 9 agents                                                                      │
│                                                                               │
│ ❯ Create new agent                                                            │
│                                                                               │
│   Built-in agents (always available)                                         │
│   general-purpose · sonnet                                                   │
│   Explore · haiku                                                            │
│   Plan · sonnet                                                              │
```

Select **"Create new agent"**

### Step 2: Choose Location

```
│ Choose location                                                               │
│                                                                               │
│ ❯ 1. Project (.claude/agents/)                                                │
│   2. Personal (~/.claude/agents/)                                             │
```

**Choose 1** (Project) — this makes the agent available only in this project.

### Step 3: Choose Creation Method

```
│ Creation method                                                               │
│                                                                               │
│ ❯ 1. Generate with Claude (recommended)                                       │
│   2. Manual configuration                                                     │
```

**Choose 1** — Let Claude generate the agent based on your description.

### Step 4: Describe Your Agent

```
│ Describe what this agent should do and when it should be used                │
│                                                                               │
│ e.g., Help me plan a content marketing strategy...                           │
```

**Type this**:
```
Help me plan startup ideas: research competitors, analyze business models,
identify market gaps, and suggest go-to-market strategies.
Use this when I ask "help me plan a startup" or "analyze this business idea."
```

Press **Enter**.

### Step 5: Claude Generates the Agent

```
│ ✽  Generating agent from description...                                      │
```

Claude Code creates:
- Agent name: `startup-planner`
- Instructions based on your description
- Tool permissions (WebSearch, Read)
- Saves to `.claude/agents/startup-planner.md`

### Step 6: Test Your New Subagent

Now test it! In Claude Code, say:

```
Use the startup-planner subagent to analyze this business idea:
"A platform that connects freelance writers with small businesses"
```

**What happens**:
1. Main Claude Code launches your `startup-planner` subagent
2. Subagent researches competitors, analyzes the market
3. Subagent completes its analysis and returns findings
4. Control returns to main Claude Code
5. Main Claude presents the business plan to you

**Key insight**: You just created a reusable specialist that you can invoke anytime with a simple request.

### What You Just Learned

- ✅ Creating subagents is **easy** (4 steps via `/agents`)
- ✅ Claude generates the agent from your plain-language description
- ✅ Subagents are stored as Markdown files (`.claude/agents/`)
- ✅ You can invoke them explicitly: "Use the [name] subagent to..."
- ✅ Subagents complete one task and return results to main Claude Code

---

## Where Subagents Live

Subagents are stored as Markdown files with YAML frontmatter:

**Project-level**: `.claude/agents/` (specific to this project)
**User-level**: `~/.claude/agents/` (available across all your projects)

**Example subagent file structure**:
```markdown
---
name: startup-planner
description: Analyzes business ideas and creates go-to-market strategies
model: sonnet
color: purple
---

# Startup Planning Instructions

When analyzing a business idea:
1. Research competitors and market size
2. Identify unique value propositions
3. Suggest business model options
4. Create go-to-market strategy
...
```

---

## What You Can Do Now

**YOU JUST LEARNED**:
- ✅ What subagents are (specialized AI assistants)
- ✅ How the execution model works (one task, one completion)
- ✅ How to use the built-in Plan subagent (automatic)
- ✅ How to create your first custom subagent (via `/agents`)
- ✅ How to invoke subagents explicitly
- ✅ Where subagents are stored (`.claude/agents/`)

**PRACTICE NOW**:
- Create 2-3 custom subagents for your workflow
- Try the Test Generator, Documentation Writer, or Bug Hunter examples
- Invoke them explicitly: "Use the [name] subagent to..."

---

## Try With AI

Open Claude Code and complete these hands-on exercises:

### Exercise 1: Create Your Own Subagent

Follow the hands-on steps from earlier in this lesson:

1. Type `/agents`
2. Choose "Create new agent"
3. Choose "Project" location
4. Choose "Generate with Claude"
5. Describe what it should do (try Blog Writer, Learning Guide, or Meeting Notes Organizer)
6. Test your new subagent by invoking it explicitly

**Expected outcome**: You'll have a working custom subagent stored in `.claude/agents/` that you can invoke anytime.

### Exercise 2: Trigger the Plan Subagent

```
I want to create a 6-month content marketing plan for my startup.
Create a strategy showing the phases and what each phase includes.
```

**Expected outcome**: Plan subagent researches content strategies, then presents a multi-phase breakdown (audience research → content pillars → production schedule → distribution). Observe the subagent working, then returning control to main Claude Code.

### Exercise 3: Test Your Custom Subagent

If you created a startup-planner subagent in Exercise 1:

```
Use the startup-planner subagent to analyze this business idea:
"A mobile app that helps people find and book local fitness classes"
```

**Expected outcome**: Your custom subagent launches, researches the market, returns findings to main Claude Code, which presents them to you. You'll see the one-task, one-completion pattern in action.