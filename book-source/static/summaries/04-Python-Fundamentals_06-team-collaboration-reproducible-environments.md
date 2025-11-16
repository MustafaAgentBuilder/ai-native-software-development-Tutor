<!-- Claude is Work to Build this Project -->
---
original_path: 04-Python-Fundamentals/12-python-uv-package-manager/06-team-collaboration-reproducible-environments.md
chapter: 04-Python-Fundamentals
difficulty: intermediate
read_time: 30
generated: 2025-11-15
---

# Summary

Team collaboration and reproducible environments solve the "works on my machine" problem through careful management of configuration files and version control integration. The two-file system distinguishes between pyproject.toml (flexible constraints like ">=2.31.0") and uv.lock (exact pinned versions like "==2.32.1"), balancing flexibility during development with reproducibility across teams. When teammates clone a project, running `uv sync` recreates the exact environment from uv.lock in seconds, ensuring byte-for-byte identical package versions. Git integration requires committing both pyproject.toml and uv.lock while excluding .venv/ (too large, recreatable) and cache files. The collaborative workflow demonstrates how developers add dependencies, commit updated lockfiles, and teammates sync to matching environments seamlessly. Production deployments use `uv sync --no-dev` to install only runtime dependencies, keeping deployments lean and secure. Lockfile conflicts arise when multiple developers modify dependencies on different branches; resolution involves regenerating the lockfile with `uv lock` rather than manual editing. The lesson establishes that onboarding new team members takes under 30 seconds with UV (clone, sync, verify), eliminating the traditional multi-hour environment setup. This reproducibility extends from local development through CI/CD pipelines to production, ensuring consistency everywhere.

## Key Concepts

- Two-file system separates flexible constraints (pyproject.toml) from exact versions (uv.lock) for development flexibility with team reproducibility
- uv sync recreates exact environments from lockfiles in seconds, ensuring byte-for-byte identical packages across all team members
- Git workflow commits configuration files (pyproject.toml, uv.lock) while excluding recreatable directories (.venv/) and cache
- Production deployments use --no-dev flag to install only runtime dependencies, excluding testing and development tools
- Lockfile conflicts require regeneration via uv lock command rather than manual editing, ensuring dependency resolution integrity
