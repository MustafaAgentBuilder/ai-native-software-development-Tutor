---
title: "Creating Your First UV Project"
chapter: 12
lesson: 3
duration_minutes: 20

# HIDDEN SKILLS METADATA (Institutional Integration Layer)
# Not visible to students; enables competency assessment and differentiation
skills:
  - name: "Initialize UV Project"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Content Creation"
    measurable_at_this_level: "Student can create a new UV project by expressing intent to Claude Code/Gemini CLI, understanding the generated structure (pyproject.toml, .python-version, src/)"

  - name: "Understand Project Configuration"
    proficiency_level: "A2"
    category: "Conceptual"
    bloom_level: "Understand"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can explain pyproject.toml's purpose (project metadata and dependencies) in plain language and recognize why virtual environments isolate projects"

  - name: "Navigate Project Structure"
    proficiency_level: "A2"
    category: "Technical"
    bloom_level: "Understand"
    digcomp_area: "Content Creation"
    measurable_at_this_level: "Student can identify and explain the purpose of each generated file: pyproject.toml, .python-version, src/, and .venv"

learning_objectives:
  - objective: "Create a new UV project by expressing intent to Claude Code or Gemini CLI"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student successfully creates a new project with `uv init` via AI assistance and understands the generated structure"

  - objective: "Explain what a virtual environment is and why projects need isolation"
    proficiency_level: "A2"
    bloom_level: "Understand"
    assessment_method: "Student describes virtual environment concept using analogies and plain language (no technical jargon)"

  - objective: "Add a production dependency to a project with AI"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student uses `uv add` via Claude Code/Gemini CLI to add a package (e.g., requests)"

  - objective: "Distinguish between pyproject.toml (modern) and requirements.txt (legacy)"
    proficiency_level: "A2"
    bloom_level: "Understand"
    assessment_method: "Student compares the two approaches and articulates why pyproject.toml is modern Python standard"

cognitive_load:
  new_concepts: 7
  assessment: "7 new concepts: Python project definition, project structure, pyproject.toml purpose, virtual environment isolation, dependency specification vs. installation, UV's automatic venv handling, modern vs. legacy configuration. Within A2-B1 limit of 7 concepts. ✓"

differentiation:
  extension_for_advanced: "Customize pyproject.toml metadata (project name, author, description) with AI guidance; explore Python version pinning"
  remedial_for_struggling: "Focus on core concept: 'A project is a folder with configuration telling UV what your code needs.' Virtual environment = separate toolbox (analogy). Let AI handle all commands."

# Generation metadata
generated_by: "lesson-writer v3.0.0"
source_spec: "specs/011-python-uv/plan.md"
created: "2025-11-13"
last_modified: "2025-11-13"
git_author: "Claude Code"
workflow: "/sp.implement"
version: "1.0.0"
---

# Creating Your First UV Project

## What Is a Python Project?

A **Python project** is a folder on your computer that contains your code and configuration files that tell UV what packages your code needs.

Think of it like a kitchen:
- Your code is the recipe (the instructions)
- The project folder is the kitchen (organized workspace)
- Dependencies are the ingredients (packages you need)
- A virtual environment is the toolbox—each project gets its own so packages don't conflict

UV handles this organization automatically. Let's create your first project.

## Step 1: Create a New Project (Direct Command)

Creating a project is simple. Run this command:

```bash
uv init my-first-app
```

**What this does:**
- Creates a new folder called `my-first-app`
- Generates project structure with configuration files
- Sets up everything you need to start coding

**Time:** Under 1 second

Now navigate into your project:

```bash
cd my-first-app
```

## Step 2: Explore the Project Structure

When UV created your project, it generated several files. Let's look at them.

**Visual Project Structure:**

```
my-first-app/
├── .git/                    # Git repository (UV initializes git automatically)
├── .gitignore               # Files git should ignore
├── .python-version          # Tells UV which Python version to use
├── pyproject.toml           # Your project's configuration file
├── README.md                # Description of your project
├── main.py                  # Your starter script
└── .venv/                   # Virtual environment (created when you add dependencies)
```

Each file has a purpose. Let's understand the important ones.

### pyproject.toml: Your Project's Brain

