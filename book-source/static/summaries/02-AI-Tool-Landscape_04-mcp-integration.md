---
original_path: docs/02-AI-Tool-Landscape/05-claude-code-features-and-workflows/04-mcp-integration.md
chapter: 02-AI-Tool-Landscape
difficulty: intermediate
read_time: 12-15 min
generated: 2025-11-15
---

# Summary

Model Context Protocol (MCP) extends Claude Code's capabilities beyond local file access to external systems, solving the limitation that Claude can only see files on your computer by default. MCP functions as a standardized connection system enabling Claude Code to safely access websites, documentation, databases, and APIs through specialized server helpers. Each MCP server acts as a domain specialist: Playwright MCP for web browsing, Context7 MCP for up-to-date documentation, GitHub MCP for repository queries, and Database MCP for database access.

Security considerations are paramount because unlike local file operations, MCP servers can access internet, APIs, and external systems. Safe practices include using only trusted MCP servers (widely used, reputable sources), storing tokens and secrets in system keychain rather than plain text, and never pasting secrets into files. The lesson demonstrates adding two beginner-friendly servers: Playwright MCP for web browsing (`claude mcp add --transport stdio playwright npx @playwright/mcp@latest`) and Context7 MCP for documentation (`claude mcp add --transport stdio context7 npx @upstash/context7-mcp`).

Practical workflows showcase MCP's power: the shopping workflow uses Playwright to browse Amazon, find products matching preferences, extract details, and return structured information with natural iteration capability ("filter to long-sleeve" or "show only Prime-eligible"). The documentation workflow leverages Context7 to fetch current official documentation, summarize key concepts, and provide citations with links, effectively creating a "know about anything new" button for staying current without manual website searching.

MCP unlocks external access systematically, transforming Claude Code from local-only tool to integrated system capable of reaching beyond computer boundaries. The strategic value lies in knowing when to use MCP versus local file operations: anytime information or capabilities exist outside your computer (current documentation, website data, external APIs, database queries), MCP provides the bridge while maintaining security through approved, standardized connections rather than unrestricted access.

## Key Concepts

- MCP as standardized bridge: Connects Claude Code to external tools and data sources through safe, approved specialist servers
- Security-first approach: Use trusted servers, store credentials in system keychain, audit permissions before granting access
- Playwright MCP workflow: Browse websites, extract information, navigate pages naturally with iterative refinement commands
- Context7 MCP workflow: Fetch up-to-date library and API documentation with summaries, citations, and authoritative links
- External access use case: Anytime needed information or capabilities live outside local computer (docs, websites, APIs, databases)
