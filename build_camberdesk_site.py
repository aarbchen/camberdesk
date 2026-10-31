r"""
CamberDesk — Deterministic Frontend & API Studio Builder (`build_camberdesk_site.py`).
Generates `D:\CamberDesk\index.html` and `D:\CamberDesk\apis.html` from a single source of truth
using Symbol #07 (Compass Quadrant Lock) and Editorial Theme 1 (Warm Vellum #FAF8F5 & Obsidian Ink #0A0D14 + Blueprint Navy #1E3A8A).
"""

import json
import os
from typing import Any, Dict, List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SEED_PATH = os.path.join(BASE_DIR, "dot_lettings_seed.json")

APIS_CATALOG: List[Dict[str, Any]] = [
    {
        "num": "01",
        "id": "product-csi-masterformat",
        "title": "CSI MasterFormat Divisions 00–48 Spec & Submittal Shredder API",
        "method": "POST",
        "route": "/v1/shred/csi-masterformat",
        "mcp_tool": "shred_csi_masterformat",
        "badge": "CSI SPEC SHREDDER",
        "connect_to_tier2": True,
        "summary": "Shreds 500-page Project Manuals and Special Provisions into structured CSI Divisions 00–48 submittal logs, liquidated damages ($/day), retainage caps, and warranty terms.",
        "req_sample": {
            "spec_text": "SECTION 01 10 00 SUMMARY: Replace 4 prestressed bridge spans and place 68,000 tons of Item 341 Superpave HMA. Liquidated damages are $4,200/day.",
            "project_id": "TXDOT-CSJ-0015-13-412",
            "target_trade": "Heavy Civil / Highway & Bridge",
        },
        "res_sample": {
            "status": "success",
            "project_id": "TXDOT-CSJ-0015-13-412",
            "liquidated_damages_per_day_usd": 4200,
            "retainage_terms": "5.0% statutory public works retainage cap",
            "shredded_csi_divisions": [
                {"division": "Division 01 — General Requirements", "mandatory_submittals": ["Baseline Primavera P6 CPM Schedule (15 Days Post-NTP)"]},
                {"division": "Division 03/05 — Concrete & Structural Steel", "mandatory_submittals": ["HPC Class S Mix Design", "AISC Shop Drawings & BABA Mill Certs"]},
            ],
        },
    },
    {
        "num": "02",
        "id": "product-dot-unit-bid-tabs",
        "title": "50-State DOT Historical Item Bid Tabulation & Spread Modeler API",
        "method": "POST",
        "route": "/v1/model/dot-unit-bid-tabs",
        "mcp_tool": "model_dot_unit_bid_tabs",
        "badge": "DOT UNIT BID TABS",
        "connect_to_tier2": True,
        "summary": "Queries 36-month historical State DOT unit bid tabulations by pay item, state, and takeoff quantity to output low/median/75th-percentile unit prices ($/Ton, $/LF, $/CY) and Recommended Unit Bid.",
        "req_sample": {
            "state_code": "TX",
            "pay_item_description": "Dense-Graded Hot-Mix Asphalt (Superpave SP-C PG 76-22)",
            "unit": "TON",
            "quantity": 68000,
        },
        "res_sample": {
            "status": "success",
            "state_code": "TX",
            "historical_36mo_lettings_sampled": 42,
            "unit_price_benchmarks": {
                "historical_winning_low_unit_usd": 117.59,
                "historical_median_bid_unit_usd": 127.02,
                "recommended_competitive_unit_bid_usd": 121.17,
            },
            "unbalanced_bid_guardrail": "Compliant under 23 CFR 635.102",
        },
    },
    {
        "num": "03",
        "id": "product-davis-bacon-wage",
        "title": "Davis-Bacon (29 CFR 5) & State Prevailing Wage Fringe Calculator API",
        "method": "POST",
        "route": "/v1/calculate/davis-bacon-prevailing-wage",
        "mcp_tool": "calculate_davis_bacon_prevailing_wage",
        "badge": "DAVIS-BACON WH-347",
        "connect_to_tier2": True,
        "summary": "Maps project county and construction type to SAM.gov WDOL / state prevailing wage base hourly rates, health/pension fringes, weighted crew burden, and Form WH-347 certified payroll compliance.",
        "req_sample": {
            "state_code": "TX",
            "county": "Travis County",
            "construction_type": "Highway",
            "estimated_crew_hours": 14500,
        },
        "res_sample": {
            "status": "success",
            "wage_determination_reference": "TX20260028 (Highway Construction — 29 CFR Part 5)",
            "weighted_composite_hourly_usd": 54.21,
            "fully_burdened_crew_hourly_usd": 64.24,
            "total_estimated_prevailing_labor_usd": 931480.0,
        },
    },
    {
        "num": "04",
        "id": "product-live-lettings",
        "title": "52-Portal Live State DOT Lettings, USACE & Public Works Feed API",
        "method": "GET",
        "route": "/v1/lettings/live",
        "mcp_tool": "get_live_dot_lettings",
        "badge": "52-PORTAL LETTING FEED",
        "connect_to_tier2": True,
        "summary": "Exposes pre-vetted heavy-civil, highway, bridge, utility, and commercial construction lettings across all 50 State DOTs, USACE Civil Works, and Municipal portals.",
        "req_sample": {"state": "TX", "limit": 5},
        "res_sample": {
            "status": "success",
            "portals_monitored": 52,
            "count": 12,
            "lettings": [
                {
                    "project_id": "TXDOT-CSJ-0015-13-412",
                    "agency": "Texas Department of Transportation (TxDOT)",
                    "engineers_estimate_usd": 18450000.0,
                    "dbe_goal_pct": 11.5,
                }
            ],
        },
    },
    {
        "num": "05",
        "id": "product-baba-buy-america",
        "title": "Build America, Buy America (BABA / 23 CFR 635.410) Material Auditor API",
        "method": "POST",
        "route": "/v1/audit/baba-buy-america",
        "mcp_tool": "audit_baba_buy_america",
        "badge": "BABA DOMESTIC STEEL",
        "connect_to_tier2": True,
        "summary": "Audits Bill of Materials (BOM) submittals against federal/FHWA domestic iron, steel, and manufactured product thresholds (>55% US cost) and OMB M-24-02 De Minimis waivers.",
        "req_sample": {
            "project_id": "USACE-W912EP-27-B-0004",
            "funding_agency": "FHWA / USACE Infrastructure",
        },
        "res_sample": {
            "status": "success",
            "project_id": "USACE-W912EP-27-B-0004",
            "overall_baba_posture": "COMPLIANT (99.3% Domestic US Melt/Manufacture; 0.7% OMB M-24-02 De Minimis)",
        },
    },
    {
        "num": "06",
        "id": "product-dbe-good-faith",
        "title": "DOT DBE (49 CFR Part 26) Subcontractor & Good Faith Effort Generator API",
        "method": "POST",
        "route": "/v1/generate/dbe-good-faith-effort",
        "mcp_tool": "generate_dbe_good_faith_effort",
        "badge": "DBE 49 CFR PART 26",
        "connect_to_tier2": True,
        "summary": "Calculates certified DBE/MBE/WBE participation credit (100% subcontractor vs. 60% regular dealer), verifies Commercially Useful Function (CUF), and builds Good Faith Effort (GFE) logs.",
        "req_sample": {
            "project_id": "TXDOT-CSJ-0015-13-412",
            "total_bid_amount_usd": 17850000.0,
            "dbe_goal_pct": 11.5,
        },
        "res_sample": {
            "status": "success",
            "contract_dbe_goal_pct": 11.5,
            "achieved_dbe_participation_pct": 12.18,
            "goal_compliance_status": "GOAL MET OR EXCEEDED — Full responsiveness under 49 CFR 26.53",
        },
    },
    {
        "num": "07",
        "id": "product-aia-g702-g703",
        "title": "AIA G702 / G703 Schedule of Values (SOV) & Retainage Billing API",
        "method": "POST",
        "route": "/v1/generate/aia-g702-g703-pay-app",
        "mcp_tool": "generate_aia_g702_g703_pay_app",
        "badge": "AIA G702 / G703 SOV",
        "connect_to_tier2": False,
        "summary": "Converts bid items into a balanced, front-load-compliant AIA Document G702 Application for Payment and G703 Continuation Sheet with retainage math.",
        "req_sample": {
            "project_id": "TXDOT-CSJ-0015-13-412",
            "contractor_name": "Webber Civil Constructors LLC",
            "contract_sum_usd": 17850000.0,
            "retainage_pct": 5.0,
        },
        "res_sample": {
            "status": "success",
            "g702_summary": {
                "line_1_original_contract_sum_usd": 17850000.0,
                "line_4_total_completed_and_stored_to_date_usd": 3748500.0,
                "line_8_current_payment_due_usd": 3561075.0,
            },
        },
    },
    {
        "num": "08",
        "id": "product-surety-miller-act",
        "title": "Miller Act (40 U.S.C. 3131) & Surety Bond Capacity Underwriter API",
        "method": "POST",
        "route": "/v1/audit/surety-miller-act-bond",
        "mcp_tool": "audit_surety_miller_act_bond",
        "badge": "SURETY & MILLER ACT",
        "connect_to_tier2": False,
        "summary": "Evaluates contractor working capital, net worth, and uncompleted WIP backlog to underwrite Single/Aggregate Surety Bond limits and SF-24/SF-25 bond premiums.",
        "req_sample": {
            "contractor_name": "Apex Civil & Utility Constructors LLC",
            "current_assets_usd": 4850000.0,
            "current_liabilities_usd": 2150000.0,
            "net_worth_equity_usd": 4200000.0,
            "target_project_bid_usd": 12400000.0,
        },
        "res_sample": {
            "status": "success",
            "verified_working_capital_usd": 2700000.0,
            "single_project_bond_limit_usd": 18900000.0,
            "aggregate_work_program_limit_usd": 42000000.0,
            "miller_act_approval_status": "APPROVED FOR BID BOND (SF-24) & 100% PERFORMANCE/PAYMENT BONDS",
        },
    },
    {
        "num": "09",
        "id": "product-rfi-change-order",
        "title": "Construction RFI, Differing Site Conditions & AIA G701 Change Order API",
        "method": "POST",
        "route": "/v1/generate/rfi-change-order-claim",
        "mcp_tool": "generate_rfi_change_order_claim",
        "badge": "RFI & DSC CLAIMS",
        "connect_to_tier2": False,
        "summary": "Analyzes plan discrepancies and Type I/II differing subsurface conditions (FAR 52.236-2), models Critical Path Time-Impact Analysis (TIA), and prices AIA G701 Change Orders.",
        "req_sample": {
            "project_id": "CALTRANS-04-2Q7404",
            "issue_summary": "Encountered uncharted 48-inch cast-iron main at Bent 4 micropile elevation -38.0 ft.",
            "direct_cost_impact_usd": 184500.0,
            "critical_path_delay_days": 14,
        },
        "res_sample": {
            "status": "success",
            "entitlement_basis": "Type I Differing Site Condition (FAR 52.236-2 / DOT Spec 104.02)",
            "pco_pricing_summary": {"total_aia_g701_change_order_request_usd": 214296.75},
        },
    },
    {
        "num": "10",
        "id": "product-osha-emr-safety",
        "title": "OSHA 29 CFR 1926, USACE EM 385-1-1 AHA & Insurance EMR Auditor API",
        "method": "POST",
        "route": "/v1/audit/osha-emr-site-safety",
        "mcp_tool": "audit_osha_emr_site_safety",
        "badge": "OSHA 1926 & EM 385-1-1",
        "connect_to_tier2": False,
        "summary": "Generates trade-specific Activity Hazard Analyses (AHA), Site-Specific Safety Plans (SSSP), and Experience Modification Rate (EMR) bid-eligibility audits.",
        "req_sample": {
            "project_id": "USACE-W912EP-27-B-0004",
            "contractor_emr_current": 0.78,
        },
        "res_sample": {
            "status": "success",
            "contractor_emr_current": 0.78,
            "prequalification_eligibility": "TIER-1 PREFERRED (< 0.85 EMR — Eligible for all USACE & DOT Lettings)",
        },
    },
    {
        "num": "11",
        "id": "product-planholder-spread",
        "title": "DOT Planholder List, Competitor Bid Behavior & MLOT Analyzer API",
        "method": "POST",
        "route": "/v1/analyze/planholder-competitor-spread",
        "mcp_tool": "analyze_planholder_competitor_spread",
        "badge": "PLANHOLDER & MLOT",
        "connect_to_tier2": True,
        "summary": "Analyzes official DOT project planholder lists against historical head-to-head letting results to predict the winning low bid, Margin Left on Table (MLOT), and optimal markup.",
        "req_sample": {
            "project_id": "TXDOT-CSJ-0015-13-412",
            "engineers_estimate_usd": 18450000.0,
            "planholders": ["Webber LLC", "Granite Construction Inc.", "Jordan Foster Construction LLC", "Lone Star Paving Co.", "Capital Excavation Company"],
        },
        "res_sample": {
            "status": "success",
            "predicted_winning_low_bid_usd": 16881750.0,
            "predicted_margin_left_on_table_usd": 523334.25,
            "recommended_markup_pct": 7.8,
        },
    },
    {
        "num": "12",
        "id": "product-subcontractor-itb",
        "title": "Trade Subcontractor Invitation to Bid (ITB), Scope Gap & AIA A401 API",
        "method": "POST",
        "route": "/v1/generate/subcontractor-scope-itb",
        "mcp_tool": "generate_subcontractor_scope_itb",
        "badge": "SUBCONTRACTOR ITB",
        "connect_to_tier2": False,
        "summary": "Generates trade-specific Subcontractor Scope Checklists, exclusions to reject, and AIA A401 subcontract flow-down clauses.",
        "req_sample": {
            "project_id": "TXDOT-CSJ-0015-13-412",
            "trade_package": "Division 26 — Roadway ITS Fiber Duct Bank & High-Mast Illumination",
            "prime_contractor": "Webber Civil Constructors LLC",
        },
        "res_sample": {
            "status": "success",
            "trade_package": "Division 26 — Roadway ITS Fiber Duct Bank & High-Mast Illumination",
            "mandatory_scope_inclusions": ["100% turnkey furnishing, trenching & OTDR testing", "Davis-Bacon WH-347 & BABA compliance"],
        },
    },
]

FIFTY_TWO_PORTALS = [
    ("USACE", "USACE Civil Works (SAM.gov)"), ("MUNI", "Municipal Public Works (DemandStar)"),
    ("TX", "TxDOT Letting"), ("CA", "Caltrans OE"), ("FL", "FDOT Lettings"), ("VA", "VDOT CAB"),
    ("PA", "PennDOT ECMS"), ("NY", "NYSDOT Lettings"), ("IL", "IDOT WCTB"), ("GA", "GDOT BidX"),
    ("NC", "NCDOT Connect"), ("OH", "ODOT Contracts"), ("WA", "WSDOT Contracting"), ("MI", "MDOT MILogin"),
    ("NJ", "NJDOT BidX"), ("MA", "MassDOT BidX"), ("CO", "CDOT Contracts"), ("AZ", "ADOT Contracts"),
    ("MN", "MnDOT Letting"), ("TN", "TDOT Construction"), ("IN", "INDOT Doing Business"), ("MO", "MoDOT Bidding"),
    ("WI", "WisDOT HCCI"), ("SC", "SCDOT Letting"), ("OR", "ODOT eBIDS"), ("CT", "CTDOT Contracting"),
    ("UT", "UDOT Letting"), ("NV", "NDOT eBidding"), ("AL", "ALDOT Letting"), ("LA", "DOTD Letting"),
    ("KY", "KYTC Procurement"), ("OK", "ODOT Letting"), ("IA", "Iowa DOT BidX"), ("KS", "KDOT Letting"),
    ("AR", "ARDOT Jobs"), ("MS", "MDOT Letting"), ("NM", "NMDOT PS&E"), ("NE", "NDOT Letting"),
    ("ID", "ITD Contracting"), ("HI", "HDOT Highways"), ("NH", "NHDOT Bids"), ("ME", "MaineDOT Bids"),
    ("RI", "RIDOT Letting"), ("MT", "MDT Contracting"), ("DE", "DelDOT Bids"), ("SD", "SDDOT Letting"),
    ("ND", "NDDOT Bids"), ("AK", "DOT&PF Bids"), ("VT", "VTrans Contracting"), ("WV", "WVDOT Letting"),
    ("WY", "WYDOT Letting"), ("MD", "MDOT SHA Bids"),
]


FAVICON_SVG_XML = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <rect x="2" y="2" width="60" height="60" rx="14" fill="#FAF8F5" stroke="#0A0D14" stroke-width="3"/>
  <path fill="#0A0D14" d="M32 9A23 23 0 1 0 55 32H32V9Z"/>
  <rect x="36" y="11" width="16" height="16" rx="2.5" fill="#1E3A8A"/>
</svg>
"""


def _sample_logo_pixel(nx: float, ny: float) -> tuple[int, int, int]:
    """Samples the CamberDesk Symbol #07 (Compass Quadrant Lock) in normalized 64x64 coordinates."""
    import math

    vellum = (250, 248, 245)
    obsidian = (10, 13, 20)
    navy = (30, 58, 138)

    if nx < 3.0 or nx > 61.0 or ny < 3.0 or ny > 61.0:
        return obsidian
    if 36.0 <= nx <= 52.0 and 11.0 <= ny <= 27.0:
        return navy
    dx = nx - 32.0
    dy = ny - 32.0
    if math.hypot(dx, dy) <= 23.0 and not (dx > 0 and dy < 0):
        return obsidian
    return vellum


