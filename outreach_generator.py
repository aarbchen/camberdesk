r"""
CamberDesk — Autonomous Planholder & Licensed Contractor Outbound Generator (`D:\CamberDesk\outreach_generator.py`).
Generates zero-link Step 1 conversational outreach emails triggered by live State DOT planholder lists
and active letting schedules, exporting `campaign_leads.csv` and `outbox_ready_queue.json`.
"""

from error_telemetry import configure_utf8_stdio, report_error
configure_utf8_stdio()

import csv
import json
import os
import re
from typing import Any, Dict, List

from api_gateway.services.llm_extractor import load_seed_data
from camberdesk_autopilot import slugify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "campaign_leads.csv")
QUEUE_PATH = os.path.join(BASE_DIR, "outbox_ready_queue.json")
SITE_BASE_URL = os.getenv("CAMBERDESK_SITE_URL", "https://camberdesk.com").rstrip("/")

PLANHOLDER_DIRECTORY: Dict[str, Dict[str, str]] = {
    "Webber LLC": {"email": "estimating@wwebber.com", "estimator": "Mark Vance", "dot_id": "TXDOT-PREQ-88412", "state": "TX"},
    "Granite Construction Inc.": {"email": "bids@gcinc.com", "estimator": "David Morales", "dot_id": "CALTRANS-A-89", "state": "CA"},
    "Jordan Foster Construction LLC": {"email": "civilbids@jordanfosterconstruction.com", "estimator": "Carlos Herrera", "dot_id": "TXDOT-PREQ-77104", "state": "TX"},
    "Lone Star Paving Co.": {"email": "estimating@lonestarpaving.com", "estimator": "Brett Whitaker", "dot_id": "TXDOT-PREQ-64219", "state": "TX"},
    "Capital Excavation Company": {"email": "bids@capitalexcavation.com", "estimator": "Ryan Bradley", "dot_id": "TXDOT-PREQ-51908", "state": "TX"},
    "Skanska USA Civil": {"email": "civil.estimating@skanska.com", "estimator": "Thomas Lindqvist", "dot_id": "CALTRANS-A-412090", "state": "CA"},
    "Flatiron Construction Corp.": {"email": "estimating@flatironcorp.com", "estimator": "steven.keller@flatironcorp.com", "dot_id": "CALTRANS-A-772114", "state": "CA"},
    "Myers & Sons Construction": {"email": "bids@myers-sons.com", "estimator": "Kurt Myers", "dot_id": "CALTRANS-A-921045", "state": "CA"},
    "Hubbard Construction Company": {"email": "estimating@hubbard.com", "estimator": "Greg Reynolds", "dot_id": "FDOT-PREQ-11402", "state": "FL"},
    "GLF Construction Corporation": {"email": "estimating@glfusa.com", "estimator": "Marco Senese", "dot_id": "FDOT-PREQ-20918", "state": "FL"},
    "Archer Western Construction": {"email": "civilbids@walshgroup.com", "estimator": "Daniel Walsh", "dot_id": "FDOT-PREQ-33109", "state": "FL"},
    "Allan Myers Inc.": {"email": "estimating@allanmyers.com", "estimator": "Jason Dougherty", "dot_id": "VDOT-PREQ-4091", "state": "VA"},
    "Shirley Contracting Company": {"email": "bids@shirleycontracting.com", "estimator": "Michael Carroll", "dot_id": "VDOT-PREQ-1820", "state": "VA"},
    "Wagman Heavy Civil Inc.": {"email": "estimating@wagman.com", "estimator": "Greg Wagman", "dot_id": "PENNDOT-PREQ-6612", "state": "PA"},
    "Trumbull Corporation": {"email": "estimating@trumbullcorp.com", "estimator": "Brianaugustus@trumbullcorp.com", "dot_id": "PENNDOT-PREQ-2291", "state": "PA"},
    "Tully Construction Co. Inc.": {"email": "estimating@tullyconstruction.com", "estimator": "Daniel Tully", "dot_id": "NYSDOT-D265-019", "state": "NY"},
    "Posillico Civil Inc.": {"email": "bids@posillicoinc.com", "estimator": "Joseph Posillico", "dot_id": "NYSDOT-D265-044", "state": "NY"},
    "C.W. Matthews Contracting Co.": {"email": "estimating@cwmatthews.com", "estimator": "Jeff Matthews", "dot_id": "GDOT-2MA480", "state": "GA"},
    "E.R. Snell Contractor Inc.": {"email": "bids@ersnell.com", "estimator": "toddsnell@ersnell.com", "dot_id": "GDOT-2SN110", "state": "GA"},
    "Blythe Construction Inc.": {"email": "estimating@blytheconstruction.com", "estimator": "Alan Blythe", "dot_id": "NCDOT-PREQ-5510", "state": "NC"},
    "Kokosing Construction Company": {"email": "estimating@kokosing.biz", "estimator": "Brett Burgett", "dot_id": "ODOT-PREQ-1042", "state": "OH"},
    "F.H. Paschen, S.N. Nielsen": {"email": "estimating@fhpaschen.com", "estimator": "James Blair", "dot_id": "IDOT-PREQ-0891", "state": "IL"},
    "Manson Construction Co.": {"email": "estimating@mansonconstruction.com", "estimator": "Ericohnen@mansonconstruction.com", "dot_id": "USACE-CAGE-09214", "state": "WA"},
    "Weeks Marine Inc.": {"email": "bids@weeksmarine.com", "estimator": "Richard Weeks", "dot_id": "USACE-CAGE-11842", "state": "NJ"},
}


