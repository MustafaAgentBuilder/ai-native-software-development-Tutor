---
title: "Team Collaboration and Reproducible Environments with AI"
chapter: 12
lesson: 6
duration_minutes: 30

# HIDDEN SKILLS METADATA (Institutional Integration Layer)
# Not visible to students; enables competency assessment and differentiation
skills:
  - name: "Share Projects Reproducibly"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Collaboration"
    measurable_at_this_level: "Student can prepare a project for teammates (ensure lockfile exists, commit to git), recreate environments from lockfiles (`uv sync`), and verify environment matches original developer's setup"

  - name: "Understand Lockfile Purpose"
    proficiency_level: "B1"
    category: "Conceptual"
    bloom_level: "Understand"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can explain the difference between pyproject.toml (constraints) and uv.lock (pinned versions), why lockfiles ensure reproducibility, and when to update lockfiles"

  - name: "Manage Version Control with UV"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Collaboration"
    measurable_at_this_level: "Student can integrate UV projects with Git workflow, commit correct files (pyproject.toml + uv.lock), and understand what to ignore (.venv, __pycache__)"

learning_objectives:
  - objective: "Apply reproducible environment workflows to share projects with teammates using lockfiles and `uv sync`"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Hands-on: Prepare project for teammate, teammate recreates environment successfully"

  - objective: "Explain the difference between pyproject.toml and uv.lock, understanding version pinning and reproducibility"
    proficiency_level: "B1"
    bloom_level: "Understand"
    assessment_method: "Conceptual explanation with examples; identify when to update each file"

  - objective: "Integrate UV projects with Git workflow, committing appropriate files and managing collaborative development"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Git integration scenario: commit project, simulate teammate clone/setup, verify reproducibility"

cognitive_load:
  new_concepts: 7
  assessment: "7 new concepts: reproducible environments, pyproject.toml vs. uv.lock distinction, `uv sync` command, Git integration, production deployment, lockfile updates, team onboarding. Within B1 limit of 10 concepts. ✓"

differentiation:
  extension_for_advanced: "Explore lockfile conflicts in team scenarios; implement CI/CD with UV for automated testing; manage complex dependency resolution"
  remedial_for_struggling: "Focus on core workflow: 'Commit both files, teammate runs `uv sync`, environment matches exactly.' Practice one scenario fully before adding complexity"

# Generation metadata
generated_by: "lesson-writer v3.0.0"
source_spec: "specs/011-python-uv/plan.md"
created: "2025-11-13"
last_modified: "2025-11-13"
git_author: "Claude Code"
workflow: "/sp.implement"
version: "1.0.0"
---

# Team Collaboration and Reproducible Environments with AI

## The "Works on My Machine" Problem

You've created a fantastic Python project. Your code runs perfectly on your computer. You invite a teammate to work on it and... their environment doesn't match yours. They get errors. Dependencies are different versions. The Python version is different. Nothing works.

This is the **"works on my machine" problem**, and it's plagued software teams for decades.

The solution? **Reproducible environments** — using UV to ensure that every developer on your team has the exact same library versions, the exact same Python version, and the exact same environment setup. No surprises. No debugging environment differences.

This is the capstone lesson of the UV chapter: we're moving from individual development to team workflows.

## Understanding: What Makes Environments Reproducible?

### The Two Files Your Project Needs

Your UV project contains two critical files that work together:

**File 1: `pyproject.toml` (Constraints)**

This file says "what I want, roughly":

```toml
[project]
dependencies = [
    "requests>=2.31.0",
    "flask>=3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black>=23.0",
]
```

Notice the `>=` signs. This means "I want `requests`, version 2.31.0 or higher." It's flexible—if a newer version appears, that's fine.

**File 2: `uv.lock` (Pinned Versions)**

This file says "here's exactly what I have":

```
requests==2.32.1
flask==3.0.2
pytest==7.4.0
black==23.12.0
```

Notice the `==` signs. This means "I tested with this exact version." It's strict—everyone gets this exact version.


