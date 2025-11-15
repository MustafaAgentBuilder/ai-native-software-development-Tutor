---
original_path: 04-Python-Fundamentals/12-python-uv-package-manager/03-creating-first-uv-project-with-ai.md
chapter: 04-Python-Fundamentals
difficulty: intermediate
read_time: 20
generated: 2025-11-15
---

# Summary

Creating a UV project introduces the foundational concepts of Python project structure and dependency management. A Python project is an organized folder containing code and configuration files that define dependencies. UV's `uv init` command generates a complete project structure in under one second, including pyproject.toml for modern configuration, .python-version for Python version pinning, main.py as the starter script, and a virtual environment (.venv/) for isolated package storage. The pyproject.toml file represents Python's modern standard, replacing the legacy requirements.txt approach with richer metadata and dependency specification capabilities. Virtual environments solve the critical problem of dependency isolation—allowing different projects to use different versions of the same library without conflicts. UV automates virtual environment creation and management, making isolation invisible to developers. Adding dependencies via `uv add` updates both pyproject.toml (specification) and uv.lock (exact versions), ensuring reproducibility. The lesson distinguishes between dependency specification (declaring what you need) and installation (actually obtaining packages), emphasizing that pyproject.toml is committed to version control while .venv/ is recreated locally by each developer.

## Key Concepts

- Python projects organize code and configuration in structured folders with pyproject.toml as the brain defining dependencies
- Virtual environments provide isolated package storage, preventing conflicts between projects needing different library versions
- pyproject.toml represents modern Python standard, offering richer configuration than legacy requirements.txt files
- UV automates project initialization and virtual environment management, making complex tasks simple and fast
- Dependency specification (pyproject.toml) and installation (.venv/) are separate concepts with different purposes in team workflows