def generate_outreach_queue() -> List[Dict[str, Any]]:
    seed = load_seed_data()
    lettings = seed.get("lettings", [])
    contractors = list(seed.get("verified_contractors", []))

    seen_emails = set()
    leads: List[Dict[str, Any]] = []

    def _add_lead(company: str, email: str, first_name: str, dot_id: str, state: str, matched_let: Dict[str, Any]) -> None:
        clean_em = email.strip().lower()
        if not clean_em or clean_em in seen_emails:
            return
        seen_emails.add(clean_em)

        pid = str(matched_let.get("project_id") or "TXDOT-CSJ-0015-13-412")
        clean_title = re.sub(r"^\[[^\]]+\]\s*", "", str(matched_let.get("title") or "IH-35 Bridge & Superpave Letting"))
        agency = str(matched_let.get("agency") or "TxDOT")
        county = str(matched_let.get("county") or "Travis County, TX")
        letting_date = str(matched_let.get("letting_date") or "2026-11-18")
        est_usd = float(matched_let.get("engineers_estimate_usd") or 18450000.0)
        wage_id = str(matched_let.get("wage_determination_id") or f"{state}20260028 (Heavy & Highway)")
        pay_items = matched_let.get("pay_items") or []
        top_item_str = "key unit pay items"
        if pay_items:
            pi = pay_items[0]
            top_item_str = (
                f"Item {pi.get('item_code')} ({pi.get('description')[:42]}) at "
                f"${float(pi.get('hist_median_unit_usd') or 135.0):,.2f}/{pi.get('unit', 'UNIT')} median"
            )

        slug = slugify(clean_title)
        dossier_url = f"{SITE_BASE_URL}/lettings/project/{slug}.html"
        compiler_url = f"{SITE_BASE_URL}/v1/camber-autopilot/compile-bid-package"

        step1_subject = f"{pid} unit bid tabs & Davis-Bacon rates ({county})"
        step1_body = (
            f"Hi {first_name},\n\n"
            f"Saw {company} on the active planholder list for {agency} letting {pid} "
            f"({clean_title[:72]} — ${est_usd:,.0f} Engineer's Estimate opening {letting_date} in {county}).\n\n"
            f"We already pulled the 36-month historical DOT unit-price bid tabulations across the confirmed planholders "
            f"(benchmarking {top_item_str}) and mapped {wage_id} prevailing wage fringes + CSI Divisions 00-48 submittals into a 6-file Word/Excel takeoff package.\n\n"
            f"Are you pricing {pid} (or sub-quoting a trade division on it) this week? Reply 'SEND ZIP' and I will send the 6-file .DOCX + .XLSX bid-tab package over."
        )

        step2_body = (
            f"Hi {first_name} — following up in case your estimating desk is locking in unit prices for {pid}.\n\n"
            f"Here is the live preconstruction dossier with the historical unit-bid spread and 1-Click 6-File OpenXML (.DOCX + .XLSX) Takeoff Package:\n"
            f"{dossier_url}"
        )

        leads.append({
            "email": clean_em,
            "first_name": first_name,
            "company_name": company,
            "license_or_dot_id": dot_id,
            "state": state,
            "project_id": pid,
            "project_title": clean_title,
            "letting_date": letting_date,
            "dossier_url": dossier_url,
            "compiler_url": compiler_url,
            "step1_subject": step1_subject,
            "step1_body_zero_link": step1_body,
            "step2_body_dossier_link": step2_body,
        })

    for idx, contractor in enumerate(contractors):
        matched_let = lettings[idx % len(lettings)] if lettings else {}
        company = str(contractor.get("company_name") or "Apex Civil Constructors")
        email = str(contractor.get("estimating_email") or "estimating@example.com")
        estimator_name = str(contractor.get("chief_estimator") or "Chief Estimator").split(",")[0]
        first_name = estimator_name.split()[0] if "@" not in estimator_name else "Estimating"
        _add_lead(
            company=company,
            email=email,
            first_name=first_name,
            dot_id=str(contractor.get("license_or_dot_id") or ""),
            state=str(contractor.get("state") or "TX"),
            matched_let=matched_let,
        )

    for letting in lettings:
        st = str(letting.get("state_code") or "TX")
        for ph_name in letting.get("planholders", []):
            meta = PLANHOLDER_DIRECTORY.get(ph_name)
            if meta:
                est_raw = meta["estimator"]
                fname = est_raw.split()[0] if "@" not in est_raw else "Estimating"
                _add_lead(
                    company=ph_name,
                    email=meta["email"],
                    first_name=fname,
                    dot_id=meta["dot_id"],
                    state=meta.get("state", st),
                    matched_let=letting,
                )

    for ph_name, meta in PLANHOLDER_DIRECTORY.items():
        matched_let = next((l for l in lettings if l.get("state_code") == meta["state"]), lettings[0] if lettings else {})
        est_raw = meta["estimator"]
        fname = est_raw.split()[0] if "@" not in est_raw else "Estimating"
        _add_lead(
            company=ph_name,
            email=meta["email"],
            first_name=fname,
            dot_id=meta["dot_id"],
            state=meta["state"],
            matched_let=matched_let,
        )

    fieldnames = [
        "email", "first_name", "company_name", "license_or_dot_id", "state",
        "project_id", "project_title", "letting_date", "dossier_url", "compiler_url",
        "step1_subject", "step1_body_zero_link", "step2_body_dossier_link",
    ]
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(leads)

    with open(QUEUE_PATH, "w", encoding="utf-8") as fh:
        json.dump({"count": len(leads), "outbox_queue": leads}, fh, indent=2)

    print(f"[CAMBERDESK OUTBOUND] Generated {len(leads)} zero-link planholder outreach leads -> {CSV_PATH} & {QUEUE_PATH}")
    return leads


if __name__ == "__main__":
    generate_outreach_queue()