### Why Both Files?

Think of it like a recipe versus a specific meal:

- **pyproject.toml** = Recipe ("Use flour, roughly 2-3 cups")
- **uv.lock** = Exact meal ("2.5 cups of King Arthur flour, batch #2024-10")

When you're **developing alone**, `pyproject.toml` is flexible enough. You might use requests 2.31 or 2.32; both work fine.

But when you're **on a team**, you need the exact meal. If developer A used requests 2.31 and developer B used requests 2.32, and they have different behavior, you'll spend hours debugging an environment difference (not a code bug).

That's why UV **automatically creates and updates `uv.lock`** every time you run `uv add` or `uv sync`.


## Real-World Scenario 1: Preparing Your Project for a Teammate

You've built a web scraper with UV. Now you want your teammate Maria to work on it.

### Step 1: Ensure Both Files Exist

Verify your project has both `pyproject.toml` and `uv.lock`. If `uv.lock` doesn't exist:

```bash
uv lock
```

### Step 2: Commit Both Files to Git

```bash
# These files go to Git:
git add pyproject.toml uv.lock .python-version

# These do NOT go to Git (already in .gitignore):
# .venv/           <- Virtual environment
# __pycache__/     <- Python cache
# *.pyc            <- Compiled bytecode
```

**Why not commit `.venv`?** It's 50+ MB of dependencies. Everyone can recreate it in seconds using `uv.lock`.

## Real-World Scenario 2: Teammate Clone and Setup

Maria just cloned your project. She has:

```
web-scraper/
├── pyproject.toml    # Constraints
├── uv.lock           # Exact versions
└── src/
    └── scraper.py    # Your code
```

She does **not** have `.venv/` yet—she'll create it.

### She Runs `uv sync`

```bash
uv sync
```

**Output:**
```
Resolved 15 packages in 0.25s
Downloaded 15 packages in 0.18s
Installed 15 packages in 0.08s
```

**What happened:**
1. UV read `uv.lock`
2. Downloaded exact versions (requests 2.32.1, beautifulsoup4 4.12.0, etc.)
3. Created `.venv/` with those exact packages

Maria's environment is now byte-for-byte identical to yours.

### She Runs Your Code

```bash
uv run python src/scraper.py
```

**Output:**
```
Scraping https://example.com...
Found 42 items
Saved to results.json
```

Perfect. No "works on my machine" problems.

---

## Real-World Scenario 3: Adding a New Dependency Mid-Project

Two weeks later, Maria needs `pandas` for data analysis.

### Maria Adds the Dependency

```bash
uv add pandas
```

**Output:**
```
Resolved 52 packages in 0.40s
Downloaded 52 packages in 0.31s
Installed 52 packages in 0.12s
```

UV updates both `pyproject.toml` and `uv.lock` with pandas and its 50+ dependencies.

### Maria Commits

```bash
git add pyproject.toml uv.lock
git commit -m "Add pandas for data analysis"
```

### You Pull and Sync

```bash
git pull
uv sync
```

Now you have pandas too, with the exact same version Maria has.

---

## Real-World Scenario 4: Production Deployment

When deploying to production, you don't need dev tools (pytest, black, etc.). Use:

```bash
uv sync --no-dev
```

This installs only production dependencies (`requests`, `beautifulsoup4`, `pandas`) and skips dev tools. Keeps your production environment lean, fast, and secure.

---

## Lockfile Updates: When and Why

### Scenario 1: Adding a New Dependency

When you run `uv add new-package`, UV **automatically updates `uv.lock`**:

```bash
uv add requests
# uv.lock is updated automatically
git add pyproject.toml uv.lock
git commit -m "Add requests"
```

### Scenario 2: Updating Existing Packages

After months, you want to update dependencies:

```bash
# Check what's available
uv pip compile --upgrade pyproject.toml

# Actually update (test thoroughly before committing!)
uv lock --upgrade
```

