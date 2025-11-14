---
sidebar_position: 7
title: "Hooks and Extensibility"
duration: "5-7 min"
learning_objectives:
  - "Understand hooks as event-triggered automation"
  - "Create a simple SessionStart hook"
  - "Recognize common hook events (PreToolUse, PostToolUse, SessionStart, SessionEnd)"
  - "Test hooks in a real Claude Code session"
---

# Hooks and Extensibility

## The Problem: Repeating Setup Every Session

You're working on a project. Every time you start a new Claude Code session, you manually:
1. Explain the project structure
2. Remind Claude about your naming conventions
3. Load environment variables
4. Set up project context

By the third session today, you're frustrated. **Why can't Claude Code just do this automatically when a session starts?**

**That's what hooks solve.**

---

## What Are Hooks?

**Definition**: Hooks are automated scripts that run when specific events occur in Claude Code—like when a session starts, a file is edited, or a tool runs.

**Think of hooks as**: Event listeners that trigger actions automatically.

A hook has three parts:
1. **Event**: What triggers the hook (like "SessionStart")
2. **Condition** (optional): Which tools or files match
3. **Action**: What command runs automatically

**Key benefit**: Automate repetitive tasks so you focus on creative work, not setup.

#### 💬 AI Colearning Prompt
> "Explain what hooks are in Claude Code. Give 2-3 real-world examples where a hook would save time by automating a repetitive task."

---

## Hook Events: When Hooks Trigger

Claude Code recognizes four main event types that can trigger hooks:

### PreToolUse
Fires **before** Claude Code runs a command or tool.

**Example use case**: Validation hook that checks requirements before running a build script.

### PostToolUse
Fires **after** Claude Code completes a command or tool.

**Example use case**: Format code immediately after edit, or run tests after saving.

### SessionStart
Fires **when you open a Claude Code session**.

**Example use case**: Load environment variables, initialize project context, or run startup checks.

### SessionEnd
Fires **when you close a Claude Code session**.

**Example use case**: Cleanup tasks, save session logs, or sync project state.

#### 🎓 Expert Insight
> In AI-driven development, hooks automate the routine follow-ups that developers used to do manually. Your value isn't in running `npm test` after every edit—it's in understanding WHEN testing matters and what the results tell you about your design.

---

## Real-World Hook Examples

Here are three practical scenarios showing hooks in action:

| **Scenario** | **Hook Type** | **Event Trigger** | **Action** | **Benefit** |
|---|---|---|---|---|
| **Code Formatting** | PostToolUse | After Claude edits a `.py` file | Run `black --line-length 88 file.py` | Consistent code style without manual intervention |
| **Test Validation** | PostToolUse | After any changes to `src/` directory | Run `pytest` and report results | Catch bugs immediately instead of later |
| **Environment Setup** | SessionStart | When new Claude Code session opens | Load variables from `.env` and run `source setup.sh` | Project context always ready without manual setup |

Each hook saves time by automating what you would otherwise do manually after specific events.

---

## Why Hooks Matter for Professional Workflows

Imagine you're part of a development team. Without hooks:
- After every edit, someone manually runs formatters: **repetitive, error-prone**
- Tests run on a schedule instead of immediately: **bugs discovered late**
- Setup requires manual steps: **onboarding takes longer**

With hooks:
- Code automatically formatted **immediately after edit**
- Tests run **automatically whenever code changes**
- Project environment **auto-loads on session start**

Hooks are about **automating the predictable parts of your workflow** so you focus on the strategic thinking—the parts only humans can do.

#### 🤝 Practice Exercise

> **Think of a repetitive task** you've done recently (running tests, formatting code, deploying, checking linting). **Ask your AI**: "In Claude Code, how would a hook help automate this repetitive task? What event would trigger it?"

**Expected Outcome**: You'll understand how hooks map to your real workflows and why automation matters for productivity.

---

## Hands-On: Create Your First Hook

Let's create a simple SessionStart hook that displays a welcome message when you open Claude Code.

### Step 1: Create Settings File

Hooks are configured in `.claude/settings.json`. Create this file in your project:

```bash
mkdir -p .claude
touch .claude/settings.json
```

### Step 2: Add a SessionStart Hook

Edit `.claude/settings.json` and add:

```json
{
  "hooks": [
    {
      "event": "SessionStart",
      "type": "command",
      "command": "echo 'Welcome to your project! Claude Code session started.'"
    }
  ]
}
```

**What this does**:
- **event**: Triggers when session starts
- **type**: "command" means run a bash command
- **command**: The actual command to run (echo a welcome message)

### Step 3: Test Your Hook

Close and restart Claude Code in this project:

```bash
exit  # if already in a session
claude
```

**What you should see**:
```
Welcome to your project! Claude Code session started.
```

The hook ran automatically when the session started!

### Step 4: Make It More Useful

Update `.claude/settings.json` to show project info:

```json
{
  "hooks": [
    {
      "event": "SessionStart",
      "type": "command",
      "command": "echo 'Project: $(basename $(pwd)) | Files: $(ls -1 | wc -l) | Last modified: $(ls -lt | head -2 | tail -1 | awk \"{print \\$6, \\$7, \\$8}\")'"
    }
  ]
}
```

Restart Claude Code:

```bash
exit
claude
```

**Now you see**:
```
Project: my-project | Files: 15 | Last modified: Nov 14 10:23
```

Useful project context **automatically** every session!

---

## Common Questions About Hooks

### "Aren't hooks the same as Skills or Plugins?"

No—each serves a different purpose:

- **Hooks**: Automate Claude Code's behavior in response to events (like "format code after edit")
- **Skills**: Extend Claude's knowledge and capabilities with new functions or custom commands (like "extract PDF forms")
- **MCP**: Connect external tools to Claude Code (like "access GitHub repositories")
- **Plugins**: Bundle all of the above together as complete customizations (marketplace packages)

Think of it this way: Skills and MCP add **new capabilities**. Hooks add **automation**. They're complementary, not overlapping.

### "Will I encounter hook errors?"

Possibly, but they're usually non-blocking. If a hook fails:
- Claude Code continues working (hook errors don't stop your session)
- The error is logged, not shown as a blocker
- You can investigate later

Debugging hooks is advanced content (Part 5). For now, just know hook errors won't stop you from working.

### "Should I enable hooks right now?"

Not necessary. Claude Code works perfectly fine without custom hooks. You can:
- Use Claude Code productively without any hooks
- Learn about hooks conceptually now
- Build hooks later when you're ready to optimize your workflow

**No pressure to customize right now—focus on mastering basic workflows first.**

---

## Try With AI

Open Claude Code and explore hooks conceptually with your AI companion.

### Prompt 1: Understand Hooks

```
claude "Explain hooks in Claude Code. Give 2-3 useful examples where a hook would save time by automating a repetitive task."
```

**Expected outcome**: AI explains hooks as event-triggered automation and provides concrete examples (format code, run tests, load environment).

### Prompt 2: Identify Opportunities

Think of a task you do repeatedly in your projects (running tests, formatting code, checking linting, deploying, loading configuration).

```
claude "I frequently [describe your repetitive task]. Could a Claude Code hook help automate this? If so, what would it do?"
```

**Expected outcome**: AI identifies how a hook could eliminate the repetitive step, discusses which event would trigger it, and explains the time savings.

### Prompt 3: Future Learning Path

```
claude "Can I build custom hooks in Claude Code? How hard is it? When would I learn this? What are the prerequisites?"
```

**Expected outcome**: AI clarifies that hook building is intermediate-to-advanced content, explains prerequisites (Part 5), and positions hooks in the larger Claude Code customization landscape.
