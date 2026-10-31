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
                  <a href="#checkout" onclick="switchSpaView('checkout')" class="px-4 py-2.5 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] text-xs font-mono font-bold transition">Included in Tier 2 ($499/mo)</a>
                </div>
              </div>
              <div class="lg:col-span-5 space-y-3 min-w-0">
                <div class="text-xs font-mono font-bold text-[#0A0D14]">// REQUEST &amp; RESPONSE SCHEMA PREVIEW</div>
                <pre class="p-3.5 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] text-xs font-mono font-medium text-[#0F172A] leading-relaxed overflow-x-auto max-w-full">{req_json}</pre>
                <pre class="p-3.5 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1] text-xs font-mono font-medium text-[#064E3B] leading-relaxed overflow-x-auto max-w-full">{res_json}</pre>
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
            <textarea id="sandbox-req-box" rows="6" class="w-full p-3.5 rounded-lg bg-[#F4F1EA] border border-[#CBD5E1] text-xs font-mono font-medium text-[#0F172A] leading-relaxed">{json.dumps(APIS_CATALOG[0]['req_sample'], indent=2)}</textarea>
          </div>
          <div class="min-w-0">
            <div class="text-xs font-mono font-bold text-[#0A0D14] mb-1.5">Live Structured Response (200 OK)</div>
            <pre id="sandbox-res-box" class="p-3.5 rounded-lg bg-[#F4F1EA] border border-[#CBD5E1] text-xs font-mono font-medium text-[#064E3B] leading-relaxed overflow-x-auto max-w-full">{json.dumps(APIS_CATALOG[0]['res_sample'], indent=2)}</pre>
          </div>
        </div>
        <button type="button" onclick="executeSandboxCall()" class="px-4 py-2.5 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-bold text-xs font-mono transition">Execute Stateless API Call</button>
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

    function switchSpaView(viewName) {{
      document.documentElement.style.scrollBehavior = 'auto';
      window.scrollTo(0, 0);
      const views = ['overview', 'apis', 'lettings', 'checkout'];
      views.forEach(v => {{
        const el = document.getElementById('page-' + v);
        if (el) el.classList.toggle('hidden', v !== viewName);
      }});
      if (viewName === 'lettings') renderLettingsRoute('#lettings');
    }}

    function filterMainLettingTable(portalFilter) {{
      const container = document.getElementById('contract-directory');
      if (container) container.style.minHeight = container.offsetHeight + 'px';
      const rows = document.querySelectorAll('[data-letting-row]');
      let shown = 0;
      rows.forEach(r => {{
        const p = r.getAttribute('data-letting-portal') || '';
        const match = !portalFilter || portalFilter === 'all' || p === portalFilter;
        r.style.display = match ? '' : 'none';
        if (match) shown++;
      }});
      const badge = document.getElementById('letting-shown-badge');
      if (badge) badge.textContent = shown + ' PREVIEW LETTINGS SHOWN';
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

    function openApiSandbox(cardId) {{
      const meta = (window.API_META || {{}})[cardId];
      const cat = (window.CATALOG || {{}})[cardId];
      if (!meta) return;
      const sel = document.getElementById('sandbox-api-select');
      if (sel) sel.value = cardId;
      const reqBox = document.getElementById('sandbox-req-box');
      const resBox = document.getElementById('sandbox-res-box');
      if (reqBox) reqBox.value = JSON.stringify(meta.defaultPayload, null, 2);
      if (resBox) resBox.textContent = JSON.stringify(cat, null, 2);
    }}

    function executeSandboxCall() {{
      const sel = document.getElementById('sandbox-api-select');
      const cardId = sel ? sel.value : 'product-csi-masterformat';
      const cat = (window.CATALOG || {{}})[cardId] || {{ status: 'success' }};
      const resBox = document.getElementById('sandbox-res-box');
      if (resBox) resBox.textContent = JSON.stringify(cat, null, 2);
    }}

    function setCheckoutBilling(mode) {{
      const isAnnual = mode === 'annual';
      const t1 = document.getElementById('price-tier1');
      const t2 = document.getElementById('price-tier2');
      const t3 = document.getElementById('price-tier3');
      const b1 = document.getElementById('btn-checkout-tier1');
      const b2 = document.getElementById('btn-checkout-tier2');
      const b3 = document.getElementById('btn-checkout-tier3');
      if (t1) t1.textContent = isAnnual ? '$1,990 / yr' : '$199 / mo';
      if (t2) t2.textContent = isAnnual ? '$4,490 / yr' : '$499 / mo';
      if (t3) t3.textContent = isAnnual ? '$14,900 / yr' : '$1,499 / mo';
      if (b1) b1.href = isAnnual ? 'https://buy.stripe.com/8x228q4aC2pdbt69UE7wA03?client_reference_id=camberdesk_tier1_annual' : 'https://buy.stripe.com/28E28qcH8d3R54I7Mw7wA01?client_reference_id=camberdesk_tier1_monthly';
      if (b2) b2.href = isAnnual ? 'https://buy.stripe.com/fZu3cudLcaVJ9kYgj27wA05?client_reference_id=camberdesk_tier2_annual' : 'https://buy.stripe.com/5kQcN4cH8gg3cxa2sc7wA04?client_reference_id=camberdesk_tier2_monthly';
      if (b3) b3.href = isAnnual ? 'https://buy.stripe.com/fZuaEW22uaVJ8gU4Ak7wA07?client_reference_id=camberdesk_tier3_annual' : 'https://buy.stripe.com/14A9ASaz02pdcxa2sc7wA06?client_reference_id=camberdesk_tier3_monthly';
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
    """

    high_contrast_style = """  <style>
    body { color: #0A0D14; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
    p, li, td, th, label, span { letter-spacing: -0.005em; }
    pre, code, textarea { font-variant-ligatures: none; }
  </style>"""

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
<body class="bg-[#FAF8F5] text-[#0A0D14] font-sans antialiased">
  <!-- Top Telemetry Bar -->
  <div class="bg-[#EAE6DF] border-b border-[#CBD5E1] px-4 py-2 text-xs font-mono font-medium text-[#0A0D14] flex items-center justify-between overflow-x-auto whitespace-nowrap">
    <div class="flex items-center gap-2">
      <span class="inline-block w-2.5 h-2.5 rounded-full bg-[#065F46]"></span>
      <span class="text-[#0A0D14] font-extrabold">LIVE MONITORING: 52 GOVERNMENT &amp; DOT PORTALS ACTIVE</span>
      <span class="text-[#1E3A8A] font-bold">|</span>
      <span class="text-[#111827] font-semibold">{ticker_items}</span>
    </div>
    <div class="hidden lg:flex items-center gap-3 text-[#1E3A8A] font-bold">
      <span>12 LIVE ENDPOINTS</span> &bull; <span>6-FILE .ZIP TAKEOFF COMPILER</span>
    </div>
  </div>

  <!-- Navigation Header -->
  <header class="sticky top-0 z-40 border-b border-[#CBD5E1] bg-white/95 backdrop-blur">
    <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
      {_render_logo_lockup("50-STATE DOT BID-TAB, PREVAILING-WAGE & CSI TAKEOFF ENGINE", "#overview")}
      <nav class="hidden md:flex items-center gap-6 text-sm font-bold">
        <a href="#overview" onclick="switchSpaView('overview')" class="text-[#0A0D14] hover:text-[#1E3A8A]">Overview</a>
        <a href="#lettings" onclick="switchSpaView('lettings')" class="text-[#0A0D14] hover:text-[#1E3A8A]">Live DOT Lettings</a>
        <a href="#apis" onclick="switchSpaView('apis')" class="text-[#0A0D14] hover:text-[#1E3A8A]">API Catalog</a>
        <a href="#checkout" onclick="switchSpaView('checkout')" class="px-4 py-2 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-bold transition">Self-Serve Pricing</a>
      </nav>
    </div>
  </header>

  <!-- VIEW 1: OVERVIEW (#page-overview) -->
  <main id="page-overview" class="max-w-7xl mx-auto px-6 py-12 space-y-16">
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

    <!-- Section: Why Basic Plan Rooms Fail Chief Estimators (#capture-moat) -->
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
    </section>

    <!-- Live Letting Directory (#contract-directory) -->
    <section id="contract-directory" style="overflow-anchor: none;" class="p-6 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div class="text-xs font-mono font-bold text-[#1E3A8A]">// LIVE 52-PORTAL DOT, USACE &amp; PUBLIC WORKS LETTING WIRE</div>
          <h2 class="text-xl font-extrabold text-[#0A0D14]">Upcoming Heavy-Civil, Highway, Bridge &amp; Utility Lettings</h2>
        </div>
        <span id="letting-shown-badge" class="px-3 py-1 rounded bg-[#EAE6DF] border border-[#94A3B8] text-xs font-mono font-bold text-[#0A0D14]">{len(lettings)} PREVIEW LETTINGS SHOWN</span>
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

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div id="checkout-card-tier1" class="p-6 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm space-y-4">
        <div class="text-xs font-mono font-bold text-[#0A0D14]">TIER 1 // CAMBERWIRE PRO</div>
        <div id="price-tier1" class="text-3xl font-extrabold text-[#0A0D14]">$199 / mo</div>
        <p class="text-sm font-medium text-[#111827] leading-relaxed">Real-time 50-State DOT, USACE Civil &amp; Municipal letting alerts + official planholder tracking.</p>
        <a id="btn-checkout-tier1" href="https://buy.stripe.com/28E28qcH8d3R54I7Mw7wA01?client_reference_id=camberdesk_tier1_monthly" class="block text-center py-2.5 rounded-lg bg-[#EAE6DF] hover:bg-[#0A0D14] text-[#0A0D14] hover:text-white border border-[#94A3B8] font-bold text-xs font-mono transition">Activate Tier 1</a>
      </div>

      <div id="checkout-card-tier2" class="p-6 rounded-2xl bg-white border-2 border-[#0A0D14] shadow-md space-y-4">
        <div class="text-xs font-mono font-bold text-[#1E3A8A]">TIER 2 // CAMBERDESK AUTOPILOT (RECOMMENDED)</div>
        <div id="price-tier2" class="text-3xl font-extrabold text-[#0A0D14]">$499 / mo</div>
        <p class="text-sm font-medium text-[#111827] leading-relaxed">Full pre-shredded CSI Divisions 00–48 dossiers, 36-month DOT item bid tabulations, Davis-Bacon WH-347 rates, and API key for all 12 microservices.</p>
        <a id="btn-checkout-tier2" href="https://buy.stripe.com/5kQcN4cH8gg3cxa2sc7wA04?client_reference_id=camberdesk_tier2_monthly" class="block text-center py-2.5 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-bold text-xs font-mono transition">Activate Tier 2 Autopilot</a>
      </div>

      <div id="checkout-card-tier3" class="p-6 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm space-y-4">
        <div class="text-xs font-mono font-bold text-[#065F46]">TIER 3 // 6-FILE .ZIP TAKEOFF COMPILER</div>
        <div id="price-tier3" class="text-3xl font-extrabold text-[#0A0D14]">$1,499 / mo</div>
        <p class="text-sm font-medium text-[#111827] leading-relaxed">Unlimited 1-Click 6-File OpenXML (.DOCX + .XLSX with live formulas) Bid-Tab, Prevailing-Wage &amp; AIA G702/G703 compilations.</p>
        <a id="btn-checkout-tier3" href="https://buy.stripe.com/14A9ASaz02pdcxa2sc7wA06?client_reference_id=camberdesk_tier3_monthly" class="block text-center py-2.5 rounded-lg bg-[#1E3A8A] hover:bg-[#0A0D14] text-white font-bold text-xs font-mono transition">Activate Tier 3 Compiler</a>
      </div>
    </div>

    <div class="p-4 rounded-xl bg-white border border-[#CBD5E1] text-xs font-mono font-semibold text-[#0A0D14]">
      All 12 individual CamberDesk microservices are also available on RapidAPI and via <code class="text-[#1E3A8A] font-bold">@camberdesk/mcp-server</code>.
    </div>
  </section>

  <footer class="border-t border-[#CBD5E1] bg-[#EAE6DF] py-8 mt-16">
    <div class="max-w-7xl mx-auto px-6 flex flex-wrap items-center justify-between gap-4 text-xs font-mono font-bold text-[#0A0D14]">
      <div>ALL 52 FEDERAL USACE &amp; 50-STATE DOT PORTAL MONITORS ACTIVE</div>
      <div>&copy; 2026 CamberDesk Inc. &bull; Stateless Preconstruction &amp; DOT Bid-Tab DaaS</div>
    </div>
  </footer>

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
<body class="bg-[#FAF8F5] text-[#0A0D14] font-sans antialiased">
  <header class="sticky top-0 z-40 border-b border-[#CBD5E1] bg-white/95 backdrop-blur">
    <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
      {_render_logo_lockup("12 STATELESS PRECONSTRUCTION REST & MCP MICROSERVICES", "index.html")}
      <nav class="hidden md:flex items-center gap-6 text-sm font-bold">
        <a href="index.html" class="text-[#0A0D14] hover:text-[#1E3A8A]">Overview</a>
        <a href="lettings/index.html" class="text-[#0A0D14] hover:text-[#1E3A8A]">Live DOT Lettings</a>
        <a href="apis.html" class="text-[#1E3A8A] font-extrabold">API Catalog</a>
        <a href="index.html#checkout" class="px-4 py-2 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-bold transition">Self-Serve Pricing</a>
      </nav>
    </div>
  </header>
  <main class="max-w-7xl mx-auto px-6 py-12">
    {api_catalog_block}
  </main>
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
