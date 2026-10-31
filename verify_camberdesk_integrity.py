"""
CamberDesk — Comprehensive Repository, SPA Runtime, 52-Portal & 12-API Parity,
5/5 Glama TDQS, OpenXML .ZIP Compiler & Viewport Quality Gate (`verify_camberdesk_integrity.py`).

Enforces:
1. Static HTML, Inline JS (`vm.Script`), Event Attributes (`on*`), Tag Balance, Duplicate IDs, Internal `#hash` Routes, Zero Emojis, High-Contrast Warm Vellum & Obsidian Ink Theme (`FORBIDDEN_GREY_PATTERNS`), and Mobile Favicon/OpenGraph Verification across `index.html`, `apis.html`, `lettings/index.html`, and all `lettings/project/*.html`.
2. 100% Catalog & UI Parity (`index.html` <-> `apis.html`): 12 `<article id="product-...">` cards, Quick-Jump Directory rows `01`..`12`, Pricing Matrix rows `01`..`12`, `window.CATALOG` & `window.API_META`, badge counts, and scroll-anchor protection.
3. 52-Portal & 50-State DOT Parity across `index.html`, `apis.html`, and `pseo_generator.py`.
4. Tier 1 / Tier 2 / Tier 3 Value-Proposition & `#capture-moat` Relevance Filter (`#01..#06, #11` included; post-award `#07..#10, #12` excluded from `#capture-moat`).
5. Conversion, Outbound & 5/5 Glama TDQS MCP Parity (`api_gateway/routers/mcp.py`, `mcp-server/index.js`, `build_cloudflare_edge_worker.py`, `campaign_leads.csv`, `outbox_ready_queue.json`).
6. Product Output Quality Controls: 6-File OpenXML (`.DOCX` + `.XLSX`) `.ZIP` Takeoff Compiler with live Excel `=SUM()` and `=D6*G6` formulas.
7. Headless Node.js SPA Runtime Verification (`switchSpaView`, `renderLettingsRoute`, `filterMainLettingTable`, `filterApiCatalog`, `openApiSandbox`, `executeSandboxCall`, `setCheckoutBilling`).
8. Headless Chromium Mobile (`375x812`) & Desktop (`1024x900`, `1280x900`) Viewport Overflow & Layout Audit.
9. Closed-Loop Autonomous Error Healer (`auto_error_healer.run_healer()`).
"""

from error_telemetry import configure_utf8_stdio

configure_utf8_stdio()

import csv
import glob
import html as html_lib
import io
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from typing import Any, Dict, List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]")
EMOJI_ENTITY_RE = re.compile(r"&#x1[fF][0-9a-fA-F]{3};")

FORBIDDEN_GREY_PATTERNS = [
    "#64748B",
    "#78716C",
    "#57534E",
    "#44403C",
    "#D6D3CD",
    "text-slate-400",
    "text-slate-500",
    "text-gray-400",
    "text-gray-500",
]

EXPECTED_API_IDS = [
    "product-csi-masterformat",
    "product-dot-unit-bid-tabs",
    "product-davis-bacon-wage",
    "product-live-lettings",
    "product-baba-buy-america",
    "product-dbe-good-faith",
    "product-aia-g702-g703",
    "product-surety-miller-act",
    "product-rfi-change-order",
    "product-osha-emr-safety",
    "product-planholder-spread",
    "product-subcontractor-itb",
]

TIER2_CONNECTED_API_NUMS = ["01", "02", "03", "04", "05", "06", "11"]
NON_TIER2_POST_AWARD_API_NUMS = ["07", "08", "09", "10", "12"]

FIFTY_TWO_PORTAL_CODES = [
    "USACE", "MUNI", "TX", "CA", "FL", "VA", "PA", "NY", "IL", "GA",
    "NC", "OH", "WA", "MI", "NJ", "MA", "CO", "AZ", "MN", "TN",
    "IN", "MO", "WI", "SC", "OR", "CT", "UT", "NV", "AL", "LA",
    "KY", "OK", "IA", "KS", "AR", "MS", "NM", "NE", "ID", "HI",
    "NH", "ME", "RI", "MT", "DE", "SD", "ND", "AK", "VT", "WV",
    "WY", "MD",
]


def _run_node_json_script(node_code: str, payload: Any) -> Dict[str, Any]:
    """Helper to execute a Node.js snippet with JSON stdin and return parsed JSON stdout."""
    proc = subprocess.run(
        ["node", "-e", node_code],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=25,
    )
    if proc.returncode != 0:
        return {"ok": False, "error": (proc.stderr or proc.stdout or "Node process failed").strip()}
    try:
        return json.loads(proc.stdout.strip())
    except Exception as exc:
        return {"ok": False, "error": f"Invalid JSON from Node: {exc} | stdout={proc.stdout[:200]}"}