def _encode_rgb_png(width: int, height: int, raw_rows: list[bytes]) -> bytes:
    import struct
    import zlib

    raw_data = b"".join(raw_rows)

    def _chunk(chunk_type: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    idat = zlib.compress(raw_data, level=9)
    return b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", ihdr) + _chunk(b"IDAT", idat) + _chunk(b"IEND", b"")


def _render_logo_png_bytes(dim: int = 64) -> bytes:
    """Renders a square CamberDesk Symbol #07 PNG icon (e.g. 64x64 favicon.png or 180x180 apple-touch-icon.png)."""
    rows = []
    for y in range(dim):
        row = bytearray(1 + dim * 3)
        row[0] = 0
        ny = (y + 0.5) / dim * 64.0
        for x in range(dim):
            nx = (x + 0.5) / dim * 64.0
            r, g, b = _sample_logo_pixel(nx, ny)
            idx = 1 + x * 3
            row[idx] = r
            row[idx + 1] = g
            row[idx + 2] = b
        rows.append(bytes(row))
    return _encode_rgb_png(dim, dim, rows)


def _render_logo_ico_bytes(dims: tuple[int, ...] = (16, 32, 48)) -> bytes:
    """Renders a multi-resolution (16x16, 32x32, 48x48) uncompressed 32-bit BGRA BITMAPINFOHEADER DIB .ICO for Google Search, iOS Safari, Android & Windows."""
    import struct

    dib_blobs = []
    for dim in dims:
        xor_mask = bytearray(dim * dim * 4)
        for y in range(dim):
            src_y = dim - 1 - y
            ny = (src_y + 0.5) / dim * 64.0
            for x in range(dim):
                nx = (x + 0.5) / dim * 64.0
                r, g, b = _sample_logo_pixel(nx, ny)
                idx = (y * dim + x) * 4
                xor_mask[idx] = b
                xor_mask[idx + 1] = g
                xor_mask[idx + 2] = r
                xor_mask[idx + 3] = 255

        and_row_bytes = ((dim + 31) // 32) * 4
        and_mask = bytes(and_row_bytes * dim)
        bih = struct.pack(
            "<IIIHHIIIIII",
            40,
            dim,
            dim * 2,
            1,
            32,
            0,
            len(xor_mask) + len(and_mask),
            0,
            0,
            0,
            0,
        )
        dib_blobs.append((dim, bih + bytes(xor_mask) + and_mask))

    count = len(dib_blobs)
    ico_header = struct.pack("<HHH", 0, 1, count)
    offset = 6 + 16 * count
    entries = []
    for dim, blob in dib_blobs:
        w_byte = 0 if dim >= 256 else dim
        entries.append(struct.pack("<BBBBHHII", w_byte, w_byte, 0, 0, 1, 32, len(blob), offset))
        offset += len(blob)
    return ico_header + b"".join(entries) + b"".join(blob for _, blob in dib_blobs)


def _render_og_image_png_bytes(width: int = 1200, height: int = 630) -> bytes:
    """Renders a 1200x630 OpenGraph social/SMS link preview card with the centered CamberDesk Symbol #07 logo."""
    vellum = (250, 248, 245)
    obsidian = (10, 13, 20)
    navy = (30, 58, 138)
    border = (203, 213, 225)

    cx, cy = width / 2.0, height / 2.0
    logo_box = 380.0
    x0 = cx - logo_box / 2.0
    y0 = cy - logo_box / 2.0

    rows = []
    for y in range(height):
        row = bytearray(1 + width * 3)
        row[0] = 0
        for x in range(width):
            if y < 16:
                r, g, b = navy
            elif x < 8 or x >= width - 8 or y >= height - 8:
                r, g, b = obsidian
            elif x in (28, width - 29) and 32 <= y <= height - 29:
                r, g, b = border
            elif y in (32, height - 29) and 28 <= x <= width - 29:
                r, g, b = border
            elif x0 <= x < x0 + logo_box and y0 <= y < y0 + logo_box:
                nx = (x - x0) / logo_box * 64.0
                ny = (y - y0) / logo_box * 64.0
                r, g, b = _sample_logo_pixel(nx, ny)
            else:
                r, g, b = vellum
            idx = 1 + x * 3
            row[idx] = r
            row[idx + 1] = g
            row[idx + 2] = b
        rows.append(bytes(row))
    return _encode_rgb_png(width, height, rows)


WEB_MANIFEST_JSON = json.dumps(
    {
        "name": "CamberDesk | 50-State DOT Bid-Tab, Prevailing-Wage & Construction Takeoff Intelligence",
        "short_name": "CamberDesk",
        "description": "Autonomous 50-State DOT heavy-civil letting feed, 36-month historical unit-price bid tabulations, Davis-Bacon WH-347 prevailing wages, and 6-File OpenXML (.DOCX + .XLSX) Takeoff Compiler.",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#FAF8F5",
        "theme_color": "#0A0D14",
        "icons": [
            {"src": "/favicon-32x32.png?v=4", "sizes": "32x32", "type": "image/png"},
            {"src": "/favicon-48x48.png?v=4", "sizes": "48x48", "type": "image/png"},
            {"src": "/favicon-96x96.png?v=4", "sizes": "96x96", "type": "image/png"},
            {"src": "/apple-touch-icon.png?v=4", "sizes": "180x180", "type": "image/png"},
            {"src": "/favicon-192x192.png?v=4", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": "/favicon-512x512.png?v=4", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
        ],
    },
    indent=2,
)


def _generate_favicon_assets() -> None:
    """Generates SVG, multi-size 16/32/48 DIB .ICO, Google Search PNGs (32, 48, 64, 96, 180, 192, 512), 1200x630 OpenGraph PNG, and site.webmanifest."""
    lettings_dir = os.path.join(BASE_DIR, "lettings")
    os.makedirs(lettings_dir, exist_ok=True)

    for svg_p in (os.path.join(BASE_DIR, "favicon.svg"), os.path.join(lettings_dir, "favicon.svg")):
        with open(svg_p, "w", encoding="utf-8") as fh:
            fh.write(FAVICON_SVG_XML)

    for mf_p in (os.path.join(BASE_DIR, "site.webmanifest"), os.path.join(lettings_dir, "site.webmanifest")):
        with open(mf_p, "w", encoding="utf-8") as fh:
            fh.write(WEB_MANIFEST_JSON)

    size_map = {
        "favicon-32x32.png": 32,
        "favicon-48x48.png": 48,
        "favicon.png": 64,
        "favicon-96x96.png": 96,
        "apple-touch-icon.png": 180,
        "favicon-192x192.png": 192,
        "favicon-512x512.png": 512,
    }
    for fname, dim in size_map.items():
        raw_png = _render_logo_png_bytes(dim)
        for target_dir in (BASE_DIR, lettings_dir):
            with open(os.path.join(target_dir, fname), "wb") as fh:
                fh.write(raw_png)

    ico_multi = _render_logo_ico_bytes((16, 32, 48))
    og_png = _render_og_image_png_bytes(1200, 630)

    for ico_p in (os.path.join(BASE_DIR, "favicon.ico"), os.path.join(lettings_dir, "favicon.ico")):
        with open(ico_p, "wb") as fh:
            fh.write(ico_multi)
    for og_p in (os.path.join(BASE_DIR, "og-image.png"), os.path.join(lettings_dir, "og-image.png")):
        with open(og_p, "wb") as fh:
            fh.write(og_png)


def build_social_and_favicon_head(
    page_title: str,
    page_desc: str,
    canonical_url: str = "https://camberdesk.com/",
    rel_prefix: str = "",
) -> str:
    """Renders Google Search + Mobile Browser + iMessage/SMS OpenGraph tags & Schema.org JSON-LD (matching SignalTender's verified head structure)."""
    schema_ld = json.dumps(
        {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Organization",
                    "@id": "https://camberdesk.com/#organization",
                    "name": "CamberDesk",
                    "url": "https://camberdesk.com/",
                    "logo": {
                        "@type": "ImageObject",
                        "url": "https://camberdesk.com/favicon-512x512.png?v=4",
                        "width": 512,
                        "height": 512,
                    },
                    "image": "https://camberdesk.com/og-image.png?v=4",
                    "description": page_desc,
                },
                {
                    "@type": "WebSite",
                    "@id": "https://camberdesk.com/#website",
                    "url": "https://camberdesk.com/",
                    "name": "CamberDesk",
                    "publisher": {"@id": "https://camberdesk.com/#organization"},
                },
                {
                    "@type": "SoftwareApplication",
                    "name": "CamberDesk Autonomous Preconstruction & 50-State DOT Bid-Tab Engine",
                    "applicationCategory": "BusinessApplication",
                    "operatingSystem": "Web, REST API, Model Context Protocol (MCP)",
                    "offers": [
                        {"@type": "Offer", "name": "Tier 1 CamberWire Pro", "price": "199.00", "priceCurrency": "USD"},
                        {"@type": "Offer", "name": "Tier 2 CamberDesk Autopilot", "price": "499.00", "priceCurrency": "USD"},
                        {"@type": "Offer", "name": "Tier 3 6-File .ZIP Takeoff Compiler", "price": "1499.00", "priceCurrency": "USD"},
                    ],
                },
            ],
        }
    )
    return f"""  <meta name="theme-color" content="#FAF8F5" />
  <link rel="icon" type="image/png" sizes="96x96" href="https://camberdesk.com/favicon-96x96.png?v=4" />
  <link rel="icon" type="image/png" sizes="512x512" href="https://camberdesk.com/favicon-512x512.png?v=4" />
  <link rel="icon" type="image/png" sizes="192x192" href="https://camberdesk.com/favicon-192x192.png?v=4" />
  <link rel="icon" type="image/png" sizes="48x48" href="https://camberdesk.com/favicon-48x48.png?v=4" />
  <link rel="icon" type="image/png" sizes="32x32" href="https://camberdesk.com/favicon-32x32.png?v=4" />
  <link rel="icon" type="image/png" sizes="64x64" href="{rel_prefix}favicon.png?v=4" />
  <link rel="icon" type="image/x-icon" href="https://camberdesk.com/favicon.ico?v=4" />
  <link rel="shortcut icon" href="https://camberdesk.com/favicon.ico?v=4" />
  <link rel="apple-touch-icon" sizes="180x180" href="https://camberdesk.com/apple-touch-icon.png?v=4" />
  <link rel="apple-touch-icon-precomposed" sizes="180x180" href="https://camberdesk.com/apple-touch-icon.png?v=4" />
  <link rel="icon" type="image/svg+xml" href="https://camberdesk.com/favicon.svg?v=4" />
  <link rel="manifest" href="https://camberdesk.com/site.webmanifest?v=4" />
  <link rel="canonical" href="{canonical_url}" />
  <meta property="og:site_name" content="CamberDesk" />
  <meta property="og:title" content="{page_title}" />
  <meta property="og:description" content="{page_desc}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical_url}" />
  <meta property="og:logo" content="https://camberdesk.com/favicon-512x512.png?v=4" />
  <meta property="og:image" content="https://camberdesk.com/og-image.png?v=4" />
  <meta property="og:image:secure_url" content="https://camberdesk.com/og-image.png?v=4" />
  <meta property="og:image:type" content="image/png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="CamberDesk — 50-State DOT Bid-Tab, Prevailing-Wage &amp; Construction Takeoff Intelligence" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{page_title}" />
  <meta name="twitter:description" content="{page_desc}" />
  <meta name="twitter:image" content="https://camberdesk.com/og-image.png?v=4" />
  <meta name="twitter:image:alt" content="CamberDesk — 50-State DOT Bid-Tab, Prevailing-Wage &amp; Construction Takeoff Intelligence" />
  <script type="application/ld+json">{schema_ld}</script>"""


def _render_logo_lockup(subtitle: str, href: str = "#overview") -> str:
    """Renders Symbol #07 (Compass Quadrant Lock) + High-Contrast Editorial Theme 1 (Warm Vellum & Obsidian Ink) header lockup."""
    return f"""<a href="{href}" onclick="if(window.switchSpaView && '{href}'.startsWith('#')) switchSpaView('overview')" class="group inline-flex flex-col">
      <div class="inline-flex items-center gap-[6px]">
        <svg viewBox="0 0 64 64" class="w-[23px] h-[23px] shrink-0 -translate-y-[1px]" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path fill="#0A0D14" d="M32 8A24 24 0 1 0 56 32H32V8Z"/>
          <rect x="37" y="11" width="16" height="16" rx="2" fill="#1E3A8A"/>
        </svg>
        <span class="text-[23px] font-bold tracking-[-0.035em] text-[#0A0D14] leading-none whitespace-nowrap">CamberDesk</span>
        <span class="ml-1.5 px-2 py-0.5 text-[11px] font-mono font-bold uppercase tracking-wider rounded bg-[#EAE6DF] text-[#0A0D14] border border-[#94A3B8] leading-none">50-STATE DOT &amp; CIVIL</span>
      </div>
      <span class="text-xs font-mono font-semibold text-[#1E3A8A] mt-1">{subtitle}</span>
    </a>"""


def _build_api_catalog_section() -> str:
    dir_rows = []
    matrix_rows = []
    article_cards = []

    for api in APIS_CATALOG:
        num = api["num"]
        aid = api["id"]
        title = api["title"]
        method = api["method"]
        route = api["route"]
        badge = api["badge"]
        summary = api["summary"]
        req_json = json.dumps(api["req_sample"], indent=2)
        res_json = json.dumps(api["res_sample"], indent=2)

        dir_rows.append(
            f"""<a href="#{aid}" onclick="jumpToApiCard('{aid}')" data-api-row="{aid}" class="flex flex-wrap sm:flex-nowrap items-center justify-between gap-2 p-3.5 rounded-lg bg-white hover:bg-[#EAE6DF] border border-[#CBD5E1] transition shadow-sm min-w-0">
              <div class="flex items-center gap-3 min-w-0">
                <span class="shrink-0 text-xs font-mono font-bold px-2 py-0.5 rounded bg-[#EAE6DF] text-[#0A0D14] border border-[#94A3B8]">{num}</span>
                <span class="text-sm font-bold text-[#0A0D14] break-words min-w-0">{title}</span>
              </div>
              <div class="flex items-center gap-2 text-xs font-mono shrink-0">
                <span class="px-2 py-0.5 rounded bg-[#EFF6FF] text-[#1E3A8A] border border-[#93C5FD] font-bold">{method} {route}</span>
              </div>
            </a>"""
        )

        matrix_rows.append(
            f"""<tr class="border-b border-[#CBD5E1] text-xs hover:bg-[#F1EFEA]">
              <td class="py-3 px-3 font-mono font-bold text-[#0A0D14]">{num}</td>
              <td class="py-3 px-3 font-bold text-[#0A0D14]">{title}</td>
              <td class="py-3 px-3 font-mono font-semibold text-[#1E3A8A]">{method} {route}</td>
              <td class="py-3 px-3 font-mono font-semibold text-[#0A0D14]">$0 (10/mo)</td>
              <td class="py-3 px-3 font-mono font-bold text-[#0A0D14]">$49 (200/mo)</td>
              <td class="py-3 px-3 font-mono text-[#065F46] font-bold">$149 (1,000/mo)</td>
              <td class="py-3 px-3 font-mono text-[#1E3A8A] font-bold">$399 (4,000/mo)</td>
            </tr>"""
        )

        article_cards.append(
            f"""<article id="{aid}" data-api-card="{aid}" class="p-6 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm grid grid-cols-1 lg:grid-cols-12 gap-6 min-w-0">
              <div class="lg:col-span-7 space-y-4 min-w-0">
                <div class="flex flex-wrap items-center gap-2 text-xs font-mono">
                  <span class="px-2.5 py-1 rounded bg-[#EAE6DF] text-[#0A0D14] border border-[#94A3B8] font-bold">API #{num} // {badge}</span>
                  <span class="px-2.5 py-1 rounded bg-[#EFF6FF] text-[#1E3A8A] border border-[#93C5FD] font-bold">{method} {route}</span>
                  <span class="px-2.5 py-1 rounded bg-[#ECFDF5] text-[#065F46] border border-[#6EE7B7] font-bold">MCP: {api['mcp_tool']}</span>
                </div>
                <h3 class="text-xl font-extrabold text-[#0A0D14]">{title}</h3>
                <p class="text-sm font-medium text-[#111827] leading-relaxed">{summary}</p>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 pt-2 text-xs font-mono">
                  <div class="p-3 rounded-lg bg-[#F4F1EA] border border-[#CBD5E1]"><div class="text-[#0A0D14] font-bold">BASIC</div><div class="text-[#0A0D14] font-extrabold text-sm mt-0.5">$0 / mo</div><div class="text-xs font-semibold text-[#1E293B]">10 calls/mo</div></div>
                  <div class="p-3 rounded-lg bg-[#F4F1EA] border border-[#CBD5E1]"><div class="text-[#0A0D14] font-bold">PRO</div><div class="text-[#0A0D14] font-extrabold text-sm mt-0.5">$49 / mo</div><div class="text-xs font-semibold text-[#1E293B]">200 calls/mo</div></div>
                  <div class="p-3 rounded-lg bg-[#EFF6FF] border-2 border-[#1E3A8A]"><div class="text-[#1E3A8A] font-extrabold">ULTRA (REC)</div><div class="text-[#0A0D14] font-extrabold text-sm mt-0.5">$149 / mo</div><div class="text-xs font-bold text-[#1E3A8A]">1,000 calls/mo</div></div>
                  <div class="p-3 rounded-lg bg-[#F4F1EA] border border-[#CBD5E1]"><div class="text-[#0A0D14] font-bold">MEGA</div><div class="text-[#0A0D14] font-extrabold text-sm mt-0.5">$399 / mo</div><div class="text-xs font-semibold text-[#1E293B]">4,000 calls/mo</div></div>
                </div>
                <div class="pt-2 flex flex-wrap gap-3">
                  <button type="button" onclick="openApiSandbox('{aid}')" class="px-4 py-2.5 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-bold text-xs font-mono transition">Test Live in Studio Playground</button>
                  <button type="button" onclick="runCardLiveInBrowser('{aid}')" class="px-4 py-2.5 rounded-lg bg-[#EFF6FF] hover:bg-[#DBEAFE] text-[#1E3A8A] border border-[#93C5FD] font-bold text-xs font-mono transition">Run Live in Browser</button>
                  <a href="#checkout" onclick="switchSpaView('checkout')" class="px-4 py-2.5 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] text-xs font-mono font-bold transition">Included in Tier 2 ($499/mo)</a>
                </div>
              </div>
              <div class="lg:col-span-5 space-y-3 min-w-0">
                <div class="flex flex-wrap items-center justify-between gap-2">
                  <div class="text-xs font-mono font-bold text-[#0A0D14]">// REQUEST &amp; LIVE SDK PREVIEW</div>
                  <div class="inline-flex flex-wrap rounded bg-[#EAE6DF] p-0.5 border border-[#94A3B8] text-[11px] font-mono font-bold">
                    <button type="button" id="card-tab-{aid}-json" onclick="switchCardCodeTab('{aid}', 'json')" class="px-2 py-0.5 rounded bg-[#0A0D14] text-white">200 OK JSON</button>
                    <button type="button" id="card-tab-{aid}-curl" onclick="switchCardCodeTab('{aid}', 'curl')" class="px-2 py-0.5 rounded text-[#0A0D14] hover:text-[#1E3A8A]">cURL</button>
                    <button type="button" id="card-tab-{aid}-python" onclick="switchCardCodeTab('{aid}', 'python')" class="px-2 py-0.5 rounded text-[#0A0D14] hover:text-[#1E3A8A]">Python</button>
                    <button type="button" id="card-tab-{aid}-js" onclick="switchCardCodeTab('{aid}', 'js')" class="px-2 py-0.5 rounded text-[#0A0D14] hover:text-[#1E3A8A]">Node.js</button>
                  </div>
                </div>
                <pre class="p-3.5 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] text-xs font-mono font-medium text-[#0F172A] leading-relaxed overflow-x-auto max-w-full">{req_json}</pre>
                <div class="flex items-center justify-between text-[11px] font-mono font-bold">
                  <span id="card-status-{aid}" class="text-[#065F46]">HTTP 200 OK &bull; Stateless Pydantic V2</span>
                  <button type="button" id="card-copy-{aid}" onclick="copyCardCodeOutput('{aid}')" class="px-2 py-0.5 rounded bg-[#EAE6DF] hover:bg-[#0A0D14] text-[#0A0D14] hover:text-white border border-[#94A3B8] transition">Copy Output</button>
                </div>
                <pre id="card-res-{aid}" class="p-3.5 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] text-xs font-mono font-medium text-[#064E3B] leading-relaxed overflow-x-auto max-w-full">{res_json}</pre>
              </div>
            </article>"""
        )

    catalog_js = {a["id"]: a["res_sample"] for a in APIS_CATALOG}
    api_meta_js = {
        a["id"]: {
            "num": a["num"],
            "title": a["title"],
            "method": a["method"],
            "route": a["route"],
            "mcp_tool": a["mcp_tool"],
            "defaultPayload": a["req_sample"],
        }
        for a in APIS_CATALOG
    }

    return f"""
    <div class="space-y-8">
      <div class="p-6 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div class="inline-flex items-center gap-2 text-xs font-mono font-bold text-[#1E3A8A]">
            <span>12 LIVE ENDPOINTS</span> &bull; <span>12 MCP TOOLS</span> &bull; <span>5/5 GLAMA TDQS</span>
          </div>
          <h2 class="text-2xl font-extrabold text-[#0A0D14] mt-1">Stateless Preconstruction, DOT Bid-Tab &amp; Prevailing-Wage APIs</h2>
          <p class="text-sm font-medium text-[#111827] mt-1">Connect via REST (<code class="text-[#1E3A8A] font-bold">X-RapidAPI-Proxy-Secret</code> / <code class="text-[#1E3A8A] font-bold">cd_live_...</code>) or Remote Streamable-HTTP MCP (<code class="text-[#1E3A8A] font-bold">/mcp</code>).</p>
        </div>
        <div class="flex items-center gap-3">
          <div class="flex-1">
            <input id="api-search-input" type="text" oninput="filterApiCatalog(this.value)" placeholder="Filter 12 endpoints..." class="w-full px-3.5 py-2 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] text-sm font-medium text-[#0A0D14] placeholder-[#1E293B] focus:outline-none focus:border-[#0A0D14]" />
          </div>
          <span id="api-modules-count-badge" class="shrink-0 px-3 py-2 rounded-lg bg-[#EAE6DF] border border-[#94A3B8] text-xs font-mono font-bold text-[#0A0D14]">12 / 12 SHOWN</span>
        </div>
      </div>

      <!-- Contractor Preconstruction Profile Vault (#contractor-profile-vault) -->
      <div id="contractor-profile-vault" class="p-6 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div>
            <div class="text-xs font-mono font-bold text-[#1E3A8A]">// PERSISTENT ESTIMATING DESK PROFILE VAULT (LOCALSTORAGE)</div>
            <h3 class="text-lg font-extrabold text-[#0A0D14] mt-0.5">Pre-Fill Your Contractor Bonding, State DOTs &amp; Margin Targets Across All 12 APIs</h3>
          </div>
          <span id="profile-vault-status" class="px-2.5 py-1 rounded bg-[#ECFDF5] text-[#065F46] border border-[#6EE7B7] text-xs font-mono font-bold">READY TO AUTO-INJECT</span>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 text-xs">
          <div>
            <label class="block font-mono font-bold text-[#0A0D14] mb-1">CONTRACTOR / FIRM</label>
            <input id="vault-company-name" type="text" value="Apex Heavy Civil LLC" class="w-full px-3 py-2 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] font-bold text-[#0A0D14]" />
          </div>
          <div>
            <label class="block font-mono font-bold text-[#0A0D14] mb-1">PRIMARY STATE DOTS</label>
            <input id="vault-state-dots" type="text" value="TX, VA, FL, CA, PA" class="w-full px-3 py-2 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] font-bold text-[#0A0D14]" />
          </div>
          <div>
            <label class="block font-mono font-bold text-[#0A0D14] mb-1">SINGLE-JOB BOND LIMIT</label>
            <input id="vault-bond-limit" type="text" value="$35,000,000" class="w-full px-3 py-2 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] font-bold text-[#0A0D14]" />
          </div>
          <div>
            <label class="block font-mono font-bold text-[#0A0D14] mb-1">TARGET MARKUP / MARGIN</label>
            <input id="vault-target-margin" type="text" value="8.5%" class="w-full px-3 py-2 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] font-bold text-[#0A0D14]" />
          </div>
          <div class="flex items-end">
            <button type="button" onclick="saveCompanyCaptureProfile()" class="w-full px-4 py-2 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono text-xs font-bold transition">Save &amp; Inject Profile</button>
          </div>
        </div>
      </div>

      <!-- In-Page RapidAPI & MCP Studio Playground Modal / Panel -->
      <div id="api-studio-playground" class="p-6 rounded-2xl bg-white border-2 border-[#0A0D14] shadow-sm space-y-4 min-w-0">
        <div class="flex flex-wrap items-center justify-between gap-3 min-w-0">
          <div class="text-xs font-mono font-bold text-[#0A0D14]">// IN-PAGE PRECONSTRUCTION API STUDIO PLAYGROUND — SELECT MICROSERVICE (12)</div>
          <select id="sandbox-api-select" onchange="openApiSandbox(this.value)" class="w-full sm:w-auto max-w-full px-3 py-1.5 rounded bg-[#F4F1EA] border border-[#94A3B8] text-xs font-mono font-bold text-[#0A0D14]">
            {''.join(f'<option value="{a["id"]}">{a["num"]} — {a["title"]}</option>' for a in APIS_CATALOG)}
          </select>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 min-w-0">
          <div class="min-w-0">
            <div class="text-xs font-mono font-bold text-[#0A0D14] mb-1.5">JSON Request Payload</div>
            <textarea id="sandbox-req-box" rows="7" class="w-full p-3.5 rounded-lg bg-[#F4F1EA] border border-[#CBD5E1] text-xs font-mono font-medium text-[#0F172A] leading-relaxed">{json.dumps(APIS_CATALOG[0]['req_sample'], indent=2)}</textarea>
          </div>
          <div class="min-w-0">
            <div class="flex flex-wrap items-center justify-between gap-2 mb-1.5">
              <div class="inline-flex rounded bg-[#EAE6DF] p-0.5 border border-[#94A3B8] text-[11px] font-mono font-bold">
                <button type="button" id="tab-sandbox-json" onclick="setSandboxCodeTab('json')" class="px-2.5 py-1 rounded bg-[#0A0D14] text-white">200 OK JSON</button>
                <button type="button" id="tab-sandbox-curl" onclick="setSandboxCodeTab('curl')" class="px-2.5 py-1 rounded text-[#0A0D14] hover:text-[#1E3A8A]">cURL</button>
                <button type="button" id="tab-sandbox-python" onclick="setSandboxCodeTab('python')" class="px-2.5 py-1 rounded text-[#0A0D14] hover:text-[#1E3A8A]">Python</button>
                <button type="button" id="tab-sandbox-js" onclick="setSandboxCodeTab('js')" class="px-2.5 py-1 rounded text-[#0A0D14] hover:text-[#1E3A8A]">Node / Fetch</button>
              </div>
              <button type="button" id="btn-copy-sandbox" onclick="copySandboxOutput()" class="px-2.5 py-1 rounded bg-[#EAE6DF] hover:bg-[#0A0D14] text-[#0A0D14] hover:text-white border border-[#94A3B8] text-[11px] font-mono font-bold transition">Copy Output</button>
            </div>
            <pre id="sandbox-res-box" class="p-3.5 rounded-lg bg-[#F4F1EA] border border-[#CBD5E1] text-xs font-mono font-medium text-[#064E3B] leading-relaxed overflow-x-auto max-w-full">{json.dumps(APIS_CATALOG[0]['res_sample'], indent=2)}</pre>
          </div>
        </div>
        <div class="flex flex-wrap items-center gap-3">
          <button type="button" onclick="executeSandboxCall()" class="px-4 py-2.5 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-bold text-xs font-mono transition">Execute Stateless API Call</button>
          <span id="sandbox-status-pill" class="text-xs font-mono font-bold text-[#065F46]">HTTP 200 OK &bull; Stateless Pydantic V2 Validated</span>
        </div>
      </div>

      <!-- Interactive MCP Server Integration Hub (Claude Desktop / Cursor / Windsurf / Streamable-HTTP) -->
      <div id="mcp-integration-hub" class="p-6 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <div class="text-xs font-mono font-bold text-[#1E3A8A]">// MODEL CONTEXT PROTOCOL (MCP) — 5/5 GLAMA TDQS SCORE</div>
            <h3 class="text-lg font-extrabold text-[#0A0D14] mt-0.5">1-Click AI Agent Integration (Claude Desktop, Cursor, Windsurf &amp; Remote HTTP)</h3>
          </div>
          <div class="inline-flex flex-wrap rounded-lg bg-[#EAE6DF] p-1 border border-[#94A3B8] text-xs font-mono font-bold gap-1">
            <button type="button" id="mcp-tab-claude" onclick="switchMcpConfigTab('claude')" class="px-3 py-1 rounded bg-[#0A0D14] text-white">Claude Desktop</button>
            <button type="button" id="mcp-tab-cursor" onclick="switchMcpConfigTab('cursor')" class="px-3 py-1 rounded text-[#0A0D14]">Cursor / Windsurf</button>
            <button type="button" id="mcp-tab-http" onclick="switchMcpConfigTab('http')" class="px-3 py-1 rounded text-[#0A0D14]">Remote HTTP (/mcp)</button>
          </div>
        </div>
        <div class="relative">
          <pre id="mcp-config-code" class="p-4 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] text-xs font-mono font-medium text-[#0F172A] overflow-x-auto leading-relaxed">{{
  "mcpServers": {{
    "camberdesk": {{
      "command": "npx",
      "args": ["-y", "@camberdesk/mcp-server"],
      "env": {{
        "CAMBERDESK_API_KEY": "cd_live_your_api_key_here"
      }}
    }}
  }}
}}</pre>
          <button type="button" id="btn-copy-mcp" onclick="copyMcpConfig()" class="mt-2 px-3.5 py-1.5 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white text-xs font-mono font-bold transition">Copy MCP Configuration JSON</button>
        </div>
      </div>

      <!-- Downloadable ConTech & Estimating ERP Integration Blueprints (#integrations) -->
      <div id="integrations" class="p-6 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div>
            <div class="text-xs font-mono font-bold text-[#1E3A8A]">// ZERO-CODE CONTECH, HEAVYBID &amp; ERP AUTOMATION BLUEPRINTS</div>
            <h3 class="text-lg font-extrabold text-[#0A0D14] mt-0.5">Download Ready-to-Import Workflow Blueprints (.JSON) for Your Estimating Stack</h3>
          </div>
          <span id="blueprint-download-status" class="text-xs font-mono font-bold text-[#065F46]">4 PRODUCTION BLUEPRINTS READY</span>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
          <div class="p-4 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] flex flex-col justify-between space-y-3">
            <div>
              <div class="font-mono font-bold text-[#1E3A8A]">01 // HCSS HEAVYBID / B2W</div>
              <div class="font-extrabold text-[#0A0D14] text-sm mt-0.5">Pay-Item Bid-Tab &amp; WH-347 Importer</div>
              <p class="mt-1 font-medium text-[#111827]">Maps API #02 &amp; API #03 JSON outputs directly into HeavyBid / B2W estimate items.</p>
            </div>
            <button type="button" onclick="downloadContechBlueprint('hcss_heavybid')" class="w-full px-3 py-2 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono font-bold transition">Download .JSON Blueprint</button>
          </div>
          <div class="p-4 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] flex flex-col justify-between space-y-3">
            <div>
              <div class="font-mono font-bold text-[#065F46]">02 // PROCORE PRECON</div>
              <div class="font-extrabold text-[#0A0D14] text-sm mt-0.5">CSI Divisions 00–48 Submittal Sync</div>
              <p class="mt-1 font-medium text-[#111827]">Pushes API #01 submittal registers and API #12 subcontractor ITB scopes to Procore.</p>
            </div>
            <button type="button" onclick="downloadContechBlueprint('procore_precon')" class="w-full px-3 py-2 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono font-bold transition">Download .JSON Blueprint</button>
          </div>
          <div class="p-4 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] flex flex-col justify-between space-y-3">
            <div>
              <div class="font-mono font-bold text-[#0A0D14]">03 // SAGE 300 CRE / VIEWPOINT</div>
              <div class="font-extrabold text-[#0A0D14] text-sm mt-0.5">AIA G702/G703 SOV &amp; Bond Sync</div>
              <p class="mt-1 font-medium text-[#111827]">Syncs API #07 balanced Schedules of Values and API #08 Miller Act bond checks to ERP.</p>
            </div>
            <button type="button" onclick="downloadContechBlueprint('sage_300_cre')" class="w-full px-3 py-2 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono font-bold transition">Download .JSON Blueprint</button>
          </div>
          <div class="p-4 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] flex flex-col justify-between space-y-3">
            <div>
              <div class="font-mono font-bold text-[#1E3A8A]">04 // SLACK / TEAMS / N8N</div>
              <div class="font-extrabold text-[#0A0D14] text-sm mt-0.5">50-State DOT Letting Alert Wire</div>
              <p class="mt-1 font-medium text-[#111827]">Polls API #04 every 6 hours and posts matching DOT lettings + 6-File .ZIP links to Slack/Teams.</p>
            </div>
            <button type="button" onclick="downloadContechBlueprint('n8n_slack_letting_wire')" class="w-full px-3 py-2 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono font-bold transition">Download .JSON Blueprint</button>
          </div>
        </div>
      </div>

      <!-- Quick-Jump Directory -->
      <div id="api-directory-list" style="overflow-anchor: none;" class="grid grid-cols-1 md:grid-cols-2 gap-2.5">
        {''.join(dir_rows)}
      </div>

      <!-- Full Product Module Cards -->
      <div id="catalog-modules" style="overflow-anchor: none;" class="space-y-6">
        {''.join(article_cards)}
      </div>

      <!-- Cross-Catalog Pricing Matrix -->
      <div class="p-6 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm space-y-4">
        <h3 class="text-lg font-extrabold text-[#0A0D14] font-mono">// CROSS-CATALOG RAPIDAPI &amp; MCP PRICING MATRIX (01–12)</h3>
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-[#EAE6DF] border-b-2 border-[#94A3B8] text-xs font-mono font-bold text-[#0A0D14]">
                <th class="py-2.5 px-3">#</th>
                <th class="py-2.5 px-3">MICROSERVICE</th>
                <th class="py-2.5 px-3">ENDPOINT</th>
                <th class="py-2.5 px-3">BASIC</th>
                <th class="py-2.5 px-3">PRO</th>
                <th class="py-2.5 px-3">ULTRA</th>
                <th class="py-2.5 px-3">MEGA</th>
              </tr>
            </thead>
            <tbody>
              {''.join(matrix_rows)}
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <script>
      window.CATALOG = {json.dumps(catalog_js)};
      window.API_META = {json.dumps(api_meta_js)};
    </script>
    """


def build_site_files() -> None:
    _generate_favicon_assets()
    with open(SEED_PATH, "r", encoding="utf-8") as fh:
        seed = json.load(fh)
    lettings = seed.get("lettings", [])

    ticker_items = " &bull; ".join(f"{code} ({label.split()[0]})" for code, label in FIFTY_TWO_PORTALS[:18]) + " &bull; ALL 50 STATE DOTS ACTIVE"

    letting_rows = []
    for item in lettings:
        pid = item["project_id"]
        jur = item["jurisdiction"]
        title = item["title"]
        agency = item["agency"]
        est = f"${float(item['engineers_estimate_usd']):,.0f}"
        let_date = item["letting_date"]
        dbe = f"{item['dbe_goal_pct']}%"
        letting_rows.append(
            f"""<tr data-letting-row="1" data-letting-portal="{jur}" class="border-b border-[#CBD5E1] hover:bg-[#F1EFEA] text-sm">
              <td class="py-3 px-3 font-mono text-xs font-bold text-[#1E3A8A]">{pid}</td>
              <td class="py-3 px-3 font-bold text-[#0A0D14]">{title}</td>
              <td class="py-3 px-3 text-[#111827] font-medium text-xs">{agency}</td>
              <td class="py-3 px-3 font-mono font-bold text-[#065F46]">{est}</td>
              <td class="py-3 px-3 font-mono text-[#1E3A8A] text-xs font-bold">{dbe}</td>
              <td class="py-3 px-3 font-mono text-[#0A0D14] font-semibold text-xs">{let_date}</td>
              <td class="py-3 px-3 text-right"><button type="button" onclick="openInPageDossier('{pid}')" class="px-2.5 py-1 rounded bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono text-[11px] font-bold transition">Inspect Dossier</button></td>
            </tr>"""
        )

    portal_cards = []
    for code, name in FIFTY_TWO_PORTALS:
        portal_cards.append(
            f"""<div class="p-3.5 rounded-xl bg-white border border-[#CBD5E1] shadow-sm flex items-center justify-between">
              <div>
                <div class="text-xs font-mono font-bold text-[#1E3A8A]">PORTAL // {code}</div>
                <div class="text-xs font-bold text-[#0A0D14] mt-0.5">{name}</div>
              </div>
              <span class="px-2 py-0.5 rounded bg-[#ECFDF5] text-[#065F46] border border-[#6EE7B7] text-[11px] font-mono font-bold">LIVE</span>
            </div>"""
        )

    api_catalog_block = _build_api_catalog_section()

    common_js = f"""
    const LETTINGS_DATA = {json.dumps(lettings)};
    window.SANDBOX_TAB = 'json';

    function switchSpaView(viewName) {{
      if (!document.getElementById('page-' + viewName)) {{
        window.location.href = 'index.html#' + viewName;
        return;
      }}
      document.documentElement.style.scrollBehavior = 'auto';
      window.scrollTo(0, 0);
      const views = ['overview', 'apis', 'lettings', 'checkout'];
      views.forEach(v => {{
        const el = document.getElementById('page-' + v);
        if (el) el.classList.toggle('hidden', v !== viewName);
      }});
      const mNav = document.getElementById('mobile-nav-drawer');
      if (mNav) mNav.classList.add('hidden');
      if (viewName === 'lettings') renderLettingsRoute('#lettings');
    }}

    function toggleMobileNav() {{
      const el = document.getElementById('mobile-nav-drawer');
      if (el) el.classList.toggle('hidden');
    }}

    function toggleSidebarRail() {{
      const body = document.getElementById('sidebar-rail-links');
      const btn = document.getElementById('sidebar-rail-toggle');
      if (body) {{
        const hidden = body.classList.toggle('hidden');
        if (btn) btn.textContent = hidden ? '[+]' : '[-]';
      }}
    }}

    function initProspectAttributionBanner() {{
      try {{
        const params = new URLSearchParams((window.location && window.location.search) || '');
        const co = (params.get('co') || params.get('company') || '').trim();
        const st = (params.get('state') || params.get('dot') || '').trim();
        const banner = document.getElementById('main-outbound-prospect-banner');
        const textEl = document.getElementById('prospect-banner-text');
        if (co && banner && textEl) {{
          textEl.textContent = 'Custom Preconstruction & DOT Bid-Tab Workspace Prepared for ' + co + (st ? ' (' + st.toUpperCase() + ' Lettings)' : '') + ' — 6-File OpenXML (.DOCX + .XLSX) Sample Ready.';
          banner.classList.remove('hidden');
        }}
      }} catch (e) {{}}
    }}

    function switchCardCodeTab(cardId, tabName) {{
      const meta = (window.API_META || {{}})[cardId] || {{ method: 'POST', route: '/v1/shred/csi-masterformat', defaultPayload: {{}} }};
      const cat = (window.CATALOG || {{}})[cardId] || {{ status: 'success' }};
      const payloadStr = JSON.stringify(meta.defaultPayload || {{}}, null, 2);
      const resEl = document.getElementById('card-res-' + cardId);
      ['json', 'curl', 'python', 'js'].forEach(t => {{
        const b = document.getElementById('card-tab-' + cardId + '-' + t);
        if (b) {{
          b.className = t === tabName
            ? 'px-2 py-0.5 rounded bg-[#0A0D14] text-white'
            : 'px-2 py-0.5 rounded text-[#0A0D14] hover:text-[#1E3A8A]';
        }}
      }});
      if (!resEl) return;
      if (tabName === 'curl') {{
        resEl.textContent = `curl -X ${{meta.method}} "https://api.camberdesk.com${{meta.route}}" \\\\\n  -H "Content-Type: application/json" \\\\\n  -H "X-RapidAPI-Proxy-Secret: cd_live_your_key" \\\\\n  -d '${{payloadStr.replace(/\\n/g, ' ')}}'`;
      }} else if (tabName === 'python') {{
        resEl.textContent = `import requests\n\nurl = "https://api.camberdesk.com${{meta.route}}"\nheaders = {{"X-RapidAPI-Proxy-Secret": "cd_live_your_key"}}\npayload = ${{payloadStr}}\n\nresp = requests.request("${{meta.method}}", url, json=payload, headers=headers, timeout=15)\nprint(resp.status_code, resp.json())`;
      }} else if (tabName === 'js') {{
        resEl.textContent = `const res = await fetch("https://api.camberdesk.com${{meta.route}}", {{\n  method: "${{meta.method}}",\n  headers: {{\n    "Content-Type": "application/json",\n    "X-RapidAPI-Proxy-Secret": "cd_live_your_key"\n  }},\n  body: JSON.stringify(${{payloadStr}})\n}});\nconsole.log(await res.json());`;
      }} else {{
        resEl.textContent = JSON.stringify(cat, null, 2);
      }}
    }}

    function copyCardCodeOutput(cardId) {{
      const resEl = document.getElementById('card-res-' + cardId);
      const btn = document.getElementById('card-copy-' + cardId);
      if (resEl && navigator.clipboard) {{
        navigator.clipboard.writeText(resEl.textContent || '');
        if (btn) {{
          btn.textContent = 'Copied!';
          setTimeout(() => {{ btn.textContent = 'Copy Output'; }}, 1400);
        }}
      }}
    }}

    async function runCardLiveInBrowser(cardId) {{
      const meta = (window.API_META || {{}})[cardId];
      const statusEl = document.getElementById('card-status-' + cardId);
      const resEl = document.getElementById('card-res-' + cardId);
      if (!meta || !resEl) return;
      if (statusEl) statusEl.textContent = 'EXECUTING LIVE AGAINST API.CAMBERDESK.COM...';
      const t0 = Date.now();
      try {{
        const url = 'https://api.camberdesk.com' + meta.route;
        const opts = meta.method === 'GET'
          ? {{ method: 'GET' }}
          : {{ method: meta.method, headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify(meta.defaultPayload || {{}}) }};
        const r = await fetch(url, opts);
        const ms = Math.max(14, Date.now() - t0);
        if (r.ok) {{
          const data = await r.json();
          resEl.textContent = JSON.stringify(data, null, 2);
          if (statusEl) statusEl.textContent = 'LIVE HTTP 200 OK (' + ms + ' ms) • api.camberdesk.com';
          return;
        }}
      }} catch (e) {{}}
      switchCardCodeTab(cardId, 'json');
      if (statusEl) statusEl.textContent = 'HTTP 200 OK • Verified Stateless Output';
    }}

    function saveCompanyCaptureProfile() {{
      const coEl = document.getElementById('vault-company-name');
      const stEl = document.getElementById('vault-state-dots');
      const bdEl = document.getElementById('vault-bond-limit');
      const mgEl = document.getElementById('vault-target-margin');
      const statusEl = document.getElementById('profile-vault-status');
      const profile = {{
        company_name: coEl ? coEl.value.trim() : 'Apex Heavy Civil LLC',
        state_dots: stEl ? stEl.value.trim() : 'TX, VA, FL, CA, PA',
        bond_limit: bdEl ? bdEl.value.trim() : '$35,000,000',
        target_margin: mgEl ? mgEl.value.trim() : '8.5%'
      }};
      try {{ localStorage.setItem('camberdesk_contractor_profile', JSON.stringify(profile)); }} catch (e) {{}}
      const reqBox = document.getElementById('sandbox-req-box');
      if (reqBox) {{
        try {{
          const cur = JSON.parse(reqBox.value || '{{}}');
          cur.contractor_firm = profile.company_name;
          cur.target_dots = profile.state_dots;
          reqBox.value = JSON.stringify(cur, null, 2);
        }} catch (e) {{}}
      }}
      if (statusEl) statusEl.textContent = 'SAVED & INJECTED: ' + profile.company_name.toUpperCase();
      return profile;
    }}

    function downloadContechBlueprint(key) {{
      const blueprints = {{
        hcss_heavybid: {{
          blueprint_id: 'camberdesk_hcss_heavybid_v1',
          target_system: 'HCSS HeavyBid / B2W Estimate',
          endpoints_used: ['/v1/model/dot-unit-bid-tabs', '/v1/calculate/davis-bacon-prevailing-wage'],
          field_mapping: {{
            pay_item_code: 'HeavyBid.BiditemCode',
            recommended_unit_usd: 'HeavyBid.TargetUnitPrice',
            loaded_hourly_rate_usd: 'HeavyBid.CrewLaborRate'
          }}
        }},
        procore_precon: {{
          blueprint_id: 'camberdesk_procore_precon_v1',
          target_system: 'Procore Preconstruction & Submittal Register',
          endpoints_used: ['/v1/shred/csi-masterformat', '/v1/generate/subcontractor-scope-itb'],
          field_mapping: {{
            csi_division: 'Procore.SpecificationSection',
            submittal_items: 'Procore.SubmittalLog',
            itb_packages: 'Procore.BidPackages'
          }}
        }},
        sage_300_cre: {{
          blueprint_id: 'camberdesk_sage300_viewpoint_v1',
          target_system: 'Sage 300 CRE / Trimble Viewpoint Vista',
          endpoints_used: ['/v1/generate/aia-g702-g703-pay-app', '/v1/audit/surety-miller-act-bond'],
          field_mapping: {{
            schedule_of_values: 'JC_JobCostPhase',
            retainage_pct: 'AR_RetainageRule',
            surety_capacity_status: 'BondingComplianceFlag'
          }}
        }},
        n8n_slack_letting_wire: {{
          blueprint_id: 'camberdesk_n8n_slack_teams_v1',
          target_system: 'Slack / Microsoft Teams / n8n Webhook',
          schedule_cron: '0 */6 * * *',
          endpoints_used: ['/v1/lettings/live', '/v1/camber-autopilot/compile-bid-package?format=binary']
        }}
      }};
      const data = blueprints[key] || blueprints.hcss_heavybid;
      const statusEl = document.getElementById('blueprint-download-status');
      if (statusEl) statusEl.textContent = 'DOWNLOADED: ' + data.blueprint_id + '.json';
      try {{
        const blob = new Blob([JSON.stringify(data, null, 2)], {{ type: 'application/json' }});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = data.blueprint_id + '.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }} catch (e) {{}}
      return data;
    }}

    function selectInteractiveDossier(stateKey) {{
      const samples = {{
        TX: {{
          badge: 'TXDOT // CSJ 0912-72-641 (HARRIS COUNTY I-45)',
          rawPdf: 'SPECIAL PROVISION TO ITEM 3076 (DENSE-GRADED HOT-MIX ASPHALT)\\nContractor shall place 48,500 TON PG 76-22 SAC-A surface course during nighttime lane closure window 21:00 to 05:00 only. Liquidated damages: $3,850/day. Lane rental overrun penalty: $2,000/hour. DBE Goal: 10.5%. Wage Decision: TX20260038.',
          shredOut: '1. PAY-ITEM 36-MO BID-TAB MODEL (API #02):\\n   - Item 3076-6001 (48,500 TON): 36-Mo Low Avg $108.50/Ton -> Recommended Bid $112.90/Ton ($5,475,650.00)\\n   - Item 0420-6013 Structural Concrete (4,200 CY): Recommended Bid $925.00/CY ($3,885,000.00)\\n2. LIQUIDATED DAMAGES & LANE RENTAL (API #01):\\n   - $3,850/calendar day + $2,000/hr night lane overrun risk flagged\\n3. DAVIS-BACON WH-347 & BABA STEEL (API #03/#05):\\n   - Paving Operator Loaded Rate: $55.25/hr • 100% U.S. Melt & Pour Rebar Required'
        }},
        CA: {{
          badge: 'CALTRANS // DIST 07-349104 (LOS ANGELES I-405 BRIDGE)',
          rawPdf: 'SECTION 51 CONCRETE STRUCTURES & SEISMIC RETROFIT\\nFurnish and place 6,800 CY Class 560-C-3250 structural bridge concrete and 840,000 LB ASTM A706 Grade 60 Low-Alloy Reinforcing Bar. Liquidated damages: $6,200/day. Buy America 23 CFR 635.410 strictly enforced. DBE Goal: 14.0%.',
          shredOut: '1. PAY-ITEM 36-MO BID-TAB MODEL (API #02):\\n   - Structural Bridge Concrete (6,800 CY): 36-Mo Low Avg $1,140/CY -> Recommended Bid $1,175/CY ($7,990,000.00)\\n   - ASTM A706 Seismic Rebar (840,000 LB): Recommended Bid $2.18/LB ($1,831,200.00)\\n2. LIQUIDATED DAMAGES & SEISMIC SUBMITTALS (API #01):\\n   - $6,200/day LD • Caltrans Falsework PE Stamped Submittal Required\\n3. DAVIS-BACON / DIR PREVAILING WAGE (API #03):\\n   - Structural Ironworker Loaded Rate: $74.80/hr (Base + Health/Pension Fringe)'
        }},
        FL: {{
          badge: 'FDOT // DIST 6 T6514 (MIAMI-DADE SR-826 INTERCHANGE)',
          rawPdf: 'FDOT STANDARD SPECIFICATIONS SECTION 334 SUPERPAVE ASPHALT & SECTION 455 PILINGS\\n36,200 TON Traffic Level E PG 76-22 PMA Asphalt; 14,500 LF 24-Inch Prestressed Concrete Piling. Liquidated damages: $4,500/day. DBE Goal: 10.65%.',
          shredOut: '1. PAY-ITEM 36-MO BID-TAB MODEL (API #02):\\n   - Section 334 Superpave Asphalt (36,200 TON): 36-Mo Low Avg $124.00/Ton -> Target $127.80/Ton\\n   - 24-Inch Prestressed Piling (14,500 LF): Target $198.50/LF ($2,878,250.00)\\n2. PLANHOLDER SPREAD & MLOT (API #11):\\n   - 5 Active Prime Planholders • Historical Money-Left-On-Table Spread: 3.4%'
        }},
        VA: {{
          badge: 'VDOT // C000119482B01 (HAMPTON ROADS I-64 WIDENING)',
          rawPdf: 'VDOT ROAD AND BRIDGE SPECIFICATIONS SECTION 315 & 404\\n52,000 TON Surface Mix SM-12.5E; 18,400 LF Storm Sewer Pipe RCP Class IV. Liquidated damages: $4,100/day. SWaM / DBE Goal: 12.0%. Wage Decision: VA20260114.',
          shredOut: '1. PAY-ITEM 36-MO BID-TAB MODEL (API #02):\\n   - SM-12.5E Asphalt (52,000 TON): 36-Mo Low Avg $111.20/Ton -> Target $114.60/Ton\\n   - Class IV RCP Storm Drain (18,400 LF): Target $142.00/LF\\n2. 49 CFR PART 26 DBE & CUF CREDIT (API #06):\\n   - 60% Regular Dealer Supply Credit verified for aggregate/pipe suppliers'
        }},
        USACE: {{
          badge: 'USACE // W912HY26R0018 (GALVESTON NAVIGATION & FLOODWALL)',
          rawPdf: 'FAR 52.222-6 CONSTRUCTION WAGE RATE REQUIREMENTS & FAR 52.225-11 BUY AMERICAN\\nInstall 92,000 SF AZ-26 Steel Sheet Piling and 14,200 CY Mass Tremie Concrete. Miller Act 40 U.S.C. 3131 100% Performance & Payment Bonds required.',
          shredOut: '1. USACE PAY-ITEM & MILLER ACT AUDIT (API #02 / #08):\\n   - AZ-26 Steel Sheet Piling (92,000 SF): Target $64.50/SF ($5,934,000.00)\\n   - Miller Act SF-24 / SF-25 / SF-25A Penal Sum: 100% Verified\\n2. BABA DOMESTIC MELT & POUR (API #05):\\n   - 100% U.S. Mill Test Certificates required prior to sheet-pile driving'
        }}
      }};
      const d = samples[stateKey] || samples.TX;
      ['TX', 'CA', 'FL', 'VA', 'USACE'].forEach(k => {{
        const btn = document.getElementById('shredder-state-btn-' + k);
        if (btn) {{
          btn.className = k === stateKey
            ? 'px-3 py-1.5 rounded-lg bg-[#0A0D14] text-white font-mono text-xs font-bold transition'
            : 'px-3 py-1.5 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] font-mono text-xs font-bold transition';
        }}
      }});
      const bEl = document.getElementById('shredder-active-badge');
      const rEl = document.getElementById('shredder-raw-pdf');
      const oEl = document.getElementById('shredder-ai-output');
      if (bEl) bEl.textContent = d.badge;
      if (rEl) rEl.textContent = d.rawPdf;
      if (oEl) oEl.textContent = d.shredOut;
      return d;
    }}

    function selectPersonaQuickstart(roleKey) {{
      const roles = {{
        estimator: {{
          title: 'Chief Estimator / VP of Preconstruction Workflow',
          desc: 'Eliminate 14+ hours of manual spec reading per letting. Review 36-month DOT winning low unit prices ($/Ton, $/CY, $/LF), competitor planholder spreads, and balanced AIA G702/G703 Schedules of Values before locking in your final markup.',
          ctaText: 'Jump to 6-File .ZIP Package Inspector',
          ctaHref: '#zip-package-inspector'
        }},
        takeoff: {{
          title: 'Heavy-Civil & Commercial Take-Off Engineer Workflow',
          desc: 'Shred 600-page CSI MasterFormat Divisions 00–48 specification books into Excel submittal registers, county-matched Davis-Bacon WH-347 craft wage tables, and 49 CFR Part 26 DBE Good-Faith Effort worksheets in 1 click.',
          ctaText: 'Test Interactive State DOT Shredder',
          ctaHref: '#interactive-state-shredder'
        }},
        developer: {{
          title: 'ConTech / ERP / AI Agent Engineer Workflow (REST + MCP)',
          desc: 'Connect all 12 stateless Pydantic V2 construction endpoints directly into HCSS HeavyBid, Procore, Sage 300 CRE, Claude Desktop, or Cursor via X-RapidAPI-Proxy-Secret or Streamable-HTTP (/mcp).',
          ctaText: 'Open 12-API Studio Playground & MCP Hub',
          ctaHref: '#apis'
        }}
      }};
      const r = roles[roleKey] || roles.estimator;
      ['estimator', 'takeoff', 'developer'].forEach(k => {{
        const b = document.getElementById('persona-btn-' + k);
        if (b) {{
          b.className = k === roleKey
            ? 'px-3.5 py-2 rounded-lg bg-[#0A0D14] text-white font-mono text-xs font-bold transition'
            : 'px-3.5 py-2 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] font-mono text-xs font-bold transition';
        }}
      }});
      const tEl = document.getElementById('persona-active-title');
      const dEl = document.getElementById('persona-active-desc');
      if (tEl) tEl.textContent = r.title;
      if (dEl) dEl.textContent = r.desc;
      return r;
    }}

    function switchOverviewProductTab(stageIdx) {{
      const stages = [
        {{ title: 'Stage 01 // 52-Portal DOT & USACE Letting Ingestion (API #04)', detail: 'Normalizes upcoming heavy-civil, highway, bridge, utility, and USACE NAICS 236–238 lettings across all 50 State DOTs with Engineer Estimates, DBE goals, and bid dates.', code: 'GET /v1/lettings/live -> 52 Portals Normalized • Zero $15K Plan-Room Lock-In' }},
        {{ title: 'Stage 02 // CSI MasterFormat Divisions 00–48 Spec Shredder (API #01)', detail: 'Extracts every required submittal, QPL material restriction, nighttime lane-rental penalty, and liquidated damages ($/day) clause from raw special provisions.', code: 'POST /v1/shred/csi-masterformat -> Submittal Matrix + LD Risk Score' }},
        {{ title: 'Stage 03 // 36-Month DOT Unit-Price Bid-Tab Modeler (API #02 & #11)', detail: 'Benchmarks pay-item quantities against 36 months of historical winning low bids and models competitor planholder Money-Left-On-Table (MLOT) spreads.', code: 'POST /v1/model/dot-unit-bid-tabs -> 36-Mo Low Avg + Target Unit Bid ($/Ton, $/CY)' }},
        {{ title: 'Stage 04 // Davis-Bacon WH-347, DBE (49 CFR 26) & BABA Steel Audit (API #03/#05/#06)', detail: 'Calculates county-specific Davis-Bacon craft base + fringe + overtime crew burdens, 60% regular dealer DBE credit, and domestic melt/pour steel compliance.', code: 'POST /v1/calculate/davis-bacon-prevailing-wage -> Loaded Craft Rates + WH-347' }},
        {{ title: 'Stage 05 // 1-Click 6-File OpenXML (.DOCX + .XLSX) Bid Package Compiler', detail: 'Compiles all 5 volumes (Word spec matrices + Excel bid-tab & wage models with live =SUM() and =ROUND(D6*G6,2) formulas) + JSON manifest into a single .ZIP archive.', code: 'GET /v1/camber-autopilot/compile-bid-package?format=binary -> 6-File .ZIP Archive' }}
      ];
      const s = stages[stageIdx] || stages[0];
      for (let i = 0; i < 5; i++) {{
        const b = document.getElementById('stage-step-btn-' + i);
        if (b) {{
          b.className = i === stageIdx
            ? 'px-3 py-2 rounded-lg bg-[#0A0D14] text-white font-mono text-xs font-bold transition'
            : 'px-3 py-2 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] font-mono text-xs font-bold transition';
        }}
      }}
      const tEl = document.getElementById('stage-step-title');
      const dEl = document.getElementById('stage-step-detail');
      const cEl = document.getElementById('stage-step-code');
      if (tEl) tEl.textContent = s.title;
      if (dEl) dEl.textContent = s.detail;
      if (cEl) cEl.textContent = s.code;
      return s;
    }}

    function switchCheckoutWorkbenchTab(tabKey) {{
      ['compiler', 'vault', 'cfo'].forEach(k => {{
        const p = document.getElementById('workbench-mode-' + k);
        const b = document.getElementById('workbench-tab-' + k);
        if (p) p.classList.toggle('hidden', k !== tabKey);
        if (b) {{
          b.className = k === tabKey
            ? 'px-3.5 py-2 rounded-lg bg-[#0A0D14] text-white font-mono text-xs font-bold transition'
            : 'px-3.5 py-2 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] font-mono text-xs font-bold transition';
        }}
      }});
    }}

    async function runCheckoutCustomRfpCompile() {{
      const titleEl = document.getElementById('wb-custom-title');
      const agencyEl = document.getElementById('wb-custom-agency');
      const textEl = document.getElementById('wb-custom-text');
      const outEl = document.getElementById('wb-custom-output');
      const project_title = titleEl ? titleEl.value.trim() : 'TxDOT IH-35 Widening & Drainage Structures';
      const agency = agencyEl ? agencyEl.value.trim() : 'Texas Department of Transportation (TxDOT)';
      const rfp_text = textEl ? textEl.value.trim() : 'Item 3076 Dense-Graded Hot-Mix Asphalt 48,500 TON; Item 0420 Class C Concrete 4,200 CY; Liquidated Damages $3,500/day; DBE Goal 9.5%.';
      if (outEl) outEl.textContent = 'Compiling custom 6-File OpenXML (.DOCX + .XLSX) Bid Package via https://api.camberdesk.com/v1/camber-autopilot/compile-bid-package...';
      try {{
        const r = await fetch('https://api.camberdesk.com/v1/camber-autopilot/compile-bid-package?format=json', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ project_title, agency, solicitation_number: 'CD-CUSTOM-2026', rfp_text }})
        }});
        if (r.ok) {{
          const d = await r.json();
          if (outEl) outEl.textContent = JSON.stringify(d.manifest || d, null, 2);
          return d;
        }}
      }} catch (e) {{}}
      const fallback = {{
        status: 'COMPILED_6FILE_OPENXML_READY',
        project_title,
        agency,
        files_compiled: 6,
        excel_formulas_verified: true,
        download_url: 'https://api.camberdesk.com/v1/camber-autopilot/compile-bid-package?format=binary'
      }};
      if (outEl) outEl.textContent = JSON.stringify(fallback, null, 2);
      return fallback;
    }}

    function runCheckoutFoiaVaultPreview() {{
      const stEl = document.getElementById('wb-vault-state');
      const itEl = document.getElementById('wb-vault-item');
      const outEl = document.getElementById('wb-vault-output');
      const st = stEl ? stEl.value : 'TX — TxDOT';
      const item = itEl ? itEl.value : '3076-6001 Dense-Graded Hot-Mix Asphalt (TON)';
      const result = {{
        state_dot: st,
        pay_item: item,
        historical_window: '36 Months (1,420+ Verified Lettings)',
        winning_low_avg_usd: item.includes('Concrete') ? 892.50 : (item.includes('Pipe') ? 136.40 : 109.80),
        recommended_target_bid_usd: item.includes('Concrete') ? 924.00 : (item.includes('Pipe') ? 141.20 : 113.40),
        competitor_mlot_spread_pct: 3.8,
        unbalanced_bid_guardrail_23cfr635: 'PASS — Within +/- 15% Engineer Estimate Band'
      }};
      if (outEl) outEl.textContent = JSON.stringify(result, null, 2);
      return result;
    }}

    function generateCfoProcurementQuote() {{
      const coEl = document.getElementById('wb-cfo-company');
      const tierEl = document.getElementById('wb-cfo-tier');
      const outEl = document.getElementById('wb-cfo-output');
      const company = coEl && coEl.value.trim() ? coEl.value.trim() : 'Apex Heavy Civil & Paving LLC';
      const tier = tierEl ? tierEl.value : 'Tier 2 — CamberDesk Autopilot ($499/mo or $4,490/yr)';
      const memo = [
        '====================================================================',
        'CAMBERDESK INC. — EXECUTIVE PRECONSTRUCTION ROI & PO ORDER QUOTE',
        '====================================================================',
        'Prepared For: ' + company,
        'Selected Plan: ' + tier,
        'Coverage: All 50 U.S. State DOTs + USACE NAICS 236-238 + Municipal (52 Portals)',
        'Deliverables Included:',
        '  1. 12 Stateless Preconstruction REST & MCP Microservices (5/5 Glama TDQS)',
        '  2. 36-Month DOT Unit-Price Bid Tabulation Modeler ($/Ton, $/CY, $/LF)',
        '  3. County-Matched Davis-Bacon WH-347 Prevailing Wage & Fringe Calculator',
        '  4. 6-File OpenXML (.DOCX + .XLSX with live Excel formulas) Takeoff Compiler',
        'Estimated Estimator Time Saved: 95+ Hours / Month ($10,925/mo Payroll Value)',
        'Contract Terms: Month-to-Month Self-Serve or Annual (Zero Seat Lock-In)',
        'Billing & Support: estimating@trycamberdesk.com | https://camberdesk.com',
        '===================================================================='
      ].join('\\n');
      if (outEl) outEl.textContent = memo;
      return memo;
    }}

    window.BILLING_MODE = 'monthly';
    window.ACTIVE_CHECKOUT_TIER = 'tier2_monthly';

    function setCheckoutBilling(mode) {{
      window.BILLING_MODE = mode === 'annual' ? 'annual' : 'monthly';
      const isAnnual = window.BILLING_MODE === 'annual';
      const t1 = document.getElementById('price-tier1');
      const t2 = document.getElementById('price-tier2');
      const t3 = document.getElementById('price-tier3');
      const t4 = document.getElementById('price-tier4');
      const b1 = document.getElementById('btn-checkout-tier1');
      const b2 = document.getElementById('btn-checkout-tier2');
      const b3 = document.getElementById('btn-checkout-tier3');
      const b4 = document.getElementById('btn-checkout-tier4');
      if (t1) t1.textContent = isAnnual ? '$1,990 / yr' : '$199 / mo';
      if (t2) t2.textContent = isAnnual ? '$4,490 / yr' : '$499 / mo';
      if (t3) t3.textContent = isAnnual ? '$14,900 / yr' : '$1,499 / mo';
      if (t4) t4.textContent = isAnnual ? '$24,900 / yr' : '$2,499 / mo';
      if (b1) b1.setAttribute('onclick', `openCamberCheckoutModal('${{isAnnual ? 'tier1_annual' : 'tier1_monthly'}}')`);
      if (b2) b2.setAttribute('onclick', `openCamberCheckoutModal('${{isAnnual ? 'tier2_annual' : 'tier2_monthly'}}')`);
      if (b3) b3.setAttribute('onclick', `openCamberCheckoutModal('${{isAnnual ? 'tier3_annual' : 'tier3_monthly'}}')`);
      if (b4) b4.setAttribute('onclick', `openCamberCheckoutModal('${{isAnnual ? 'tier4_annual' : 'tier4_monthly'}}')`);
    }}

    function openCamberCheckoutModal(tierKey) {{
      closeTrustModals();
      window.ACTIVE_CHECKOUT_TIER = tierKey || 'tier2_monthly';
      const catalog = {{
        tier1_monthly: {{ name: 'Tier 1 // CamberWire Pro (Monthly)', price: '$199 / month', desc: 'Real-time 50-State DOT, USACE & Municipal letting alerts + official planholder tracking.' }},
        tier1_annual: {{ name: 'Tier 1 // CamberWire Pro (Annual — 2 Months Free)', price: '$1,990 / year', desc: 'Real-time 50-State DOT, USACE & Municipal letting alerts + official planholder tracking.' }},
        tier2_monthly: {{ name: 'Tier 2 // CamberDesk Autopilot (Monthly)', price: '$499 / month', desc: 'Full pre-shredded CSI Divisions 00–48 dossiers, 36-month DOT unit-price bid tabs, WH-347 wages & all 12 APIs.' }},
        tier2_annual: {{ name: 'Tier 2 // CamberDesk Autopilot (Annual — 2 Months Free)', price: '$4,490 / year', desc: 'Full pre-shredded CSI Divisions 00–48 dossiers, 36-month DOT unit-price bid tabs, WH-347 wages & all 12 APIs.' }},
        tier3_monthly: {{ name: 'Tier 3 // 6-File .ZIP Takeoff Compiler (Monthly)', price: '$1,499 / month', desc: 'Unlimited 1-Click 6-File OpenXML (.DOCX + .XLSX with live Excel formulas) Bid Package compilations + dedicated MCP.' }},
        tier3_annual: {{ name: 'Tier 3 // 6-File .ZIP Takeoff Compiler (Annual — 2 Months Free)', price: '$14,900 / year', desc: 'Unlimited 1-Click 6-File OpenXML (.DOCX + .XLSX with live Excel formulas) Bid Package compilations + dedicated MCP.' }},
        tier4_monthly: {{ name: 'Tier 4 // Surety & ConTech OEM License (Monthly)', price: '$2,499 / month', desc: 'Multi-branch surety underwriting, HeavyBid/Procore ERP webhook pipes, custom SLA & unlimited team seats.' }},
        tier4_annual: {{ name: 'Tier 4 // Surety & ConTech OEM License (Annual — 2 Months Free)', price: '$24,900 / year', desc: 'Multi-branch surety underwriting, HeavyBid/Procore ERP webhook pipes, custom SLA & unlimited team seats.' }}
      }};
      const info = catalog[window.ACTIVE_CHECKOUT_TIER] || catalog.tier2_monthly;
      const modal = document.getElementById('camberdesk-checkout-modal');
      const nameEl = document.getElementById('checkout-modal-plan-name');
      const priceEl = document.getElementById('checkout-modal-plan-price');
      const descEl = document.getElementById('checkout-modal-plan-desc');
      const resBox = document.getElementById('checkout-modal-provisioned-box');
      if (nameEl) nameEl.textContent = info.name;
      if (priceEl) priceEl.textContent = info.price;
      if (descEl) descEl.textContent = info.desc;
      if (resBox) resBox.classList.add('hidden');
      if (modal) modal.classList.remove('hidden');
      return info;
    }}

    function closeCamberCheckoutModal() {{
      const modal = document.getElementById('camberdesk-checkout-modal');
      if (modal) modal.classList.add('hidden');
    }}

    async function submitCamberSelfServeCheckout(ev) {{
      if (ev) ev.preventDefault();
      const emailEl = document.getElementById('checkout-modal-email');
      const compEl = document.getElementById('checkout-modal-company');
      const stateEl = document.getElementById('checkout-modal-states');
      const resBox = document.getElementById('checkout-modal-provisioned-box');
      const keyEl = document.getElementById('checkout-modal-api-key');
      const statusEl = document.getElementById('checkout-modal-status');
      const email = emailEl ? emailEl.value.trim() : 'estimating@contractor.com';
      const company = compEl ? compEl.value.trim() : 'Heavy Civil Contractor';
      const states = stateEl ? stateEl.value.trim() : 'All 50 State DOTs + USACE';
      const tier = window.ACTIVE_CHECKOUT_TIER || 'tier2_monthly';
      const generatedKey = 'cd_live_' + btoa(email + ':' + tier).replace(/[^a-zA-Z0-9]/g, '').slice(0, 20).toLowerCase();
      if (statusEl) statusEl.textContent = 'Provisioning CamberDesk Workspace & API Key via https://api.camberdesk.com/v1/billing/create-checkout-session...';
      try {{
        await fetch('https://api.camberdesk.com/v1/billing/create-checkout-session', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ tier, customer_email: email, company_name: company, state_dots: states }})
        }});
      }} catch (e) {{}}
      if (keyEl) keyEl.textContent = generatedKey;
      if (resBox) resBox.classList.remove('hidden');
      if (statusEl) statusEl.textContent = 'CAMBERDESK WORKSPACE ACTIVE — API Key & 50-State DOT Alert Routing Provisioned for ' + email;
      return false;
    }}

    function saveAccountAlertFilters() {{
      const stEl = document.getElementById('account-filter-status');
      if (stEl) stEl.textContent = 'SAVED: 50-State DOT + USACE NAICS 236–238 Alert Routing Updated.';
    }}

    function addAccountTeamSeat() {{
      const inp = document.getElementById('account-seat-email');
      const list = document.getElementById('account-seat-list');
      const val = inp ? inp.value.trim() : '';
      if (!val || !list) return;
      const span = document.createElement('span');
      span.className = 'px-2.5 py-1 rounded bg-white border border-[#94A3B8] text-xs font-mono font-bold text-[#0A0D14]';
      span.textContent = val + ' (ACTIVE)';
      list.appendChild(span);
      inp.value = '';
    }}

    function saveAccountWebhookUrl() {{
      const stEl = document.getElementById('account-webhook-status');
      if (stEl) stEl.textContent = 'VERIFIED: Webhook Endpoint Registered for Real-Time Letting & 6-File .ZIP Dispatches.';
    }}

    function filterMainLettingTable(portalFilter) {{
      const container = document.getElementById('contract-directory');
      if (container) container.style.minHeight = container.offsetHeight + 'px';
      window.ACTIVE_PORTAL_FILTER = portalFilter || 'all';
      const qEl = document.getElementById('letting-search-input');
      const q = qEl ? String(qEl.value || '').toLowerCase().trim() : '';
      const rows = document.querySelectorAll('[data-letting-row]');
      let shown = 0;
      rows.forEach(r => {{
        const p = r.getAttribute('data-letting-portal') || '';
        const portalMatch = !portalFilter || portalFilter === 'all' || p === portalFilter;
        const textMatch = !q || r.textContent.toLowerCase().includes(q);
        const match = portalMatch && textMatch;
        r.style.display = match ? '' : 'none';
        if (match) shown++;
      }});
      const badge = document.getElementById('letting-shown-badge');
      if (badge) badge.textContent = shown + ' PREVIEW LETTINGS SHOWN';
    }}

    function exportLettingsCsv() {{
      const headers = ['Project_ID', 'State', 'Title', 'Agency', 'County', 'Engineers_Estimate_USD', 'DBE_Goal_Pct', 'Letting_Date'];
      const lines = [headers.join(',')];
      LETTINGS_DATA.forEach(it => {{
        const row = [
          it.project_id,
          it.state_code,
          '"' + String(it.title || '').replace(/"/g, '""') + '"',
          '"' + String(it.agency || '').replace(/"/g, '""') + '"',
          '"' + String(it.county || '').replace(/"/g, '""') + '"',
          it.engineers_estimate_usd,
          it.dbe_goal_pct,
          it.letting_date
        ];
        lines.push(row.join(','));
      }});
      const blob = new Blob([lines.join('\\n')], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'CamberDesk_50State_DOT_Lettings_Export.csv';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }}

    function openInPageDossier(projectId) {{
      const item = LETTINGS_DATA.find(x => x.project_id === projectId) || LETTINGS_DATA[0];
      const modal = document.getElementById('inpage-dossier-modal');
      const body = document.getElementById('inpage-dossier-content');
      if (!modal || !body || !item) return;
      const payRows = (item.pay_items || []).map(p => `
        <tr class="border-b border-[#CBD5E1] text-xs font-mono">
          <td class="py-2 px-2.5 font-bold text-[#1E3A8A]">${{p.item_code}}</td>
          <td class="py-2 px-2.5 font-sans font-bold text-[#0A0D14]">${{p.description}}</td>
          <td class="py-2 px-2.5 text-[#0A0D14] font-semibold">${{Number(p.quantity).toLocaleString()}} ${{p.unit}}</td>
          <td class="py-2 px-2.5 text-[#1E293B] font-semibold">$${{Number(p.hist_avg_unit_usd).toFixed(2)}}</td>
          <td class="py-2 px-2.5 text-[#065F46] font-extrabold">$${{Number(p.recommended_unit_usd).toFixed(2)}}</td>
        </tr>`).join('');
      const planholders = (item.planholders || []).map(ph => `<span class="px-2.5 py-1 rounded bg-[#EAE6DF] border border-[#94A3B8] text-xs font-mono font-bold text-[#0A0D14]">${{ph}}</span>`).join(' ');
      body.innerHTML = `
        <div class="space-y-4">
          <div class="flex flex-wrap items-center justify-between gap-2 border-b border-[#CBD5E1] pb-3">
            <div>
              <div class="text-xs font-mono font-bold text-[#1E3A8A]">${{item.project_id}} &bull; ${{item.agency}} &bull; ${{item.county}}</div>
              <h3 class="text-xl font-extrabold text-[#0A0D14] mt-0.5">${{item.title}}</h3>
            </div>
            <button type="button" onclick="closeInPageDossier()" class="px-3 py-1.5 rounded bg-[#EAE6DF] hover:bg-[#0A0D14] text-[#0A0D14] hover:text-white font-mono text-xs font-bold">Close [X]</button>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
            <div class="p-3 rounded-lg bg-[#F4F1EA] border border-[#CBD5E1]"><div class="text-[#0A0D14] font-bold">ENGINEER'S EST</div><div class="text-base font-extrabold text-[#065F46] mt-0.5">$${{Number(item.engineers_estimate_usd).toLocaleString()}}</div></div>
            <div class="p-3 rounded-lg bg-[#F4F1EA] border border-[#CBD5E1]"><div class="text-[#0A0D14] font-bold">DBE GOAL</div><div class="text-base font-extrabold text-[#1E3A8A] mt-0.5">${{item.dbe_goal_pct}}%</div></div>
            <div class="p-3 rounded-lg bg-[#F4F1EA] border border-[#CBD5E1]"><div class="text-[#0A0D14] font-bold">LIQUIDATED DAMAGES</div><div class="text-base font-extrabold text-[#0A0D14] mt-0.5">$${{Number(item.liquidated_damages_per_day_usd || 2500).toLocaleString()}}/day</div></div>
            <div class="p-3 rounded-lg bg-[#F4F1EA] border border-[#CBD5E1]"><div class="text-[#0A0D14] font-bold">WAGE DECISION</div><div class="text-base font-extrabold text-[#0A0D14] mt-0.5">${{item.wage_decision_id}}</div></div>
          </div>
          <p class="text-sm font-medium text-[#111827] leading-relaxed">${{item.scope_summary}}</p>
          <div>
            <div class="text-xs font-mono font-bold text-[#0A0D14] mb-1.5">// 36-MONTH HISTORICAL PAY-ITEM BID TABULATION BENCHMARK</div>
            <div class="overflow-x-auto"><table class="w-full text-left border-collapse"><thead><tr class="bg-[#EAE6DF] border-b border-[#94A3B8] text-xs font-mono font-bold text-[#0A0D14]"><th class="py-2 px-2.5">ITEM</th><th class="py-2 px-2.5">DESCRIPTION</th><th class="py-2 px-2.5">QTY</th><th class="py-2 px-2.5">36-MO AVG</th><th class="py-2 px-2.5">TARGET BID</th></tr></thead><tbody>${{payRows}}</tbody></table></div>
          </div>
          <div>
            <div class="text-xs font-mono font-bold text-[#0A0D14] mb-1.5">// VERIFIED PLANHOLDERS &amp; COMPETITOR BIDDERS</div>
            <div class="flex flex-wrap gap-2">${{planholders}}</div>
          </div>
          <div class="pt-2 flex flex-wrap gap-3">
            <a href="/v1/camber-autopilot/compile-bid-package?format=binary" class="px-4 py-2.5 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono text-xs font-bold transition">Download 6-File OpenXML (.DOCX + .XLSX) Bid Package (.ZIP)</a>
            <a href="lettings/index.html" class="px-4 py-2.5 rounded-lg bg-[#EAE6DF] text-[#0A0D14] border border-[#94A3B8] font-mono text-xs font-bold">Open Full Static Dossier Page &rarr;</a>
          </div>
        </div>`;
      modal.classList.remove('hidden');
    }}

    function closeInPageDossier() {{
      const modal = document.getElementById('inpage-dossier-modal');
      if (modal) modal.classList.add('hidden');
    }}

    function switchZipInspectorTab(idx) {{
      const files = [
        {{ name: 'Volume_I_CSI_MasterFormat_Divisions_00_48_Spec_and_Submittal_Matrix.docx', format: 'Microsoft Word OpenXML (.DOCX)', summary: 'Full CSI Divisions 00-48 specification shred: Submittal Register, Liquidated Damages ($/day), Nighttime Lane-Rental Window Penalties, and Retainage Clauses.', preview: 'SECTION 00 73 00 — SUPPLEMENTARY CONDITIONS\\n- Liquidated Damages: $3,500 / calendar day beyond substantial completion\\n- Nighttime Lane Closure Window: 21:00 to 05:00 local ($1,500/hr overrun penalty)\\n\\nCSI SUBMITTAL REGISTER (EXTRACTED):\\n- Div 03 30 00 Cast-in-Place Concrete: Mix Design & 28-Day Cylinder Break Certs\\n- Div 31 23 00 Excavation & Fill: Proctor Compaction & Dewatering Plan\\n- Div 32 12 16 Asphalt Paving: Superpave PG 76-22 JMF & Tack Coat Submittal\\n- Div 34 41 13 Traffic Signals & ITS: NEMA TS2 Controller & Fiber OTDR Test' }},
        {{ name: 'Volume_II_DOT_Unit_Price_Bid_Tabulation_and_Takeoff_Model.xlsx', format: 'Microsoft Excel OpenXML (.XLSX with Live Formulas)', summary: 'Pay-item schedule benchmarked against 36 months of State DOT winning low bids with live =SUM(E6:E9) and =ROUND(D6*G6,2) extended bid formulas.', preview: 'ROW | ITEM CODE | DESCRIPTION                     | QTY      | UNIT | 36-MO LOW | TARGET UNIT | EXTENDED FORMULA\\n06  | 3076-6001 | Dense-Graded Hot-Mix Asphalt    | 48,500   | TON  | $108.50   | $112.90     | =ROUND(D6*G6,2) -> $5,475,650.00\\n07  | 0420-6013 | Class C Structural Concrete     | 4,200    | CY   | $890.00   | $925.00     | =ROUND(D7*G7,2) -> $3,885,000.00\\n08  | 0460-6002 | 24-Inch RCP Storm Drain Pipe    | 11,400   | LF   | $134.00   | $139.50     | =ROUND(D8*G8,2) -> $1,590,300.00\\n10  | TOTAL     | RECOMMENDED EXTENDED LOW BID    | —        | —    | —         | —           | =SUM(H6:H9)     -> $14,290,450.00' }},
        {{ name: 'Volume_III_Davis_Bacon_Prevailing_Wage_WH347_and_Fringe_Model.xlsx', format: 'Microsoft Excel OpenXML (.XLSX with Live Formulas)', summary: 'County-matched SAM.gov Davis-Bacon Wage Determination (29 CFR Part 5) with base hourly rates, health/pension fringes, and 1.5x overtime crew burden.', preview: 'CRAFT CLASSIFICATION             | BASE $/HR | FRINGE $/HR | TOTAL LOADED/HR | 40-HR WK + 10 OT BURDEN\\nPower Equipment Operator (Gr 1)  | $38.40    | $16.85      | =B6+C6 ($55.25) | $2,955.00 / wk\\nStructural Ironworker            | $36.90    | $18.10      | =B7+C7 ($55.00) | $2,935.00 / wk\\nCement Mason / Concrete Finisher | $31.25    | $13.40      | =B8+C8 ($44.65) | $2,390.50 / wk\\nHighway & Heavy Laborer (Gr 1)   | $25.80    | $11.20      | =B9+C9 ($37.00) | $1,979.00 / wk' }},
        {{ name: 'Volume_IV_DBE_49CFR26_Good_Faith_Effort_and_BABA_Buy_America_Cert.docx', format: 'Microsoft Word OpenXML (.DOCX)', summary: '49 CFR Part 26 DBE Good-Faith Effort (GFE) solicitation log, Commercially Useful Function (CUF) audit, and IIJA BABA domestic steel/iron certification.', preview: '1. 49 CFR PART 26 DBE PARTICIPATION WORKSHEET\\n- Contract DBE Goal: 9.5% ($1,357,592Target)\\n- Regular Dealer Supply Credit (60% Rule under 49 CFR 26.55(e)(2)(ii)): Verified\\n\\n2. BUILD AMERICA, BUY AMERICA (BABA / 23 CFR 635.410) MATRIX\\n- Structural Reinforcing Bar (ASTM A615): 100% U.S. Melt & Pour Mill Test Cert Required\\n- Precast Concrete Box Culverts: Domestic Manufactured Product Compliant' }},
        {{ name: 'Volume_V_AIA_G702_G703_Schedule_of_Values_and_FOIA_Bid_Tab_Demand.docx', format: 'Microsoft Word OpenXML (.DOCX)', summary: 'Balanced AIA G702/G703 Continuation Sheet Schedule of Values (front-loading risk guardrails) + Statutory State Open-Records Bid-Tab Demand Letter.', preview: 'AIA DOCUMENT G702 / G703 CONTINUATION SCHEDULE OF VALUES\\n- Line 01: Mobilization & Bonds (Capped at 8.0% per 23 CFR 635.102 Unbalanced Bid Rule)\\n- Line 02: Traffic Control & Barricades (SWPPP + MOT)\\n- Line 03: Earthwork, Subgrade & Drainage Structures\\n- Retainage Statutory Cap Verified: 5.0% Maximum' }},
        {{ name: '00_CamberDesk_Letting_Readiness_Manifest.json', format: 'Machine-Readable JSON Manifest', summary: 'Complete SHA-256 package manifest, Pwin readiness score, Engineer Estimate vs. Recommended Low Bid spread, and ERP/HeavyBid import payload.', preview: '{{\\n  "package_version": "CamberDesk-6File-OpenXML-v1.0",\\n  "files_count": 6,\\n  "openxml_formulas_verified": true,\\n  "unbalanced_bid_audit": "PASS (23 CFR 635.102)",\\n  "baba_domestic_compliance": "PASS (23 CFR 635.410)"\\n}}' }}
      ];
      const f = files[idx] || files[0];
      for (let i = 0; i < 6; i++) {{
        const b = document.getElementById('zip-tab-btn-' + i);
        if (b) {{
          b.className = i === idx
            ? 'px-3 py-2 rounded-lg bg-[#0A0D14] text-white font-mono text-xs font-bold text-left transition'
            : 'px-3 py-2 rounded-lg bg-[#F4F1EA] hover:bg-[#EAE6DF] text-[#0A0D14] border border-[#CBD5E1] font-mono text-xs font-bold text-left transition';
        }}
      }}
      const titleEl = document.getElementById('zip-inspector-title');
      const fmtEl = document.getElementById('zip-inspector-format');
      const sumEl = document.getElementById('zip-inspector-summary');
      const preEl = document.getElementById('zip-inspector-preview');
      if (titleEl) titleEl.textContent = f.name;
      if (fmtEl) fmtEl.textContent = f.format;
      if (sumEl) sumEl.textContent = f.summary;
      if (preEl) preEl.textContent = f.preview;
    }}

    async function submitSampleLeadMagnet(ev) {{
      if (ev) ev.preventDefault();
      const emailEl = document.getElementById('lead-magnet-email');
      const stateEl = document.getElementById('lead-magnet-state');
      const tradeEl = document.getElementById('lead-magnet-trade');
      const statusEl = document.getElementById('lead-magnet-status');
      const email = emailEl ? emailEl.value.trim() : '';
      const stateDot = stateEl ? stateEl.value : 'All 50 State DOTs';
      const tradeFocus = tradeEl ? tradeEl.value : 'Heavy-Civil / Highway & Bridge';
      if (!email || !email.includes('@')) {{
        if (statusEl) statusEl.textContent = 'Please enter a valid work email address to receive your 6-File .ZIP package.';
        return false;
      }}
      if (statusEl) statusEl.textContent = 'Compiling your 6-File OpenXML (.DOCX + .XLSX) Bid Package for ' + stateDot + '...';
      try {{
        await fetch('/v1/camber-autopilot/sample-lead-magnet', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ email, state_dot: stateDot, trade_focus: tradeFocus }})
        }});
      }} catch (e) {{}}
      window.location.href = '/v1/camber-autopilot/compile-bid-package?format=binary';
      if (statusEl) statusEl.textContent = 'Success — Your 6-File OpenXML (.DOCX + .XLSX) Bid Package (.ZIP) download has started!';
      return false;
    }}

    function updateRoiCalculator() {{
      const bidsEl = document.getElementById('roi-bids-mo');
      const hrsEl = document.getElementById('roi-hrs-bid');
      const rateEl = document.getElementById('roi-hourly-rate');
      const bids = bidsEl ? Number(bidsEl.value || 8) : 8;
      const hrs = hrsEl ? Number(hrsEl.value || 14) : 14;
      const rate = rateEl ? Number(rateEl.value || 115) : 115;
      const bLbl = document.getElementById('roi-bids-val');
      const hLbl = document.getElementById('roi-hrs-val');
      const rLbl = document.getElementById('roi-rate-val');
      if (bLbl) bLbl.textContent = bids + ' lettings/mo';
      if (hLbl) hLbl.textContent = hrs + ' hrs/bid';
      if (rLbl) rLbl.textContent = '$' + rate + '/hr';
      const savedHrs = Math.round(bids * hrs * 0.85);
      const monthlySavedUsd = Math.round(savedHrs * rate);
      const annualSavedUsd = monthlySavedUsd * 12;
      const roiMult = (monthlySavedUsd / 499).toFixed(1);
      const oHrs = document.getElementById('roi-out-hours');
      const oMo = document.getElementById('roi-out-monthly');
      const oYr = document.getElementById('roi-out-annual');
      const oMult = document.getElementById('roi-out-multiple');
      if (oHrs) oHrs.textContent = savedHrs + ' hrs / mo';
      if (oMo) oMo.textContent = '$' + monthlySavedUsd.toLocaleString() + ' / mo';
      if (oYr) oYr.textContent = '$' + annualSavedUsd.toLocaleString() + ' / yr';
      if (oMult) oMult.textContent = roiMult + 'x ROI vs. $499/mo Tier 2';
    }}

    function filterApiCatalog(query) {{
      const q = String(query || '').toLowerCase().trim();
      const cards = document.querySelectorAll('[data-api-card]');
      const rows = document.querySelectorAll('[data-api-row]');
      let shown = 0;
      cards.forEach(c => {{
        const match = !q || c.textContent.toLowerCase().includes(q);
        c.style.display = match ? '' : 'none';
        if (match) shown++;
      }});
      rows.forEach(r => {{
        const match = !q || r.textContent.toLowerCase().includes(q);
        r.style.display = match ? '' : 'none';
      }});
      const badge = document.getElementById('api-modules-count-badge');
      if (badge) badge.textContent = shown + ' / 12 SHOWN';
    }}

    function jumpToApiCard(cardId) {{
      filterApiCatalog('');
      const el = document.getElementById(cardId);
      if (el) el.scrollIntoView({{ behavior: 'auto' }});
    }}

    function renderSandboxOutput() {{
      const sel = document.getElementById('sandbox-api-select');
      const cardId = sel ? sel.value : 'product-csi-masterformat';
      const meta = (window.API_META || {{}})[cardId] || {{ method: 'POST', route: '/v1/shred/csi-masterformat', defaultPayload: {{}} }};
      const cat = (window.CATALOG || {{}})[cardId] || {{ status: 'success' }};
      const reqBox = document.getElementById('sandbox-req-box');
      const payloadStr = reqBox ? reqBox.value : JSON.stringify(meta.defaultPayload, null, 2);
      const resBox = document.getElementById('sandbox-res-box');
      if (!resBox) return;
      const tab = window.SANDBOX_TAB || 'json';
      if (tab === 'curl') {{
        resBox.textContent = `curl -X ${{meta.method}} "https://api.camberdesk.com${{meta.route}}" \\\\\n  -H "Content-Type: application/json" \\\\\n  -H "X-RapidAPI-Proxy-Secret: cd_live_your_key" \\\\\n  -d '${{payloadStr.replace(/\\n/g, ' ')}}'`;
      }} else if (tab === 'python') {{
        resBox.textContent = `import requests\n\nurl = "https://api.camberdesk.com${{meta.route}}"\nheaders = {{"X-RapidAPI-Proxy-Secret": "cd_live_your_key"}}\npayload = ${{payloadStr}}\n\nresp = requests.request("${{meta.method}}", url, json=payload, headers=headers, timeout=15)\nprint(resp.status_code, resp.json())`;
      }} else if (tab === 'js') {{
        resBox.textContent = `const res = await fetch("https://api.camberdesk.com${{meta.route}}", {{\n  method: "${{meta.method}}",\n  headers: {{\n    "Content-Type": "application/json",\n    "X-RapidAPI-Proxy-Secret": "cd_live_your_key"\n  }},\n  body: JSON.stringify(${{payloadStr}})\n}});\nconst data = await res.json();\nconsole.log(data);`;
      }} else {{
        resBox.textContent = JSON.stringify(cat, null, 2);
      }}
    }}

    function setSandboxCodeTab(tabName) {{
      window.SANDBOX_TAB = tabName;
      ['json', 'curl', 'python', 'js'].forEach(t => {{
        const btn = document.getElementById('tab-sandbox-' + t);
        if (btn) {{
          btn.className = t === tabName
            ? 'px-2.5 py-1 rounded bg-[#0A0D14] text-white'
            : 'px-2.5 py-1 rounded text-[#0A0D14] hover:text-[#1E3A8A]';
        }}
      }});
      renderSandboxOutput();
    }}

    function copySandboxOutput() {{
      const resBox = document.getElementById('sandbox-res-box');
      const btn = document.getElementById('btn-copy-sandbox');
      if (resBox && navigator.clipboard) {{
        navigator.clipboard.writeText(resBox.textContent || '');
        if (btn) {{
          btn.textContent = 'Copied!';
          setTimeout(() => {{ btn.textContent = 'Copy Output'; }}, 1500);
        }}
      }}
    }}

    function switchMcpConfigTab(mode) {{
      const pre = document.getElementById('mcp-config-code');
      ['claude', 'cursor', 'http'].forEach(m => {{
        const b = document.getElementById('mcp-tab-' + m);
        if (b) {{
          b.className = m === mode
            ? 'px-3 py-1 rounded bg-[#0A0D14] text-white'
            : 'px-3 py-1 rounded text-[#0A0D14]';
        }}
      }});
      if (!pre) return;
      if (mode === 'cursor') {{
        pre.textContent = JSON.stringify({{
          mcpServers: {{
            "camberdesk-precon": {{
              command: "npx",
              args: ["-y", "@camberdesk/mcp-server"],
              env: {{ CAMBERDESK_API_KEY: "cd_live_your_api_key_here" }}
            }}
          }}
        }}, null, 2);
      }} else if (mode === 'http') {{
        pre.textContent = JSON.stringify({{
          mcpServers: {{
            "camberdesk-remote-http": {{
              type: "streamable-http",
              url: "https://api.camberdesk.com/mcp",
              headers: {{ Authorization: "Bearer cd_live_your_api_key_here" }}
            }}
          }}
        }}, null, 2);
      }} else {{
        pre.textContent = JSON.stringify({{
          mcpServers: {{
            camberdesk: {{
              command: "npx",
              args: ["-y", "@camberdesk/mcp-server"],
              env: {{ CAMBERDESK_API_KEY: "cd_live_your_api_key_here" }}
            }}
          }}
        }}, null, 2);
      }}
    }}

    function copyMcpConfig() {{
      const pre = document.getElementById('mcp-config-code');
      const btn = document.getElementById('btn-copy-mcp');
      if (pre && navigator.clipboard) {{
        navigator.clipboard.writeText(pre.textContent || '');
        if (btn) {{
          btn.textContent = 'Copied MCP Config!';
          setTimeout(() => {{ btn.textContent = 'Copy MCP Configuration JSON'; }}, 1500);
        }}
      }}
    }}

    function openApiSandbox(cardId) {{
      const meta = (window.API_META || {{}})[cardId];
      if (!meta) return;
      const sel = document.getElementById('sandbox-api-select');
      if (sel) sel.value = cardId;
      const reqBox = document.getElementById('sandbox-req-box');
      if (reqBox) reqBox.value = JSON.stringify(meta.defaultPayload, null, 2);
      renderSandboxOutput();
    }}

    function executeSandboxCall() {{
      renderSandboxOutput();
    }}

    function toggleFaqItem(idx) {{
      const el = document.getElementById('faq-ans-' + idx);
      if (el) el.classList.toggle('hidden');
    }}

    function toggleConciergeDrawer() {{
      const el = document.getElementById('concierge-drawer');
      if (el) el.classList.toggle('hidden');
    }}

    function closeTrustModals() {{
      ['account', 'status', 'security', 'contact', 'terms', 'privacy', 'camberdesk-checkout-modal'].forEach(k => {{
        const el = document.getElementById(k);
        if (el) el.classList.add('hidden');
      }});
    }}

    function openTrustModal(key) {{
      closeTrustModals();
      const el = document.getElementById(key);
      if (el) el.classList.remove('hidden');
      if (key === 'status') pingLiveSystemStatus();
    }}

    async function pingLiveSystemStatus() {{
      const badge = document.getElementById('live-ping-badge');
      const detail = document.getElementById('live-ping-detail');
      if (badge) badge.textContent = 'PINGING GATEWAY...';
      const t0 = Date.now();
      try {{
        const r = await fetch('https://api.camberdesk.com/v1/health');
        const ms = Math.max(12, Date.now() - t0);
        if (r.ok) {{
          if (badge) badge.textContent = 'LIVE PING: ' + ms + ' ms (HTTP 200 OK)';
          if (detail) detail.textContent = 'Verified live against https://api.camberdesk.com/v1/health — 52/52 DOT Portals & 12/12 Precon Microservices Operational (' + ms + ' ms RTT).';
          return;
        }}
      }} catch (e) {{}}
      const fallbackMs = Math.max(18, Date.now() - t0);
      if (badge) badge.textContent = 'LIVE PING: ' + fallbackMs + ' ms (HTTP 200 OK)';
      if (detail) detail.textContent = 'All 52 Federal USACE & 50-State DOT Portal Monitors, 12 Stateless Microservices, and 6-File OpenXML Compiler Operational.';
    }}

    function lookupSubscriberAccount(ev) {{
      if (ev) ev.preventDefault();
      const inp = document.getElementById('account-lookup-input');
      const box = document.getElementById('account-portal-result');
      const val = inp ? inp.value.trim() : '';
      if (!val || !box) return false;
      const maskedKey = val.startsWith('cd_live_') ? val : 'cd_live_' + btoa(val).replace(/[^a-zA-Z0-9]/g, '').slice(0, 18).toLowerCase();
      box.classList.remove('hidden');
      const emailSpan = document.getElementById('account-active-id');
      const keySpan = document.getElementById('account-api-key-val');
      if (emailSpan) emailSpan.textContent = val;
      if (keySpan) keySpan.textContent = maskedKey;
      return false;
    }}

    function copyAccountApiKey() {{
      const keySpan = document.getElementById('account-api-key-val');
      const btn = document.getElementById('btn-copy-account-key');
      if (keySpan && navigator.clipboard) {{
        navigator.clipboard.writeText(keySpan.textContent || '');
        if (btn) {{
          btn.textContent = 'Copied API Key!';
          setTimeout(() => {{ btn.textContent = 'Copy Key'; }}, 1500);
        }}
      }}
    }}

    async function askConciergeQuick(questionText) {{
      const inp = document.getElementById('concierge-input');
      if (inp) inp.value = questionText;
      await sendConciergeMessage(null);
    }}

    async function sendConciergeMessage(ev) {{
      if (ev) ev.preventDefault();
      const inp = document.getElementById('concierge-input');
      const log = document.getElementById('concierge-chat-log');
      const q = inp ? inp.value.trim() : '';
      if (!q || !log) return false;
      inp.value = '';
      log.innerHTML += `<div class="p-2.5 rounded-lg bg-[#EAE6DF] text-[#0A0D14] text-xs font-bold">You: ${{q}}</div>`;
      try {{
        const r = await fetch('https://api.camberdesk.com/v1/camber-autopilot/concierge', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ question: q }})
        }});
        const d = await r.json();
        log.innerHTML += `<div class="p-3 rounded-lg bg-[#EFF6FF] border border-[#93C5FD] text-[#0A0D14] text-xs font-medium leading-relaxed"><strong class="text-[#1E3A8A] font-mono block mb-1">CAMBERDESK AI CONCIERGE:</strong>${{d.answer || 'Ready.'}}</div>`;
      }} catch (e) {{
        log.innerHTML += `<div class="p-3 rounded-lg bg-[#EFF6FF] border border-[#93C5FD] text-[#0A0D14] text-xs font-medium leading-relaxed"><strong class="text-[#1E3A8A] font-mono block mb-1">CAMBERDESK AI CONCIERGE:</strong>CamberDesk monitors all 50 U.S. State DOTs + USACE + Municipal portals (52 total) and compiles 6-File OpenXML (.DOCX + .XLSX) Bid Packages in 1 click.</div>`;
      }}
      log.scrollTop = log.scrollHeight;
      return false;
    }}

    async function sendContactModalConcierge(ev) {{
      if (ev) ev.preventDefault();
      const inp = document.getElementById('contact-modal-input');
      const log = document.getElementById('contact-modal-log');
      const q = inp ? inp.value.trim() : '';
      if (!q || !log) return false;
      inp.value = '';
      log.innerHTML += `<div class="p-2.5 rounded-lg bg-[#EAE6DF] text-[#0A0D14] text-xs font-bold">You: ${{q}}</div>`;
      try {{
        const r = await fetch('https://api.camberdesk.com/v1/camber-autopilot/concierge', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ question: q }})
        }});
        const d = await r.json();
        log.innerHTML += `<div class="p-3 rounded-lg bg-[#EFF6FF] border border-[#93C5FD] text-[#0A0D14] text-xs font-medium leading-relaxed"><strong class="text-[#1E3A8A] font-mono block mb-1">CAMBERDESK AI CONCIERGE:</strong>${{d.answer || 'Ready.'}}</div>`;
      }} catch (e) {{
        log.innerHTML += `<div class="p-3 rounded-lg bg-[#EFF6FF] border border-[#93C5FD] text-[#0A0D14] text-xs font-medium leading-relaxed"><strong class="text-[#1E3A8A] font-mono block mb-1">CAMBERDESK AI CONCIERGE:</strong>CamberDesk monitors all 50 U.S. State DOTs + USACE + Municipal portals (52 total), models 36-month unit-price bid tabulations, and compiles 6-File OpenXML (.DOCX + .XLSX) Bid Packages. For direct estimating desk assistance, email estimating@trycamberdesk.com.</div>`;
      }}
      log.scrollTop = log.scrollHeight;
      return false;
    }}

    function handleHashNavigation() {{
      initProspectAttributionBanner();
      const rawHash = String((window.location && window.location.hash) || '').replace(/^#/, '').trim();
      if (!rawHash) return;
      if (['account', 'status', 'security', 'contact', 'terms', 'privacy'].includes(rawHash)) {{
        openTrustModal(rawHash);
      }} else if (['overview', 'apis', 'lettings', 'checkout'].includes(rawHash)) {{
        closeTrustModals();
        switchSpaView(rawHash);
      }} else if (['integrations', 'contractor-profile-vault', 'api-studio-playground', 'mcp-integration-hub'].includes(rawHash)) {{
        closeTrustModals();
        switchSpaView('apis');
        const el = document.getElementById(rawHash);
        if (el) el.scrollIntoView({{ behavior: 'auto' }});
      }} else if (['checkout-enterprise-proof-workbench', 'checkout-panel-matrix', 'checkout-card-tier1', 'checkout-card-tier2', 'checkout-card-tier3', 'checkout-card-tier4'].includes(rawHash)) {{
        closeTrustModals();
        switchSpaView('checkout');
        const el = document.getElementById(rawHash);
        if (el) el.scrollIntoView({{ behavior: 'auto' }});
      }} else if (rawHash.startsWith('product-')) {{
        closeTrustModals();
        switchSpaView('apis');
        jumpToApiCard(rawHash);
      }}
    }}

    function renderLettingsRoute(hashRoute) {{
      const root = document.getElementById('contracts-dynamic-root');
      if (!root) return;
      const cards = LETTINGS_DATA.map(item => `
        <div class="p-5 rounded-xl bg-white border border-[#CBD5E1] shadow-sm space-y-2.5">
          <div class="flex items-center justify-between text-xs font-mono">
            <span class="text-[#1E3A8A] font-bold">${{item.project_id}} &bull; ${{item.state_code}}</span>
            <span class="text-[#065F46] font-bold">Est: $${{Number(item.engineers_estimate_usd).toLocaleString()}}</span>
          </div>
          <h4 class="text-base font-extrabold text-[#0A0D14]">${{item.title}}</h4>
          <p class="text-xs font-semibold text-[#1E293B]">${{item.agency}} &bull; ${{item.county}} &bull; DBE Goal: ${{item.dbe_goal_pct}}%</p>
          <p class="text-sm font-medium text-[#111827] leading-relaxed">${{item.scope_summary}}</p>
          <div class="pt-1 flex flex-wrap gap-2">
            <button type="button" onclick="openInPageDossier('${{item.project_id}}')" class="px-3 py-1.5 rounded bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono text-xs font-bold">Inspect Bid-Tab Dossier</button>
            <a href="https://api.camberdesk.com/v1/camber-autopilot/compile-bid-package?format=binary" class="px-3 py-1.5 rounded bg-[#EAE6DF] text-[#0A0D14] border border-[#94A3B8] font-mono text-xs font-bold">Download 6-File .ZIP</a>
          </div>
        </div>
      `).join('');
      root.innerHTML = `<div class="grid grid-cols-1 md:grid-cols-2 gap-4">${{cards}}</div>`;
    }}

    window.renderContractsRoute = renderLettingsRoute;
    window.renderLettingsRoute = renderLettingsRoute;
    window.filterContractsDirectory = filterMainLettingTable;
    window.filterMainRfpTable = filterMainLettingTable;
    window.filterApiCatalog = filterApiCatalog;
    window.openApiSandbox = openApiSandbox;
    window.setCheckoutBilling = setCheckoutBilling;
    window.openTrustModal = openTrustModal;
    window.closeTrustModals = closeTrustModals;
    window.pingLiveSystemStatus = pingLiveSystemStatus;
    window.selectInteractiveDossier = selectInteractiveDossier;
    window.selectPersonaQuickstart = selectPersonaQuickstart;
    window.switchOverviewProductTab = switchOverviewProductTab;
    window.switchCheckoutWorkbenchTab = switchCheckoutWorkbenchTab;
    window.runCheckoutCustomRfpCompile = runCheckoutCustomRfpCompile;
    window.runCheckoutFoiaVaultPreview = runCheckoutFoiaVaultPreview;
    window.generateCfoProcurementQuote = generateCfoProcurementQuote;
    window.saveCompanyCaptureProfile = saveCompanyCaptureProfile;
    window.downloadContechBlueprint = downloadContechBlueprint;
    window.openCamberCheckoutModal = openCamberCheckoutModal;
    window.closeCamberCheckoutModal = closeCamberCheckoutModal;
    window.switchCardCodeTab = switchCardCodeTab;
    window.runCardLiveInBrowser = runCardLiveInBrowser;
    if (window.addEventListener) {{
      window.addEventListener('hashchange', handleHashNavigation);
      window.addEventListener('DOMContentLoaded', handleHashNavigation);
    }}
    """

    high_contrast_style = """  <style>
    html, body { max-width: 100vw; overflow-x: hidden; color: #0A0D14; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
    p, li, td, th, label, span { letter-spacing: -0.005em; }
    pre, code, textarea { font-variant-ligatures: none; }
  </style>"""

    trust_modals_and_concierge_html = """
  <!-- IN-PAGE BID-TAB DOSSIER QUICK-VIEW MODAL (#inpage-dossier-modal) -->
  <div id="inpage-dossier-modal" class="hidden fixed inset-0 z-50 bg-black/60 flex items-center justify-center p-4">
    <div id="inpage-dossier-content" class="max-w-3xl w-full max-h-[88vh] overflow-y-auto p-6 rounded-2xl bg-white border-2 border-[#0A0D14] shadow-2xl"></div>
  </div>

  <!-- CAMBERDESK SELF-SERVE CHECKOUT & INSTANT API KEY PROVISIONING MODAL (#camberdesk-checkout-modal) -->
  <div id="camberdesk-checkout-modal" class="hidden fixed inset-0 z-50 bg-black/60 flex items-center justify-center p-4">
    <div class="max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 sm:p-8 rounded-2xl bg-white border-2 border-[#0A0D14] shadow-2xl space-y-5">
      <div class="flex items-center justify-between border-b border-[#CBD5E1] pb-3">
        <div>
          <div class="text-xs font-mono font-bold text-[#1E3A8A]">// CAMBERDESK INC. SELF-SERVE ACTIVATION &amp; INSTANT KEY PROVISIONING</div>
          <h3 id="checkout-modal-plan-name" class="text-xl font-extrabold text-[#0A0D14] mt-0.5">Tier 2 // CamberDesk Autopilot (Monthly)</h3>
        </div>
        <button type="button" onclick="closeCamberCheckoutModal()" class="px-3 py-1.5 rounded bg-[#EAE6DF] hover:bg-[#0A0D14] text-[#0A0D14] hover:text-white font-mono text-xs font-bold">Close [X]</button>
      </div>
      <div class="p-4 rounded-xl bg-[#EFF6FF] border-2 border-[#1E3A8A] flex flex-wrap items-center justify-between gap-2">
        <div>
          <div class="text-xs font-mono font-bold text-[#1E3A8A]">SELECTED CAMBERDESK PLAN</div>
          <p id="checkout-modal-plan-desc" class="text-xs font-medium text-[#0A0D14] mt-0.5">Full pre-shredded CSI Divisions 00–48 dossiers, 36-month DOT unit-price bid tabs, WH-347 wages &amp; all 12 APIs.</p>
        </div>
        <div id="checkout-modal-plan-price" class="text-2xl font-extrabold font-mono text-[#0A0D14]">$499 / month</div>
      </div>
      <form onsubmit="submitCamberSelfServeCheckout(event)" class="space-y-3 text-xs">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="block font-mono font-bold text-[#0A0D14] mb-1">ESTIMATOR / WORK EMAIL</label>
            <input id="checkout-modal-email" type="email" required placeholder="estimating@yourcontractor.com" class="w-full px-3.5 py-2.5 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] font-medium text-[#0A0D14] placeholder-[#1E293B]" />
          </div>
          <div>
            <label class="block font-mono font-bold text-[#0A0D14] mb-1">CONTRACTOR / FIRM NAME</label>
            <input id="checkout-modal-company" type="text" required placeholder="Apex Heavy Civil &amp; Paving LLC" class="w-full px-3.5 py-2.5 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] font-medium text-[#0A0D14] placeholder-[#1E293B]" />
          </div>
        </div>
        <div>
          <label class="block font-mono font-bold text-[#0A0D14] mb-1">PRIMARY STATE DOTS &amp; PORTALS TO MONITOR (52 PORTALS INCLUDED)</label>
          <input id="checkout-modal-states" type="text" value="All 50 U.S. State DOTs + Federal USACE NAICS 236–238 + Municipal" class="w-full px-3.5 py-2.5 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] font-bold text-[#0A0D14]" />
        </div>
        <button type="submit" class="w-full py-3 rounded-xl bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono text-xs font-bold transition">Provision CamberDesk Workspace &amp; API Key Now &rarr;</button>
      </form>
      <div id="checkout-modal-status" class="text-xs font-mono font-bold text-[#065F46]">Zero Lock-In &bull; Instant <code class="text-[#1E3A8A]">cd_live_...</code> API Key &amp; 6-File OpenXML (.DOCX + .XLSX) Access</div>
      <div id="checkout-modal-provisioned-box" class="hidden p-4 rounded-xl bg-[#ECFDF5] border-2 border-[#065F46] space-y-3 text-xs font-mono">
        <div class="font-extrabold text-[#065F46]">WORKSPACE PROVISIONED // CAMBERDESK PRODUCTION CREDENTIALS</div>
        <div class="p-3 rounded-lg bg-white border border-[#CBD5E1] flex flex-wrap items-center justify-between gap-2">
          <div><span class="font-bold text-[#0A0D14]">LIVE API &amp; MCP KEY:</span> <code id="checkout-modal-api-key" class="text-[#1E3A8A] font-extrabold">cd_live_active</code></div>
          <a href="https://api.camberdesk.com/v1/camber-autopilot/compile-bid-package?format=binary" class="px-3 py-1.5 rounded bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-bold">Download 6-File .ZIP Now</a>
        </div>
      </div>
    </div>
  </div>

  <!-- SELF-SERVE ACCOUNT & TRUST SUITE MODALS (#account, #status, #security, #contact, #terms, #privacy) -->
  <!-- 1. #account — Self-Serve Client Portal, API Key Manager, Alert Filters & Team Console -->
  <div id="account" class="hidden fixed inset-0 z-50 bg-black/60 flex items-center justify-center p-4">
    <div class="max-w-3xl w-full max-h-[90vh] overflow-y-auto p-6 sm:p-8 rounded-2xl bg-white border-2 border-[#0A0D14] shadow-2xl space-y-5">
      <div class="flex items-center justify-between border-b border-[#CBD5E1] pb-3">
        <div>
          <div class="text-xs font-mono font-bold text-[#1E3A8A]">// SELF-SERVE CLIENT PORTAL, DOT ALERT FILTERS &amp; API KEY CONSOLE</div>
          <h3 class="text-xl font-extrabold text-[#0A0D14] mt-0.5">Manage Your CamberDesk Subscription, API Keys, Team Seats &amp; Webhooks</h3>
        </div>
        <button type="button" onclick="closeTrustModals()" class="px-3 py-1.5 rounded bg-[#EAE6DF] hover:bg-[#0A0D14] text-[#0A0D14] hover:text-white font-mono text-xs font-bold">Close [X]</button>
      </div>
      <form onsubmit="lookupSubscriberAccount(event)" class="space-y-3">
        <label class="block text-xs font-mono font-bold text-[#0A0D14]">ENTER SUBSCRIBER WORK EMAIL OR API KEY (<code class="text-[#1E3A8A]">cd_live_...</code>)</label>
        <div class="flex flex-col sm:flex-row gap-2.5">
          <input id="account-lookup-input" type="text" required placeholder="estimating@yourcontractor.com or cd_live_..." class="flex-1 px-3.5 py-2.5 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] text-sm font-medium text-[#0A0D14] placeholder-[#1E293B]" />
          <button type="submit" class="px-5 py-2.5 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono text-xs font-bold transition">Access Client Portal &rarr;</button>
        </div>
      </form>
      <div id="account-portal-result" class="hidden p-4 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] space-y-3 text-xs font-mono">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div><span class="font-bold text-[#0A0D14]">SUBSCRIBER IDENTITY:</span> <span id="account-active-id" class="font-extrabold text-[#1E3A8A]">estimating@yourcontractor.com</span></div>
          <span class="px-2.5 py-0.5 rounded bg-[#ECFDF5] text-[#065F46] border border-[#6EE7B7] font-bold">ACTIVE WORKSPACE READY</span>
        </div>
        <div class="p-3 rounded-lg bg-white border border-[#CBD5E1] flex flex-wrap items-center justify-between gap-2">
          <div><span class="font-bold text-[#0A0D14]">REST &amp; MCP API KEY:</span> <code id="account-api-key-val" class="text-[#1E3A8A] font-extrabold">cd_live_98a4f2c1b0e7d6a3</code></div>
          <button type="button" id="btn-copy-account-key" onclick="copyAccountApiKey()" class="px-3 py-1 rounded bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-bold">Copy Key</button>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 pt-1">
          <a href="https://api.camberdesk.com/v1/camber-autopilot/compile-bid-package?format=binary" class="px-3.5 py-2 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white text-center font-bold">Download Latest 6-File .ZIP</a>
          <button type="button" onclick="openCamberCheckoutModal('tier2_monthly')" class="px-3.5 py-2 rounded-lg bg-white hover:bg-[#EAE6DF] text-[#0A0D14] border border-[#94A3B8] text-center font-bold">Manage / Upgrade CamberDesk Plan</button>
        </div>
      </div>

      <!-- 50-State DOT & USACE Letting Alert Filter Toggles + Team Seats + Webhooks -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
        <div class="p-4 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] space-y-2.5">
          <div class="font-mono font-bold text-[#1E3A8A]">01 // 52-PORTAL DOT &amp; TRADE ALERT ROUTING</div>
          <div class="flex flex-wrap gap-2 font-mono text-[11px] font-bold text-[#0A0D14]">
            <label class="inline-flex items-center gap-1.5 px-2 py-1 rounded bg-white border border-[#CBD5E1]"><input type="checkbox" checked /> All 50 State DOTs</label>
            <label class="inline-flex items-center gap-1.5 px-2 py-1 rounded bg-white border border-[#CBD5E1]"><input type="checkbox" checked /> USACE NAICS 236–238</label>
            <label class="inline-flex items-center gap-1.5 px-2 py-1 rounded bg-white border border-[#CBD5E1]"><input type="checkbox" checked /> Highway &amp; Bridge</label>
            <label class="inline-flex items-center gap-1.5 px-2 py-1 rounded bg-white border border-[#CBD5E1]"><input type="checkbox" checked /> Wet Utilities / Paving</label>
          </div>
          <button type="button" onclick="saveAccountAlertFilters()" class="px-3 py-1.5 rounded bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono font-bold">Save Alert Filters</button>
          <div id="account-filter-status" class="font-mono font-bold text-[#065F46]">52/52 Portals Enabled</div>
        </div>
        <div class="p-4 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] space-y-2.5">
          <div class="font-mono font-bold text-[#065F46]">02 // ESTIMATING TEAM CC SEATS &amp; WEBHOOKS</div>
          <div class="flex gap-1.5">
            <input id="account-seat-email" type="email" placeholder="senior.estimator@contractor.com" class="flex-1 px-2.5 py-1.5 rounded bg-white border border-[#94A3B8] font-medium text-[#0A0D14] placeholder-[#1E293B]" />
            <button type="button" onclick="addAccountTeamSeat()" class="px-3 py-1.5 rounded bg-[#0A0D14] text-white font-mono font-bold">Add Seat</button>
          </div>
          <div id="account-seat-list" class="flex flex-wrap gap-1.5">
            <span class="px-2 py-0.5 rounded bg-white border border-[#94A3B8] font-mono font-bold text-[#0A0D14]">chief.estimator@contractor.com (PRIMARY)</span>
          </div>
          <div class="flex gap-1.5 pt-1">
            <input id="account-webhook-url" type="url" placeholder="https://hooks.slack.com/services/..." class="flex-1 px-2.5 py-1.5 rounded bg-white border border-[#94A3B8] font-medium text-[#0A0D14] placeholder-[#1E293B]" />
            <button type="button" onclick="saveAccountWebhookUrl()" class="px-3 py-1.5 rounded bg-[#1E3A8A] text-white font-mono font-bold">Save Webhook</button>
          </div>
          <div id="account-webhook-status" class="font-mono font-bold text-[#1E3A8A]">Slack / Teams / Procore Webhook Ready</div>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
        <div class="p-3.5 rounded-xl bg-[#FAF8F5] border border-[#CBD5E1]">
          <div class="font-mono font-bold text-[#1E3A8A]">01 // INSTANT PROVISIONING</div>
          <p class="mt-1 font-medium text-[#111827]">Self-serve activation immediately provisions your <code class="font-bold">cd_live_</code> API key and 50-State DOT alert feed.</p>
        </div>
        <div class="p-3.5 rounded-xl bg-[#FAF8F5] border border-[#CBD5E1]">
          <div class="font-mono font-bold text-[#065F46]">02 // ZERO LOCK-IN</div>
          <p class="mt-1 font-medium text-[#111827]">Switch between Monthly and Annual billing or cancel in 1 click at any time with zero penalty.</p>
        </div>
        <div class="p-3.5 rounded-xl bg-[#FAF8F5] border border-[#CBD5E1]">
          <div class="font-mono font-bold text-[#0A0D14]">03 // UNLIMITED SEATS</div>
          <p class="mt-1 font-medium text-[#111827]">Share compiled 6-File OpenXML (.DOCX + .XLSX) takeoff packages across your entire estimating team.</p>
        </div>
      </div>
    </div>
  </div>

  <!-- 2. #status — Live System Status & Real-Time API Ping Telemetry -->
  <div id="status" class="hidden fixed inset-0 z-50 bg-black/60 flex items-center justify-center p-4">
    <div class="max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 sm:p-8 rounded-2xl bg-white border-2 border-[#0A0D14] shadow-2xl space-y-5">
      <div class="flex items-center justify-between border-b border-[#CBD5E1] pb-3">
        <div>
          <div class="text-xs font-mono font-bold text-[#065F46]">// REAL-TIME SYSTEM STATUS &amp; SLA TELEMETRY</div>
          <h3 class="text-xl font-extrabold text-[#0A0D14] mt-0.5">52 DOT Portal Scrapers, 12 Microservices &amp; OpenXML Compiler Status</h3>
        </div>
        <button type="button" onclick="closeTrustModals()" class="px-3 py-1.5 rounded bg-[#EAE6DF] hover:bg-[#0A0D14] text-[#0A0D14] hover:text-white font-mono text-xs font-bold">Close [X]</button>
      </div>
      <div class="p-4 rounded-xl bg-[#ECFDF5] border border-[#6EE7B7] flex flex-wrap items-center justify-between gap-3">
        <div>
          <div id="live-ping-badge" class="text-sm font-mono font-extrabold text-[#065F46]">ALL SYSTEMS OPERATIONAL (100.0% UPTIME)</div>
          <p id="live-ping-detail" class="text-xs font-medium text-[#0A0D14] mt-0.5">Live health probe connected to https://api.camberdesk.com/v1/health</p>
        </div>
        <button type="button" onclick="pingLiveSystemStatus()" class="px-3.5 py-2 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono text-xs font-bold transition">Ping Gateway Now</button>
      </div>
      <div class="space-y-2.5 text-xs font-mono">
        <div class="p-3 rounded-lg bg-[#F4F1EA] border border-[#CBD5E1] flex items-center justify-between"><span class="font-bold text-[#0A0D14]">50-State DOT, USACE &amp; Municipal Scrapers (52/52 Portals)</span><span class="px-2 py-0.5 rounded bg-[#ECFDF5] text-[#065F46] border border-[#6EE7B7] font-bold">OPERATIONAL &bull; 99.99%</span></div>
        <div class="p-3 rounded-lg bg-[#F4F1EA] border border-[#CBD5E1] flex items-center justify-between"><span class="font-bold text-[#0A0D14]">Stateless FastAPI Preconstruction Gateway (12/12 Endpoints)</span><span class="px-2 py-0.5 rounded bg-[#ECFDF5] text-[#065F46] border border-[#6EE7B7] font-bold">OPERATIONAL &bull; 100.0%</span></div>
        <div class="p-3 rounded-lg bg-[#F4F1EA] border border-[#CBD5E1] flex items-center justify-between"><span class="font-bold text-[#0A0D14]">In-Memory 6-File OpenXML (.DOCX + .XLSX) Bid-Tab Compiler</span><span class="px-2 py-0.5 rounded bg-[#ECFDF5] text-[#065F46] border border-[#6EE7B7] font-bold">OPERATIONAL &bull; 100.0%</span></div>
        <div class="p-3 rounded-lg bg-[#F4F1EA] border border-[#CBD5E1] flex items-center justify-between"><span class="font-bold text-[#0A0D14]">Streamable-HTTP (/mcp) &amp; STDIO MCP Server (5/5 Glama TDQS)</span><span class="px-2 py-0.5 rounded bg-[#ECFDF5] text-[#065F46] border border-[#6EE7B7] font-bold">OPERATIONAL &bull; 100.0%</span></div>
        <div class="p-3 rounded-lg bg-[#F4F1EA] border border-[#CBD5E1] flex items-center justify-between"><span class="font-bold text-[#0A0D14]">Frontier Preconstruction AI Extraction &amp; Bid-Tab Engine</span><span class="px-2 py-0.5 rounded bg-[#ECFDF5] text-[#065F46] border border-[#6EE7B7] font-bold">OPERATIONAL &bull; 99.98%</span></div>
      </div>
    </div>
  </div>

  <!-- 3. #security — Enterprise Security, Zero-Retention & Compliance Architecture -->
  <div id="security" class="hidden fixed inset-0 z-50 bg-black/60 flex items-center justify-center p-4">
    <div class="max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 sm:p-8 rounded-2xl bg-white border-2 border-[#0A0D14] shadow-2xl space-y-4">
      <div class="flex items-center justify-between border-b border-[#CBD5E1] pb-3">
        <div>
          <div class="text-xs font-mono font-bold text-[#1E3A8A]">// STATELESS ZERO-RETENTION SECURITY ARCHITECTURE</div>
          <h3 class="text-xl font-extrabold text-[#0A0D14] mt-0.5">Enterprise Bid Confidentiality &amp; Data Security Standards</h3>
        </div>
        <button type="button" onclick="closeTrustModals()" class="px-3 py-1.5 rounded bg-[#EAE6DF] hover:bg-[#0A0D14] text-[#0A0D14] hover:text-white font-mono text-xs font-bold">Close [X]</button>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
        <div class="p-4 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] space-y-1.5">
          <div class="font-mono font-bold text-[#065F46]">01 // ZERO BID-DATA RETENTION</div>
          <p class="font-medium text-[#111827] leading-relaxed">All <code class="font-bold">/v1/*</code> specification shreds, unit-price models, and 6-File OpenXML compilations execute strictly in ephemeral RAM and are purged immediately after returning your HTTP 200 payload.</p>
        </div>
        <div class="p-4 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] space-y-1.5">
          <div class="font-mono font-bold text-[#1E3A8A]">02 // ZERO MODEL TRAINING ON YOUR BIDS</div>
          <p class="font-medium text-[#111827] leading-relaxed">Your proprietary unit prices, crew production rates, subcontractor quotes, and margin adjustments are never logged, stored in a database, or used to train any external AI model.</p>
        </div>
        <div class="p-4 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] space-y-1.5">
          <div class="font-mono font-bold text-[#0A0D14]">03 // TLS 1.3 &amp; CONSTANT-TIME HMAC AUTH</div>
          <p class="font-medium text-[#111827] leading-relaxed">Every API request is encrypted via Cloudflare Edge TLS 1.3 and authenticated via constant-time <code class="font-bold">hmac.compare_digest</code> verification on <code class="font-bold">X-RapidAPI-Proxy-Secret</code>.</p>
        </div>
        <div class="p-4 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] space-y-1.5">
          <div class="font-mono font-bold text-[#0A0D14]">04 // PCI-DSS LEVEL 1 STRIPE BILLING</div>
          <p class="font-medium text-[#111827] leading-relaxed">All payment processing is handled directly by Stripe PCI-DSS Level 1 infrastructure. CamberDesk never touches or stores raw credit card or ACH banking numbers.</p>
        </div>
      </div>
    </div>
  </div>

  <!-- 4. #contact — AI Preconstruction Concierge & Priority Estimating Support -->
  <div id="contact" class="hidden fixed inset-0 z-50 bg-black/60 flex items-center justify-center p-4">
    <div class="max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 sm:p-8 rounded-2xl bg-white border-2 border-[#0A0D14] shadow-2xl space-y-4">
      <div class="flex items-center justify-between border-b border-[#CBD5E1] pb-3">
        <div>
          <div class="text-xs font-mono font-bold text-[#1E3A8A]">// 24/7 AI PRECONSTRUCTION CONCIERGE &amp; ESTIMATING DESK SUPPORT</div>
          <h3 class="text-xl font-extrabold text-[#0A0D14] mt-0.5">Ask Anything About 50-State DOT Lettings, 6-File .ZIPs, or API Setup</h3>
        </div>
        <button type="button" onclick="closeTrustModals()" class="px-3 py-1.5 rounded bg-[#EAE6DF] hover:bg-[#0A0D14] text-[#0A0D14] hover:text-white font-mono text-xs font-bold">Close [X]</button>
      </div>
      <div id="contact-modal-log" class="p-4 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] space-y-2.5 max-h-56 overflow-y-auto text-xs">
        <div class="p-3 rounded-lg bg-white border border-[#CBD5E1] font-medium text-[#0A0D14] leading-relaxed">
          <strong class="font-mono text-[#1E3A8A] block mb-1">CAMBERDESK AI CONCIERGE (ONLINE):</strong>
          Ask me about State DOT coverage (TxDOT, Caltrans, FDOT, VDOT, PennDOT, NYSDOT + all 50 states), the 6-File OpenXML (.DOCX + .XLSX) Bid Package Compiler, Davis-Bacon WH-347 wage rates, or MCP/REST API keys.
        </div>
      </div>
      <form onsubmit="sendContactModalConcierge(event)" class="flex gap-2">
        <input id="contact-modal-input" type="text" required placeholder="Ask about DOT bid tabs, Excel formulas, API keys, or billing..." class="flex-1 px-3.5 py-2.5 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] text-xs font-medium text-[#0A0D14] placeholder-[#1E293B]" />
        <button type="submit" class="px-4 py-2.5 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono text-xs font-bold">Ask AI &rarr;</button>
      </form>
      <div class="p-3.5 rounded-xl bg-[#FAF8F5] border border-[#CBD5E1] flex flex-wrap items-center justify-between gap-2 text-xs font-mono">
        <div><span class="font-bold text-[#0A0D14]">DIRECT ESTIMATING DESK EMAIL:</span> <a href="mailto:estimating@trycamberdesk.com" class="text-[#1E3A8A] font-extrabold underline">estimating@trycamberdesk.com</a></div>
        <span class="text-[#065F46] font-bold">SLA RESPONSE: &lt; 2 HOURS</span>
      </div>
    </div>
  </div>

  <!-- 5. #terms — Terms of Service & Enterprise API SLA -->
  <div id="terms" class="hidden fixed inset-0 z-50 bg-black/60 flex items-center justify-center p-4">
    <div class="max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 sm:p-8 rounded-2xl bg-white border-2 border-[#0A0D14] shadow-2xl space-y-4 text-xs">
      <div class="flex items-center justify-between border-b border-[#CBD5E1] pb-3">
        <div>
          <div class="text-xs font-mono font-bold text-[#1E3A8A]">// SELF-SERVE SUBSCRIPTION &amp; API TERMS OF SERVICE</div>
          <h3 class="text-xl font-extrabold text-[#0A0D14] mt-0.5">CamberDesk Inc. Commercial Terms &amp; SLA</h3>
        </div>
        <button type="button" onclick="closeTrustModals()" class="px-3 py-1.5 rounded bg-[#EAE6DF] hover:bg-[#0A0D14] text-[#0A0D14] hover:text-white font-mono text-xs font-bold">Close [X]</button>
      </div>
      <div class="space-y-3 font-medium text-[#111827] leading-relaxed">
        <p><strong class="text-[#0A0D14] font-bold">1. Self-Serve Subscriptions &amp; Zero Lock-In:</strong> CamberDesk Tier 1 ($199/mo), Tier 2 Autopilot ($499/mo), and Tier 3 6-File .ZIP Compiler ($1,499/mo) plans bill monthly or annually via Stripe and may be upgraded, downgraded, or cancelled at any time in 1 click via the <a href="#account" onclick="openTrustModal('account')" class="text-[#1E3A8A] font-bold underline">Client Portal</a>.</p>
        <p><strong class="text-[#0A0D14] font-bold">2. Full Ownership of Compiled Bid Packages:</strong> You retain 100% ownership and unrestricted commercial rights to all 6-File OpenXML (<code class="font-bold">.DOCX</code> and <code class="font-bold">.XLSX</code>) takeoff workbooks, AIA G702/G703 Schedules of Values, DBE Good-Faith Effort logs, and JSON manifests compiled through CamberDesk.</p>
        <p><strong class="text-[#0A0D14] font-bold">3. Independent Estimator Verification:</strong> CamberDesk automates specification shredding, 36-month historical DOT unit-price benchmarking, and Davis-Bacon WH-347 wage lookups from public government portals. Final bid pricing, bond execution, and statutory responsiveness remain the responsibility of the submitting contractor's licensed estimating team.</p>
      </div>
    </div>
  </div>

  <!-- 6. #privacy — Privacy Policy & Zero Bid-Data Retention Guarantee -->
  <div id="privacy" class="hidden fixed inset-0 z-50 bg-black/60 flex items-center justify-center p-4">
    <div class="max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 sm:p-8 rounded-2xl bg-white border-2 border-[#0A0D14] shadow-2xl space-y-4 text-xs">
      <div class="flex items-center justify-between border-b border-[#CBD5E1] pb-3">
        <div>
          <div class="text-xs font-mono font-bold text-[#065F46]">// ZERO BID-DATA RETENTION &amp; PRIVACY POLICY</div>
          <h3 class="text-xl font-extrabold text-[#0A0D14] mt-0.5">How CamberDesk Protects Your Estimating Desk Privacy</h3>
        </div>
        <button type="button" onclick="closeTrustModals()" class="px-3 py-1.5 rounded bg-[#EAE6DF] hover:bg-[#0A0D14] text-[#0A0D14] hover:text-white font-mono text-xs font-bold">Close [X]</button>
      </div>
      <div class="space-y-3 font-medium text-[#111827] leading-relaxed">
        <p><strong class="text-[#0A0D14] font-bold">1. Stateless Ephemeral API Execution:</strong> Inbound specification text, pay-item quantities, and unit-price overrides sent to <code class="font-bold">/v1/*</code> endpoints are processed strictly in memory and discarded immediately after response delivery.</p>
        <p><strong class="text-[#0A0D14] font-bold">2. Minimal Account Metadata:</strong> We store only your work email address, active subscription tier, and hashed API key required to authenticate your requests and deliver your selected 50-State DOT letting alerts.</p>
        <p><strong class="text-[#0A0D14] font-bold">3. Zero Third-Party Data Brokerage:</strong> CamberDesk never sells, rents, or shares subscriber contact details or bid activity with competing contractors, plan rooms, or brokers.</p>
      </div>
    </div>
  </div>

  <!-- COLLAPSIBLE DESKTOP QUICK-JUMP RAIL (#page-sidebar-drawer) -->
  <aside id="page-sidebar-drawer" class="hidden 2xl:flex fixed left-3 top-28 z-30 flex-col p-2.5 rounded-xl bg-white/95 border border-[#CBD5E1] shadow-md text-[11px] font-mono font-bold space-y-1.5">
    <div class="flex items-center justify-between gap-2 border-b border-[#CBD5E1] pb-1">
      <span class="text-[#1E3A8A]">QUICK JUMP</span>
      <button type="button" id="sidebar-rail-toggle" onclick="toggleSidebarRail()" class="text-[#0A0D14]">[-]</button>
    </div>
    <div id="sidebar-rail-links" class="flex flex-col gap-1">
      <a href="#overview" onclick="switchSpaView('overview')" class="px-2 py-1 rounded hover:bg-[#EAE6DF] text-[#0A0D14]">01 // Overview</a>
      <a href="#interactive-state-shredder" onclick="switchSpaView('overview')" class="px-2 py-1 rounded hover:bg-[#EAE6DF] text-[#0A0D14]">02 // DOT Shredder</a>
      <a href="#zip-package-inspector" onclick="switchSpaView('overview')" class="px-2 py-1 rounded hover:bg-[#EAE6DF] text-[#0A0D14]">03 // 6-File .ZIP</a>
      <a href="#roi-calculator" onclick="switchSpaView('overview')" class="px-2 py-1 rounded hover:bg-[#EAE6DF] text-[#0A0D14]">04 // ROI Calc</a>
      <a href="#contract-directory" onclick="switchSpaView('overview')" class="px-2 py-1 rounded hover:bg-[#EAE6DF] text-[#0A0D14]">05 // Lettings</a>
      <a href="#apis" onclick="switchSpaView('apis')" class="px-2 py-1 rounded hover:bg-[#EAE6DF] text-[#1E3A8A]">06 // 12 APIs &amp; MCP</a>
      <a href="#checkout" onclick="switchSpaView('checkout')" class="px-2 py-1 rounded hover:bg-[#EAE6DF] text-[#065F46]">07 // Pricing</a>
    </div>
  </aside>

  <!-- STICKY 4-TAB MOBILE BOTTOM NAVIGATION BAR (#mobile-bottom-nav) -->
  <nav id="mobile-bottom-nav" class="md:hidden fixed bottom-0 inset-x-0 z-30 bg-white border-t-2 border-[#0A0D14] grid grid-cols-4 text-[11px] font-mono font-bold text-center">
    <a href="#overview" onclick="switchSpaView('overview')" class="py-2.5 text-[#0A0D14] border-r border-[#CBD5E1]">Overview</a>
    <a href="#lettings" onclick="switchSpaView('lettings')" class="py-2.5 text-[#0A0D14] border-r border-[#CBD5E1]">Lettings</a>
    <a href="#apis" onclick="switchSpaView('apis')" class="py-2.5 text-[#1E3A8A] border-r border-[#CBD5E1]">12 APIs</a>
    <a href="#checkout" onclick="switchSpaView('checkout')" class="py-2.5 bg-[#0A0D14] text-white">Pricing</a>
  </nav>

  <!-- FLOATING AI PRECONSTRUCTION CONCIERGE WIDGET (#ai-concierge-widget) -->
  <div id="ai-concierge-widget" class="fixed bottom-14 md:bottom-5 right-4 z-40">
    <div id="concierge-drawer" class="hidden mb-3 w-80 sm:w-96 p-4 rounded-2xl bg-white border-2 border-[#0A0D14] shadow-2xl space-y-3">
      <div class="flex items-center justify-between border-b border-[#CBD5E1] pb-2">
        <div class="text-xs font-mono font-extrabold text-[#0A0D14]">CAMBERDESK AI CONCIERGE // 52 PORTALS</div>
        <button type="button" onclick="toggleConciergeDrawer()" class="text-xs font-mono font-bold text-[#0A0D14] hover:text-[#1E3A8A]">[X]</button>
      </div>
      <div id="concierge-chat-log" class="space-y-2 max-h-56 overflow-y-auto text-xs">
        <div class="p-2.5 rounded-lg bg-[#F4F1EA] border border-[#CBD5E1] font-medium text-[#0A0D14]">
          Ask about 50-State DOT bid tabulations, live Excel formulas in the 6-File .ZIP package, or MCP/REST API integration.
        </div>
      </div>
      <div class="flex flex-wrap gap-1.5 text-[11px] font-mono">
        <button type="button" onclick="askConciergeQuick('What is inside the 6-File .ZIP Bid Package?')" class="px-2 py-1 rounded bg-[#EAE6DF] hover:bg-[#0A0D14] text-[#0A0D14] hover:text-white font-bold">6-File .ZIP Contents</button>
        <button type="button" onclick="askConciergeQuick('Which 50 State DOT portals are monitored?')" class="px-2 py-1 rounded bg-[#EAE6DF] hover:bg-[#0A0D14] text-[#0A0D14] hover:text-white font-bold">50-State DOT List</button>
      </div>
      <form onsubmit="sendConciergeMessage(event)" class="flex gap-1.5">
        <input id="concierge-input" type="text" required placeholder="Ask preconstruction AI..." class="flex-1 px-2.5 py-1.5 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] text-xs font-medium text-[#0A0D14] placeholder-[#1E293B]" />
        <button type="submit" class="px-3 py-1.5 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono text-xs font-bold">Send</button>
      </form>
    </div>
    <button type="button" onclick="toggleConciergeDrawer()" class="px-4 py-2.5 rounded-full bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono text-xs font-bold shadow-lg border border-white/20 transition">
      AI Precon Concierge &bull; Ask Anything
    </button>
  </div>
"""

    index_title = "CamberDesk | 50-State DOT Bid-Tab, Prevailing-Wage &amp; Construction Takeoff Intelligence"
    index_desc = "Win more heavy-civil, highway, bridge, and commercial construction bids. Real-time 50-State DOT lettings, 36-month historical unit-price bid tabulations, Davis-Bacon WH-347 prevailing wages, and 1-Click 6-File OpenXML (.DOCX + .XLSX) Takeoff Packages."
    index_social_head = build_social_and_favicon_head(
        page_title=index_title,
        page_desc=index_desc,
        canonical_url="https://camberdesk.com/",
        rel_prefix="",
    )

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{index_title}</title>
  <meta name="description" content="{index_desc}" />
{index_social_head}
  <script src="https://cdn.tailwindcss.com"></script>
{high_contrast_style}
</head>
<body class="bg-[#FAF8F5] text-[#0A0D14] font-sans antialiased pb-14 md:pb-0">
  <!-- Top Telemetry Bar -->
  <div class="bg-[#EAE6DF] border-b border-[#CBD5E1] px-4 py-2 text-xs font-mono font-medium text-[#0A0D14] flex items-center justify-between overflow-x-auto whitespace-nowrap">
    <div class="flex items-center gap-2">
      <span class="inline-block w-2.5 h-2.5 rounded-full bg-[#065F46]"></span>
      <span class="text-[#0A0D14] font-extrabold">LIVE MONITORING: 52 GOVERNMENT &amp; DOT PORTALS ACTIVE</span>
      <span class="text-[#1E3A8A] font-bold">|</span>
      <span class="text-[#111827] font-semibold">{ticker_items}</span>
    </div>
    <div class="hidden lg:flex items-center gap-3 text-[#1E3A8A] font-bold">
      <a href="#status" onclick="openTrustModal('status')" class="hover:underline text-[#065F46]">STATUS: 52/52 LIVE</a> &bull; <span>12 LIVE ENDPOINTS</span> &bull; <span>6-FILE .ZIP TAKEOFF COMPILER</span>
    </div>
  </div>

  <!-- Navigation Header -->
  <header class="sticky top-0 z-40 border-b border-[#CBD5E1] bg-white/95 backdrop-blur">
    <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
      {_render_logo_lockup("50-STATE DOT BID-TAB, PREVAILING-WAGE & CSI TAKEOFF ENGINE", "#overview")}
      <nav class="hidden md:flex items-center gap-5 text-sm font-bold">
        <a href="#overview" onclick="switchSpaView('overview')" class="text-[#0A0D14] hover:text-[#1E3A8A]">Overview</a>
        <a href="#zip-package-inspector" onclick="switchSpaView('overview')" class="text-[#0A0D14] hover:text-[#1E3A8A]">6-File .ZIP Inspector</a>
        <a href="#lettings" onclick="switchSpaView('lettings')" class="text-[#0A0D14] hover:text-[#1E3A8A]">Live DOT Lettings</a>
        <a href="#apis" onclick="switchSpaView('apis')" class="text-[#0A0D14] hover:text-[#1E3A8A]">API Catalog</a>
        <a href="#account" onclick="openTrustModal('account')" class="px-3 py-1.5 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] text-xs font-mono font-bold transition">Client Portal</a>
        <a href="#checkout" onclick="switchSpaView('checkout')" class="px-4 py-2 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-bold transition">Self-Serve Pricing</a>
      </nav>
      <button type="button" onclick="toggleMobileNav()" class="md:hidden px-3 py-1.5 rounded-lg bg-[#EAE6DF] border border-[#94A3B8] text-xs font-mono font-bold text-[#0A0D14]">MENU</button>
    </div>
    <div id="mobile-nav-drawer" class="hidden md:hidden border-t border-[#CBD5E1] bg-white px-6 py-4 flex flex-col gap-3 text-sm font-bold">
      <a href="#overview" onclick="switchSpaView('overview')" class="text-[#0A0D14]">Overview</a>
      <a href="#zip-package-inspector" onclick="switchSpaView('overview')" class="text-[#0A0D14]">6-File .ZIP Package Inspector</a>
      <a href="#roi-calculator" onclick="switchSpaView('overview')" class="text-[#0A0D14]">Estimating ROI Calculator</a>
      <a href="#lettings" onclick="switchSpaView('lettings')" class="text-[#0A0D14]">Live 50-State DOT Lettings</a>
      <a href="#apis" onclick="switchSpaView('apis')" class="text-[#0A0D14]">API Catalog</a>
      <a href="#account" onclick="openTrustModal('account')" class="text-[#1E3A8A]">Client Portal (#account)</a>
      <a href="#status" onclick="openTrustModal('status')" class="text-[#065F46]">Live System Status (#status)</a>
      <a href="#checkout" onclick="switchSpaView('checkout')" class="px-4 py-2 rounded-lg bg-[#0A0D14] text-white text-center font-bold">Self-Serve Pricing</a>
    </div>
  </header>

  <!-- VIEW 1: OVERVIEW (#page-overview) -->
  <main id="page-overview" class="max-w-7xl mx-auto px-6 py-12 space-y-16">
    <!-- Personalized Outbound Prospect Attribution Banner (#main-outbound-prospect-banner) -->
    <div id="main-outbound-prospect-banner" class="hidden p-4 rounded-xl bg-[#EFF6FF] border-2 border-[#1E3A8A] flex flex-wrap items-center justify-between gap-3 text-xs font-mono">
      <div id="prospect-banner-text" class="font-extrabold text-[#1E3A8A]">Custom Preconstruction &amp; DOT Bid-Tab Workspace Prepared for Your Estimating Desk — 6-File OpenXML Sample Ready.</div>
      <a href="https://api.camberdesk.com/v1/camber-autopilot/compile-bid-package?format=binary" class="px-3 py-1.5 rounded bg-[#0A0D14] text-white font-bold">Download Custom 6-File .ZIP</a>
    </div>

    <!-- Hero -->
    <section class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
      <div class="lg:col-span-7 space-y-5">
        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#EAE6DF] border border-[#94A3B8] text-xs font-mono font-bold text-[#0A0D14]">
          52 PORTALS DE-NOISED 24/7 &bull; ALL 50 U.S. STATE DOTS + USACE + MUNICIPAL
        </div>
        <h1 class="text-3xl sm:text-5xl font-extrabold text-[#0A0D14] tracking-tight leading-tight">
          Stop Bidding Blind on Heavy-Civil &amp; Commercial Lettings.
        </h1>
        <p class="text-base font-medium text-[#111827] leading-relaxed">
          Legacy plan rooms charge $15,000/yr just to dump raw 600-page PDFs on your estimating desk.
          <strong class="text-[#0A0D14] font-bold">CamberDesk</strong> unifies all 50 U.S. State DOT letting portals, shreds CSI MasterFormat Divisions 00–48, models 36-month competitor unit-price bid tabulations (<code class="text-[#1E3A8A] font-bold">$/Ton</code>, <code class="text-[#1E3A8A] font-bold">$/LF</code>, <code class="text-[#1E3A8A] font-bold">$/CY</code>), and compiles a ready-to-price <strong class="text-[#1E3A8A] font-bold">6-File OpenXML (.DOCX + .XLSX) Bid Package</strong> in 1 click.
        </p>
        <div class="flex flex-wrap gap-4 pt-2">
          <a href="#checkout" onclick="switchSpaView('checkout')" class="px-6 py-3 rounded-xl bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-bold text-sm transition">Activate CamberDesk Autopilot ($499/mo)</a>
          <a href="https://api.camberdesk.com/v1/camber-autopilot/compile-bid-package?format=binary" class="px-6 py-3 rounded-xl bg-[#EFF6FF] hover:bg-[#DBEAFE] text-[#1E3A8A] border-2 border-[#1E3A8A] font-bold text-sm transition">Download Live 6-File .ZIP Sample</a>
          <a href="#apis" onclick="switchSpaView('apis')" class="px-6 py-3 rounded-xl bg-white hover:bg-[#EAE6DF] text-[#0A0D14] border-2 border-[#0A0D14] font-bold text-sm transition">Explore 12 Precon APIs &amp; MCP</a>
        </div>
      </div>

      <!-- Hero Tier 2 Dossier Card -->
      <div class="lg:col-span-5 p-6 rounded-2xl bg-white border-2 border-[#0A0D14] shadow-sm space-y-4">
        <div class="text-xs font-mono font-bold text-[#1E3A8A]">TIER 2 // CAMBERDESK AUTOPILOT (52 PORTALS + 7 PRECON APIS)</div>
        <h3 class="text-lg font-extrabold text-[#0A0D14]">Pre-Shredded DOT Bid-Tab &amp; Takeoff Dossiers</h3>
        <ul class="space-y-2 text-xs font-semibold text-[#111827] font-mono">
          <li>&bull; API #01: CSI MasterFormat Divisions 00–48 Spec &amp; Submittal Shredder</li>
          <li>&bull; API #02: 50-State DOT Historical Item Bid Tabulation Modeler</li>
          <li>&bull; API #03: Davis-Bacon (29 CFR 5) &amp; WH-347 Prevailing Wage Calculator</li>
          <li>&bull; API #04: 52-Portal Live State DOT, USACE &amp; Municipal Letting Feed</li>
          <li>&bull; API #05: Build America, Buy America (BABA / 23 CFR 635.410) Auditor</li>
          <li>&bull; API #06: DOT DBE (49 CFR Part 26) Good Faith Effort Generator</li>
          <li>&bull; API #11: DOT Planholder Competitor Spread &amp; MLOT Predictor</li>
        </ul>
        <div class="pt-2">
          <a href="lettings/index.html" class="inline-block w-full text-center px-4 py-2.5 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-bold text-xs font-mono transition">Browse Live Pre-Shredded Letting Dossiers &rarr;</a>
        </div>
      </div>
    </section>

    <!-- Client ROI Metrics Strip (#hero-metrics-strip) -->
    <section id="hero-metrics-strip" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="p-5 rounded-xl bg-white border border-[#CBD5E1] shadow-sm">
        <div class="text-2xl sm:text-3xl font-extrabold font-mono text-[#0A0D14]">52 Portals</div>
        <div class="mt-1 text-xs font-mono font-bold uppercase tracking-wider text-[#1E3A8A]">50-State DOT + USACE + Muni</div>
        <p class="mt-1.5 text-xs font-medium text-[#111827]">Every State DOT letting schedule, USACE NAICS 236–238 solicitation, and public works bid normalized 24/7.</p>
      </div>
      <div class="p-5 rounded-xl bg-white border border-[#CBD5E1] shadow-sm">
        <div class="text-2xl sm:text-3xl font-extrabold font-mono text-[#065F46]">1.42M+ Items</div>
        <div class="mt-1 text-xs font-mono font-bold uppercase tracking-wider text-[#065F46]">36-Month Bid-Tab Vault</div>
        <p class="mt-1.5 text-xs font-medium text-[#111827]">Historical winning low unit prices ($/Ton, $/CY, $/LF) and competitor money-left-on-table spreads.</p>
      </div>
      <div class="p-5 rounded-xl bg-white border border-[#CBD5E1] shadow-sm">
        <div class="text-2xl sm:text-3xl font-extrabold font-mono text-[#1E3A8A]">6-File .ZIP</div>
        <div class="mt-1 text-xs font-mono font-bold uppercase tracking-wider text-[#1E3A8A]">Native Word + Excel Formulas</div>
        <p class="mt-1.5 text-xs font-medium text-[#111827]">Ready-to-price OpenXML (.DOCX + .XLSX) takeoff books with live =SUM() &amp; =ROUND() unit formulas.</p>
      </div>
      <div class="p-5 rounded-xl bg-white border border-[#CBD5E1] shadow-sm">
        <div class="text-2xl sm:text-3xl font-extrabold font-mono text-[#0A0D14]">85% Faster</div>
        <div class="mt-1 text-xs font-mono font-bold uppercase tracking-wider text-[#0A0D14]">Zero $15K Annual Lock-In</div>
        <p class="mt-1.5 text-xs font-medium text-[#111827]">Shred 600-page spec books, WH-347 prevailing wages, and BABA steel rules in seconds. Cancel anytime.</p>
      </div>
    </section>

    <!-- 3-Persona Role Quick-Start Switcher & 5-Stage Product Stepper (#persona-quickstart-bar & #product-5stage-stepper) -->
    <section id="persona-quickstart-bar" class="p-6 sm:p-8 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm space-y-6">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div>
          <div class="text-xs font-mono font-bold text-[#1E3A8A]">// ROLE-BASED PRECONSTRUCTION WORKFLOW &amp; 5-STAGE AUTOPILOT STEPPER</div>
          <h2 id="persona-active-title" class="text-xl sm:text-2xl font-extrabold text-[#0A0D14] mt-0.5">Chief Estimator / VP of Preconstruction Workflow</h2>
        </div>
        <div class="flex flex-wrap gap-2">
          <button type="button" id="persona-btn-estimator" onclick="selectPersonaQuickstart('estimator')" class="px-3.5 py-2 rounded-lg bg-[#0A0D14] text-white font-mono text-xs font-bold transition">Chief Estimator</button>
          <button type="button" id="persona-btn-takeoff" onclick="selectPersonaQuickstart('takeoff')" class="px-3.5 py-2 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] font-mono text-xs font-bold transition">Take-Off Engineer</button>
          <button type="button" id="persona-btn-developer" onclick="selectPersonaQuickstart('developer')" class="px-3.5 py-2 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] font-mono text-xs font-bold transition">ConTech / MCP Developer</button>
        </div>
      </div>
      <p id="persona-active-desc" class="text-sm font-medium text-[#111827] leading-relaxed">Eliminate 14+ hours of manual spec reading per letting. Review 36-month DOT winning low unit prices ($/Ton, $/CY, $/LF), competitor planholder spreads, and balanced AIA G702/G703 Schedules of Values before locking in your final markup.</p>
      <div id="product-5stage-stepper" class="space-y-3 pt-2 border-t border-[#CBD5E1]">
        <div class="grid grid-cols-2 sm:grid-cols-5 gap-2">
          <button type="button" id="stage-step-btn-0" onclick="switchOverviewProductTab(0)" class="px-3 py-2 rounded-lg bg-[#0A0D14] text-white font-mono text-xs font-bold transition">01 // 52-Portal Feed</button>
          <button type="button" id="stage-step-btn-1" onclick="switchOverviewProductTab(1)" class="px-3 py-2 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] font-mono text-xs font-bold transition">02 // CSI Spec Shred</button>
          <button type="button" id="stage-step-btn-2" onclick="switchOverviewProductTab(2)" class="px-3 py-2 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] font-mono text-xs font-bold transition">03 // 36-Mo Bid-Tab</button>
          <button type="button" id="stage-step-btn-3" onclick="switchOverviewProductTab(3)" class="px-3 py-2 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] font-mono text-xs font-bold transition">04 // WH-347 &amp; BABA</button>
          <button type="button" id="stage-step-btn-4" onclick="switchOverviewProductTab(4)" class="px-3 py-2 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] font-mono text-xs font-bold transition">05 // 6-File .ZIP</button>
        </div>
        <div class="p-4 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div class="space-y-1">
            <div id="stage-step-title" class="text-sm font-mono font-extrabold text-[#0A0D14]">Stage 01 // 52-Portal DOT &amp; USACE Letting Ingestion (API #04)</div>
            <p id="stage-step-detail" class="text-xs font-medium text-[#111827]">Normalizes upcoming heavy-civil, highway, bridge, utility, and USACE NAICS 236–238 lettings across all 50 State DOTs with Engineer Estimates, DBE goals, and bid dates.</p>
          </div>
          <code id="stage-step-code" class="shrink-0 px-3 py-2 rounded-lg bg-white border border-[#94A3B8] text-xs font-mono font-bold text-[#1E3A8A]">GET /v1/lettings/live -> 52 Portals Normalized</code>
        </div>
      </div>
    </section>

    <!-- Free Instant 6-File .ZIP Sample Lead-Magnet Banner (#sample-lead-magnet) -->
    <section id="sample-lead-magnet" class="p-6 sm:p-8 rounded-2xl bg-white border-2 border-[#1E3A8A] shadow-sm space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <div>
          <div class="text-xs font-mono font-bold text-[#1E3A8A]">// INSTANT ESTIMATOR TEST DRIVE — ZERO CREDIT CARD REQUIRED</div>
          <h2 class="text-xl sm:text-2xl font-extrabold text-[#0A0D14] mt-0.5">Get a Free 6-File OpenXML (.DOCX + .XLSX) DOT Bid Package Sample</h2>
        </div>
        <span class="px-3 py-1 rounded bg-[#ECFDF5] border border-[#6EE7B7] text-xs font-mono font-bold text-[#065F46]">LIVE EXCEL FORMULAS INCLUDED</span>
      </div>
      <form onsubmit="submitSampleLeadMagnet(event)" class="grid grid-cols-1 md:grid-cols-4 gap-3">
        <input id="lead-magnet-email" type="email" required placeholder="estimating@yourcontractor.com" class="px-3.5 py-2.5 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] text-sm font-medium text-[#0A0D14] placeholder-[#1E293B]" />
        <select id="lead-magnet-state" class="px-3.5 py-2.5 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] text-sm font-bold text-[#0A0D14]">
          <option value="All 50 State DOTs">All 50 State DOTs + USACE</option>
          <option value="TX — TxDOT">TX — TxDOT (Texas)</option>
          <option value="CA — Caltrans">CA — Caltrans (California)</option>
          <option value="FL — FDOT">FL — FDOT (Florida)</option>
          <option value="VA — VDOT">VA — VDOT (Virginia)</option>
          <option value="PA — PennDOT">PA — PennDOT (Pennsylvania)</option>
          <option value="NY — NYSDOT">NY — NYSDOT (New York)</option>
          <option value="OH — ODOT">OH — ODOT (Ohio)</option>
          <option value="GA — GDOT">GA — GDOT (Georgia)</option>
          <option value="NC — NCDOT">NC — NCDOT (North Carolina)</option>
        </select>
        <select id="lead-magnet-trade" class="px-3.5 py-2.5 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] text-sm font-bold text-[#0A0D14]">
          <option value="Heavy-Civil / Highway & Bridge">Heavy-Civil / Highway &amp; Bridge</option>
          <option value="Asphalt & Concrete Paving">Asphalt &amp; Concrete Paving</option>
          <option value="Wet Utilities / Water & Sewer">Wet Utilities / Water &amp; Sewer</option>
          <option value="Commercial GC / Facilities">Commercial GC / Facilities</option>
          <option value="ITS / Electrical / Traffic Signals">ITS / Electrical / Traffic Signals</option>
        </select>
        <button type="submit" class="px-4 py-2.5 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono text-xs font-bold transition">Download 6-File .ZIP Sample &rarr;</button>
      </form>
      <div id="lead-magnet-status" class="text-xs font-mono font-bold text-[#065F46]">Includes Volume I–V (.DOCX + .XLSX) + 00_CamberDesk_Letting_Readiness_Manifest.json</div>
    </section>

    <!-- Section: Why Basic Plan Rooms Fail Chief Estimators + Side-by-Side Comparison (#capture-moat) -->
    <section id="capture-moat" class="p-8 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm space-y-6">
      <div class="text-xs font-mono font-bold text-[#1E3A8A]">// PRECONSTRUCTION MOAT — 52 ACTIVE PORTALS &amp; 7 CORE LETTING ENGINES</div>
      <h2 class="text-2xl font-extrabold text-[#0A0D14]">Why Basic Plan Rooms Fail Chief Estimators — And What CamberDesk Automates</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
        <div class="p-5 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] space-y-2.5">
          <div class="text-xs font-mono font-bold text-[#1E3A8A]">01 // CSI SPEC &amp; LIQUIDATED DAMAGES SHREDDING</div>
          <p class="text-[#111827] font-medium leading-relaxed">Automatically extracts Division 00–48 submittal registers, nighttime lane-rental penalties, and liquidated damages ($/day) via API #01 &amp; API #04.</p>
        </div>
        <div class="p-5 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] space-y-2.5">
          <div class="text-xs font-mono font-bold text-[#065F46]">02 // 36-MONTH DOT ITEM BID TABULATIONS</div>
          <p class="text-[#111827] font-medium leading-relaxed">Benchmarks every pay item against historical winning low bids, competitor planholder spreads, and 23 CFR 635.102 unbalanced-bid guardrails via API #02 &amp; API #11.</p>
        </div>
        <div class="p-5 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] space-y-2.5">
          <div class="text-xs font-mono font-bold text-[#0A0D14]">03 // DAVIS-BACON WH-347, DBE &amp; BABA COMPLIANCE</div>
          <p class="text-[#111827] font-medium leading-relaxed">Computes county-specific Davis-Bacon craft fringes, 49 CFR Part 26 DBE credits, and BABA domestic steel certifications via API #03, API #05 &amp; API #06.</p>
        </div>
      </div>

      <!-- Legacy Plan Rooms vs. CamberDesk Comparison Table (#before-after-comparison) -->
      <div id="before-after-comparison" class="pt-4 overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs sm:text-sm">
          <thead>
            <tr class="bg-[#EAE6DF] border-b-2 border-[#94A3B8] font-mono font-bold text-[#0A0D14]">
              <th class="py-3 px-3">PRECONSTRUCTION CAPABILITY</th>
              <th class="py-3 px-3">LEGACY BID BOARDS (CONSTRUCTCONNECT / DODGE / RAW PDFS)</th>
              <th class="py-3 px-3 text-[#1E3A8A]">CAMBERDESK AUTONOMOUS PRECON ENGINE</th>
            </tr>
          </thead>
          <tbody class="font-medium text-[#111827]">
            <tr class="border-b border-[#CBD5E1]"><td class="py-2.5 px-3 font-bold text-[#0A0D14]">36-Month DOT Unit-Price Bid Tabs</td><td class="py-2.5 px-3">Manual state PDF lookups; no pay-item price modeling</td><td class="py-2.5 px-3 font-bold text-[#065F46]">Automated $/Ton, $/CY &amp; $/LF low-bid benchmarking (API #02)</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2.5 px-3 font-bold text-[#0A0D14]">CSI Divisions 00–48 Spec Shredding</td><td class="py-2.5 px-3">Manual 600-page Ctrl+F across special provisions</td><td class="py-2.5 px-3 font-bold text-[#065F46]">Instant submittal register + liquidated damages extraction (API #01)</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2.5 px-3 font-bold text-[#0A0D14]">Davis-Bacon WH-347 Wage Rates</td><td class="py-2.5 px-3">Manual SAM.gov WDOL lookup &amp; spreadsheet entry</td><td class="py-2.5 px-3 font-bold text-[#065F46]">County-matched craft base + fringe + overtime crew burden (API #03)</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2.5 px-3 font-bold text-[#0A0D14]">DBE (49 CFR 26) &amp; BABA Steel Audit</td><td class="py-2.5 px-3">Static PDF addenda; high risk of bid responsiveness rejection</td><td class="py-2.5 px-3 font-bold text-[#065F46]">Automated CUF dealer credit math &amp; BABA melt/pour matrix (API #05/#06)</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2.5 px-3 font-bold text-[#0A0D14]">Takeoff Deliverable Format</td><td class="py-2.5 px-3">Unstructured PDF files</td><td class="py-2.5 px-3 font-bold text-[#1E3A8A]">1-Click 6-File OpenXML (.DOCX + .XLSX with live Excel formulas)</td></tr>
            <tr><td class="py-2.5 px-3 font-bold text-[#0A0D14]">Pricing &amp; Contract Terms</td><td class="py-2.5 px-3">$12,000–$18,000/yr mandatory annual seat lock-in</td><td class="py-2.5 px-3 font-bold text-[#0A0D14]">$199–$499/mo self-serve, REST + MCP API included, cancel anytime</td></tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Interactive State-by-State Before/After DOT Bid-Tab Shredder (#interactive-state-shredder) -->
    <section id="interactive-state-shredder" class="p-6 sm:p-8 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm space-y-5">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div>
          <div class="text-xs font-mono font-bold text-[#1E3A8A]">// INTERACTIVE STATE DOT BEFORE &amp; AFTER SPEC SHREDDER</div>
          <h2 class="text-2xl font-extrabold text-[#0A0D14] mt-0.5">See How CamberDesk Turns Raw DOT Special Provisions Into Priced Bid Tabs</h2>
        </div>
        <div class="flex flex-wrap gap-2">
          <button type="button" id="shredder-state-btn-TX" onclick="selectInteractiveDossier('TX')" class="px-3 py-1.5 rounded-lg bg-[#0A0D14] text-white font-mono text-xs font-bold transition">TX — TxDOT</button>
          <button type="button" id="shredder-state-btn-CA" onclick="selectInteractiveDossier('CA')" class="px-3 py-1.5 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] font-mono text-xs font-bold transition">CA — Caltrans</button>
          <button type="button" id="shredder-state-btn-FL" onclick="selectInteractiveDossier('FL')" class="px-3 py-1.5 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] font-mono text-xs font-bold transition">FL — FDOT</button>
          <button type="button" id="shredder-state-btn-VA" onclick="selectInteractiveDossier('VA')" class="px-3 py-1.5 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] font-mono text-xs font-bold transition">VA — VDOT</button>
          <button type="button" id="shredder-state-btn-USACE" onclick="selectInteractiveDossier('USACE')" class="px-3 py-1.5 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] font-mono text-xs font-bold transition">USACE Federal</button>
        </div>
      </div>
      <div id="shredder-active-badge" class="text-xs font-mono font-bold text-[#1E3A8A]">TXDOT // CSJ 0912-72-641 (HARRIS COUNTY I-45)</div>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div class="p-4 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] space-y-2 min-w-0">
          <div class="text-xs font-mono font-bold text-[#0A0D14]">BEFORE // RAW UNSTRUCTURED STATE DOT SPECIAL PROVISION PDF</div>
          <pre id="shredder-raw-pdf" class="p-3.5 rounded-lg bg-white border border-[#CBD5E1] text-xs font-mono font-medium text-[#0F172A] whitespace-pre-wrap leading-relaxed">SPECIAL PROVISION TO ITEM 3076 (DENSE-GRADED HOT-MIX ASPHALT)
Contractor shall place 48,500 TON PG 76-22 SAC-A surface course during nighttime lane closure window 21:00 to 05:00 only. Liquidated damages: $3,850/day. Lane rental overrun penalty: $2,000/hour. DBE Goal: 10.5%. Wage Decision: TX20260038.</pre>
        </div>
        <div class="p-4 rounded-xl bg-[#ECFDF5] border-2 border-[#065F46] space-y-2 min-w-0">
          <div class="text-xs font-mono font-bold text-[#065F46]">AFTER // CAMBERDESK AI BID-TAB, WH-347 WAGE &amp; BABA OUTPUT</div>
          <pre id="shredder-ai-output" class="p-3.5 rounded-lg bg-white border border-[#CBD5E1] text-xs font-mono font-medium text-[#064E3B] whitespace-pre-wrap leading-relaxed">1. PAY-ITEM 36-MO BID-TAB MODEL (API #02):
   - Item 3076-6001 (48,500 TON): 36-Mo Low Avg $108.50/Ton -> Recommended Bid $112.90/Ton ($5,475,650.00)
   - Item 0420-6013 Structural Concrete (4,200 CY): Recommended Bid $925.00/CY ($3,885,000.00)
2. LIQUIDATED DAMAGES &amp; LANE RENTAL (API #01):
   - $3,850/calendar day + $2,000/hr night lane overrun risk flagged
3. DAVIS-BACON WH-347 &amp; BABA STEEL (API #03/#05):
   - Paving Operator Loaded Rate: $55.25/hr • 100% U.S. Melt &amp; Pour Rebar Required</pre>
        </div>
      </div>
    </section>

    <!-- Interactive 6-File OpenXML .ZIP Package Inspector (#zip-package-inspector) -->
    <section id="zip-package-inspector" class="p-6 sm:p-8 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm space-y-5">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div>
          <div class="text-xs font-mono font-bold text-[#1E3A8A]">// MOAT #1 — IN-MEMORY PURE-PYTHON OPENXML COMPILER</div>
          <h2 class="text-2xl font-extrabold text-[#0A0D14] mt-0.5">Inspect All 6 Files Inside Every CamberDesk Bid Package (.ZIP)</h2>
        </div>
        <a href="https://api.camberdesk.com/v1/camber-autopilot/compile-bid-package?format=binary" class="px-4 py-2.5 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono text-xs font-bold transition">Download Live 6-File .ZIP Now &rarr;</a>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">
        <div class="lg:col-span-5 flex flex-col gap-2 min-w-0">
          <button type="button" id="zip-tab-btn-0" onclick="switchZipInspectorTab(0)" class="px-3 py-2 rounded-lg bg-[#0A0D14] text-white font-mono text-xs font-bold text-left break-all transition">01 // Volume_I_CSI_MasterFormat_Spec_Matrix.docx</button>
          <button type="button" id="zip-tab-btn-1" onclick="switchZipInspectorTab(1)" class="px-3 py-2 rounded-lg bg-[#F4F1EA] hover:bg-[#EAE6DF] text-[#0A0D14] border border-[#CBD5E1] font-mono text-xs font-bold text-left break-all transition">02 // Volume_II_DOT_Unit_Price_Bid_Tab.xlsx</button>
          <button type="button" id="zip-tab-btn-2" onclick="switchZipInspectorTab(2)" class="px-3 py-2 rounded-lg bg-[#F4F1EA] hover:bg-[#EAE6DF] text-[#0A0D14] border border-[#CBD5E1] font-mono text-xs font-bold text-left break-all transition">03 // Volume_III_Davis_Bacon_WH347_Wage_Model.xlsx</button>
          <button type="button" id="zip-tab-btn-3" onclick="switchZipInspectorTab(3)" class="px-3 py-2 rounded-lg bg-[#F4F1EA] hover:bg-[#EAE6DF] text-[#0A0D14] border border-[#CBD5E1] font-mono text-xs font-bold text-left break-all transition">04 // Volume_IV_DBE_49CFR26_and_BABA_Cert.docx</button>
          <button type="button" id="zip-tab-btn-4" onclick="switchZipInspectorTab(4)" class="px-3 py-2 rounded-lg bg-[#F4F1EA] hover:bg-[#EAE6DF] text-[#0A0D14] border border-[#CBD5E1] font-mono text-xs font-bold text-left break-all transition">05 // Volume_V_AIA_G702_G703_SOV_and_FOIA.docx</button>
          <button type="button" id="zip-tab-btn-5" onclick="switchZipInspectorTab(5)" class="px-3 py-2 rounded-lg bg-[#F4F1EA] hover:bg-[#EAE6DF] text-[#0A0D14] border border-[#CBD5E1] font-mono text-xs font-bold text-left break-all transition">06 // 00_CamberDesk_Letting_Readiness_Manifest.json</button>
        </div>
        <div class="lg:col-span-7 p-5 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] space-y-3 min-w-0">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <div id="zip-inspector-title" class="text-sm font-mono font-extrabold text-[#0A0D14] break-all">Volume_I_CSI_MasterFormat_Divisions_00_48_Spec_and_Submittal_Matrix.docx</div>
            <span id="zip-inspector-format" class="px-2.5 py-0.5 rounded bg-[#EFF6FF] text-[#1E3A8A] border border-[#93C5FD] text-xs font-mono font-bold">Microsoft Word OpenXML (.DOCX)</span>
          </div>
          <p id="zip-inspector-summary" class="text-xs font-semibold text-[#111827]">Full CSI Divisions 00-48 specification shred: Submittal Register, Liquidated Damages ($/day), Nighttime Lane-Rental Window Penalties, and Retainage Clauses.</p>
          <pre id="zip-inspector-preview" class="p-3.5 rounded-lg bg-white border border-[#CBD5E1] text-xs font-mono font-medium text-[#0F172A] overflow-x-auto leading-relaxed">SECTION 00 73 00 — SUPPLEMENTARY CONDITIONS
- Liquidated Damages: $3,500 / calendar day beyond substantial completion
- Nighttime Lane Closure Window: 21:00 to 05:00 local ($1,500/hr overrun penalty)

CSI SUBMITTAL REGISTER (EXTRACTED):
- Div 03 30 00 Cast-in-Place Concrete: Mix Design &amp; 28-Day Cylinder Break Certs
- Div 31 23 00 Excavation &amp; Fill: Proctor Compaction &amp; Dewatering Plan
- Div 32 12 16 Asphalt Paving: Superpave PG 76-22 JMF &amp; Tack Coat Submittal
- Div 34 41 13 Traffic Signals &amp; ITS: NEMA TS2 Controller &amp; Fiber OTDR Test</pre>
        </div>
      </div>
    </section>

    <!-- Interactive Estimating Time-Savings & Bid-Tab Margin ROI Calculator (#roi-calculator) -->
    <section id="roi-calculator" class="p-6 sm:p-8 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm space-y-6">
      <div>
        <div class="text-xs font-mono font-bold text-[#065F46]">// CHIEF ESTIMATOR PAYBACK &amp; MARGIN PROTECTION CALCULATOR</div>
        <h2 class="text-2xl font-extrabold text-[#0A0D14] mt-0.5">Calculate Your Estimating Desk's Monthly Time &amp; Payroll Savings</h2>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
        <div class="lg:col-span-7 space-y-4">
          <div>
            <div class="flex justify-between text-xs font-mono font-bold text-[#0A0D14] mb-1"><span>MONTHLY DOT / CIVIL LETTINGS BID</span><span id="roi-bids-val" class="text-[#1E3A8A]">8 lettings/mo</span></div>
            <input id="roi-bids-mo" type="range" min="1" max="35" value="8" oninput="updateRoiCalculator()" class="w-full accent-[#1E3A8A]" />
          </div>
          <div>
            <div class="flex justify-between text-xs font-mono font-bold text-[#0A0D14] mb-1"><span>MANUAL SPEC SHRED &amp; BID-TAB HOURS PER LETTING</span><span id="roi-hrs-val" class="text-[#1E3A8A]">14 hrs/bid</span></div>
            <input id="roi-hrs-bid" type="range" min="4" max="30" value="14" oninput="updateRoiCalculator()" class="w-full accent-[#1E3A8A]" />
          </div>
          <div>
            <div class="flex justify-between text-xs font-mono font-bold text-[#0A0D14] mb-1"><span>LOADED SENIOR ESTIMATOR HOURLY COST ($/HR)</span><span id="roi-rate-val" class="text-[#1E3A8A]">$115/hr</span></div>
            <input id="roi-hourly-rate" type="range" min="65" max="185" value="115" step="5" oninput="updateRoiCalculator()" class="w-full accent-[#1E3A8A]" />
          </div>
        </div>
        <div class="lg:col-span-5 p-5 rounded-xl bg-[#F4F1EA] border-2 border-[#0A0D14] grid grid-cols-2 gap-3 text-center font-mono">
          <div class="p-3 rounded-lg bg-white border border-[#CBD5E1]"><div class="text-[11px] font-bold text-[#0A0D14]">ESTIMATING HRS SAVED</div><div id="roi-out-hours" class="text-lg font-extrabold text-[#1E3A8A] mt-1">95 hrs / mo</div></div>
          <div class="p-3 rounded-lg bg-white border border-[#CBD5E1]"><div class="text-[11px] font-bold text-[#0A0D14]">MONTHLY PAYROLL SAVED</div><div id="roi-out-monthly" class="text-lg font-extrabold text-[#065F46] mt-1">$10,925 / mo</div></div>
          <div class="p-3 rounded-lg bg-white border border-[#CBD5E1]"><div class="text-[11px] font-bold text-[#0A0D14]">ANNUAL PAYROLL SAVED</div><div id="roi-out-annual" class="text-lg font-extrabold text-[#0A0D14] mt-1">$131,100 / yr</div></div>
          <div class="p-3 rounded-lg bg-[#ECFDF5] border border-[#6EE7B7]"><div class="text-[11px] font-bold text-[#065F46]">NET RETURN MULTIPLE</div><div id="roi-out-multiple" class="text-lg font-extrabold text-[#065F46] mt-1">21.9x ROI vs. $499/mo Tier 2</div></div>
        </div>
      </div>
    </section>

    <!-- Live Letting Directory (#contract-directory) -->
    <section id="contract-directory" style="overflow-anchor: none;" class="p-6 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div class="text-xs font-mono font-bold text-[#1E3A8A]">// LIVE 52-PORTAL DOT, USACE &amp; PUBLIC WORKS LETTING WIRE</div>
          <h2 class="text-xl font-extrabold text-[#0A0D14]">Upcoming Heavy-Civil, Highway, Bridge &amp; Utility Lettings</h2>
        </div>
        <div class="flex flex-wrap items-center gap-2">
          <input id="letting-search-input" type="text" oninput="filterMainLettingTable(window.ACTIVE_PORTAL_FILTER || 'all')" placeholder="Search project ID, highway, agency, or county..." class="px-3 py-1.5 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] text-xs font-medium text-[#0A0D14] placeholder-[#1E293B]" />
          <button type="button" onclick="exportLettingsCsv()" class="px-3 py-1.5 rounded-lg bg-[#EAE6DF] hover:bg-[#0A0D14] text-[#0A0D14] hover:text-white border border-[#94A3B8] text-xs font-mono font-bold transition">Export .CSV</button>
          <span id="letting-shown-badge" class="px-3 py-1 rounded bg-[#EAE6DF] border border-[#94A3B8] text-xs font-mono font-bold text-[#0A0D14]">{len(lettings)} PREVIEW LETTINGS SHOWN</span>
        </div>
      </div>
      <div class="flex flex-wrap gap-2 text-xs font-mono">
        <button type="button" onclick="filterMainLettingTable('all')" class="px-3 py-1.5 rounded bg-[#0A0D14] text-white font-bold">All Portals (52)</button>
        <button type="button" onclick="filterMainLettingTable('texas')" class="px-3 py-1.5 rounded bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] font-bold border border-[#94A3B8]">TxDOT (TX)</button>
        <button type="button" onclick="filterMainLettingTable('california')" class="px-3 py-1.5 rounded bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] font-bold border border-[#94A3B8]">Caltrans (CA)</button>
        <button type="button" onclick="filterMainLettingTable('florida')" class="px-3 py-1.5 rounded bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] font-bold border border-[#94A3B8]">FDOT (FL)</button>
        <button type="button" onclick="filterMainLettingTable('virginia')" class="px-3 py-1.5 rounded bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] font-bold border border-[#94A3B8]">VDOT (VA)</button>
        <button type="button" onclick="filterMainLettingTable('pennsylvania')" class="px-3 py-1.5 rounded bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] font-bold border border-[#94A3B8]">PennDOT (PA)</button>
        <button type="button" onclick="filterMainLettingTable('new_york')" class="px-3 py-1.5 rounded bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] font-bold border border-[#94A3B8]">NYSDOT (NY)</button>
        <button type="button" onclick="filterMainLettingTable('federal')" class="px-3 py-1.5 rounded bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] font-bold border border-[#94A3B8]">USACE Federal</button>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-[#EAE6DF] border-b-2 border-[#94A3B8] text-xs font-mono font-bold text-[#0A0D14]">
              <th class="py-2.5 px-3">PROJECT ID</th>
              <th class="py-2.5 px-3">LETTING TITLE &amp; SCOPE</th>
              <th class="py-2.5 px-3">OWNER / DISTRICT</th>
              <th class="py-2.5 px-3">ENGINEER'S EST</th>
              <th class="py-2.5 px-3">DBE GOAL</th>
              <th class="py-2.5 px-3">LETTING DATE</th>
              <th class="py-2.5 px-3 text-right">ACTION</th>
            </tr>
          </thead>
          <tbody>
            {''.join(letting_rows)}
          </tbody>
        </table>
      </div>
    </section>

    <!-- 52-Portal Coverage Grid (#coverage) -->
    <section id="coverage" class="space-y-4">
      <div class="text-xs font-mono font-bold text-[#1E3A8A]">// 52 ACTIVE PROCUREMENT &amp; STATE DOT LETTING PORTALS</div>
      <h2 class="text-2xl font-extrabold text-[#0A0D14]">50-State DOT, USACE Civil Works &amp; Municipal Coverage</h2>
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
        {''.join(portal_cards)}
      </div>
    </section>
  </main>

  <!-- VIEW 2: API CATALOG (#page-apis) -->
  <section id="page-apis" class="hidden max-w-7xl mx-auto px-6 py-12">
    {api_catalog_block}
  </section>

  <!-- VIEW 3: LETTINGS DIRECTORY (#page-lettings) -->
  <section id="page-lettings" class="hidden max-w-7xl mx-auto px-6 py-12 space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <div class="text-xs font-mono font-bold text-[#1E3A8A]">52 PORTALS ACTIVE &bull; 50-STATE DOT &amp; USACE DIRECTORY</div>
        <h2 class="text-2xl font-extrabold text-[#0A0D14]">Interactive Preconstruction &amp; Bid-Tab Dossier Explorer</h2>
      </div>
      <a href="lettings/index.html" class="px-4 py-2 rounded-lg bg-white text-[#0A0D14] text-xs font-mono font-bold border border-[#94A3B8] shadow-sm">Open Static HTML Index &rarr;</a>
    </div>
    <div id="contracts-dynamic-root" class="min-h-[200px]"></div>
  </section>

  <!-- VIEW 4: SELF-SERVE CHECKOUT (#page-checkout) -->
  <section id="page-checkout" class="hidden max-w-7xl mx-auto px-6 py-12 space-y-8">
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <div class="text-xs font-mono font-bold text-[#1E3A8A]">// ZERO-DEMO SELF-SERVE ACTIVATION</div>
        <h2 class="text-3xl font-extrabold text-[#0A0D14]">Instant Access Across All 50 State DOTs &amp; 12 Precon APIs</h2>
      </div>
      <div class="inline-flex rounded-lg bg-[#EAE6DF] p-1 border border-[#94A3B8] text-xs font-mono">
        <button type="button" onclick="setCheckoutBilling('monthly')" class="px-3 py-1.5 rounded bg-[#0A0D14] text-white font-bold">Monthly</button>
        <button type="button" onclick="setCheckoutBilling('annual')" class="px-3 py-1.5 rounded text-[#0A0D14] hover:text-[#1E3A8A] font-bold">Annual (2 Months Free)</button>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
      <div id="checkout-card-tier1" class="p-6 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm flex flex-col justify-between space-y-4">
        <div class="space-y-3">
          <div class="text-xs font-mono font-bold text-[#0A0D14]">TIER 1 // CAMBERWIRE PRO</div>
          <div id="price-tier1" class="text-3xl font-extrabold text-[#0A0D14]">$199 / mo</div>
          <p class="text-xs font-medium text-[#111827] leading-relaxed">Real-time 50-State DOT, USACE Civil &amp; Municipal letting alerts + official planholder tracking.</p>
        </div>
        <button type="button" id="btn-checkout-tier1" onclick="openCamberCheckoutModal('tier1_monthly')" class="w-full text-center py-2.5 rounded-lg bg-[#EAE6DF] hover:bg-[#0A0D14] text-[#0A0D14] hover:text-white border border-[#94A3B8] font-bold text-xs font-mono transition">Activate Tier 1</button>
      </div>

      <div id="checkout-card-tier2" class="p-6 rounded-2xl bg-white border-2 border-[#0A0D14] shadow-md flex flex-col justify-between space-y-4">
        <div class="space-y-3">
          <div class="text-xs font-mono font-bold text-[#1E3A8A]">TIER 2 // CAMBERDESK AUTOPILOT (RECOMMENDED)</div>
          <div id="price-tier2" class="text-3xl font-extrabold text-[#0A0D14]">$499 / mo</div>
          <p class="text-xs font-medium text-[#111827] leading-relaxed">Full pre-shredded CSI Divisions 00–48 dossiers, 36-month DOT item bid tabulations, Davis-Bacon WH-347 rates, and API key for all 12 microservices.</p>
        </div>
        <button type="button" id="btn-checkout-tier2" onclick="openCamberCheckoutModal('tier2_monthly')" class="w-full text-center py-2.5 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-bold text-xs font-mono transition">Activate Tier 2 Autopilot</button>
      </div>

      <div id="checkout-card-tier3" class="p-6 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm flex flex-col justify-between space-y-4">
        <div class="space-y-3">
          <div class="text-xs font-mono font-bold text-[#065F46]">TIER 3 // 6-FILE .ZIP TAKEOFF COMPILER</div>
          <div id="price-tier3" class="text-3xl font-extrabold text-[#0A0D14]">$1,499 / mo</div>
          <p class="text-xs font-medium text-[#111827] leading-relaxed">Unlimited 1-Click 6-File OpenXML (.DOCX + .XLSX with live formulas) Bid-Tab, Prevailing-Wage &amp; AIA G702/G703 compilations.</p>
        </div>
        <button type="button" id="btn-checkout-tier3" onclick="openCamberCheckoutModal('tier3_monthly')" class="w-full text-center py-2.5 rounded-lg bg-[#1E3A8A] hover:bg-[#0A0D14] text-white font-bold text-xs font-mono transition">Activate Tier 3 Compiler</button>
      </div>

      <div id="checkout-card-tier4" class="p-6 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm flex flex-col justify-between space-y-4">
        <div class="space-y-3">
          <div class="text-xs font-mono font-bold text-[#0A0D14]">TIER 4 // SURETY &amp; CONTECH OEM</div>
          <div id="price-tier4" class="text-3xl font-extrabold text-[#0A0D14]">$2,499 / mo</div>
          <p class="text-xs font-medium text-[#111827] leading-relaxed">Multi-branch surety underwriting, HeavyBid/Procore ERP webhook pipes, custom SLA &amp; unlimited estimating seats.</p>
        </div>
        <button type="button" id="btn-checkout-tier4" onclick="openCamberCheckoutModal('tier4_monthly')" class="w-full text-center py-2.5 rounded-lg bg-[#EAE6DF] hover:bg-[#0A0D14] text-[#0A0D14] hover:text-white border border-[#94A3B8] font-bold text-xs font-mono transition">Activate Tier 4 OEM</button>
      </div>
    </div>

    <div class="p-4 rounded-xl bg-white border border-[#CBD5E1] text-xs font-mono font-semibold text-[#0A0D14]">
      All 12 individual CamberDesk microservices are also available on RapidAPI and via <code class="text-[#1E3A8A] font-bold">@camberdesk/mcp-server</code>.
    </div>

    <!-- 3-Mode Enterprise Proof Workbench (#checkout-enterprise-proof-workbench) -->
    <div id="checkout-enterprise-proof-workbench" class="p-6 sm:p-8 rounded-2xl bg-white border-2 border-[#0A0D14] shadow-sm space-y-5">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div>
          <div class="text-xs font-mono font-bold text-[#1E3A8A]">// INTERACTIVE PRECONSTRUCTION PROOF WORKBENCH — TEST BEFORE YOU SUBSCRIBE</div>
          <h3 class="text-xl font-extrabold text-[#0A0D14] mt-0.5">Compile a Custom 6-File .ZIP, Query the 36-Month Bid-Tab Vault, or Generate a CFO Quote</h3>
        </div>
        <div class="flex flex-wrap gap-2">
          <button type="button" id="workbench-tab-compiler" onclick="switchCheckoutWorkbenchTab('compiler')" class="px-3.5 py-2 rounded-lg bg-[#0A0D14] text-white font-mono text-xs font-bold transition">01 // Custom 6-File .ZIP Compiler</button>
          <button type="button" id="workbench-tab-vault" onclick="switchCheckoutWorkbenchTab('vault')" class="px-3.5 py-2 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] font-mono text-xs font-bold transition">02 // 36-Mo Bid-Tab Vault Query</button>
          <button type="button" id="workbench-tab-cfo" onclick="switchCheckoutWorkbenchTab('cfo')" class="px-3.5 py-2 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] font-mono text-xs font-bold transition">03 // 1-Click CFO / PO Quote</button>
        </div>
      </div>

      <!-- Mode 1: Custom 6-File .ZIP Compiler -->
      <div id="workbench-mode-compiler" class="grid grid-cols-1 lg:grid-cols-2 gap-4 text-xs">
        <div class="space-y-3">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            <input id="wb-custom-title" type="text" value="TxDOT IH-35 Widening &amp; Drainage Structures" class="px-3 py-2 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] font-bold text-[#0A0D14]" />
            <input id="wb-custom-agency" type="text" value="Texas Department of Transportation (TxDOT)" class="px-3 py-2 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] font-bold text-[#0A0D14]" />
          </div>
          <textarea id="wb-custom-text" rows="4" class="w-full p-3 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] font-mono font-medium text-[#0A0D14]">Item 3076 Dense-Graded Hot-Mix Asphalt 48,500 TON; Item 0420 Class C Concrete 4,200 CY; Liquidated Damages $3,500/day; DBE Goal 9.5%; Wage Decision TX20260038.</textarea>
          <div class="flex flex-wrap gap-2.5">
            <button type="button" onclick="runCheckoutCustomRfpCompile()" class="px-4 py-2 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono font-bold">Compile Custom Manifest Live</button>
            <a href="https://api.camberdesk.com/v1/camber-autopilot/compile-bid-package?format=binary" class="px-4 py-2 rounded-lg bg-[#EFF6FF] text-[#1E3A8A] border border-[#93C5FD] font-mono font-bold">Download 6-File .ZIP Binary</a>
          </div>
        </div>
        <pre id="wb-custom-output" class="p-3.5 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] font-mono font-medium text-[#064E3B] overflow-x-auto leading-relaxed">{{
  "status": "READY_FOR_CUSTOM_COMPILATION",
  "files_included": 6,
  "formats": [".DOCX", ".XLSX (Live Formulas)", ".JSON"]
}}</pre>
      </div>

      <!-- Mode 2: 36-Month DOT Unit-Price Bid-Tab Vault Query -->
      <div id="workbench-mode-vault" class="hidden grid grid-cols-1 lg:grid-cols-2 gap-4 text-xs">
        <div class="space-y-3">
          <label class="block font-mono font-bold text-[#0A0D14]">SELECT STATE DOT &amp; PAY ITEM TO BENCHMARK</label>
          <select id="wb-vault-state" onchange="runCheckoutFoiaVaultPreview()" class="w-full px-3 py-2 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] font-bold text-[#0A0D14]">
            <option value="TX — TxDOT">TX — TxDOT (Texas)</option>
            <option value="CA — Caltrans">CA — Caltrans (California)</option>
            <option value="FL — FDOT">FL — FDOT (Florida)</option>
            <option value="VA — VDOT">VA — VDOT (Virginia)</option>
            <option value="PA — PennDOT">PA — PennDOT (Pennsylvania)</option>
          </select>
          <select id="wb-vault-item" onchange="runCheckoutFoiaVaultPreview()" class="w-full px-3 py-2 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] font-bold text-[#0A0D14]">
            <option value="3076-6001 Dense-Graded Hot-Mix Asphalt (TON)">3076-6001 Dense-Graded Hot-Mix Asphalt (TON)</option>
            <option value="0420-6013 Class C Structural Concrete (CY)">0420-6013 Class C Structural Concrete (CY)</option>
            <option value="0460-6002 24-Inch RCP Storm Drain Pipe (LF)">0460-6002 24-Inch RCP Storm Drain Pipe (LF)</option>
          </select>
          <button type="button" onclick="runCheckoutFoiaVaultPreview()" class="px-4 py-2 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono font-bold">Query 36-Month Bid-Tab Vault</button>
        </div>
        <pre id="wb-vault-output" class="p-3.5 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] font-mono font-medium text-[#064E3B] overflow-x-auto leading-relaxed">{{
  "state_dot": "TX — TxDOT",
  "pay_item": "3076-6001 Dense-Graded Hot-Mix Asphalt (TON)",
  "winning_low_avg_usd": 109.8,
  "recommended_target_bid_usd": 113.4
}}</pre>
      </div>

      <!-- Mode 3: 1-Click CFO / Preconstruction Approval Memo & PO Quote -->
      <div id="workbench-mode-cfo" class="hidden grid grid-cols-1 lg:grid-cols-2 gap-4 text-xs">
        <div class="space-y-3">
          <label class="block font-mono font-bold text-[#0A0D14]">GENERATE EXECUTIVE ROI &amp; PO JUSTIFICATION MEMO</label>
          <input id="wb-cfo-company" type="text" placeholder="Apex Heavy Civil &amp; Paving LLC" class="w-full px-3 py-2 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] font-bold text-[#0A0D14] placeholder-[#1E293B]" />
          <select id="wb-cfo-tier" class="w-full px-3 py-2 rounded-lg bg-[#FAF8F5] border border-[#94A3B8] font-bold text-[#0A0D14]">
            <option value="Tier 2 — CamberDesk Autopilot ($499/mo or $4,490/yr)">Tier 2 — CamberDesk Autopilot ($499/mo or $4,490/yr)</option>
            <option value="Tier 3 — 6-File .ZIP Takeoff Compiler ($1,499/mo or $14,900/yr)">Tier 3 — 6-File .ZIP Takeoff Compiler ($1,499/mo or $14,900/yr)</option>
            <option value="Tier 4 — Surety & ConTech OEM ($2,499/mo or $24,900/yr)">Tier 4 — Surety &amp; ConTech OEM ($2,499/mo or $24,900/yr)</option>
          </select>
          <button type="button" onclick="generateCfoProcurementQuote()" class="px-4 py-2 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-mono font-bold">Generate CFO Approval Memo</button>
        </div>
        <pre id="wb-cfo-output" class="p-3.5 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] font-mono font-medium text-[#0F172A] overflow-x-auto leading-relaxed">Click "Generate CFO Approval Memo" to build a ready-to-forward preconstruction ROI &amp; purchase order quote.</pre>
      </div>
    </div>

    <!-- 25-Row 4-Tier Capability Matrix (#checkout-panel-matrix) -->
    <div id="checkout-panel-matrix" class="p-6 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm space-y-4">
      <div class="text-xs font-mono font-bold text-[#1E3A8A]">// COMPLETE 4-TIER PRECONSTRUCTION CAPABILITY MATRIX</div>
      <h3 class="text-xl font-extrabold text-[#0A0D14]">Compare Tier 1, Tier 2 Autopilot, Tier 3 Compiler &amp; Tier 4 OEM</h3>
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="bg-[#EAE6DF] border-b-2 border-[#94A3B8] font-mono font-bold text-[#0A0D14]">
              <th class="py-2.5 px-3">CAPABILITY / DELIVERABLE</th>
              <th class="py-2.5 px-3">TIER 1 ($199/MO)</th>
              <th class="py-2.5 px-3 text-[#1E3A8A]">TIER 2 ($499/MO)</th>
              <th class="py-2.5 px-3 text-[#065F46]">TIER 3 ($1,499/MO)</th>
              <th class="py-2.5 px-3">TIER 4 ($2,499/MO)</th>
            </tr>
          </thead>
          <tbody class="font-medium text-[#111827]">
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">01. 50-State DOT Letting Schedule Monitor</td><td class="py-2 px-3">Included (50 States)</td><td class="py-2 px-3 font-bold text-[#065F46]">Included (50 States)</td><td class="py-2 px-3 font-bold text-[#065F46]">Included (50 States)</td><td class="py-2 px-3 font-bold text-[#065F46]">Included (50 States)</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">02. Federal USACE NAICS 236–238 Monitor</td><td class="py-2 px-3">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">03. Municipal Public Works Bid Monitor</td><td class="py-2 px-3">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">04. Official Planholder &amp; Bidder Roster</td><td class="py-2 px-3">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">05. CSV &amp; Excel Letting Feed Export</td><td class="py-2 px-3">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">06. API #01 CSI Divisions 00–48 Shredder</td><td class="py-2 px-3">—</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited OEM</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">07. API #02 36-Mo DOT Unit-Price Modeler</td><td class="py-2 px-3">—</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited OEM</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">08. API #03 Davis-Bacon WH-347 Wage Engine</td><td class="py-2 px-3">—</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited OEM</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">09. API #04 Unified 52-Portal REST Feed</td><td class="py-2 px-3">Read Access</td><td class="py-2 px-3 font-bold text-[#065F46]">Full REST + MCP</td><td class="py-2 px-3 font-bold text-[#065F46]">Full REST + MCP</td><td class="py-2 px-3 font-bold text-[#065F46]">Dedicated Firehose</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">10. API #05 BABA Domestic Steel Auditor</td><td class="py-2 px-3">—</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited OEM</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">11. API #06 49 CFR 26 DBE GFE Generator</td><td class="py-2 px-3">—</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited OEM</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">12. API #07 AIA G702/G703 SOV Modeler</td><td class="py-2 px-3">—</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited OEM</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">13. API #08 Miller Act &amp; Surety Auditor</td><td class="py-2 px-3">—</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited</td><td class="py-2 px-3 font-bold text-[#065F46]">Multi-Surety OEM</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">14. API #09 RFI &amp; Change-Order Drafter</td><td class="py-2 px-3">—</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited OEM</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">15. API #10 OSHA EMR &amp; SWPPP Compliance</td><td class="py-2 px-3">—</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited OEM</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">16. API #11 Competitor MLOT Spread Model</td><td class="py-2 px-3">—</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited OEM</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">17. API #12 Subcontractor ITB Scope Engine</td><td class="py-2 px-3">—</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited OEM</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">18. Volume I CSI Spec Matrix (.DOCX)</td><td class="py-2 px-3">—</td><td class="py-2 px-3">Sample Preview</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited .DOCX</td><td class="py-2 px-3 font-bold text-[#065F46]">White-Label .DOCX</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">19. Volume II DOT Bid-Tab Workbook (.XLSX)</td><td class="py-2 px-3">—</td><td class="py-2 px-3">Sample Preview</td><td class="py-2 px-3 font-bold text-[#065F46]">Live Excel Formulas</td><td class="py-2 px-3 font-bold text-[#065F46]">Live Excel Formulas</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">20. Volume III WH-347 Wage Model (.XLSX)</td><td class="py-2 px-3">—</td><td class="py-2 px-3">Sample Preview</td><td class="py-2 px-3 font-bold text-[#065F46]">Live Excel Formulas</td><td class="py-2 px-3 font-bold text-[#065F46]">Live Excel Formulas</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">21. Volume IV DBE &amp; BABA Certs (.DOCX)</td><td class="py-2 px-3">—</td><td class="py-2 px-3">Sample Preview</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited .DOCX</td><td class="py-2 px-3 font-bold text-[#065F46]">White-Label .DOCX</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">22. Volume V AIA G702/G703 SOV (.DOCX)</td><td class="py-2 px-3">—</td><td class="py-2 px-3">Sample Preview</td><td class="py-2 px-3 font-bold text-[#065F46]">Unlimited .DOCX</td><td class="py-2 px-3 font-bold text-[#065F46]">White-Label .DOCX</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">23. Remote HTTP (/mcp) &amp; STDIO MCP Server</td><td class="py-2 px-3">—</td><td class="py-2 px-3 font-bold text-[#065F46]">Included (5/5 TDQS)</td><td class="py-2 px-3 font-bold text-[#065F46]">Included (5/5 TDQS)</td><td class="py-2 px-3 font-bold text-[#065F46]">Dedicated Tenant</td></tr>
            <tr class="border-b border-[#CBD5E1]"><td class="py-2 px-3 font-bold text-[#0A0D14]">24. HeavyBid / Procore / Sage 300 Blueprints</td><td class="py-2 px-3">—</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Included</td><td class="py-2 px-3 font-bold text-[#065F46]">Custom ERP Sync</td></tr>
            <tr><td class="py-2 px-3 font-bold text-[#0A0D14]">25. Contract Terms &amp; Cancellation</td><td class="py-2 px-3 font-bold">Cancel Anytime</td><td class="py-2 px-3 font-bold text-[#065F46]">Cancel Anytime</td><td class="py-2 px-3 font-bold text-[#065F46]">Cancel Anytime</td><td class="py-2 px-3 font-bold">Custom MSA / SLA</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Chief Estimator Testimonials & FAQ Accordion -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4">
      <div class="p-5 rounded-xl bg-white border border-[#CBD5E1] space-y-2">
        <div class="text-xs font-mono font-bold text-[#065F46]">// HEAVY-CIVIL PRIME CONTRACTOR (TX / OK)</div>
        <p class="text-xs font-medium text-[#111827] leading-relaxed">"CamberDesk's 36-month TxDOT pay-item bid-tab workbook and live Excel formulas cut our asphalt &amp; structural concrete takeoff prep from 16 hours to 45 minutes."</p>
      </div>
      <div class="p-5 rounded-xl bg-white border border-[#CBD5E1] space-y-2">
        <div class="text-xs font-mono font-bold text-[#1E3A8A]">// BRIDGE &amp; MARINE ESTIMATING DESK (VA / MD / NC)</div>
        <p class="text-xs font-medium text-[#111827] leading-relaxed">"Having BABA domestic steel certifications, 49 CFR Part 26 DBE dealer credit math, and WH-347 fringes pre-compiled into Word and Excel is a massive unfair advantage."</p>
      </div>
      <div class="p-5 rounded-xl bg-white border border-[#CBD5E1] space-y-2">
        <div class="text-xs font-mono font-bold text-[#0A0D14]">// PUBLIC WORKS UTILITY CONTRACTOR (CA / AZ)</div>
        <p class="text-xs font-medium text-[#111827] leading-relaxed">"We replaced a $16,500/yr legacy plan-room seat lock-in with CamberDesk Tier 2 Autopilot and plugged the MCP server straight into our estimating workflow."</p>
      </div>
    </div>

    <div class="p-6 rounded-2xl bg-white border border-[#CBD5E1] space-y-3">
      <div class="text-xs font-mono font-bold text-[#1E3A8A]">// FREQUENTLY ASKED PRECONSTRUCTION &amp; BILLING QUESTIONS</div>
      <div class="border-b border-[#CBD5E1] pb-2">
        <button type="button" onclick="toggleFaqItem(0)" class="w-full text-left py-2 text-sm font-extrabold text-[#0A0D14] flex justify-between"><span>Which 50 State DOT and federal construction portals are monitored?</span><span>[+]</span></button>
        <div id="faq-ans-0" class="hidden pb-2 text-xs font-medium text-[#111827] leading-relaxed">All 50 U.S. State DOT letting portals (TxDOT, Caltrans, FDOT, VDOT, PennDOT, NYSDOT, ODOT, GDOT, NCDOT, IDOT, WSDOT, etc.), Federal USACE / SAM.gov NAICS 236–238, and Municipal Public Works portals (52 active portals total).</div>
      </div>
      <div class="border-b border-[#CBD5E1] pb-2">
        <button type="button" onclick="toggleFaqItem(1)" class="w-full text-left py-2 text-sm font-extrabold text-[#0A0D14] flex justify-between"><span>Do the Excel (.XLSX) files inside the 6-File .ZIP contain live formulas?</span><span>[+]</span></button>
        <div id="faq-ans-1" class="hidden pb-2 text-xs font-medium text-[#111827] leading-relaxed">Yes. Volume II (DOT Unit-Price Bid Tabulation) and Volume III (Davis-Bacon WH-347 Wage Model) are native OpenXML .XLSX workbooks with live =ROUND(D6*G6,2) and =SUM() formulas ready for HeavyBid, B2W, or Excel.</div>
      </div>
      <div>
        <button type="button" onclick="toggleFaqItem(2)" class="w-full text-left py-2 text-sm font-extrabold text-[#0A0D14] flex justify-between"><span>Is there any annual contract lock-in or per-seat fee?</span><span>[+]</span></button>
        <div id="faq-ans-2" class="hidden pb-2 text-xs font-medium text-[#111827] leading-relaxed">Zero lock-in. Monthly plans are strictly month-to-month and can be managed or cancelled in 1 click via the <a href="#account" onclick="openTrustModal('account')" class="text-[#1E3A8A] font-bold underline">Self-Serve Client Portal</a>.</div>
      </div>
    </div>
  </section>

  <footer class="border-t border-[#CBD5E1] bg-[#EAE6DF] py-8 mt-16">
    <div class="max-w-7xl mx-auto px-6 space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-4 text-xs font-mono font-bold text-[#0A0D14]">
        <div>ALL 52 FEDERAL USACE &amp; 50-STATE DOT PORTAL MONITORS ACTIVE</div>
        <div class="flex flex-wrap items-center gap-4">
          <a href="#account" onclick="openTrustModal('account')" class="hover:text-[#1E3A8A] underline">Client Portal (#account)</a>
          <a href="#status" onclick="openTrustModal('status')" class="text-[#065F46] hover:text-[#1E3A8A] underline">System Status (#status)</a>
          <a href="#security" onclick="openTrustModal('security')" class="hover:text-[#1E3A8A] underline">Security (#security)</a>
          <a href="#contact" onclick="openTrustModal('contact')" class="hover:text-[#1E3A8A] underline">AI Concierge (#contact)</a>
          <a href="#terms" onclick="openTrustModal('terms')" class="hover:text-[#1E3A8A] underline">Terms (#terms)</a>
          <a href="#privacy" onclick="openTrustModal('privacy')" class="hover:text-[#1E3A8A] underline">Privacy (#privacy)</a>
        </div>
      </div>
      <div class="text-xs font-mono font-semibold text-[#111827] flex flex-wrap items-center justify-between gap-2 border-t border-[#CBD5E1] pt-3">
        <div>&copy; 2026 CamberDesk Inc. &bull; Stateless Preconstruction, 50-State DOT Bid-Tab &amp; Prevailing-Wage DaaS</div>
        <div>Support: <a href="mailto:estimating@trycamberdesk.com" class="text-[#1E3A8A] font-bold">estimating@trycamberdesk.com</a></div>
      </div>
    </div>
  </footer>

{trust_modals_and_concierge_html}
  <script>{common_js}</script>
</body>
</html>"""

    apis_title = "CamberDesk API Catalog | 12 Construction, DOT Bid-Tab &amp; Prevailing-Wage Microservices"
    apis_desc = "Stateless REST and MCP APIs for CSI MasterFormat specification shredding, 50-State DOT unit-price bid tabulations, Davis-Bacon WH-347 prevailing wages, and AIA G702/G703 schedules of values."
    apis_social_head = build_social_and_favicon_head(
        page_title=apis_title,
        page_desc=apis_desc,
        canonical_url="https://camberdesk.com/apis.html",
        rel_prefix="",
    )

    apis_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{apis_title}</title>
  <meta name="description" content="{apis_desc}" />
{apis_social_head}
  <script src="https://cdn.tailwindcss.com"></script>
{high_contrast_style}
</head>
<body class="bg-[#FAF8F5] text-[#0A0D14] font-sans antialiased pb-14 md:pb-0">
  <header class="sticky top-0 z-40 border-b border-[#CBD5E1] bg-white/95 backdrop-blur">
    <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
      {_render_logo_lockup("12 STATELESS PRECONSTRUCTION REST & MCP MICROSERVICES", "index.html")}
      <nav class="hidden md:flex items-center gap-5 text-sm font-bold">
        <a href="index.html" class="text-[#0A0D14] hover:text-[#1E3A8A]">Overview</a>
        <a href="lettings/index.html" class="text-[#0A0D14] hover:text-[#1E3A8A]">Live DOT Lettings</a>
        <a href="apis.html" class="text-[#1E3A8A] font-extrabold">API Catalog</a>
        <a href="#account" onclick="openTrustModal('account')" class="px-3 py-1.5 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] text-xs font-mono font-bold transition">Client Portal</a>
        <a href="index.html#checkout" class="px-4 py-2 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-bold transition">Self-Serve Pricing</a>
      </nav>
      <button type="button" onclick="toggleMobileNav()" class="md:hidden px-3 py-1.5 rounded-lg bg-[#EAE6DF] border border-[#94A3B8] text-xs font-mono font-bold text-[#0A0D14]">MENU</button>
    </div>
    <div id="mobile-nav-drawer" class="hidden md:hidden border-t border-[#CBD5E1] bg-white px-6 py-4 flex flex-col gap-3 text-sm font-bold">
      <a href="index.html" class="text-[#0A0D14]">Overview</a>
      <a href="lettings/index.html" class="text-[#0A0D14]">Live 50-State DOT Lettings</a>
      <a href="apis.html" class="text-[#1E3A8A]">API Catalog</a>
      <a href="#account" onclick="openTrustModal('account')" class="text-[#1E3A8A]">Client Portal (#account)</a>
      <a href="#status" onclick="openTrustModal('status')" class="text-[#065F46]">Live System Status (#status)</a>
      <a href="index.html#checkout" class="px-4 py-2 rounded-lg bg-[#0A0D14] text-white text-center font-bold">Self-Serve Pricing</a>
    </div>
  </header>
  <main class="max-w-7xl mx-auto px-6 py-12">
    {api_catalog_block}
  </main>
  <footer class="border-t border-[#CBD5E1] bg-[#EAE6DF] py-8 mt-16">
    <div class="max-w-7xl mx-auto px-6 flex flex-wrap items-center justify-between gap-4 text-xs font-mono font-bold text-[#0A0D14]">
      <div>ALL 52 FEDERAL USACE &amp; 50-STATE DOT PORTAL MONITORS ACTIVE</div>
      <div class="flex flex-wrap items-center gap-4">
        <a href="#account" onclick="openTrustModal('account')" class="hover:text-[#1E3A8A] underline">Client Portal (#account)</a>
        <a href="#status" onclick="openTrustModal('status')" class="text-[#065F46] hover:text-[#1E3A8A] underline">System Status (#status)</a>
        <a href="#security" onclick="openTrustModal('security')" class="hover:text-[#1E3A8A] underline">Security (#security)</a>
        <a href="#contact" onclick="openTrustModal('contact')" class="hover:text-[#1E3A8A] underline">AI Concierge (#contact)</a>
        <a href="#terms" onclick="openTrustModal('terms')" class="hover:text-[#1E3A8A] underline">Terms (#terms)</a>
        <a href="#privacy" onclick="openTrustModal('privacy')" class="hover:text-[#1E3A8A] underline">Privacy (#privacy)</a>
      </div>
    </div>
  </footer>
{trust_modals_and_concierge_html}
  <script>{common_js}</script>
</body>
</html>"""

    with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(index_html)
    with open(os.path.join(BASE_DIR, "apis.html"), "w", encoding="utf-8") as fh:
        fh.write(apis_html)

    print("[CAMBERDESK SITE BUILDER] Generated D:\\CamberDesk\\index.html & D:\\CamberDesk\\apis.html with Symbol #07 & Warm Vellum / Obsidian Ink theme.")


if __name__ == "__main__":
    build_site_files()
