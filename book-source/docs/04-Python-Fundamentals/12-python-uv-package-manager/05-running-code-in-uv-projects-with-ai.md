<!-- Claude is Work to Build this Project -->
---
title: "Running Python Code in UV Projects with AI"
chapter: 12
lesson: 5
duration_minutes: 30

# HIDDEN SKILLS METADATA (Institutional Integration Layer)
# Not visible to students; enables competency mapping and differentiation
skills:
  - name: "Execute Python in Isolated Environments"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Content Creation"
    measurable_at_this_level: "Student can run Python scripts and tests in project-specific environments using `uv run`, understanding that UV automatically isolates code from system-wide packages"

  - name: "Understand Virtual Environment Isolation"
    proficiency_level: "B1"
    category: "Conceptual"
    bloom_level: "Understand"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can explain why environment isolation prevents conflicts between projects, demonstrate the difference between `uv run python` and system `python`, and troubleshoot module-not-found errors"

  - name: "Run Tests with Pytest"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Content Creation"
    measurable_at_this_level: "Student can execute pytest tests in a UV project environment using `uv run pytest` and interpret test results"

learning_objectives:
  - objective: "Execute Python scripts and tests in project environments by expressing intent to Claude Code or Gemini CLI"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student successfully runs multiple scripts (main.py, test files, web servers) using `uv run` with AI assistance"

  - objective: "Explain why environment isolation matters and demonstrate the difference between uv run and system Python"
    proficiency_level: "B1"
    bloom_level: "Understand"
    assessment_method: "Student articulates isolation benefits in plain language and shows concrete difference when running code with vs. without `uv run`"

  - objective: "Troubleshoot module-not-found errors and environment-related issues using AI"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student diagnoses and fixes at least one environment error with AI assistance"

  - objective: "Run tests with pytest in project environment"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student executes `uv run pytest` and interprets test output"

cognitive_load:
  new_concepts: 7
  assessment: "7 new concepts: (1) uv run command, (2) environment isolation, (3) automatic activation, (4) running scripts vs. modules, (5) pytest workflow, (6) environment debugging, (7) isolation benefits. Within B1 limit of 10 concepts. ✓"

differentiation:
  extension_for_advanced: "Explore environment variables with UV; create custom scripts that validate environment state; automate multi-file test runs"
  remedial_for_struggling: "Focus on core concept: 'uv run means use this project's packages.' Use analogy: separate toolboxes for each project. Let AI handle all commands."

# Generation metadata
generated_by: "lesson-writer v3.1.0"
source_spec: "specs/011-python-uv/plan.md"
created: "2025-11-13"
last_modified: "2025-11-13"
git_author: "Claude Code"
workflow: "/sp.implement"
version: "1.0.0"
---

# Running Python Code in UV Projects with AI

## Why Environment Isolation Matters

Before you run any Python code in a UV project, you need to understand one critical concept: **environment isolation**.

Imagine you're working on two different projects:
- **Project A**: Needs `requests` version 2.28 to work correctly
- **Project B**: Needs `requests` version 2.31 for some new features

If you installed packages globally (the old way), installing version 2.31 for Project B would break Project A. This is called the **"dependency conflict" problem**, and it's one of the main reasons virtual environments exist.

**UV solves this with automatic environment isolation:**
- Each UV project gets its own separate "toolbox" of packages
- Project A's packages don't affect Project B
- You can have different versions of the same library in different projects
- No conflicts, no "works on my machine but not on yours" problems

The command `uv run` is what activates this isolation automatically. When you type `uv run python script.py`, UV:
1. Checks if the project has a virtual environment set up
2. Activates that environment (without you typing activation commands)
3. Runs your script in that isolated environment
4. Everything just works

This is the core difference between `uv run python` and just typing `python` at your terminal.

## The Difference: `uv run` vs. System Python

Let's see this in action.

**Scenario**: You have a project with the `requests` library installed via UV. Your system doesn't have `requests` installed globally.

### Without `uv run` (fails):

```bash
python -c "import requests; print(requests.__version__)"
```

**Result:**
```
ModuleNotFoundError: No module named 'requests'
```

Why? You're using system Python, which doesn't have your project's packages.

### With `uv run` (works):

```bash
# This uses UV's project environment instead of system Python
uv run python -c "import requests; print(requests.__version__)"
```

**Output:**
```
2.31.0
```

**What happened:**
- `uv run` activated your project's isolated environment
- Python accessed the `requests` library from that environment
- **No manual activation needed**—UV handles everything

## Running Scripts in Your Project

Now let's run actual Python scripts stored in your project.

### Scenario 1: Running a Simple Script