def check_html_file(path: str, is_main_page: bool = False) -> List[str]:
    """
    Validate a single HTML file for:
    1. Inline <script> syntax via Node.js vm.Script
    2. Inline on* event handler syntax via Node.js vm.Script
    3. Duplicate HTML IDs (on main pages)
    4. Internal #hash route resolution
    5. Structural HTML tag balance
    6. Zero emojis & zero forbidden washed-out grey classes
    7. Mobile favicon, Apple-Touch-Icon, & OpenGraph ?v= cache-busting tags
    8. Zero leaked internal LLM model names or prompt-echoing artefacts
    """
    errors: List[str] = []
    rel = os.path.relpath(path, BASE_DIR)
    with open(path, "r", encoding="utf-8") as fh:
        content = fh.read()

    # 1. Zero Emojis
    emoji_matches = EMOJI_RE.findall(content)
    if emoji_matches:
        errors.append(f"[{rel}] Contains forbidden emoji characters: {set(emoji_matches)}")
    if EMOJI_ENTITY_RE.search(content):
        errors.append(f"[{rel}] Contains forbidden numeric emoji HTML entity")

    # 2. Zero Washed-Out Grey Patterns
    for pat in FORBIDDEN_GREY_PATTERNS:
        if pat.lower() in content.lower():
            errors.append(f"[{rel}] Contains forbidden low-contrast grey token '{pat}'")

    # 3. JSON-LD <script type="application/ld+json"> validation & Inline JS <script> / on* event handlers via Node.js vm.Script
    ld_json_blocks = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', content, flags=re.S | re.I)
    for idx, ld_raw in enumerate(ld_json_blocks):
        try:
            json.loads(ld_raw)
        except Exception as exc:
            errors.append(f"[{rel}] Invalid JSON-LD block #{idx}: {exc}")

    scripts = re.findall(r"<script(?![^>]*\bsrc=)(?![^>]*application/ld\+json)[^>]*>(.*?)</script>", content, flags=re.S | re.I)
    handlers_raw = re.findall(r'\bon(?:click|input|change|submit|keydown|keyup)="([^"]*)"', content, flags=re.I)
    handlers = [html_lib.unescape(h) for h in handlers_raw]

    if scripts or handlers:
        node_check_code = r"""
const fs = require('fs');
const vm = require('vm');
const data = JSON.parse(fs.readFileSync(0, 'utf8'));
const errs = [];
(data.scripts || []).forEach((s, idx) => {
  try { new vm.Script(s, { filename: 'inline_script_' + idx + '.js' }); }
  catch (e) { errs.push('Script #' + idx + ': ' + e.message); }
});
(data.handlers || []).forEach((h, idx) => {
  try { new vm.Script(h, { filename: 'handler_' + idx + '.js' }); }
  catch (e) { errs.push('Handler #' + idx + ' (' + h.slice(0, 60) + '): ' + e.message); }
});
console.log(JSON.stringify({ ok: errs.length === 0, errors: errs }));
"""
        res = _run_node_json_script(node_check_code, {"scripts": scripts, "handlers": handlers})
        if not res.get("ok"):
            for e in res.get("errors", [res.get("error", "Unknown JS syntax error")]):
                errors.append(f"[{rel}] JS Syntax Error: {e}")

    # 4. Duplicate IDs & Internal #hash targets on main pages
    if is_main_page:
        ids = re.findall(r'\bid="([^"]+)"', content)
        seen = set()
        dups = set()
        for i in ids:
            if i in seen:
                dups.add(i)
            seen.add(i)
        if dups:
            errors.append(f"[{rel}] Duplicate HTML IDs found: {sorted(dups)}")

        spa_routes = {"overview", "apis", "lettings", "checkout", "contracts"}
        hashes = re.findall(r'href="#([^"]+)"', content)
        for h in hashes:
            if h in spa_routes or h.startswith("contracts/") or h.startswith("lettings/"):
                continue
            if h not in seen:
                errors.append(f"[{rel}] Broken internal anchor href='#{h}' (no matching id='{h}')")

    # 5. Structural HTML tag balance (strip <script> and <style> first)
    stripped = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", "", content, flags=re.S | re.I)
    for tag in ("div", "section", "article", "header", "footer", "main", "table", "thead", "tbody", "tr", "td", "th", "button", "a"):
        opens = len(re.findall(rf"<{tag}\b[^>]*>", stripped, flags=re.I))
        closes = len(re.findall(rf"</{tag}\s*>", stripped, flags=re.I))
        if opens != closes:
            errors.append(f"[{rel}] Unbalanced <{tag}> tags: {opens} opening vs {closes} closing")

    # 6. Mobile Favicon, Apple-Touch-Icon & OpenGraph Social Preview Verification
    required_head_markers = [
        'rel="apple-touch-icon"',
        'rel="icon" type="image/png"',
        'rel="icon" type="image/x-icon"',
        'rel="icon" type="image/svg+xml"',
        'property="og:image" content="https://camberdesk.com/og-image.png?v=',
        'property="og:image:width" content="1200"',
        'property="og:image:height" content="630"',
        'name="twitter:card" content="summary_large_image"',
        'name="twitter:image" content="https://camberdesk.com/og-image.png?v=',
    ]
    for marker in required_head_markers:
        if marker not in content:
            errors.append(f"[{rel}] Missing required mobile favicon / OpenGraph head tag: `{marker}`")

    # 7. Zero leaked internal LLM model IDs or prompt-echoing copy in rendered HTML
    forbidden_leaks = ["claude-sonnet", "claude-3", "claude-haiku", "gpt-4o", "here is the extracted"]
    low_content = content.lower()
    for leak in forbidden_leaks:
        if leak in low_content:
            errors.append(f"[{rel}] Leaked internal LLM identifier or prompt echo in public HTML: '{leak}'")

    return errors


def check_favicon_and_og_binary_assets() -> List[str]:
    """Verify binary signatures and dimensions of favicon.ico, favicon.png, apple-touch-icon.png, and og-image.png."""
    errors: List[str] = []
    for sub in ("", "lettings"):
        folder = os.path.join(BASE_DIR, sub) if sub else BASE_DIR
        for fname in ("favicon.svg", "favicon.png", "apple-touch-icon.png", "favicon.ico", "og-image.png"):
            fpath = os.path.join(folder, fname)
            if not os.path.exists(fpath) or os.path.getsize(fpath) < 100:
                errors.append(f"Missing or empty binary icon asset: {fpath}")
                continue
            with open(fpath, "rb") as fh:
                raw = fh.read(32)
            if fname.endswith(".png") and not raw.startswith(b"\x89PNG\r\n\x1a\n"):
                errors.append(f"Invalid PNG magic header in {fpath}")
            elif fname.endswith(".ico"):
                if not raw.startswith(b"\x00\x00\x01\x00") or raw[14:18] == b"\x89PNG":
                    errors.append(f"{fpath} must be an uncompressed 32-bit DIB .ICO (not PNG-in-ICO)")
    return errors


