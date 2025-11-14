---
sidebar_position: 9
title: "Discovering and Using Claude Code Plugins"
duration: "10-12 min"
learning_objectives:
  - "Understand plugins as bundled capabilities (skills + agents + hooks + MCP)"
  - "Discover available plugins through marketplaces"
  - "Install and use pre-built plugins from Anthropic's skills repository"
  - "Recognize when a plugin solves your workflow needs"
---

# Discovering and Using Claude Code Plugins

## The Problem: Reinventing the Wheel

You've learned to create skills, use subagents, and connect MCP servers. But what if someone has already built exactly what you need?

**Scenario**: You want Claude to help with:
- Creating visual designs (canvas art, diagrams)
- Building web apps with React components
- Testing web applications automatically
- Following your company's brand guidelines

**Question**: Should you build these capabilities from scratch, or use what already exists?

**Answer**: Use existing plugins from marketplaces.

---

## What Are Plugins?

**Definition**: A plugin is a **bundled package** that can include:

1. **Skills** (autonomous capabilities Claude discovers)
2. **Subagents** (specialized AI assistants)
3. **Hooks** (event-driven automation)
4. **Commands** (slash commands like `/design`)
5. **MCP configuration** (external integrations)

**Think of plugins as**: Pre-built toolkits that extend Claude's capabilities in specific domains (design, testing, development, enterprise workflows).

**Key insight**: You don't need to build everything yourself. Marketplaces provide ready-to-use plugins created by Anthropic and the community.

---

## Discovering Plugins: Anthropic's Skills Marketplace

The easiest way to extend Claude Code is using **Anthropic's official skills repository**—a curated collection of pre-built capabilities.

### What's Available in the Skills Repository?

The Anthropic skills marketplace provides **two main plugin bundles**:

**1. example-skills** - Creative and Development Capabilities:
- Algorithmic art using p5.js with particle systems
- Visual design (canvas art, diagrams)
- Web application testing via Playwright
- HTML artifacts using React and Tailwind CSS
- Slack GIF creation
- Internal communications (reports, newsletters, FAQs)
- Brand guidelines application
- Theme styling
- Skill creator guide
- MCP server building guide

**2. document-skills** - Document Processing Suite:
- Word documents (.docx)
- PDFs (.pdf)
- PowerPoint presentations (.pptx)
- Excel spreadsheets (.xlsx)
- Advanced file manipulation capabilities

### How to Add the Skills Marketplace

In Claude Code, run:

```bash
/plugin marketplace add anthropics/skills
```

**What happens**:
1. Claude Code connects to https://github.com/anthropics/skills
2. Downloads the marketplace configuration
3. Marketplace appears as **"anthropic-agent-skills"** in your plugin list

### Browse Available Plugins

After adding the marketplace:

```bash
/plugin
```

**What you'll see**: Interactive menu with options:
1. Browse and install plugins
2. Manage and uninstall plugins
3. Add marketplace
4. Manage marketplaces

Select **"Browse and install plugins"** → **"anthropic-agent-skills"**

**You'll see the two plugin bundles**:
- ◯ document-skills (Word, PDF, Excel, PowerPoint processing)
- ◯ example-skills (Creative, development, enterprise tools)

### Install a Plugin Bundle

**Option 1: Via UI** (Recommended):
1. Run `/plugin`
2. Select "Browse and install plugins"
3. Choose "anthropic-agent-skills"
4. Select `example-skills` or `document-skills`
5. Review what will be installed
6. Click "Install now"

**Option 2: Via Command**:
```bash
/plugin install example-skills@anthropic-agent-skills
```

Or for document processing:
```bash
/plugin install document-skills@anthropic-agent-skills
```

**What happens**:
1. Claude Code downloads all skills in the bundle
2. Installs them to `.claude/skills/` directory
3. All skills become available for Claude to use automatically

### Test Your Installed Skills

After installing `example-skills`, try:

```
Help me create a visual diagram showing how plugins, skills,
subagents, and MCP servers work together in Claude Code
```

**What happens**:
- Claude recognizes "visual diagram" trigger from the canvas-design skill
- Loads the skill's instructions automatically
- Creates visual output using the skill's capabilities

---

## Plugin Marketplaces: Beyond Anthropic

### Adding Custom Marketplaces

You can add marketplaces from:

**GitHub repositories**:
```bash
/plugin marketplace add owner/repo
```

**GitLab or other git services**:
```bash
/plugin marketplace add https://gitlab.com/company/plugins.git
```

**Local paths** (for development):
```bash
/plugin marketplace add ./my-marketplace
```

**Direct URLs**:
```bash
/plugin marketplace add https://url.of/marketplace.json
```

### List Installed Marketplaces

```bash
/plugin marketplace list
```

**What you'll see**:
- All marketplaces you've added
- Source URLs
- Number of plugins available from each

---

## When to Use Existing Plugins vs. Create Custom

