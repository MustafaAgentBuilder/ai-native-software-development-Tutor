---
sidebar_position: 3
title: "CLAUDE.md Context Files"
duration: "8-10 min"
---

# CLAUDE.md Context Files

## The Session Context Problem

Imagine this: You've been working with Claude Code on your Python project for weeks. Claude has learned your naming conventions, understood your project structure, and adapted to your coding style. You close the terminal for the evening.

The next morning, you open a new Claude Code session and type a question about your project. Claude responds with generic advice—treating your project like it's starting fresh. You have to re-explain your tech stack, your directory structure, your team's conventions.

**This is context friction.** And it's a productivity killer.

Every session starts with zero context. You either repeat explanations repeatedly, or Claude gives generic answers that don't match your project's reality.

**There's a better way.**

---

## What Is CLAUDE.md?

**CLAUDE.md is a simple markdown file placed in your project root that Claude Code automatically loads at the start of every session.** It contains the persistent context your AI companion needs—without you repeating it.

Think of it as a **persistent project brief** that travels with your code:

- Your project does X, Y, and Z
- You use Python 3.13 with FastAPI and PostgreSQL
- Files go in `src/`, tests in `tests/`, database migrations in `alembic/`
- You prefer type hints, Google-style docstrings, and error handling with custom exceptions
- Key commands to run: `uvicorn main:app --reload`, `pytest`, `alembic upgrade head`

When Claude Code starts a new session, it reads CLAUDE.md automatically. Claude **immediately understands your project** without you saying a word.

#### 💬 AI Colearning Prompt

> "Why is having persistent context in CLAUDE.md more efficient than repeating project details in every session?"

---

## How CLAUDE.md Auto-Loads

Here's the mechanism (you don't need to do anything—it's automatic):

1. **You create** `CLAUDE.md` in your project root (same directory as `package.json`, `pyproject.toml`, `go.mod`, or `.git`)
2. **You start** Claude Code in that directory: `claude`
3. **Claude Code detects** the CLAUDE.md file automatically
4. **Claude reads** the file and loads it into context
5. **Your session begins** with full project understanding—no setup required

Every new session repeats this process. CLAUDE.md is always loaded, always available.

**One-time setup. Automatic benefit forever.**

#### 🎓 Expert Insight

> In AI-driven development, context is gold. CLAUDE.md is the cheapest way to give Claude continuous project awareness. Write it once; benefit every session. This is specification-first thinking applied to AI companionship.

---

## What Goes Into CLAUDE.md

CLAUDE.md typically contains 6 sections. Use this structure as your template:

1. Project Overview: What does your project do? What problem does it solve?
2. Technology Stack: Languages, frameworks, databases, key dependencies.
3. Directory Structure: Show the layout so Claude understands where code lives.
4. Coding Conventions: Style, naming, patterns your team follows.
5. Key Commands: Common commands to run the project.
6. Important Notes: Gotchas, dependencies, security considerations.

---

## How to Create Your CLAUDE.md

You could type this all manually. Or—and this is the Claude Code way—**ask Claude to generate it for you.**

Here's the process:

### Step 1: Ask Claude Code to Generate CLAUDE.md

Start Claude Code in your project directory and ask:

```
claude "Help me create a CLAUDE.md file for this project.
What are the main sections I should include, and can you generate a template
based on what you see in the codebase?"
```

Claude will analyze your actual files and propose a CLAUDE.md structure based on your real project.

#### 🤝 Practice Exercise

> **Ask your AI**: "Create a CLAUDE.md for my [Python/Node/Go/etc] [project type] project. Include: Project Overview (2 sentences), Technology Stack (list), Directory Structure (tree), Coding Conventions (list), Key Commands (list), Important Notes (gotchas). Make it specific to what you see in the codebase."
>
> **Expected Outcome**: Claude generates a CLAUDE.md with all sections populated based on your actual project structure.

### Step 2: Review and Refine

Claude's output is a starting point. Read it carefully. Does it match your project? Are conventions accurate? If Claude guessed wrong or missed details, refine it.

### Step 3: Save the File