You have a file called `main.py` in your project that uses the `requests` library.

**main.py:**
```python
import requests

# Fetch data from a public API
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
print(f"Status: {response.status_code}")
print(f"Title: {response.json()['title']}")
```

**Run it:**
```bash
uv run python main.py
```

**Expected Output:**
```
Status: 200
Title: sunt aut facere repellat provident occaecati excepturi optio reprehenderit
```

**What happened:**
1. `uv run` activated your project environment
2. Python executed `main.py`
3. The `requests` library was available (from your project, not system)
4. The API call succeeded and printed results


## Running Tests with Pytest

First, ensure pytest is installed (from Lesson 4):

```bash
uv add --dev pytest
```

Create a test file `test_math.py`:

```python
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
```

**Run tests:**

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest test_math.py

# Run with verbose output
uv run pytest -v
```

**Expected Output:**
```
test_math.py::test_add PASSED                                      [100%]
1 passed in 0.03s
```

## Environment Isolation in Action: Side-by-Side Comparison

Let's make the isolation concept crystal clear with a concrete example.

**Project A** (`web-client/`):
```bash
cd web-client
uv add requests==2.28.0
uv run python -c "import requests; print(requests.__version__)"
# Output: 2.28.0
```

**Project B** (`data-processor/`):
```bash
cd ../data-processor
uv add requests==2.31.0
uv run python -c "import requests; print(requests.__version__)"
# Output: 2.31.0
```

**Back to Project A:**
```bash
cd ../web-client
uv run python -c "import requests; print(requests.__version__)"
# Output: 2.28.0 (unchanged - Project A's version still safe)
```

**Without UV** (old approach):
```bash
pip install requests==2.28.0  # Install globally
pip install requests==2.31.0  # Overwrites global version!
python -c "import requests; print(requests.__version__)"
# Output: 2.31.0 (Project A breaks because global version changed)
```

This is why environment isolation is non-negotiable in professional development.

## Common Execution Errors

### Error 1: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'requests'
```

**Fix:**
```bash
# Add the missing package
uv add requests

# Run your script again
uv run python your_script.py
```

### Error 2: Permission Denied (Mac/Linux)

```
bash: ./my_script.py: Permission denied
```

**Fix:**
```bash
# Don't run scripts directly - use uv run
# ❌ This fails: ./my_script.py
# ✅ This works:
uv run python my_script.py
```

**When to use AI:** For complex errors or debugging test failures, ask your AI tool to analyze the error message and suggest solutions.

## Running Web Servers (Optional)

You can use `uv run` to start web servers with hot reload:

```bash
# Add web framework
uv add fastapi uvicorn

# Start development server with auto-reload
uv run uvicorn main:app --reload
```

The `--reload` flag restarts the server automatically when you save code changes—useful for development, but don't use in production.


## Key Takeaways (For Your Mental Model)

1. **`uv run` is magic** — It activates your project environment automatically. No manual activation commands needed.

2. **Isolation prevents conflicts** — Each project has its own package versions. Changing one project doesn't break another.

3. **AI is your execution partner** — Tell your AI tool what you want to run; it provides the command. You focus on understanding, not syntax.

4. **Scripts, tests, servers—same pattern** — Whether running `main.py`, `pytest`, or `uvicorn`, the pattern is the same: `uv run <command>`

5. **Errors are learning opportunities** — ModuleNotFoundError, version mismatches, permission issues—all are solvable with AI guidance.

6. **Environment isolation is non-negotiable** — Professional Python development requires it. UV makes it invisible and automatic.

---

## Try With AI

Use your AI companion (ChatGPT, Claude Code, Gemini CLI, etc.) for these exercises.

### Prompt 1: Understanding Environment Isolation

```
Explain why `python main.py` fails but `uv run python main.py` works when my script imports requests. What is environment isolation and why does it matter?
```

**Expected outcome:** You'll understand how `uv run` activates your project environment and why bare `python` doesn't have access to project packages.

### Prompt 2: Debugging a Failed Test

```
I have a test that's failing with this error:
test_math.py::test_divide FAILED
AssertionError: assert 4.0 == 4

What does this mean? How do I fix it? Explain the difference between float and integer comparison in Python tests.
```

**Expected outcome:** You'll learn how to read test output and work with AI to diagnose and fix test failures.

### Prompt 3: Multi-Project Isolation

```
I have two UV projects on my computer:
- project-a needs requests==2.28.0
- project-b needs requests==2.31.0

Show me how UV keeps these isolated so they don't conflict. Create a demonstration showing both projects maintaining their own versions.
```

**Expected outcome:** You'll see concrete proof that environment isolation prevents version conflicts between projects.
