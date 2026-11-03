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
6. **Multi-State 6-File OpenXML `.ZIP` Jurisdiction Parity & Zero-Hallucination Gate (`api_gateway/routers/camber_autopilot.py` & `build_cloudflare_edge_worker.py`):**
   - `compile_full_bid_package` (both `POST` and `GET /v1/camber-autopilot/compile-bid-package`) must dynamically match any requested `project_id` or `state_code` (`TX`, `CA`, `FL`, `VA`, `PA`, `NY`, `IL`, `GA`, `NC`, `OH`, `US`, `MU`) and preserve custom `req.project_id` identifiers across all 6 files.
   - Every Volume V Public Records & FOIA Bid-Tab Request Letter inside the `.ZIP` must cite the exact jurisdiction's open-records statute (`STATE_OPEN_RECORDS_AUTHORITIES`) — never leak Texas Government Code Chapter 552 into non-Texas jurisdictions.
   - Zero fake or placeholder contractor names (`"Apex Civil"`, `"Granite State Paving"`, `"Acme Corp"`, `"Sample LLC"`, `"Placeholder"`, `"TBD"`).
   - `build_cloudflare_edge_worker.py` must pre-compile `.ZIP` archives for all 12 seed lettings (`PRECOMPILED_ZIPS_BY_PROJECT`) and serve the exact project/state-matched `.ZIP` at the edge.
7. **Root-Domain Edge Gateway Routing (`https://camberdesk.com/v1/*` & `https://camberdesk.com/mcp`) & 50-State Proof Workbench Parity:**
   - All API calls, `.ZIP` compiler links, MCP server URLs, health checks, and telemetry endpoints must route through `https://camberdesk.com` (never reference unresolvable `api.camberdesk.com`).
   - All interactive state dropdowns (`#lead-magnet-state`, `#wb-vault-state`, `#wb-dbe-state`) and JS preview handlers (`runCheckoutFoiaVaultPreview()`, `runCheckoutDbeClearinghousePreview()`) must support all **50 U.S. State DOTs**.
   - Never leak internal backend framework names (`"FastAPI"`, `"Supabase"`, `"Render"`) into customer-facing HTML text.
8. **Outbound Deliverability, Warmed-Mailbox Guard, In-Flight Sequence Protection & Quoted-Thread Stripping:**
   - **Strict Warmed-Mailbox Guard (`outbound_mailer.py`):** `is_mailbox_warmed_and_healthy()` must strictly enforce `score >= min_score` (never allow `score == 0` fallback).
   - **In-Flight Sequence Protection (`sync_instantly_campaign.py`):** Never delete active Instantly leads that have already been emailed (`status in (1, 2)` or `email_open_count > 0`) during campaign sync unless they violate cross-brand isolation or contain forbidden `$`/`http`.
   - **Quoted-Thread Stripping (`outbound_reply_responder.py`):** Always strip quoted email history (`_strip_quoted_thread()`) before running opt-out keyword detection or positive-reply classification so our own footer's `"reply stop or unsubscribe"` never triggers false-positive unsubscribes on positive prospect replies.
   - **Zero-Bounce & Zero-Link Cold Email Gate (`outreach_generator.py`, `mlot_sniper_generator.py`):** Every prospect must have a verified live `source_url`, valid MX record, zero `$` signs (use `USD `), and zero `http://` or `https://` links in cold email bodies.
9. **Self-Serve Stripe Checkout Modal & Deep-Link Routing (`index.html`, `api_gateway/routers/billing_webhook.py`):**
   - Navigating to `/?plan=tier1..tier4&billing=monthly|annual#checkout` must automatically open the self-serve checkout modal, and `POST /v1/billing/create-checkout-session` must accept both `{ plan, billing, email }` and `{ tier, customer_email, company_name, state_dots }`.