Save Claude's output as `CLAUDE.md` in your project root (same directory as `package.json`, `pyproject.toml`, etc.)

### Step 4: Verify Auto-Loading

Exit Claude Code (`exit` or close terminal). Open a new terminal session in the same directory:

```bash
claude
```

In the new session, ask Claude a question about your project:

```
"What's the tech stack for this project?"
```

**If Claude mentions your stack without you repeating it—CLAUDE.md loaded successfully.**

---

## Why This Matters: Context as Productivity

Here's what you've accomplished:

- ✅ **One-time creation**: 10-15 minutes to write CLAUDE.md
- ✅ **Automatic benefit**: Every session starts with full context
- ✅ **No friction**: No re-explaining project structure, conventions, or setup
- ✅ **Team alignment**: New team members read CLAUDE.md to understand the project

This is a **specification mindset** applied to AI companionship. You specify once; the AI benefits forever.

#### 💬 AI Colearning Prompt

> "How does having persistent context in CLAUDE.md improve the quality of Claude Code's suggestions compared to starting fresh each session?"

---

## Edge Cases and Troubleshooting

### CLAUDE.md Not Loading?

**Symptom**: You created CLAUDE.md, but Claude Code doesn't reference it in new sessions.

**Checklist**:
- ✅ File is named exactly `CLAUDE.md` (case-sensitive)
- ✅ File is in project root (same level as `.git`, `package.json`, etc.)
- ✅ You restarted Claude Code session (new terminal, not same session)
- ✅ File has content (not empty)

**Solution**: If all above are true, restart your terminal completely. Sometimes the session needs a fresh start.

### Unclear What Goes in CLAUDE.md?

**Symptom**: You're unsure whether something belongs in CLAUDE.md.

**Simple rule**: Ask yourself: *"Does Claude need to know this to give good suggestions?"*

- Claude needs to know your tech stack? **Yes, goes in CLAUDE.md.**
- Claude needs to know your file naming convention? **Yes.**
- Claude needs to know that your coffee machine is broken? **No.**

If Claude would ask "What's your tech stack?" without CLAUDE.md, then that information belongs in CLAUDE.md.

### Concerns About File Size?

**Symptom**: "Isn't CLAUDE.md taking up context space? Won't it fill up?"

**Reassurance**: A typical CLAUDE.md is 1-3 KB. Context is cheap; clarity is expensive.

A well-organized 2 KB CLAUDE.md saves you 10+ KB of repeated explanations every session. And it improves Claude's suggestions because the context is structured and accurate.

---

## Try With AI

Open Claude Code in your project directory and run these prompts to create your first CLAUDE.md:

**Prompt 1: Analyze Your Project**
```
Analyze the structure and technology of this project.
What are the main components, tech stack, and key directories?
```

**Expected Outcome**: Claude describes your project structure, identifying the primary language, frameworks, and file organization.

**Prompt 2: Generate CLAUDE.md**
```
Create a complete CLAUDE.md file with these sections:
- Project Overview (1-2 sentences)
- Technology Stack (bulleted list)
- Directory Structure (tree diagram)
- Coding Conventions (bulleted list)
- Key Commands (bulleted list for running, testing, deploying)
- Important Notes (any gotchas or critical context)

Base it on what you see in the codebase.
```

**Expected Outcome**: Claude generates a full CLAUDE.md ready to save to your project root.

**Prompt 3: Refine Based on Your Project**
```
Review the CLAUDE.md. Make these adjustments:
[Add your specific corrections, missing sections, or clarifications]
```

**Expected Outcome**: Claude refines CLAUDE.md based on your feedback, ensuring it's accurate and complete.

**Prompt 4 (Optional): Test Auto-Loading**
```
I've saved CLAUDE.md to my project root. I'm going to exit this session
and start a new one. In the next session, ask me about my project without
me re-explaining it. Ready?
```

*Exit Claude Code. Start a new session. Ask Claude a question about your project.*

**Expected Outcome**: Claude references your tech stack, structure, or conventions—proving CLAUDE.md auto-loaded.