This re-resolves dependencies with latest versions (respecting constraints in `pyproject.toml`) and updates `uv.lock`.

---

## Onboarding a New Team Member

New developer Alex joins the team:

```bash
# Step 1: Clone
git clone https://github.com/yourorg/web-scraper.git
cd web-scraper

# Step 2: Sync (recreates exact environment)
uv sync

# Step 3: Verify
uv run pytest
```

In 30 seconds, Alex has your exact environment. If tests pass, they're ready to develop.

---

## Handling Lockfile Conflicts (Advanced)

**Scenario**: You added `package-a` on your branch. Maria added `package-b` on hers. Now `uv.lock` has a Git conflict.

**Fix:**
```bash
# Don't manually edit uv.lock. Instead:
git merge --abort  # Undo merge
git pull           # Get latest
uv lock            # Regenerate lockfile with all changes
git add uv.lock
git commit -m "Merge dependencies from both branches"
```

**Why:** `uv lock` re-resolves all dependencies and creates a consistent lockfile automatically. Never manually edit `uv.lock`.

---

## Git Integration: What to Commit, What to Ignore

Here's the complete picture of what goes to Git and what doesn't:

| File/Directory | Commit? | Why |
|---|---|---|
| `pyproject.toml` | ✅ **YES** | Project configuration; needed for dependency resolution |
| `uv.lock` | ✅ **YES** | Exact versions; needed for reproducibility |
| `.python-version` | ✅ **YES** | Python version specification; needed for consistency |
| `src/` | ✅ **YES** | Your code |
| `.venv/` | ❌ **NO** | Environment directory; 50+ MB, recreated by `uv sync` |
| `__pycache__/` | ❌ **NO** | Python cache; recreated when code runs |
| `*.pyc` | ❌ **NO** | Compiled bytecode; recreated automatically |
| `.env` | ❌ **NO** (with care) | Secrets; use `.env.example` instead |

UV creates `.gitignore` automatically when you run `uv init`, so most of this is handled for you.

---

## The Collaboration Workflow Summary

Here's the complete team workflow with UV:

```
Developer A (You):
1. Create project with uv init
2. Add dependencies with uv add
3. Code and test
4. Commit pyproject.toml + uv.lock to Git

Developer B (Teammate):
1. Clone repository (gets pyproject.toml + uv.lock)
2. Run uv sync (recreates exact environment)
3. Code and test in identical environment
4. Add new dependency with uv add
5. Commit updated pyproject.toml + uv.lock

Developer C (New Team Member):
1. Clone repository
2. Run uv sync (3-second setup)
3. Run uv run pytest (verify everything works)
4. Start developing
```

No environment mismatches. No "works on my machine" problems. Every developer, every branch, every deployment—identical environment.

---

## Try With AI

Use your AI companion (ChatGPT, Claude Code, Gemini CLI, etc.) for these exercises.

### Prompt 1: Understanding Lockfiles

```
Explain the difference between pyproject.toml and uv.lock. Why do we need both files? What happens if my teammate only has pyproject.toml without the lockfile?
```

**Expected outcome:** You'll understand that `pyproject.toml` defines constraints (flexible) while `uv.lock` pins exact versions (reproducible), and why both are essential for team collaboration.

### Prompt 2: Simulating Team Workflow

```
I have a UV project with requests==2.31.0. My teammate Maria adds pandas to the project and commits both pyproject.toml and uv.lock. Walk me through the complete workflow:
1. What did Maria do?
2. What do I need to do after pulling her changes?
3. How do we verify we have the same environment?
```

**Expected outcome:** You'll understand the complete cycle: add dependency → commit both files → pull → sync → verify.

### Prompt 3: Handling Lockfile Conflicts

```
I added package-a on my branch. My teammate added package-b on their branch. Now we have a Git merge conflict in uv.lock. How do I resolve this safely? Why shouldn't I manually edit the lockfile?
```

**Expected outcome:** You'll learn to use `uv lock` to regenerate the lockfile instead of manually editing it during conflicts.

