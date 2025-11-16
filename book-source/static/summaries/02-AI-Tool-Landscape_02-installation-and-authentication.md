<!-- Claude is Work to Build this Project -->
---
original_path: docs/02-AI-Tool-Landscape/05-claude-code-features-and-workflows/02-installation-and-authentication.md
chapter: 02-AI-Tool-Landscape
difficulty: beginner
read_time: 8-10 min
generated: 2025-11-15
---

# Summary

Installing and authenticating Claude Code bridges the gap from conceptual understanding to practical usage. The process requires terminal access (Command Prompt, PowerShell, Windows Terminal on Windows; Terminal app on macOS; any terminal emulator on Linux) and a Claude account (either Claude.ai subscription for Pro/free tier or Claude Console account with API credits for developers).

Installation offers four methods tailored to different operating systems and preferences: official installer script via curl for macOS/Linux, Homebrew package manager for macOS users, PowerShell script for Windows systems, or npm global installation for cross-platform compatibility with Node.js 18+. After installation, verification requires running `claude --version` to confirm successful setup.

Authentication follows two paths depending on account type. Claude.ai authentication (most common for individual users) involves running `claude`, selecting the subscription login option, authenticating through the browser, and confirming successful connection. Claude Console authentication (for developers with API access) requires obtaining an API key from console.anthropic.com, pasting it when prompted, and setting usage limits to manage costs since Console authentication uses API billing rather than subscription credits.

Security considerations include understanding file system access permissions (Claude can read/write files in directories where it runs), reviewing proposed commands especially sudo or administrative operations, and for Console API users, actively monitoring token usage and setting appropriate spending limits. Best practices emphasize starting Claude Code sessions in project directories rather than system directories, carefully reviewing file changes before approval, and treating Claude Code's approval workflow as a trust-building transparency mechanism where every action is visible and explicit before execution.

## Key Concepts

- Four installation methods: Official curl script, Homebrew, PowerShell, or npm package for cross-platform flexibility
- Two authentication paths: Claude.ai subscription for individual users or Console API key for developers with direct API access
- Security boundaries: File system access limited to session directories with explicit approval workflow for all operations
- Cost management for API users: Setting usage limits and monitoring token consumption to prevent unexpected charges
- Terminal comfort as productivity multiplier: Five minutes learning basic commands unlocks 10x efficiency with AI tools