10. **Mandatory Zero Unnecessary AI Token Waste & Nightly Omniscient Screening Rule (`RULE-009-ZERO-UNNECESSARY-AI-TOKEN-WASTE`):**
   - **Pre-Database & Deterministic Fast-Pass Filtering:** Never invoke Anthropic LLMs (`messages.create`) on contract/letting URLs already stored in the database or on pre-vetted deterministic notices; always pre-filter against existing URLs and deterministic regex filters first so LLM tokens are spent exclusively on net-new, unseen records and live customer requests.
   - **Zero-Token Verification & Telemetry Caching:** Integrity and quality-control test suites must always set `use_llm_synthesis=False` (zero live LLM calls during tests), and repeat RapidAPI health/telemetry probes must be served from an in-memory SHA-256 response cache at `$0.00` token cost.
   - **Once-Per-Night Omniscient Screening (`_LAST_OMNISCIENT_AUDIT_DATE`):** `silent_camberdesk_watcher.py` and `d:\Daas\omniscient_auditor.py` must screen CamberDesk (`d:\CamberDesk\omniscient_auditor.py`) at most **once per calendar night** during the nighttime user-away window (`11:00 PM ? 6:00 AM`, `>= 15m` idle), never in an un-gated 15-minute loop.

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
- **`RULE-021-QUOTED-THREAD-AND-WARMUP-GUARD` [Pillar 2: Outbound Deliverability] (2026-10-31):** Strip quoted email history (`_strip_quoted_thread()`) before opt-out/reply classification in `outbound_reply_responder.py`, and strictly require `score >= min_score` (never `score == 0`) in `outbound_mailer.py`. *(Enforced by `check_conversion_and_distribution_surfaces`)*
- **`RULE-022-IN-FLIGHT-SEQUENCE-PROTECTION` [Pillar 2: Campaign Sync] (2026-10-31):** Never delete active in-flight Instantly leads (`status in (1, 2)` or `email_open_count > 0`) during `sync_instantly_campaign.py` runs unless they violate cross-brand isolation or contain `$`/`http`. *(Enforced by `check_conversion_and_distribution_surfaces`)*
- **`RULE-023-MULTI-STATE-ZIP-ANTI-HALLUCINATION` [Pillar 1: 6-File .ZIP Compiler] (2026-10-31):** Preserve custom `project_id` and dynamically populate jurisdiction-matched Open Records statutes (`STATE_OPEN_RECORDS_AUTHORITIES`), DOT pay items, Davis-Bacon wages, and real planholders across all states with zero fake contractor names (`Apex Civil`, `Granite State Paving`). *(Enforced by `check_product_output_quality_controls`)*
- **`RULE-024-ROOT-DOMAIN-EDGE-AND-50-STATE-WORKBENCH` [Pillar 3: Website & Edge Gateway] (2026-10-31):** Route all API, MCP, `.ZIP`, and telemetry endpoints through `https://camberdesk.com` (never `api.camberdesk.com`), and populate all 50 U.S. State DOT options in `#lead-magnet-state`, `#wb-vault-state`, and `#wb-dbe-state`. *(Enforced by `check_portal_parity_and_telemetry`)*
- **`RULE-025-CUSTOMER-FACING-COPY-DISCIPLINE` [Pillar 3: Visual & Brand Standards] (2026-10-31):** Never leak internal backend framework names (`FastAPI`, `Supabase`, `Render`) or raw JS escape artefacts into customer-facing HTML text. *(Enforced by `check_html_file`)*
- **`RULE-FRONTIER-MODEL-ONLY` [System Integrity] (2026-11-01):** Always use the frontier Anthropic model (`claude-sonnet-5-5`) across all scrapers, `camberdesk_autopilot.py`, `outbound_reply_responder.py`, and `llm_extractor.py`; never use retired models. *(Enforced by `check_frontier_model_strings`)*
- **`RULE-009-ZERO-UNNECESSARY-AI-TOKEN-WASTE` [Cost Discipline & LLM Efficiency] (2026-11-01):** Never spend Anthropic LLM tokens on already-stored database records, deterministic test suites (`use_llm_synthesis=False`), repeat RapidAPI telemetry probes (use SHA-256 response cache), or >1x/night background auditor runs. *(Enforced by `check_zero_ai_token_waste`)*
- **`RULE-INLINE-JS-SYNTAX` [System Integrity] (2026-11-01):** Every inline `<script>` block and `on*` event attribute in `index.html`, `apis.html`, and generated `/lettings/**/*.html` must pass Node.js `vm.Script` compilation with zero unescaped quotes. *(Enforced by `check_html_inline_js_vm`)*
- **`RULE-DELIVERABILITY-DNS-AUTH` [System Integrity] (2026-11-01):** Outbound email infrastructure must maintain valid SPF, DMARC (`p=quarantine`/`reject`), BIMI SVG logo, MX records on all prospect domains, and zero duplicate follow-ups. *(Enforced by `check_email_deliverability_dns`)*
- **`RULE-026-BRANDED-STRIPE-CHECKOUT-ISOLATION` [Cross-Brand Isolation & Checkout Branding] (2026-11-03):** Never use `buy.stripe.com` Payment Links in CamberDesk; always use branded `checkout.stripe.com/c/pay/cs_live_...` sessions with `order_summary_display_name == 'CamberDesk'` and zero `signaltender` strings in `payment_pages/init`. *(Enforced by `check_tier_value_prop_and_capture_moat_parity`)*
<!-- AUTONOMOUS_LEARNED_RULES_END -->

