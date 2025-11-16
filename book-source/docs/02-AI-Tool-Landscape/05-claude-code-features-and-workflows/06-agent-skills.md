<!-- Claude is Work to Build this Project -->
---
sidebar_position: 6
title: "Agent Skills"
duration: "8-10 min"
learning_objectives:
  - "Understand skills as reusable capabilities that extend Claude's knowledge"
  - "Create a working SKILL.md file with YAML frontmatter and instructions"
  - "Write effective skill descriptions that trigger autonomous discovery"
  - "Improve skills through co-learning iteration with Claude"
  - "Recognize when to use skills vs subagents"
---

# Agent Skills: Teaching Claude New Capabilities

## The Problem: Repeating Yourself Across Sessions

You're working with Claude Code on multiple blog posts this week. Every time you start a new session, you give the same instructions:

"Create an outline with 5 main sections, suggest 5 headline variations, make the introduction hook readers in the first sentence, keep paragraphs under 4 sentences..."

By the third blog post, you're frustrated. **Why can't Claude just remember how you like blog posts structured?**

You could use a subagent—but that requires explicitly saying "Use the blog-planner subagent" every time. What if Claude could **automatically** apply your blog-planning workflow whenever you mention writing a blog post?

**That's what Skills solve.**

---

## What Are Agent Skills?

**Definition**: An Agent Skill is a **reusable capability** that extends Claude Code's knowledge in specific domains. When Claude recognizes the context (like "write a blog post"), it automatically loads and applies the skill's instructions.

**Think of skills as**: Teaching materials that Claude can reference when needed—like giving Claude a handbook on "how I want blog posts structured."

**Key characteristic**: Skills are **discovered autonomously**. You create the skill once (SKILL.md file), and Claude applies it automatically when relevant—no explicit invocation needed.

### How Skills Differ from Subagents

You learned subagents in Lesson 5. Skills are similar in structure but different in **invocation control and context isolation**:

### Subagents vs. Skills: What's Actually Different?

Based on the official documentation, subagents and skills are similar in structure but have **two critical differences**:

**Similarity**: Both:
- Have YAML frontmatter (name, description, tools)
- Have markdown content (instructions)
- Live in `.claude/` directories
- Claude discovers them autonomously

**The TWO key differences: Context isolation + Invocation control**

| Feature | Subagents | Skills |
|---------|-----------|--------|
| **Context isolation** | ✅ Separate context window<br/>✅ Separate transcript file (`agent-{id}.jsonl`)<br/>Prevents main conversation pollution | ❌ Runs in main Claude Code context<br/>❌ No separate transcript<br/>Shares context with main conversation |
| **Autonomous invocation** | ✅ Claude decides when to use | ✅ Claude decides when to use |
| **Explicit invocation** | ✅ "Use the [name] subagent"<br/>(Hard invocation - guaranteed) | ❌ No hard invocation<br/>✅ **But you CAN guide by name**<br/>"Use the [name] skill" (soft guidance) |
| **File structure** | `.claude/agents/name.md` | `.claude/skills/name/SKILL.md` |
| **Tool specification** | `tools:` (inherits all if omitted) | `allowed-tools:` (restricts if specified) |

**Official quote on context isolation**:
> "Each subagent operates in its own context, preventing pollution of the main conversation and keeping it focused on high-level objectives."

**Official quote on skill invocation**:
> "Skills are **model-invoked**—Claude autonomously decides when to use them based on your request and the Skill's description. This is different from slash commands, which are **user-invoked**."

**Important clarification**: While skills don't have *hard invocation* (no system-level trigger), **you CAN guide Claude by mentioning skill names**. This provides contextual guidance that makes Claude more likely to apply that skill.

**Example**:

```
You: "Help me plan a blog post about sustainable living"

With a blog-writer subagent:
- ✅ Hard invocation: "Use the blog-writer subagent" (guaranteed launch)
- ✅ Autonomous: Claude may invoke it automatically
- ✅ Runs in isolated context (separate transcript)
- ✅ Main conversation stays clean

With a blog-writer skill:
- ✅ Soft guidance: "Use the blog-writer skill" (guides Claude's decision)
- ✅ Autonomous: Claude may apply it automatically
- ❌ Runs in main context (shares transcript with main conversation)
- ❌ Adds to main conversation context

You can also ask: "What skills do you have?" and Claude will list all available skills.
Then say: "Use the blog-writer skill for this topic" and Claude will likely apply it.
```