**What it is:** A configuration file that tells UV (and Python) everything about your project.

**What it contains:** Metadata about your project and a list of what packages it needs.

When you opened this file (or asked AI to show it), you might see something like:

```toml
[project]
name = "my-first-app"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []
```

**Don't panic about TOML syntax.** You don't need to memorize this. Here's what matters:

- **`name = "my-first-app"`** — This is your project's name
- **`requires-python = ">=3.12"`** — Your project needs Python version 3.12 or newer
- **`dependencies = []`** — When you add packages with `uv add requests`, they appear here

**The key insight:** pyproject.toml is Python's modern standard. It replaced the old `requirements.txt` file because it's more powerful and flexible.

#### 🎓 Expert Insight

> In AI-native development, you don't edit pyproject.toml by hand—you tell Claude Code or Gemini CLI to manage it. Your job: understand what it represents (your project's contract with Python), not memorize its syntax.

### .python-version: Pinning Your Python Release

This tiny file contains just one line:

```
3.12
```

**What it does:** Tells UV which Python version to use for this project.

**Why it matters:** When you work with teammates, everyone needs the same Python version. If you use Python 3.12 and your teammate uses 3.11, packages might behave differently. This file ensures everyone is synchronized.

**You never edit this manually.** UV set it automatically when you created the project.

### main.py: Your Starter Script

UV creates a simple `main.py` file to get you started:

```python
def main():
    print("Hello from my-first-app!")


if __name__ == "__main__":
    main()
```

This is where you write your Python code. You can rename this file, create additional files, or organize your project however you like.

### .venv/: Your Project's Isolated Toolbox

This is the **virtual environment**—a special folder that contains all the packages your project needs.

**You never directly open or modify .venv.** UV manages it automatically.

**Why it exists:** Imagine you have two projects:
- Project A needs `requests` version 2.28
- Project B needs `requests` version 2.31

Without isolation, installing both projects on the same computer would cause conflicts. The second installation would overwrite the first. **Virtual environments solve this:** each project gets its own separate `requests` installation.

#### 🎓 Expert Insight: The Separate Toolbox Analogy

> Think of your computer as a warehouse. Without virtual environments, all your projects share one toolbox. If Project A needs a hammer of size 10 and Project B needs a hammer of size 12, you'd have a conflict. Virtual environments give each project its own toolbox. Problem solved.

## Step 3: Add a Dependency (Direct Command)

Adding packages to your project is also simple. Let's add the `requests` library (for making HTTP requests):

```bash
uv add requests
```

