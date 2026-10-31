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
5. **Mandatory Cross-Brand Zero-Overlap & Isolation Rule (`CamberDesk` <-> `SignalTender` — Enforced by `check_zero_signaltender_overlap()` in `verify_camberdesk_integrity.py`):**
   - **Zero Prospect Email or Domain Overlap:** `harvest_verified_dot_contacts.py` (`is_excluded_by_signaltender()`) and `mlot_sniper_generator.py` must always load `D:\Daas\verified_public_govcon_contacts.json`, `completed_outreach_archive.json`, `govcon_contacts.csv`, and `campaign_leads.csv` and exclude every SignalTender email and corporate domain. `sync_instantly_campaign.py` must always pass `"skip_if_in_workspace": True` on `POST /api/v2/leads`.
   - **Zero Instantly.ai Mailbox, Campaign, or Unibox Overlap:** All CamberDesk scripts (`autonomous_mailbox_scaler.py`, `sync_instantly_campaign.py`, `outbound_mailer.py`, `outbound_reply_responder.py`, `omniscient_auditor.py`) must filter strictly to `*camberdesk*` mailboxes (`aaron@trycamberdesk.com`, `desk@trycamberdesk.com`, `estimating@trycamberdesk.com`) and never touch `*signaltender*` mailboxes or campaigns.
   - **Zero Discord Webhook Cross-Posting:** CamberDesk must use `CAMBERDESK_DISCORD_WEBHOOK_URL` and must never use SignalTender's `DISCORD_WEBHOOK_URL` (`1555743443802918993`).

---

<!-- AUTONOMOUS_LEARNED_RULES_START -->
## Autonomous Self-Improved Anti-Regression Rules (Auto-Codified by `omniscient_auditor.py` & `auto_error_healer.py`)

The following rules were automatically learned from past detections and fixes. Every future audit and code change **MUST** enforce them:

- **`RULE-001-SILENT-DETECTION-RESOLVED-ONLY` [System Telemetry] (2026-10-31):** Never post raw/open error alerts to Discord; log silently via `report_error()` and notify Discord only via `send_discord_resolution()` after repair and verification. *(Enforced by `check_silent_discord_alert_policy`)*
- **`RULE-002-FRONTIER-CLAUDE-SONNET-5-5` [Pillar 1: Products & LLM Engine] (2026-10-31):** Always use `claude-sonnet-5-5` across all CamberDesk scrapers, autopilot engines, and LLM extractors; never use retired `claude-3-*` or `haiku` models. *(Enforced by `check_frontier_model_strings`)*
- **`RULE-003-GLAMA-5-OF-5-TDQS-MCP` [Pillar 1: MCP Servers] (2026-10-31):** Every MCP tool must have zero `API #XX:` prefixes, explicit `title`, `annotations`, `outputSchema`, 100% documented `inputSchema.properties`, and 3-part sibling disambiguation. *(Enforced by `check_mcp_glama_tdqs`)*
- **`RULE-004-TIER3-OPENXML-LIVE-FORMULAS` [Pillar 1: 6-File .ZIP Compiler] (2026-10-31):** The Tier 3 6-File `.ZIP` Bid Package Compiler must always output valid OpenXML `.docx`/`.xlsx` archives containing live Excel `<f>` formulas. *(Enforced by `check_tier3_openxml_zip_integrity`)*
- **`RULE-005-52-PORTAL-12-API-PARITY` [Pillar 3: Website & Catalog] (2026-10-31):** Maintain 100% count, card, and schema parity across `index.html`, `apis.html`, `pseo_generator.py`, and `cloudflare_worker.js` (52 Portals, 50 State DOTs, 12 APIs). *(Enforced by `check_portal_and_catalog_parity`)*
- **`RULE-006-HIGH-CONTRAST-WARM-VELLUM-THEME` [Pillar 3: Visual & Brand Standards] (2026-10-31):** Enforce Editorial Theme 1 (`#FAF8F5` Warm Vellum & `#0A0D14` Obsidian Ink + `#1E3A8A` Blueprint Navy) with zero emojis and zero washed-out grey classes. *(Enforced by `check_high_contrast_and_zero_emoji`)*
- **`RULE-007-OUTREACH-LIVE-DOSSIER-URLS` [Pillar 2: Customer Acquisition] (2026-10-31):** Every `dossier_url` in `campaign_leads.csv`, `outbox_ready_queue.json`, and Discord feeds must resolve to an existing `/lettings/project/<slug>.html` file. *(Enforced by `check_outreach_dossier_urls`)*
- **`RULE-TIER3-OPENXML-INTEGRITY` [System Integrity] (2026-10-31):** Tier 3 Bid Package `.ZIP` archives must always contain 6 valid OpenXML (`.docx`/`.xlsx`) and `.json` files with well-formed XML and live Excel `=SUM()` and `=D6*G6` formulas. *(Enforced by `check_tier3_openxml_zip_integrity`)*
- **`RULE-PORTAL-CATALOG-PARITY` [System Integrity] (2026-10-31):** Maintain 100% count and card parity across `index.html`, `apis.html`, `pseo_generator.py`, MCP servers, and Cloudflare Edge Worker (`52 Portals / 50 State DOTs` and `12 APIs`). *(Enforced by `check_portal_and_catalog_parity`)*
- **`RULE-008-ZERO-SIGNALTENDER-OVERLAP` [Cross-Brand Isolation] (2026-10-31):** Maintain 100% zero overlap with SignalTender across prospect emails, corporate domains, Instantly.ai campaigns/mailboxes, Discord webhooks, and Supabase credentials. *(Enforced by `check_zero_signaltender_overlap`)*
<!-- AUTONOMOUS_LEARNED_RULES_END -->
