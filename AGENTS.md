# CamberDesk Workspace Agent Rules (`AGENTS.md`)

## Project Overview
**CamberDesk** (`https://camberdesk.com`) is an autonomous B2B Construction Preconstruction, 50-State DOT Heavy-Civil Letting, Historical Unit-Price Bid Tabulation, Davis-Bacon Prevailing Wage, and CSI MasterFormat Specification Compiler DaaS & API Ecosystem.

---

## Non-Negotiable Architectural & Engineering Rules

1. **STRICT READ-ONLY LOCK ON SIGNALTENDER (`d:\Daas` and `d:\Data API Ecosystem`) — ZERO MODIFICATIONS ALLOWED:**
   - **NEVER** create, edit, overwrite, format, rename, delete, or commit any file inside `d:\Daas` or `d:\Data API Ecosystem`.
   - You may **ONLY** read files from `d:\Daas` or `d:\Data API Ecosystem` (or invoke `D:\Daas\daas_env\Scripts\python.exe` as a read-only Python interpreter to run scripts located inside `D:\CamberDesk`).
   - All new code, configs, static pages, scripts, assets, and git operations for CamberDesk **MUST** reside exclusively inside `D:\CamberDesk`.
2. **Latest Frontier Anthropic Model Rule (`claude-sonnet-5-5`):**
   - Always use `claude-sonnet-5-5` across all scrapers, `camberdesk_autopilot.py`, and `api_gateway/services/llm_extractor.py`.
   - Never hardcode secrets or API keys; always load from `.env` via `os.getenv()`.
3. **Stateless FastAPI Microservice Gateway & 5/5 Glama TDQS MCP Standard (`api_gateway/`):**
   - All 12 construction/DOT endpoints and the Master 6-File `.ZIP` Bid-Tab Compiler (`/v1/camber-autopilot/compile-bid-package`) must use strict **Pydantic V2** (`ConfigDict`, `model_dump()`, `Field` constraints).
   - Both the Remote Streamable-HTTP MCP server (`/mcp`) and the Local STDIO MCP server (`mcp-server/index.js`) must maintain a **5/5 Glama Tool Definition Quality Score (TDQS)**:
     - Zero `"API #XX:"` prefixes in tool descriptions.
     - Explicit `title`, `annotations` (`readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false`), and typed `outputSchema` + `structuredContent`.
     - 100% documented `inputSchema.properties` with descriptions, defaults, and min/max constraints.
     - 3-part descriptions with explicit sibling-tool routing disambiguation.
4. **100% Catalog & Portal Parity (`index.html` <-> `apis.html` <-> `pseo_generator.py`):**
   - Coverage spans **52 Active Portals** (**All 50 U.S. State DOT & State Construction Portals** + **Federal USACE / SAM.gov NAICS 236–238** + **Municipal Public Works**).
   - Feature copy must use simplified **50-State DOT & Public Works** phrasing inline while keeping full 52-portal cards in dedicated coverage surfaces.
   - Zero emojis anywhere on the site; use crisp SVG engineering icons and typographic symbols.
   - Always verify the entire repository via `python verify_camberdesk_integrity.py`.