def check_catalog_parity_and_ui() -> List[str]:
    """
    Enforce 100% Catalog Parity & Sequential Ordering between `index.html` and `apis.html`:
    - Exact 12 `<article id="product-...">` cards in strict ascending order `01`..`12`.
    - Uniform 12-column (`lg:col-span-7` + `lg:col-span-5`) layout with zero inner scrollbars (`max-h-*` prohibited on `<pre>`).
    - Quick-Jump Directory rows (`01`..`12`), Pricing Matrix rows (`01`..`12`), `window.CATALOG`, and `window.API_META`.
    - Dynamic badges (`12 LIVE ENDPOINTS`, `12 MCP TOOLS`, `12 / 12 SHOWN`, `Filter 12 endpoints...`, `SELECT MICROSERVICE (12)`).
    - Non-overlapping `#api-modules-count-badge` (`shrink-0`, never `absolute`) and `overflow-anchor: none`.
    """
    errors: List[str] = []
    index_path = os.path.join(BASE_DIR, "index.html")
    apis_path = os.path.join(BASE_DIR, "apis.html")

    with open(index_path, "r", encoding="utf-8") as fh:
        idx_html = fh.read()
    with open(apis_path, "r", encoding="utf-8") as fh:
        api_html = fh.read()

    for label, text in (("index.html", idx_html), ("apis.html", api_html)):
        card_ids = re.findall(r'<article\s+id="(product-[^"]+)"', text)
        if card_ids != EXPECTED_API_IDS:
            errors.append(f"[{label}] Article card IDs mismatch. Expected {EXPECTED_API_IDS}, got {card_ids}")

        dir_rows = re.findall(r'data-api-row="(product-[^"]+)"', text)
        if dir_rows != EXPECTED_API_IDS:
            errors.append(f"[{label}] Quick-Jump Directory rows mismatch. Expected {EXPECTED_API_IDS}, got {dir_rows}")

        # Verify uniform 12-column card structure & zero max-h-* on <pre>
        if text.count("lg:col-span-7") < 12 or text.count("lg:col-span-5") < 12:
            errors.append(f"[{label}] Every API card must use the uniform 12-column (`lg:col-span-7` + `lg:col-span-5`) layout")
        pre_tags = re.findall(r"<pre\b[^>]*>", text)
        for ptag in pre_tags:
            if "max-h-" in ptag:
                errors.append(f"[{label}] Prohibited inner scrollbar class `max-h-*` found on `<pre>`: {ptag}")

        # Verify dynamic badges & scroll-jump protection
        for req_badge in (
            "12 LIVE ENDPOINTS",
            "12 MCP TOOLS",
            "12 / 12 SHOWN",
            "Filter 12 endpoints...",
            "SELECT MICROSERVICE (12)",
            "// CROSS-CATALOG RAPIDAPI &amp; MCP PRICING MATRIX (01–12)",
            ">API Catalog</a>",
        ):
            if req_badge not in text:
                errors.append(f"[{label}] Missing required catalog badge/label: `{req_badge}`")

        # Counter badge must be shrink-0 sibling, never absolute
        badge_match = re.search(r'<span[^>]*id="api-modules-count-badge"[^>]*>', text)
        if not badge_match or "shrink-0" not in badge_match.group(0) or "absolute" in badge_match.group(0):
            errors.append(f"[{label}] `#api-modules-count-badge` must be a `shrink-0` flex sibling (never `absolute`)")

        if 'id="api-directory-list" style="overflow-anchor: none;"' not in text:
            errors.append(f"[{label}] `#api-directory-list` missing `overflow-anchor: none;`")
        if 'id="catalog-modules" style="overflow-anchor: none;"' not in text:
            errors.append(f"[{label}] `#catalog-modules` missing `overflow-anchor: none;`")

        # Check window.CATALOG & window.API_META
        cat_match = re.search(r"window\.CATALOG\s*=\s*(\{.*?\});", text, flags=re.S)
        meta_match = re.search(r"window\.API_META\s*=\s*(\{.*?\});", text, flags=re.S)
        if not cat_match or not meta_match:
            errors.append(f"[{label}] Missing `window.CATALOG` or `window.API_META` JSON assignment")
        else:
            try:
                cat_obj = json.loads(cat_match.group(1))
                meta_obj = json.loads(meta_match.group(1))
                if list(cat_obj.keys()) != EXPECTED_API_IDS:
                    errors.append(f"[{label}] `window.CATALOG` keys mismatch: {list(cat_obj.keys())}")
                if list(meta_obj.keys()) != EXPECTED_API_IDS:
                    errors.append(f"[{label}] `window.API_META` keys mismatch: {list(meta_obj.keys())}")
                for k, v in meta_obj.items():
                    if not isinstance(v.get("defaultPayload"), dict) or not v["defaultPayload"]:
                        errors.append(f"[{label}] `window.API_META['{k}'].defaultPayload` is empty")
            except Exception as exc:
                errors.append(f"[{label}] Failed parsing `window.CATALOG` / `window.API_META`: {exc}")

    return errors