**Use existing plugins when**:
- Someone has already built what you need (check marketplaces first!)
- You need standard capabilities (design, testing, document processing)
- You want to follow established patterns (Anthropic's skills are well-designed)

**Create custom skills/agents when**:
- Your workflow is unique to your team/project
- No existing plugin matches your needs
- You're building company-specific capabilities (brand guidelines, internal processes)

**Bottom line**: Don't reinvent the wheel. Check marketplaces first, customize later if needed.

---

## Hands-On: Set Up the Anthropic Skills Marketplace

Let's actually add the marketplace and install a plugin bundle.

### Step 1: Start Claude Code

In your terminal:

```bash
claude
```

### Step 2: Add the Anthropic Skills Marketplace

In the Claude Code session, type:

```
/plugin marketplace add anthropics/skills
```

**Expected output**:
```
⎿ Successfully added marketplace: anthropic-agent-skills
```

The marketplace is now added! It appears as **"anthropic-agent-skills"** in the plugin system.

### Step 3: Browse Available Plugins

Type:

```
/plugin
```

**What you'll see**: Interactive menu:
```
╭─────────────────────────────────────────────────╮
│ Plugins                                         │
│                                                 │
│ ❯ 1. Browse and install plugins                │
│   2. Manage and uninstall plugins               │
│   3. Add marketplace                            │
│   4. Manage marketplaces                        │
╰─────────────────────────────────────────────────╯
```

Select **"1. Browse and install plugins"**

### Step 4: Select the Marketplace

You'll see:
```
╭─────────────────────────────────────────────────╮
│ Select marketplace                              │
│                                                 │
│ ❯ anthropic-agent-skills                       │
│   2 plugins available                           │
╰─────────────────────────────────────────────────╯
```

Select **"anthropic-agent-skills"**

### Step 5: Choose a Plugin to Install

You'll see:
```
╭─────────────────────────────────────────────────╮
│ anthropic-agent-skills › Install plugins        │
│                                                 │
│ ❯ ◯ document-skills                            │
│     Collection of document processing suite...  │
│                                                 │
│   ◯ example-skills                             │
│     Collection of example skills demonstrating...│
╰─────────────────────────────────────────────────╯
```

**Let's install `example-skills`** — select it, then choose **"Install now"**

**What happens**:
```
Installing example-skills...
✓ Downloaded plugin bundle
✓ Installed skills to .claude/skills/
✓ example-skills ready to use
```

### Step 6: Verify Installation

Back in Claude Code, ask:

```
What skills do you have available?
```

**Expected response**: Claude lists the skills from example-skills bundle, including:
- Skill creator
- Canvas design
- Algorithmic art
- Web app testing
- And more...

### Step 7: Test a Skill (Optional)

Try using one of the installed skills:

```
Help me create a simple visual diagram explaining what a plugin is
```

Claude should use the canvas-design skill to create visual output!

### What You Just Did

- ✅ Added Anthropic's official marketplace (`anthropic-agent-skills`)
- ✅ Browsed available plugin bundles via interactive UI
- ✅ Installed a real plugin bundle (`example-skills`)
- ✅ Verified skills are now available for Claude to use
- ✅ (Optional) Tested a skill from the bundle

**This setup is permanent** — the marketplace and installed plugins stay available across all Claude Code sessions in this project.

---

## What You Just Learned

- ✅ Plugins bundle multiple capabilities (skills + agents + hooks + commands + MCP)
- ✅ Marketplaces provide pre-built plugins you can install
- ✅ Anthropic's skills repository has curated, production-quality skills
- ✅ `/plugin marketplace add` connects to plugin sources
- ✅ `/plugin install` adds capabilities to your Claude Code
- ✅ Check marketplaces FIRST before building custom capabilities

---

## Official Resources

**Anthropic Skills Repository**:
- https://github.com/anthropics/skills
- Browse all available skills
- View skill source code and documentation
- Learn from professional skill examples

**Plugin Marketplaces Documentation**:
- https://code.claude.com/docs/en/plugin-marketplaces
- How to create custom marketplaces
- Team distribution strategies
- Advanced marketplace configuration

**When You're Ready to Build**:
After using existing plugins, you can learn to create custom ones in advanced content (Part 5+).

---

## What Is a Plugin? (Architecture Reference)

A plugin directory (`.claude-plugin/`) can bundle:

- **Skills** (autonomous capabilities discovered by Claude)
- **Commands** (slash commands like `/code-review`)
- **Agents** (specialized subagents with focused context)
- **Hooks** (automation triggered by events like file saves)
- **MCP Configuration** (external integrations)

**A plugin is NOT a single feature—it's an integrated collection of extensions.**

### Why Plugins Matter

**Before Plugins** (scattered):
- Skills in `.claude/skills/`
- Subagents in `.claude/agents/`
- MCP config in `~/.config/claude/`
- Hooks scattered across your project

**With Plugins** (unified):
- Everything related to a feature bundled together
- Share entire plugin with team or community
- One installation installs entire integrated system
- Version control and updates become simple

---

## Plugin Architecture: The Manifest

Every plugin starts with a manifest file: `.claude-plugin/plugin.json`

```json
{
  "name": "feature-dev",
  "version": "1.0.0",
  "description": "Feature development plugin with code review, testing, and deployment hooks",

  "components": {
    "skills": [
      { "path": "skills/code-quality-checker" },
      { "path": "skills/test-coverage-analyzer" }
    ],
    "commands": [
      { "name": "feature-dev", "path": "commands/feature-dev.md" },
      { "name": "code-review", "path": "commands/code-review.md" }
    ],
    "agents": [
      { "name": "test-orchestrator", "path": "agents/test-orchestrator.md" }
    ],
    "hooks": [
      { "trigger": "PreToolUse", "path": "hooks/pre-tool-validation.md" }
    ],
    "mcp_config": "mcp-servers.json"
  }
}
```

**What this says**: *"This plugin includes 2 skills, 2 commands, 1 agent, 1 hook, and MCP configuration."*

### Inside a Plugin Directory Structure

```
.claude-plugin/
├── plugin.json                    # Manifest
├── commands/
│   ├── feature-dev.md             # Slash command: /feature-dev
│   └── code-review.md             # Slash command: /code-review
├── agents/
│   └── test-orchestrator.md       # Specialized subagent for testing
├── skills/
│   ├── code-quality-checker/
│   │   ├── SKILL.md               # Skill definition
│   │   └── scripts/
│   │       └── analyzer.py        # Implementation script
│   └── test-coverage-analyzer/
│       ├── SKILL.md
│       └── scripts/
│           └── coverage.py
├── hooks/
│   └── pre-tool-validation.md     # Runs before tool execution
└── mcp-servers.json               # External integrations
```

**Key insight**: A **single plugin** can deliver capabilities at multiple levels. The `feature-dev` plugin gives you:

- ✅ Autonomous skills (code quality checking, coverage analysis)
- ✅ Explicit commands (`/code-review`, `/feature-dev`)
- ✅ Specialized agents (test orchestration)
- ✅ Automation hooks (pre-execution validation)
- ✅ External integrations (GitHub MCP for issue tracking)

---

## The Relationship Hierarchy: Plugins Contain Everything

Here's how all the pieces fit together:

```
┌─────────────────────────────────────────────────────┐
│                    PLUGIN (Container)               │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │         SKILLS (Autonomous Discovery)        │  │
│  │  • Code quality checker (autonomous)         │  │
│  │  • Test coverage analyzer (autonomous)       │  │
│  │  • Compliance checker (autonomous)           │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │        COMMANDS (Explicit Slash Cmds)        │  │
│  │  • /code-review                              │  │
│  │  • /feature-dev                              │  │
│  │  • /deploy                                   │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │      AGENTS (Specialized Subagents)          │  │
│  │  • test-orchestrator (runs tests)            │  │
│  │  • security-auditor (checks vulnerabilities)│  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │     HOOKS (Event-Triggered Automation)       │  │
│  │  • PreToolUse: Validate before execution    │  │
│  │  • PostToolUse: Log execution results        │  │
│  │  • SessionStart: Initialize context          │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │  MCP CONFIGURATION (External Integrations)  │  │
│  │  • GitHub MCP (@github activation)          │  │
│  │  • Filesystem MCP (@filesystem activation)  │  │
│  │  • Jira MCP (@jira for issue tracking)      │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Interpretation**:
- **Skills** = Claude discovers and uses autonomously based on context
- **Commands** = You explicitly invoke with `/command-name`
- **Agents** = Specialized AI assistants you delegate to for focused tasks
- **Hooks** = Automation triggered by events (file saves, session start, etc.)
- **MCP** = External integrations (APIs, databases, web services)

**All bundled in one plugin** for easy sharing and installation.

---

## Try With AI

### Exercise 1: Explore the Skills Marketplace

```
I added the Anthropic skills marketplace. Show me all available skills
and recommend 3 that would be useful for [describe your workflow:
content creation / web development / data analysis / etc.]
```

**Expected outcome**: Claude lists available skills and recommends relevant ones for your workflow.

### Exercise 2: Install and Test a Skill

```
Install the canvas-design skill from anthropics/skills.
Then help me create a simple flowchart showing how I use Claude Code
in my daily workflow.
```

**Expected outcome**: Skill installs successfully, Claude uses it to create visual output.

### Exercise 3: Understand When to Build vs. Use

```
I need Claude to help with [describe a specific task].
Should I:
(a) Look for an existing skill in the marketplace
(b) Create a custom skill
(c) Just ask Claude directly without a skill

Walk me through the decision process.
```

**Expected outcome**: Understanding of when to use existing plugins vs. create custom capabilities.