**The Practical Difference**:

**Hard invocation (subagents)**:
- "Use the blog-writer subagent" → System launches it (guaranteed)
- Separate context, separate transcript
- Use when you need isolation and guaranteed execution

**Soft guidance (skills)**:
- "Use the blog-writer skill" → Claude likely applies it (contextual guidance)
- Same context, same transcript
- Use when you want lightweight capabilities without context overhead

**When to use skills over subagents**:
- When context isolation isn't important (small, focused tasks)
- When you want Claude to be smarter by default
- When you want to guide by name but don't need guaranteed invocation
- When you want minimal overhead (no separate context management)

**When to use subagents over skills**:
- When you need **guaranteed invocation** ("Use X subagent" must work)
- When you need **context isolation** (complex tasks that shouldn't clutter main conversation)
- When you want **separate transcripts** for specialized work
- When the task is complex enough to justify separate context overhead

---

## How Skills Work: The Three-Level Architecture

### Level 1: Metadata in System Prompt (Always Loaded)

When Claude Code starts, it loads a brief summary of every available skill:

```
Available Skills:
- pdf-skill: Extract and analyze tables, forms, and fields from PDF files
- blog-writer-skill: Generate engaging blog posts with research and structure
- meeting-notes-skill: Transform messy notes into structured summaries
```

This is **tiny**—3-4 lines per skill. Claude reads these summaries and thinks: *"If the user shows me a PDF, I should probably use the pdf-skill."*

**Why this works**: Claude learns WHEN to invoke skills without needing the full SKILL.md file loaded yet.

### Level 2: Full SKILL.md When Relevant (On-Demand)

When Claude decides a skill is relevant, it fetches the complete **SKILL.md file**—the full instructions:

```yaml
---
name: "pdf-skill"
description: "Extract tables, forms, and field values from PDF files"
---

# PDF Skill

## When to Use This Skill
- User uploads a PDF and asks to extract a table
- User wants form fields extracted and validated
- User asks about PDF content structure

## How to Use This Skill
1. Run: `scripts/pdf_extractor.py --input [path] --output [format]`
2. Validate extracted data matches expected structure
3. Return structured JSON with confidence scores
```

Now Claude has the **full context** needed to execute properly. But it only loads this when relevant.

**Why this works**: Full instructions don't clutter the system prompt; they're loaded on-demand.

### Level 3: Bundled Reference Files and Scripts (Complete Toolkit)

If the SKILL.md needs supporting files, Claude accesses them:

```
.claude/skills/pdf-skill/
├── SKILL.md                 # Main instructions
├── scripts/
│   └── pdf_extractor.py     # Python script for extraction
└── reference/
    └── pdf-standards.md     # Technical reference: PDF specs
```

When Claude executes the skill, it can reference the Python script or dive into technical specs if needed.

**Real Example: PDF Form Filling Skill**

```
Flow:
1. User: "Extract all form fields from this W-2 PDF"
2. Claude reads system prompt: "pdf-skill: Extract forms and fields"
3. Claude fetches SKILL.md: "Use pdf_extractor.py"
4. Claude runs: pdf_extractor.py --input w2.pdf --output json
5. Claude references pdf-standards.md to validate field names
6. Claude returns: {"ssn": "XXX-XX-XXXX", "income": 125000, ...}
```

---

## When Claude Code Invokes Skills Automatically

Claude Code doesn't use skills randomly. It recognizes specific patterns and applies skills only when relevant:

**Pattern 1: Content Type Recognition**
- You upload a PDF → pdf-skill automatically discovered
- You paste JSON → validation-skill automatically discovered
- You show HTML → parsing-skill automatically discovered

**Pattern 2: Task Request Recognition**
- "Help me write a blog post" → blog-writer-skill
- "Organize these meeting notes" → meeting-notes-skill
- "Summarize this document" → document-analysis-skill

**Pattern 3: Explicit Request**
- "Use the blog-writer skill to draft this article"

### How to Check Available Skills

Skills don't have a dedicated `list` command. Instead, **ask Claude directly in a session**:

1. Start Claude Code: `claude`
2. Ask: "What skills do you have available?"
3. Claude will list all skills it can access with their descriptions

This conversational approach is intentional—skills are meant to be discovered naturally through interaction, not managed like system commands.

---

## Hands-On: Create Your First Custom Skill

Just like with subagents, creating a skill is **easy**. Let's create a simple blog planning skill together.

### Step 1: Create the Skill Directory Structure

Skills live in `.claude/skills/` and require a specific structure:

```bash
# In your project directory, create:
mkdir -p .claude/skills/blog-planner
```

### Step 2: Create the SKILL.md File

Create `.claude/skills/blog-planner/SKILL.md` with this content:

```markdown
---
name: "blog-planner"
description: "Help plan engaging blog posts: research topics, create outlines, suggest headlines, and draft compelling introductions. Use when user asks to plan or write blog content."
version: "1.0.0"
---

# Blog Planning Skill

## When to Use This Skill

- User asks to "plan a blog post" or "write an article"
- User mentions blog topics, headlines, or content strategy
- User needs help structuring written content

## How This Skill Works

1. **Research the topic**: Understand the subject and target audience
2. **Create outline**: Break topic into 3-5 main sections
3. **Suggest headlines**: Provide 5 compelling headline options
4. **Draft introduction**: Write an engaging first paragraph that hooks readers

## Output Format

Provide:
- **Topic Summary**: 2-3 sentence overview
- **Target Audience**: Who should read this?
- **Outline**: Numbered list of main sections
- **Headline Options**: 5 variations (descriptive, curiosity-driven, benefit-focused)
- **Introduction Draft**: 1-2 paragraph hook

## Example

**Input**: "Help me plan a blog post about sustainable living"

**Output**:
- **Topic Summary**: Practical sustainable living tips for busy professionals
- **Target Audience**: Working adults wanting eco-friendly lifestyle changes
- **Outline**:
  1. Why sustainable living matters now
  2. 5 easy swaps you can make today
  3. Long-term sustainable habits
  4. Common myths debunked
  5. Resources for deeper learning
- **Headlines**:
  1. "5 Sustainable Living Changes You Can Make This Weekend"
  2. "Busy Professional's Guide to Eco-Friendly Living"
  3. "Sustainable Living: Easier Than You Think"
- **Introduction**: "You care about the environment, but who has time for complicated lifestyle changes? Good news: sustainable living doesn't require upending your entire routine. These five simple swaps take less than an hour to implement—and they'll cut your environmental impact by 30%."
```

### Step 3: Enable the Skill

1. Start Claude Code in your project: `claude`
2. The skill is automatically discovered (no manual activation needed)
3. Test by asking: "What skills do you have?" (you should see `blog-planner`)

### Step 4: Test Your Skill

In your Claude Code session, try:

```
Help me plan a blog post about learning AI tools
```

**What happens**:
1. Claude recognizes "blog post" trigger from skill description
2. Claude loads the blog-planner skill instructions
3. Claude applies the skill's workflow (research → outline → headlines → intro)
4. You receive structured blog plan following the skill's output format

### Step 5: Co-Learning Convergence — Improve Your Skill

**Now comes the critical part**: Your skill works, but is it GOOD? Let's use co-learning to refine it.

In your Claude Code session, ask:

```
Review the blog-planner skill I just created. What could be improved?
Look at the description, instructions, and example output.
Suggest 2-3 specific improvements.
```

**What happens (Co-Learning Loop)**:

**Round 1 — AI teaches you**:
- Claude reads your SKILL.md
- Points out: "Description could be more specific—mention 'content strategy' and 'SEO-friendly'"
- Suggests: "Add a 'Common Pitfalls' section to help me avoid mistakes"
- Recommends: "Include target word count in output format"

**Round 2 — You teach AI**:
```
Good feedback! But I specifically want headlines that are curiosity-driven
(not clickbait). And I need the introduction to be exactly 2 paragraphs,
not 1-2. Update the skill with these requirements.
```

**Round 3 — AI adapts**:
- Claude updates SKILL.md with your specific preferences
- Adds: "Headlines must spark curiosity without misleading (no clickbait)"
- Changes: "Introduction Draft: Exactly 2 paragraphs" (not "1-2")

**Round 4 — You validate**:
```
Now test the updated skill on: "Help me plan a blog post about remote work productivity"
```

- You see the output
- Headlines are curiosity-driven (not clickbait) ✅
- Introduction is exactly 2 paragraphs ✅
- Skill reflects YOUR preferences now

**This is co-learning**:
- **AI taught you**: What makes descriptions effective, what sections to include
- **You taught AI**: Your specific standards (curiosity-driven, exactly 2 paragraphs)
- **Together you converged**: On a skill that matches YOUR workflow

**Key Insight**: You didn't just create a skill—you **co-designed** it through iteration. AI suggested improvements; you provided constraints; together you built something neither would have created alone.

### What You Just Learned

- ✅ Skills are **files** (`.claude/skills/{name}/SKILL.md`)
- ✅ Skills have **YAML frontmatter** (name, description, version)
- ✅ Skills are **reusable capabilities** that extend Claude's domain knowledge
- ✅ Skills improve through **co-learning** (AI reviews → You refine → Validate)
- ✅ Skills apply when **description triggers match** user requests

---

## More Skill Ideas

Try creating these skills using the same pattern:

**Meeting Notes Organizer Skill**:
```yaml
---
name: "meeting-notes-organizer"
description: "Transform messy meeting notes into structured summaries with action items, decisions, and follow-ups. Use when user shares meeting notes or transcripts."
---
```

**Learning Path Designer Skill**:
```yaml
---
name: "learning-path-designer"
description: "Create structured learning plans for any topic with progressive difficulty, resource recommendations, and practice exercises. Use when user wants to learn a new subject."
---
```

**Startup Idea Analyzer Skill**:
```yaml
---
name: "startup-idea-analyzer"
description: "Evaluate business ideas with market research, competitor analysis, and go-to-market strategy suggestions. Use when user presents a startup or business concept."
---
```

---

## Practical Example: Using the PDF Skill

Scenario: You have a PDF invoice and want to extract key fields.

### What You Do

1. Have the PDF ready (e.g., `invoice.pdf`)
2. In Claude Code, say:

```
Extract invoice details from invoice.pdf:
- Invoice number
- Date
- Total amount
- Payment due date
- Vendor name
```

### What Happens Internally

1. Claude reads system prompt summary: "pdf-skill available for PDF extraction"
2. Claude recognizes PDF content + extraction request
3. Claude fetches full SKILL.md with `pdf_extractor.py` instructions
4. Claude runs the Python script: `pdf_extractor.py --input invoice.pdf --output json`
5. Claude validates output matches PDF structure
6. Claude returns structured data with confidence scores

### What You See

```
Extracted Invoice Details:
- Invoice #: INV-2024-00531
- Date: November 13, 2024
- Total: $2,450.00
- Due: December 13, 2024
- Vendor: Tech Solutions Inc.

Confidence: 98% (all fields validated)
```

**You didn't type any commands.** The skill executed automatically because Claude recognized the context.

---

## Strategic Decision: When to Use Skills vs. Explicit Commands

**Use Skills When**:
- Task type is predictable and repeatable (PDF extraction, blog drafting, note organizing)
- You want automatic application (no explicit invocation needed)
- Multiple similar tasks in a session (skill handles consistently)

**Use Subagents When**:
- Task is complex with many variables (subagent can handle context better)
- You want explicit control (tell subagent what to do)
- Task needs specialized context (subagent can load specific strategies)

**Use Main Conversation When**:
- One-off, exploratory work
- You're learning something new
- No specialized skill exists yet

---

## Skill Best Practices (From Official Documentation)

Now that you've created your first skill, here are key best practices from Anthropic's official documentation:

### Writing Effective Descriptions

The `description` field is **critical**—it's how Claude discovers when to use your skill.

**Good description** (specific, includes triggers):
```yaml
description: "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDFs or when user mentions forms or document extraction."
```

**Bad description** (vague, no triggers):
```yaml
description: "Helps with documents"
```

**Key principles**:
- Be specific about what the skill does
- Include file types, domains, and operation names
- Mention activation triggers ("Use when...")
- Use third-person perspective (avoid "I can help you")

### Keep Skills Focused

**One skill, one workflow.** Don't create a mega-skill that tries to do everything.

**Good approach** (separate skills):
- `blog-planner` — Planning and outlining
- `blog-writer` — Actual writing and drafting
- `blog-editor` — Editing and refinement

**Bad approach** (one bloated skill):
- `blog-everything` — Does planning, writing, editing, SEO, publishing...

**Why?** Focused skills compose automatically. Claude can use multiple skills together more effectively than one complex skill trying to handle all cases.

### Start Simple, Iterate

**Don't** build complex skills with scripts and multiple files on your first try.

**Do** start with basic Markdown instructions, test them, then add complexity.

**Progression**:
1. **Version 1.0**: Basic instructions in SKILL.md (what you just created)
2. **Version 1.1**: Add examples and edge cases
3. **Version 1.2**: Add reference files if needed
4. **Version 2.0**: Add executable scripts for deterministic operations (if truly needed)

### Common Pitfalls to Avoid

**❌ Don't**:
- Use Windows-style paths (`reference\guide.md`) — always use forward slashes (`reference/guide.md`)
- Create deeply nested references — keep files one level deep from SKILL.md
- Include time-sensitive information (dates, versions that change often)
- Over-explain concepts Claude already understands
- Provide too many options without a recommended default

**✅ Do**:
- Keep SKILL.md under 500 lines (split into reference files if longer)
- Test skills with fresh Claude sessions (not just current conversation)
- Include specific examples in SKILL.md
- Version your skills (1.0.0, 1.1.0, etc.) for rollback capability
- Document installation steps for any required tools

---

## Learn More: Official Skill Examples

Want to see professional-quality skills created by Anthropic?

**Anthropic Skills Repository**: https://github.com/anthropics/skills

This GitHub repository contains real-world skill examples you can:
- Study to understand best practices
- Adapt for your own needs
- Use as starting templates

**Recommended skills to study**:
- **PDF skills** — File handling and extraction patterns
- **Data analysis skills** — Working with structured data
- **Writing skills** — Content generation workflows

**Official Documentation**:
- **How to create skills**: https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- **Best practices**: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices

---

## Reflection: Understanding Autonomous Discovery

Think about how skills differ from traditional commands:

- **Traditional command**: You know the command exists, type it explicitly (`pdf_extract --input file.pdf`)
- **Claude Code skill**: You describe what you want; Claude discovers the right skill and applies it

This shift—from "command what exists" to "describe what you want"—is fundamental to AI-native development.

**Pause and Reflect**:
- What's the difference between telling Claude Code to "use the pdf-skill" vs. just asking "extract data from this PDF"?
- Why doesn't Claude Code list all available skills in every response? (Hint: cognitive load)
- When might a skill apply even when you didn't ask for it explicitly?

---

## Try With AI

Use Claude Code for this activity (preferred). If you have another AI companion tool (ChatGPT, Gemini), you can use that instead.

### Prompt 1: Understanding Skill Discovery

```
Explain how Claude Code discovers skills automatically.
Use an analogy: it's like having a colleague who...
(a) Notices the type of work you're doing,
(b) Suggests the right tool without you asking,
(c) But doesn't interrupt with suggestions for irrelevant tasks.
Show 3 examples of tasks where Claude would discover a skill automatically.
```

**Expected outcome**: Clear explanation of autonomous skill discovery with realistic examples.

### Prompt 2: Skill Limitations and Safety

```
If skills apply automatically without explicit requests, what prevents misuse?
(a) How does Claude decide NOT to use a skill when it could?
(b) What if a skill causes unintended side effects?
(c) How would you disable a skill that you don't trust?
(d) Create a 'skill safety checklist' for evaluating whether a skill is trustworthy.
```

**Expected outcome**: Understanding of skill safety boundaries and verification procedures.

### Prompt 3: Designing Your Own Skill

```
Think about a repeated task in your work.
Design a skill that would automate it:
(a) What's the skill name and description?
(b) When would Claude Code discover it's relevant?
(c) What files and scripts would it bundle?
(d) How would you know when it's working correctly?
Example tasks: "Draft social media posts", "Organize research notes", "Create meeting agendas"
```

**Expected outcome**: Concrete skill design based on your actual work patterns.

### Prompt 4: Skill vs. Subagent Decision

```
You have two similar tasks:
Task 1: Draft weekly blog posts about productivity tips (happens 3x per week)
Task 2: Create a comprehensive content strategy for a product launch (one-time, complex planning)

For each task, should you build a Skill or a Subagent?
Explain your reasoning for each choice.
What's the tradeoff between convenience (automatic skills) and control (explicit subagents)?
```

**Expected outcome**: Clear decision framework for when to use skills vs. subagents based on task patterns.
