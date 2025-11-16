<!-- Claude is Work to Build this Project -->
---
original_path: 04-Python-Fundamentals/12-python-uv-package-manager/05-running-code-in-uv-projects-with-ai.md
chapter: 04-Python-Fundamentals
difficulty: intermediate
read_time: 30
generated: 2025-11-15
---

# Summary

Running Python code in UV projects centers on understanding environment isolation and the magic of `uv run`. Environment isolation solves the dependency conflict problem where different projects need different versions of the same library by giving each project its own separate package toolbox. The `uv run` command automatically activates the project environment, executes code with access to project dependencies, and handles everything invisibly without manual activation commands. This contrasts sharply with system Python, which lacks access to project-specific packages. The lesson demonstrates the difference: running `python script.py` fails with ModuleNotFoundError while `uv run python script.py` succeeds by using the isolated environment. This pattern applies universally to scripts, tests with pytest, and web servers—always prefix commands with `uv run` to ensure proper isolation. Side-by-side comparisons show how multiple projects maintain different library versions simultaneously without conflicts, proving isolation's value. Common errors like ModuleNotFoundError typically indicate missing dependencies or forgetting the `uv run` prefix. The lesson establishes that professional Python development requires environment isolation as non-negotiable, with UV making it automatic and transparent through intelligent command wrapping.

## Key Concepts

- Environment isolation prevents dependency conflicts by giving each project separate package storage with different library versions
- uv run automatically activates project environments without manual commands, providing transparent access to project dependencies
- System Python lacks project packages, causing ModuleNotFoundError when scripts import project dependencies without uv run
- Universal execution pattern applies to all scenarios: prefix commands with uv run for scripts, tests, and servers
- Multiple projects coexist with different library versions simultaneously due to isolated virtual environments preventing overwrites