## Mandatory Outbound Campaign Root-Cause Prevention & Self-Healing Rule (`RULE-014`)
Every outbound cold email pipeline and 5-minute silent watcher across `SignalTender` (`d:\Daas`), `CamberDesk` (`D:\CamberDesk`), and `RubricWard` (`D:\RubricWard`) **MUST** automatically detect and self-heal all 4 outbound conversion root causes without waiting for user intervention:
1. **Root Cause #1 (Zero Non-IT / Physical / Medical / Social Contract Pollution in SignalTender):** Never use bare `r"system"`, `r"infrastructure"`, or `r"network"` regexes in `outreach_generator.py` or `pseo_generator.py`; require compound IT/Cyber/Cloud/Software terms and actively exclude physical/construction/medical/social solicitations. `auto_error_healer.py` must automatically inspect `campaign_leads.csv` and heal any non-IT contract reference.
2. **Root Cause #2 (Zero NSF SBIR `541715` R&D Grant Startups in SignalTender):** `govcon_lead_harvester.is_verified_it_cyber_prospect()` must strictly reject any prospect with `"sbir"`, `"sttr"`, or `"nsf"` in `Keywords` or `541715`-only NAICS, and `autonomous_outbound_optimizer.py` must automatically purge any non-IT/SBIR leads from both local CSVs and the live Instantly campaign.
3. **Root Cause #3 (Fast 1-Day / 2-Day Follow-Up Cadence & Concrete Value Anchor in Step 1 & Step 2):** All 3 Instantly campaigns must enforce `delay: 1` day on Step 2 and `delay: 2` days on Step 3, and every Step 1 & Step 2 email (including RubricWard's primary slice) must include the concrete state/cohort benchmark figure (`below the 75th-percentile regional in-network MRF benchmark` / DOT unit-bid spread / agency solicitation).
4. **Root Cause #4 (Zero Receptionist `info@` Score Inversion or Warmed-Slot Dilution):** `_score_scraped_email()` must penalize generic receptionist prefixes (`info@`, `contact@`, `office@`, `hello@`, `admin@`, `inquiries@`) below named executives (`jsmith@`, `first.last@`) and department desks (`estimating@`, `bids@`, `billing@`, `rcm@`, `managedcare@`), `_async_crawl_one()` must crawl subpages whenever the homepage only yields a generic `info@` address, and `sync_instantly_campaign.py` must exclude `is_receptionist_or_generic_inbox()` from Instantly uploads.
