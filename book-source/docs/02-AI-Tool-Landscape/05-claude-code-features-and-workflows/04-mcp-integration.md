---
sidebar_position: 4
title: "MCP Integration"
duration: "12-15 min"
---

# MCP Integration: Connecting to External Systems

## The Problem: Claude Code's Limitation

Right now, Claude Code can only see **files on your computer**.

But what if you need Claude to:
- Browse a website to find information?
- Check the latest documentation for a library?
- Query a database?
- Access an API?

All of that lives **outside your computer**. Claude Code can't reach it... yet.

**Model Context Protocol (MCP)** solves this problem. It's like giving Claude Code safe, approved access to the outside world.

---

## Think of MCP Like This

Imagine Claude Code is a brilliant assistant who works in your office (your computer).

**Without MCP**: Your assistant can only use what's in the office—files on your desk, folders in your cabinet. That's it.

**With MCP**: You give your assistant a **phone directory** with approved contacts—a web browser expert, a documentation specialist, a database consultant. Now when your assistant needs outside information, they can call the right expert and get answers safely.

**MCP is that phone directory.** It connects Claude Code (your AI agent) to external tools and data sources in a **standardized, safe way**.

---

## What Is Model Context Protocol (MCP)?

**Simple definition**: MCP lets Claude Code safely use external tools through standardized connections.

**An "MCP server"** is a helper tool Claude can call:
- **Playwright MCP**: Lets Claude browse websites
- **Context7 MCP**: Lets Claude fetch up-to-date documentation
- **GitHub MCP**: Lets Claude query GitHub repositories
- **Database MCP**: Lets Claude query databases

Think of each MCP server as a **specialist** Claude Code can consult when needed.

---

## In This Lesson

You will:
1. Add two beginner-friendly MCP servers to Claude Code
2. Try real workflows: browse Amazon, fetch docs
3. Understand when you need external access

No programming experience required. Just copy, paste, and see it work.

## A Note on Security (Read This First)

**Why security matters with MCP**: Unlike working with local files, MCP servers can access the internet, APIs, and external systems. This is powerful but requires trust.

**Stay safe**:
- Use trusted MCP servers. In this lesson we'll use two widely used, reputable servers: Playwright MCP and Context7 MCP.
- Your tokens and secrets are stored in your system keychain (not plain text).
- Never paste secrets into files; use prompts when Claude asks or environment variables.

---

## Hands-On: Add Two Helpful MCP Servers

We'll add two servers using simple commands.

```bash
# 1) Playwright MCP (browse the web)
claude mcp add --transport stdio playwright npx @playwright/mcp@latest

# 2) Context7 MCP (get up-to-date docs)
claude mcp add --transport stdio context7 npx @upstash/context7-mcp
```

**What's happening**: You're telling Claude Code about two external helpers it can use. Each command registers an MCP server that Claude can invoke when relevant.

---

## Workflow 1: Shop Together — Find a Shirt on Amazon (Playwright MCP)

Goal: Ask Claude to browse Amazon and find a shirt that matches your preferences. No code—just a plain request.

In Claude Code, say:

```
Use the Playwright MCP to browse Amazon. Find 3 men's casual shirts under $30 with good reviews. Share links, prices, main features, and any sizing notes. Prefer neutral colors.
```

What happens:
- Claude launches the Playwright MCP to visit Amazon
- It navigates pages, extracts details, and returns a neat summary with links
- You can iterate naturally: "filter to long-sleeve" or "show only Prime-eligible"

If you get an error:
- Ensure `playwright` MCP is registered: `claude mcp list`
- Try again; websites change often, so Claude may adjust its browsing steps
- Verify your internet connection is stable

---

## Workflow 2: Learn What's New — Ask for MCP Docs (Context7 MCP)

Goal: Ask Claude to use Context7 to fetch and summarize the latest resources about MCP in Claude Code.

In Claude Code, say:

```
Use the Context7 MCP to fetch the latest official documentation and articles about MCP support in Claude Code. Summarize what MCP is, how to add a server, and any recent changes or best practices. Include links and short quotes for key points.
```

What happens:
- Claude queries Context7's knowledge sources for up-to-date docs
- You get a short, current summary with citations and links
- Ask follow-ups: "show the exact CLI command to add a server via stdio" or "compare Context7 MCP vs GitHub MCP"

**Tip**: This is your "know about anything new" button. Use it anytime you need the latest docs without hunting across websites.

---

## What You Just Learned

**MCP unlocks external access**: You've given Claude Code the ability to reach beyond your local files to browse websites, fetch documentation, and access external systems.

**Two MCP servers installed**:
- **Playwright MCP**: Browse and extract information from websites
- **Context7 MCP**: Fetch up-to-date library and API documentation

**When to use MCP**: Anytime you need information or capabilities that live outside your computer.

### Reflection Questions

**Understanding**:
- In your own words, what problem does MCP solve?
- Why is security important when using MCP servers?

**Application**:
- What websites or information sources would be most useful for YOUR projects?
- How could Context7 help you stay current with fast-changing tools and libraries?

**Next Steps**:
- What other MCP servers might you explore? (Database access? GitHub integration? Slack notifications?)
- When would you reach for MCP vs. asking Claude Code about local files?

---

## Try With AI

Use Claude Code for this activity (preferred, since you just installed it). If you already have another AI companion tool set up (e.g., ChatGPT web, Gemini CLI), you may use that instead—the prompts are the same.

### Prompt 1: MCP Troubleshooting

```
I'm trying to add an MCP server to Claude Code and it's not working.
I ran [paste your command].
The error says [paste error message].
Walk me through troubleshooting:
(a) What's the most likely cause?
(b) What should I check?
(c) Give me 3 diagnostic commands to run.
(d) If those fail, what's plan B?
```

**Expected outcome**: Troubleshooting guidance for MCP connection issues with specific diagnostic steps.

### Prompt 2: Safe Testing Workflows

```
I successfully added Playwright MCP and Context7 MCP. Now I want to test them safely.
Create 3 'Hello World' workflows for me:
(a) One using Playwright to browse a safe website like Wikipedia,
(b) One using Context7 to fetch docs for [my library/framework],
(c) One combining BOTH MCPs in a single workflow.
Include the exact prompts I should give Claude Code.
```

**Expected outcome**: Safe, tested workflows you can run immediately with exact prompts.

### Prompt 3: Security Boundaries

```
The lesson emphasizes MCP security concerns. I'm nervous about external access.
Help me establish safe boundaries:
(a) What types of MCP servers should I AVOID as a beginner?
(b) What permissions are risky?
(c) How do I audit what an MCP server can access?
(d) Create a 'MCP safety checklist' I can follow for any new MCP.
```

**Expected outcome**: Security boundaries and audit procedures you can apply to any MCP server.

### Prompt 4: Design Your Own MCP Workflow

```
I want to use MCP servers to help with: [describe your goal: research a technology / stay current with docs / gather information from websites].

Design a workflow for me:
(a) Which MCP server(s) should I use? (Playwright for browsing? Context7 for docs? Other?)
(b) What exact prompts should I give Claude Code?
(c) How do I verify the MCP server is working correctly?
(d) What could go wrong, and how do I troubleshoot it?

Show me step-by-step with copyable prompts.
```

**Expected outcome**: Complete MCP workflow design customized to your actual needs with concrete, actionable steps.