**What this does:**
1. Searches PyPI (Python's package registry) for `requests`
2. Downloads the latest version and its dependencies
3. Updates `pyproject.toml` with the package
4. Installs it into `.venv/` (your virtual environment)
5. Creates/updates `uv.lock` (ensures everyone gets the same versions)

**Time:** 1-3 seconds

**Output you'll see:**

```
Resolved 6 packages in 2.85s
Installed 5 packages in 274ms
 + certifi==2025.11.12
 + charset-normalizer==3.4.4
 + idna==3.11
 + requests==2.32.5
 + urllib3==2.5.0
```

Notice `requests` plus 4 additional packages—these are **transitive dependencies** (packages that `requests` needs to work).

UV handles all of this automatically in 1-3 seconds.

## Step 4: Understanding Dependency Specification vs. Installation

Here's an important distinction:

**Specifying a dependency** = Listing what your project needs (in pyproject.toml)
**Installing a dependency** = Downloading and setting it up (in .venv/)

When you run `uv add requests`:
1. ✅ **Specification**: Adds `requests` to pyproject.toml (says "I need this")
2. ✅ **Installation**: Downloads and installs it to .venv/ (actually gets it)

Both happen automatically with UV, but they're conceptually different.

**Why this matters:** Your pyproject.toml is what you commit to git and share with teammates. Your .venv/ is local to your computer—each person installs their own copy.

#### 💬 AI Colearning Prompt

> "Why don't I commit the .venv/ folder to git? What's the difference between sharing pyproject.toml and sharing .venv/?"

This is a great question to explore with AI. The answer will deepen your understanding of how team collaboration works.

## Modern Python: pyproject.toml vs. requirements.txt

If you learned Python before 2022, you might have seen `requirements.txt`:

```
requests==2.28.0
flask==2.0.1
```

This is the old way. It's:
- ✅ Simple to read
- ❌ Limited (no metadata about your project)
- ❌ Inflexible (doesn't support development dependencies well)

**pyproject.toml is the modern standard** because it:
- ✅ Includes project metadata (name, version, description, author)
- ✅ Supports development vs. production dependencies
- ✅ Enables powerful tooling (linting, testing, building)
- ✅ Works with multiple tools (not just pip, but also poetry, hatch, UV)

When you write `uv add flask`, UV updates your pyproject.toml automatically. You're using modern Python standards from day one.

### Comparison Table

| Aspect | requirements.txt | pyproject.toml |
|--------|------------------|----------------|
| **Project metadata** | No | Yes (name, version, author) |
| **Development dependencies** | Needs separate file | Built-in support |
| **Standard** | Pip-specific (old) | Python-wide standard (modern) |
| **Tool ecosystem** | Limited | Works with poetry, hatch, UV, etc. |
| **Your learning** | Not recommended | Use this (you're starting fresh) |

**Bottom line:** You're learning Python the modern way from day one.

## When to Use AI for Projects

**Simple project creation (use direct commands):**
- `uv init my-project` - Takes 1 second
- `uv add requests` - Takes 1-3 seconds
- No AI needed for straightforward operations

**Complex scenarios (use AI):**
- Understanding what `pyproject.toml` does
- Troubleshooting dependency conflicts
- Deciding between production vs. development dependencies
- Migrating from legacy `requirements.txt` to modern `pyproject.toml`

**Pattern:** Direct commands for simple tasks, AI for understanding and troubleshooting.

## Common Questions Answered

**Q: Why do I need a virtual environment?**
A: Each project gets isolated packages. Project A's Flask 2.0 doesn't conflict with Project B's Flask 3.0.

**Q: Do I have to use src/?**
A: UV creates it by default. It's a modern best practice. You can organize it differently, but src/ is professional and standard.

**Q: Can I change my project name?**
A: The folder name is just a folder. The project name in pyproject.toml is what matters. Ask AI to help you update it.

**Q: What if I want to use a different Python version?**
A: Tell your AI: "Update this project to use Python 3.14" and let it handle the .python-version file.

**Q: Do I commit .venv/ to git?**
A: No. Add it to `.gitignore`. Your teammates install their own .venv/ by running `uv sync` (which you'll learn in Lesson 6).

## Key Takeaways (What You Learned)

- A Python project is an organized folder with code and configuration
- pyproject.toml is the modern configuration file (replaces old requirements.txt)
- Virtual environments isolate each project's packages
- UV automates everything: `uv init` creates structure, `uv add` installs packages
- You express intent to AI; AI handles the commands
- Specification (pyproject.toml) and installation (.venv/) are separate concepts

## Try With AI

Use your AI companion (ChatGPT, Claude Code, Gemini CLI, etc.) for these exercises.

### Prompt 1: Understand Virtual Environments Deeply

```
I just created a UV project and it generated a .venv/ folder. Explain virtual environments in simple terms using an analogy. Why does each project need its own isolated environment?
```

**Expected outcome:** Clear understanding of why isolation prevents dependency conflicts.

### Prompt 2: Understand pyproject.toml

```
I have a pyproject.toml file in my UV project. Explain what this file does and why it's better than the old requirements.txt approach. Give me 2-3 concrete examples.
```

**Expected outcome:** Understanding of modern Python project configuration and its advantages.

### Prompt 3: Production vs. Development Dependencies

```
What's the difference between production dependencies and development dependencies in a Python project? Give me examples of each and explain when I'd use the --dev flag with `uv add`.
```

**Expected outcome:** Strategic understanding of dependency types and when to use each.

### Prompt 4: Troubleshoot Dependency Conflicts

```
I'm trying to add package X to my UV project, but I'm getting a dependency conflict error. How can I diagnose what's causing the conflict and resolve it?
```

**Expected outcome:** Troubleshooting strategy for complex dependency issues (where AI adds real value).