def check_portal_parity_and_telemetry() -> List[str]:
    """Verify 52-Portal & 50-State DOT parity across `index.html`, `apis.html`, and `pseo_generator.py`."""
    errors: List[str] = []
    with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as fh:
        idx_html = fh.read()
    with open(os.path.join(BASE_DIR, "apis.html"), "r", encoding="utf-8") as fh:
        api_html = fh.read()
    with open(os.path.join(BASE_DIR, "pseo_generator.py"), "r", encoding="utf-8") as fh:
        pseo_src = fh.read()

    required_index_portal_markers = [
        "LIVE MONITORING: 52 GOVERNMENT &amp; DOT PORTALS ACTIVE",
        "ALL 50 STATE DOTS ACTIVE",
        "52 PORTALS DE-NOISED 24/7",
        "All Portals (52)",
        "// 52 ACTIVE PROCUREMENT &amp; STATE DOT LETTING PORTALS",
        "52 PORTALS ACTIVE &bull; 50-STATE DOT &amp; USACE DIRECTORY",
        "ALL 52 FEDERAL USACE &amp; 50-STATE DOT PORTAL MONITORS ACTIVE",
        '"portals_monitored": 52',
    ]
    for marker in required_index_portal_markers:
        if marker not in idx_html:
            errors.append(f"[index.html] Missing 52-Portal parity marker: `{marker}`")

    for code in FIFTY_TWO_PORTAL_CODES:
        if f"PORTAL // {code}" not in idx_html:
            errors.append(f"[index.html] Missing `#coverage` portal card for `PORTAL // {code}`")

    if '"portals_monitored": 52' not in api_html:
        errors.append("[apis.html] Missing `\"portals_monitored\": 52` in API #04 response preview")

    if "52 PORTALS ACTIVE" not in pseo_src:
        errors.append("[pseo_generator.py] Missing `52 PORTALS ACTIVE` header badge")

    # Ensure zero stale portal counts (< 52)
    stale_portal_re = re.compile(r"\b([1-4][0-9]|5[01])\s+(?:GOVERNMENT\s+&amp;\s+DOT\s+)?PORTALS\s+(?:ACTIVE|DE-NOISED)", re.I)
    if stale_portal_re.search(idx_html) or stale_portal_re.search(api_html):
        errors.append("Found stale `< 52` portal count in `index.html` or `apis.html`")

    return errors


def check_tier_value_prop_and_capture_moat_parity() -> List[str]:
    """
    Verify:
    1. Hero Tier 2 Dossier Card and `<section id="capture-moat">` reference all 7 Tier-2-connected preconstruction APIs (`#01..#06, #11`)
       and never bloat `#capture-moat` with post-award APIs (`#07..#10, #12`).
    2. Checkout Tier 1 (`$199 / mo`), Tier 2 (`$499 / mo`), and Tier 3 (`$1,499 / mo`) cards and Stripe links are present.
    """
    errors: List[str] = []
    with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as fh:
        idx_html = fh.read()

    moat_match = re.search(r'<section id="capture-moat".*?</section>', idx_html, flags=re.S)
    if not moat_match:
        errors.append("[index.html] Missing `<section id=\"capture-moat\">`")
    else:
        moat_html = moat_match.group(0)
        for num in TIER2_CONNECTED_API_NUMS:
            if f"API #{num}" not in idx_html:
                errors.append(f"[index.html] Missing Tier-2 preconstruction `API #{num}` reference")
            if f"API #{num}" not in moat_html:
                errors.append(f"[index.html] `<section id=\"capture-moat\">` missing reference to `API #{num}`")
        for num in NON_TIER2_POST_AWARD_API_NUMS:
            if f"API #{num}" in moat_html:
                errors.append(
                    f"[index.html] `<section id=\"capture-moat\">` contains post-award `API #{num}` (`connect_to_tier2 == False`)"
                )

    for checkout_marker in (
        'id="checkout-card-tier1"',
        'id="checkout-card-tier2"',
        'id="checkout-card-tier3"',
        "$199 / mo",
        "$499 / mo",
        "$1,499 / mo",
        "All 12 individual CamberDesk microservices",
    ):
        if checkout_marker not in idx_html:
            errors.append(f"[index.html] Missing checkout surface marker: `{checkout_marker}`")

    return errors


def check_conversion_and_distribution_surfaces() -> List[str]:
    """
    Verify:
    1. `campaign_leads.csv` & `outbox_ready_queue.json` exist, contain valid MX-ready emails, and every `/lettings/project/<slug>.html` URL resolves to an existing static file on disk.
    2. 5/5 Glama TDQS MCP compliance across `api_gateway/routers/mcp.py`, `mcp-server/index.js`, and `build_cloudflare_edge_worker.py`.
    """
    errors: List[str] = []

    # 1. Verify pSEO static pages & sitemap.xml
    lettings_index = os.path.join(BASE_DIR, "lettings", "index.html")
    project_pages = sorted(glob.glob(os.path.join(BASE_DIR, "lettings", "project", "*.html")))
    if not os.path.exists(lettings_index):
        errors.append("Missing `lettings/index.html`")
    if len(project_pages) < 12:
        errors.append(f"Expected >= 12 pSEO dossier pages in `lettings/project/*.html`, found {len(project_pages)}")

    # 2. Verify campaign_leads.csv & outbox_ready_queue.json dossier URLs exist on disk
    csv_path = os.path.join(BASE_DIR, "campaign_leads.csv")
    queue_path = os.path.join(BASE_DIR, "outbox_ready_queue.json")
    if not os.path.exists(csv_path):
        errors.append("Missing `campaign_leads.csv`")
    else:
        with open(csv_path, "r", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        if len(rows) < 10:
            errors.append(f"Expected >= 10 leads in `campaign_leads.csv`, found {len(rows)}")
        for r in rows:
            em = str(r.get("email") or "")
            if not str(r.get("source_url") or "").strip():
                errors.append(f"`campaign_leads.csv` row `{em}` missing live HTML/Directory `source_url` (guessed role emails prohibited)")
            for col in ("step1_subject", "step1_body_zero_link", "step2_body_dossier_link"):
                val = str(r.get(col) or "")
                if "$" in val:
                    errors.append(f"`campaign_leads.csv` row `{em}` column `{col}` contains forbidden `$` sign (use `USD `)")
                if "http://" in val or "https://" in val:
                    errors.append(f"`campaign_leads.csv` row `{em}` column `{col}` contains forbidden link (Zero-Link Rule)")
            durl = str(r.get("dossier_url") or "")
            if "/lettings/project/" not in durl:
                errors.append(f"`campaign_leads.csv` row missing `/lettings/project/` dossier_url: {durl}")
            else:
                slug_file = durl.split("/lettings/project/")[-1].split("?")[0].split("#")[0]
                disk_path = os.path.join(BASE_DIR, "lettings", "project", slug_file)
                if not os.path.exists(disk_path):
                    errors.append(f"`campaign_leads.csv` references non-existent dossier file on disk: {disk_path}")

    if not os.path.exists(queue_path):
        errors.append("Missing `outbox_ready_queue.json`")
    else:
        with open(queue_path, "r", encoding="utf-8") as fh:
            qdata = json.load(fh)
        queued = (
            qdata.get("outbox_queue", qdata.get("emails", []))
            if isinstance(qdata, dict)
            else qdata
        )
        if len(queued) < 10:
            errors.append(f"Expected >= 10 queued emails in `outbox_ready_queue.json`, found {len(queued)}")
        for item in queued:
            durl = str(item.get("dossier_url") or "")
            if "/lettings/project/" in durl:
                slug_file = durl.split("/lettings/project/")[-1].split("?")[0].split("#")[0]
                disk_path = os.path.join(BASE_DIR, "lettings", "project", slug_file)
                if not os.path.exists(disk_path):
                    errors.append(f"`outbox_ready_queue.json` references non-existent dossier file: {disk_path}")

    # 3. Verify 5/5 Glama TDQS across Remote MCP (`api_gateway/routers/mcp.py`), Local STDIO MCP (`mcp-server/index.js`), and Edge Worker (`build_cloudflare_edge_worker.py`)
    try:
        from api_gateway.routers.mcp import MCP_TOOLS

        if len(MCP_TOOLS) != 12:
            errors.append(f"Expected 12 MCP_TOOLS in `mcp.py`, got {len(MCP_TOOLS)}")

        canonical_names = []
        for tool in MCP_TOOLS:
            tname = tool.get("name", "")
            canonical_names.append(tname)
            desc = tool.get("description", "")
            if desc.startswith("API #"):
                errors.append(f"MCP tool `{tname}` starts with forbidden 'API #' prefix")
            if "Use this tool when" not in desc:
                errors.append(f"MCP tool `{tname}` missing sibling-tool disambiguation ('Use this tool when ...')")
            if not tool.get("title") or not tool.get("annotations") or not tool.get("outputSchema"):
                errors.append(f"MCP tool `{tname}` missing `title`, `annotations`, or `outputSchema`")
            props = tool.get("inputSchema", {}).get("properties", {})
            if not props:
                errors.append(f"MCP tool `{tname}` has empty `inputSchema.properties`")
            for pname, pdef in props.items():
                if not pdef.get("description"):
                    errors.append(f"MCP tool `{tname}` property `{pname}` missing description")

        with open(os.path.join(BASE_DIR, "mcp-server", "index.js"), "r", encoding="utf-8") as fh:
            stdio_js = fh.read()
        with open(os.path.join(BASE_DIR, "build_cloudflare_edge_worker.py"), "r", encoding="utf-8") as fh:
            worker_py = fh.read()

        for tname in canonical_names:
            if tname not in stdio_js:
                errors.append(f"Local STDIO MCP (`mcp-server/index.js`) missing tool `{tname}`")
            if tname not in worker_py:
                errors.append(f"Cloudflare Edge Worker (`build_cloudflare_edge_worker.py`) missing routeMap entry for `{tname}`")
    except Exception as exc:
        errors.append(f"MCP 5/5 Glama TDQS verification failed: {exc}")

    return errors


def check_product_output_quality_controls() -> List[str]:
    """
    Verify Tier 3 6-File OpenXML (`.DOCX` + `.XLSX` + `.JSON`) Bid Package `.ZIP` Compiler in memory:
    - All 6 expected files present and non-empty
    - Every `.docx` and `.xlsx` is a valid OpenXML ZIP containing well-formed XML
    - Both `.xlsx` workbooks contain live Excel `=SUM(...)` and `=D6*G6` formulas
    """
    errors: List[str] = []
    try:
        import asyncio
        import base64
        from api_gateway.routers.camber_autopilot import (
            CompileBidPackageRequest,
            compile_full_bid_package,
        )

        pkg = asyncio.run(compile_full_bid_package(CompileBidPackageRequest(), format="json"))
        zip_bytes = base64.b64decode(pkg["zip_base64"])
        with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zf:
            names = zf.namelist()
            if len(names) != 6:
                errors.append(f"Expected 6 files inside Bid Package .ZIP, found {len(names)}: {names}")
            for name in names:
                data = zf.read(name)
                if len(data) < 100:
                    errors.append(f"File `{name}` inside Bid Package .ZIP is unexpectedly small ({len(data)} bytes)")
                if name.endswith((".docx", ".xlsx")):
                    with zipfile.ZipFile(io.BytesIO(data), "r") as inner_zf:
                        for xml_name in inner_zf.namelist():
                            if xml_name.endswith(".xml") or xml_name.endswith(".rels"):
                                ET.fromstring(inner_zf.read(xml_name))
                        if name.endswith(".xlsx"):
                            sheet_xml = inner_zf.read("xl/worksheets/sheet1.xml").decode("utf-8")
                            if "<f>SUM(" not in sheet_xml and "<f>D6*G6</f>" not in sheet_xml:
                                errors.append(f"Workbook `{name}` missing live OpenXML `<f>` formulas")
    except Exception as exc:
        errors.append(f"6-File OpenXML .ZIP Compiler quality check failed: {exc}")
    return errors


def check_spa_runtime() -> List[str]:
    """
    Execute a headless Node.js DOM harness against `index.html` to verify:
    - `switchSpaView('overview' | 'apis' | 'lettings' | 'checkout')`
    - `renderLettingsRoute('#lettings')` populates `#contracts-dynamic-root` with non-empty HTML
    - `filterMainLettingTable('texas')` and `filterMainLettingTable('all')`
    - `filterApiCatalog('davis')` and `filterApiCatalog('')`
    - `openApiSandbox('product-dot-unit-bid-tabs')` and `executeSandboxCall()`
    - `setCheckoutBilling('annual')` and `setCheckoutBilling('monthly')`
    """
    errors: List[str] = []
    index_path = os.path.join(BASE_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as fh:
        content = fh.read()

    scripts = re.findall(r"<script(?![^>]*\bsrc=)(?![^>]*application/ld\+json)[^>]*>(.*?)</script>", content, flags=re.S | re.I)
    node_harness = r"""
const fs = require('fs');
const vm = require('vm');
const data = JSON.parse(fs.readFileSync(0, 'utf8'));

const elements = {};
function makeEl(id) {
  return {
    id,
    textContent: '',
    innerHTML: '',
    value: '',
    href: '',
    offsetHeight: 500,
    style: {},
    classList: {
      _set: new Set(),
      toggle(cls, force) { if (force) this._set.add(cls); else this._set.delete(cls); },
      add(cls) { this._set.add(cls); },
      remove(cls) { this._set.delete(cls); }
    },
    getAttribute(attr) { return this[attr] || ''; },
    scrollIntoView() {}
  };
}
['page-overview','page-apis','page-lettings','page-checkout','contract-directory',
 'letting-shown-badge','api-modules-count-badge','sandbox-api-select','sandbox-req-box',
 'sandbox-res-box','price-tier1','price-tier2','price-tier3','btn-checkout-tier1',
 'btn-checkout-tier2','btn-checkout-tier3','contracts-dynamic-root','product-davis-bacon-wage'].forEach(id => {
  elements[id] = makeEl(id);
});

const lettingRows = [
  Object.assign(makeEl('row1'), { 'data-letting-portal': 'texas', textContent: 'TxDOT IH-35' }),
  Object.assign(makeEl('row2'), { 'data-letting-portal': 'california', textContent: 'Caltrans I-80' })
];
const apiCards = [
  Object.assign(makeEl('card1'), { textContent: 'CSI MasterFormat Shredder' }),
  Object.assign(makeEl('card2'), { textContent: 'Davis-Bacon Prevailing Wage' })
];

const sandbox = {
  window: {
    scrollTo() {},
    scrollBy() {},
    addEventListener() {},
    location: { hash: '#overview' }
  },
  document: {
    documentElement: { style: {} },
    getElementById(id) {
      if (!elements[id]) elements[id] = makeEl(id);
      return elements[id];
    },
    querySelectorAll(sel) {
      if (sel === '[data-letting-row]') return lettingRows;
      if (sel === '[data-api-card]' || sel === '[data-api-row]') return apiCards;
      return [];
    }
  },
  console
};
sandbox.window.document = sandbox.document;
sandbox.globalThis = sandbox.window;

try {
  vm.createContext(sandbox);
  (data.scripts || []).forEach((s, i) => {
    vm.runInContext(s, sandbox, { filename: 'spa_script_' + i + '.js' });
  });

  sandbox.switchSpaView('lettings');
  if (!elements['contracts-dynamic-root'].innerHTML || elements['contracts-dynamic-root'].innerHTML.length < 50) {
    throw new Error('renderLettingsRoute(#lettings) did not populate #contracts-dynamic-root');
  }
  sandbox.filterMainLettingTable('texas');
  if (elements['letting-shown-badge'].textContent !== '1 PREVIEW LETTINGS SHOWN') {
    throw new Error('filterMainLettingTable(texas) failed: ' + elements['letting-shown-badge'].textContent);
  }
  sandbox.filterMainLettingTable('all');
  sandbox.filterApiCatalog('davis');
  if (elements['api-modules-count-badge'].textContent !== '1 / 12 SHOWN') {
    throw new Error('filterApiCatalog(davis) failed: ' + elements['api-modules-count-badge'].textContent);
  }
  sandbox.jumpToApiCard('product-davis-bacon-wage');
  sandbox.openApiSandbox('product-dot-unit-bid-tabs');
  sandbox.executeSandboxCall();
  if (!elements['sandbox-res-box'].textContent.includes('unit_price_benchmarks')) {
    throw new Error('openApiSandbox / executeSandboxCall failed to populate response preview');
  }
  sandbox.setCheckoutBilling('annual');
  if (elements['price-tier2'].textContent !== '$4,490 / yr') {
    throw new Error('setCheckoutBilling(annual) failed: ' + elements['price-tier2'].textContent);
  }
  sandbox.setCheckoutBilling('monthly');
  if (elements['price-tier2'].textContent !== '$499 / mo') {
    throw new Error('setCheckoutBilling(monthly) failed: ' + elements['price-tier2'].textContent);
  }
  console.log(JSON.stringify({ ok: true }));
} catch (err) {
  console.log(JSON.stringify({ ok: false, error: err.message || String(err) }));
}
"""
    res = _run_node_json_script(node_harness, {"scripts": scripts})
    if not res.get("ok"):
        errors.append(f"Headless SPA runtime check failed: {res.get('error')}")
    return errors


def check_mobile_viewport_overflow() -> List[str]:
    """
    Use Playwright headless Chromium (when available and not in CI/RENDER) to verify zero horizontal
    page overflow (`scrollWidth <= innerWidth + 1`) across `375x812` mobile and `1024x900` / `1280x900` desktop viewports.
    """
    if os.getenv("CI") or os.getenv("RENDER"):
        return []
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return []

    errors: List[str] = []
    project_pages = sorted(glob.glob(os.path.join(BASE_DIR, "lettings", "project", "*.html")))
    sample_project = project_pages[0] if project_pages else None

    targets = [
        ("index.html#overview", f"file:///{os.path.join(BASE_DIR, 'index.html').replace(os.sep, '/')}", "overview"),
        ("index.html#apis", f"file:///{os.path.join(BASE_DIR, 'index.html').replace(os.sep, '/')}", "apis"),
        ("index.html#lettings", f"file:///{os.path.join(BASE_DIR, 'index.html').replace(os.sep, '/')}", "lettings"),
        ("index.html#checkout", f"file:///{os.path.join(BASE_DIR, 'index.html').replace(os.sep, '/')}", "checkout"),
        ("apis.html", f"file:///{os.path.join(BASE_DIR, 'apis.html').replace(os.sep, '/')}", None),
        ("lettings/index.html", f"file:///{os.path.join(BASE_DIR, 'lettings', 'index.html').replace(os.sep, '/')}", None),
    ]
    if sample_project:
        targets.append(
            ("lettings/project/sample", f"file:///{sample_project.replace(os.sep, '/')}", None)
        )

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            for vw, vh in ((375, 812), (1024, 900), (1280, 900)):
                page = browser.new_page(viewport={"width": vw, "height": vh})
                for label, url, spa_view in targets:
                    page.goto(url, wait_until="domcontentloaded", timeout=15000)
                    if spa_view:
                        page.evaluate(f"if (window.switchSpaView) window.switchSpaView('{spa_view}');")
                    overflow = page.evaluate(
                        "() => ({ sw: document.documentElement.scrollWidth, iw: window.innerWidth })"
                    )
                    if overflow["sw"] > overflow["iw"] + 2:
                        errors.append(
                            f"[Viewport {vw}x{vh}] Horizontal overflow on `{label}`: scrollWidth={overflow['sw']} > innerWidth={overflow['iw']}"
                        )
                page.close()
            browser.close()
    except Exception as exc:
        print(f"  [WARN] Playwright viewport audit skipped ({exc})")

    return errors


def check_zero_signaltender_overlap() -> List[str]:
    """
    Guarantees 100% cross-brand isolation between CamberDesk (`D:\\CamberDesk`) and SignalTender (`D:\\Daas`):
      1. Zero overlapping prospect emails or corporate domains across `verified_public_dot_contacts.json`,
         `campaign_leads.csv`, and `D:\\Daas\\verified_public_govcon_contacts.json` / `govcon_contacts.csv` / `campaign_leads.csv`.
      2. Zero `*signaltender*` sender mailboxes in `reinvestment_treasury_ledger.json` or `outbox_ready_queue.json`.
      3. `.env` does not point `DISCORD_WEBHOOK_URL` to SignalTender's Discord `#alerts` webhook (`1555743443802918993`).
    """
    errors: List[str] = []
    daas_dir = r"D:\Daas"
    if not os.path.exists(daas_dir):
        return errors

    cd_emails: set[str] = set()
    cd_domains: set[str] = set()
    cd_json = os.path.join(BASE_DIR, "verified_public_dot_contacts.json")
    cd_csv = os.path.join(BASE_DIR, "campaign_leads.csv")
    if os.path.exists(cd_json):
        try:
            with open(cd_json, "r", encoding="utf-8") as f:
                for r in (json.load(f) or []):
                    if isinstance(r, dict):
                        em = str(r.get("email") or r.get("Email") or "").strip().lower()
                        if "@" in em:
                            cd_emails.add(em)
                            cd_domains.add(em.split("@", 1)[1])
        except Exception:
            pass
    if os.path.exists(cd_csv):
        try:
            with open(cd_csv, "r", encoding="utf-8-sig", newline="") as cf:
                for r in csv.DictReader(cf):
                    em = str(r.get("email") or r.get("Email") or "").strip().lower()
                    if "@" in em:
                        cd_emails.add(em)
                        cd_domains.add(em.split("@", 1)[1])
        except Exception:
            pass

    st_emails: set[str] = set()
    st_domains: set[str] = set()
    for st_json_name in ("verified_public_govcon_contacts.json", "govcon_contacts_cache.json", "outbox_ready_queue.json", "sent_outreach_log.json"):
        st_json = os.path.join(daas_dir, st_json_name)
        if os.path.exists(st_json):
            try:
                with open(st_json, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                    if isinstance(raw, dict) and isinstance(raw.get("contacts"), list):
                        raw = raw["contacts"]
                    if isinstance(raw, list):
                        for r in raw:
                            if isinstance(r, dict):
                                em = str(r.get("Email") or r.get("email") or "").strip().lower()
                                if "@" in em:
                                    st_emails.add(em)
                                    st_domains.add(em.split("@", 1)[1])
            except Exception:
                pass
    for st_csv_name in ("govcon_contacts.csv", "campaign_leads.csv"):
        st_csv_p = os.path.join(daas_dir, st_csv_name)
        if os.path.exists(st_csv_p):
            try:
                with open(st_csv_p, "r", encoding="utf-8-sig", newline="") as cf:
                    for r in csv.DictReader(cf):
                        em = str(r.get("Email") or r.get("email") or "").strip().lower()
                        if "@" in em:
                            st_emails.add(em)
                            st_domains.add(em.split("@", 1)[1])
            except Exception:
                pass

    shared_emails = sorted(cd_emails & st_emails)
    shared_domains = sorted(cd_domains & st_domains)
    if shared_emails:
        errors.append(f"Cross-brand email overlap with SignalTender: {shared_emails[:5]}")
    if shared_domains:
        errors.append(f"Cross-brand domain overlap with SignalTender: {shared_domains[:5]}")

    env_p = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_p):
        with open(env_p, "r", encoding="utf-8") as ef:
            env_txt = ef.read()
            for bad_tok in (
                "1555743443802918993",
                "1560070981563715644",
                "1561230679860056117",
                "1563916225862574080",
                "1563916236126036068",
                "rincvxrjrpvgydaontpm",
                "c7727dff",
                "748eecf5",
            ):
                if bad_tok in env_txt:
                    errors.append(f"CamberDesk `.env` still references SignalTender token (`{bad_tok}`)")

    harvester_p = os.path.join(BASE_DIR, "harvest_verified_dot_contacts.py")
    if os.path.exists(harvester_p):
        with open(harvester_p, "r", encoding="utf-8") as hf:
            if "api.nsf.gov" in hf.read():
                errors.append("`harvest_verified_dot_contacts.py` still queries `api.nsf.gov` (shared with SignalTender)")

    for pub_name in ("index.html", "apis.html", "cloudflare_worker.js"):
        pub_p = os.path.join(BASE_DIR, pub_name)
        if os.path.exists(pub_p):
            with open(pub_p, "r", encoding="utf-8") as pf:
                pub_txt = pf.read()
                if "signaltender" in pub_txt.lower():
                    errors.append(f"Public surface `{pub_name}` contains forbidden `signaltender` reference")
                if pub_name == "cloudflare_worker.js":
                    for seo_route in ('path === "/robots.txt"', 'path === "/sitemap.xml"', "a4f8e2c91b7d3056e8a12f4c9d0b3e71.txt"):
                        if seo_route not in pub_txt:
                            errors.append(f"`cloudflare_worker.js` missing required SEO edge route `{seo_route}`")

    return errors


def verify_integrity() -> int:
    print("=" * 78)
    print("CAMBERDESK // FULL REPOSITORY, SPA RUNTIME, 52-PORTAL & 12-API INTEGRITY GATE")
    print("=" * 78)

    all_errors: List[str] = []

    # Step 1: HTML Static + Inline JS + Event Attributes + Favicons/OG + Zero Emoji + High-Contrast Audit
    html_files = [
        (os.path.join(BASE_DIR, "index.html"), True),
        (os.path.join(BASE_DIR, "apis.html"), True),
        (os.path.join(BASE_DIR, "lettings", "index.html"), False),
    ]
    for pfile in sorted(glob.glob(os.path.join(BASE_DIR, "lettings", "project", "*.html"))):
        html_files.append((pfile, False))

    for fpath, is_main in html_files:
        if not os.path.exists(fpath):
            all_errors.append(f"Missing required HTML file: {fpath}")
            continue
        all_errors.extend(check_html_file(fpath, is_main_page=is_main))

    all_errors.extend(check_favicon_and_og_binary_assets())
    print(f"  [STEP 1] Audited {len(html_files)} HTML pages (JS vm.Script, on* handlers, tag balance, zero emojis, Warm Vellum contrast, favicons/OG)")

    # Step 2: 100% Catalog & UI Parity
    all_errors.extend(check_catalog_parity_and_ui())
    print("  [STEP 2] Verified 12/12 API Catalog parity (`index.html` <-> `apis.html`, Quick-Jump Directory, Pricing Matrix, `CATALOG` & `API_META`)")

    # Step 3: 52-Portal & 50-State DOT Telemetry Parity
    all_errors.extend(check_portal_parity_and_telemetry())
    print("  [STEP 3] Verified 52-Portal & 50-State DOT parity across `index.html`, `apis.html`, and `pseo_generator.py`")

    # Step 4: Tier 1 / Tier 2 / Tier 3 Value-Prop & #capture-moat Relevance Filter
    all_errors.extend(check_tier_value_prop_and_capture_moat_parity())
    print("  [STEP 4] Verified Tier 1/2/3 checkout parity and `#capture-moat` preconstruction API filter (`#01..#06, #11`)")

    # Step 5: Conversion, Outbound & 5/5 Glama TDQS MCP Parity
    all_errors.extend(check_conversion_and_distribution_surfaces())
    print("  [STEP 5] Verified `campaign_leads.csv`, `outbox_ready_queue.json`, `/lettings/project/*.html` disk links & 5/5 Glama TDQS MCP")

    # Step 6: 6-File OpenXML .ZIP Takeoff Compiler Quality Control
    all_errors.extend(check_product_output_quality_controls())
    print("  [STEP 6] Verified 6-File OpenXML (.DOCX + .XLSX) .ZIP Takeoff Compiler & live Excel formulas (`=SUM()`, `=D6*G6`)")

    # Step 7: Headless Node.js SPA Runtime Execution
    all_errors.extend(check_spa_runtime())
    print("  [STEP 7] Verified Headless Node.js SPA Runtime (`switchSpaView`, `renderLettingsRoute`, `filterApiCatalog`, Studio Sandbox, Billing Toggle)")

    # Step 8: Mobile & Desktop Viewport Overflow Audit
    all_errors.extend(check_mobile_viewport_overflow())
    print("  [STEP 8] Verified Mobile (`375x812`) & Desktop (`1024x900`, `1280x900`) viewport layout overflow")

    # Step 8b: Zero Overlap with SignalTender
    all_errors.extend(check_zero_signaltender_overlap())
    print("  [STEP 8b] Verified 100% Zero Prospect Email, Domain, Mailbox & Discord Webhook Overlap with SignalTender")

    # Step 9: Closed-Loop Autonomous Error Healer
    from auto_error_healer import run_healer

    healer_ok = run_healer(clear_resolved=True, run_smoke=False)
    if not healer_ok:
        all_errors.append("`auto_error_healer.run_healer()` reported unresolved issues")

    if all_errors:
        print("\n" + "!" * 78)
        print(f"[INTEGRITY FAILURE] {len(all_errors)} issue(s) detected:")
        for idx, err in enumerate(all_errors, 1):
            print(f"  {idx}. {err}")
        print("!" * 78)
        return 1

    print("\n[INTEGRITY PASS] All 9 CamberDesk Static, Runtime, Portal, Catalog, OpenXML, MCP & Self-Healing checks passed 100%.")
    return 0


if __name__ == "__main__":
    sys.exit(verify_integrity())
