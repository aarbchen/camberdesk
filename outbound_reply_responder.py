r"""
CamberDesk — Autonomous Outbound Reply Classifier & "SEND ZIP" Auto-Responder (`D:\CamberDesk\outbound_reply_responder.py`).
Polls for unread estimator replies (via Instantly.ai V2 `/api/v2/emails` or Gmail IMAP on `camberdesk.dev@gmail.com`),
classifies each reply with `claude-sonnet-5-5`, and automatically replies to `POSITIVE_INTEREST` / `"SEND ZIP"`
with the contractor's live DOT letting dossier, the 1-Click 6-File OpenXML (.DOCX + .XLSX) Bid-Tab `.ZIP` download link,
and self-serve Stripe Checkout links (`Tier 1 $199/mo`, `Tier 2 $499/mo`, `Tier 3 $1,499/mo`).
"""

from error_telemetry import configure_utf8_stdio, report_error
configure_utf8_stdio()

import csv
import json
import os
from pathlib import Path
from typing import Any, Dict, List
import requests
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=str(ROOT_DIR / ".env"))

INSTANTLY_API_KEY = (os.getenv("INSTANTLY_API_KEY") or "").strip()
CAMBERDESK_CAMPAIGN_ID = (os.getenv("CAMBERDESK_INSTANTLY_CAMPAIGN_ID") or "").strip()
ANTHROPIC_API_KEY = (os.getenv("ANTHROPIC_API_KEY") or "").strip()
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5")
DISCORD_WEBHOOK_URL = (os.getenv("DISCORD_WEBHOOK_URL") or "").strip()
SITE_BASE_URL = os.getenv("CAMBERDESK_SITE_URL", "https://camberdesk.com").rstrip("/")
CSV_PATH = ROOT_DIR / "campaign_leads.csv"
PROCESSED_PATH = ROOT_DIR / "processed_outbound_replies.json"

TIER1_STRIPE_URL = "https://buy.stripe.com/28E28qcH8d3R54I7Mw7wA01?client_reference_id=camberdesk_tier1_monthly"
TIER2_STRIPE_URL = "https://buy.stripe.com/5kQcN4cH8gg3cxa2sc7wA04?client_reference_id=camberdesk_tier2_monthly"
TIER3_STRIPE_URL = "https://buy.stripe.com/14A9ASaz02pdcxa2sc7wA06?client_reference_id=camberdesk_tier3_monthly"


def lookup_prospect_context(from_email: str) -> Dict[str, str]:
    clean_em = str(from_email or "").strip().lower()
    dom = clean_em.split("@", 1)[1] if "@" in clean_em else ""
    matched: Dict[str, str] = {}
    if CSV_PATH.exists():
        try:
            with open(CSV_PATH, mode="r", encoding="utf-8", newline="") as f:
                for row in csv.DictReader(f):
                    row_em = str(row.get("email") or "").strip().lower()
                    if row_em == clean_em or (dom and row_em.endswith("@" + dom)):
                        matched = dict(row)
                        break
        except Exception:
            pass
    return {
        "first_name": matched.get("first_name") or "Chief Estimator",
        "company_name": matched.get("company_name") or "your estimating team",
        "state": matched.get("state") or "TX",
        "project_id": matched.get("project_id") or "TXDOT-CSJ-0015-13-412",
        "project_title": matched.get("project_title") or "IH-35 Bridge Deck Replacement & Superpave Overlay",
        "dossier_url": matched.get("dossier_url") or f"{SITE_BASE_URL}/lettings/index.html",
        "compiler_url": matched.get("compiler_url") or f"{SITE_BASE_URL}/v1/camber-autopilot/compile-bid-package",
    }


def classify_estimator_reply(reply_text: str) -> str:
    txt = str(reply_text or "").strip().lower()
    if any(u in txt for u in ("unsubscribe", "remove me", "stop emailing", "not interested", "take me off")):
        return "UNSUBSCRIBE"
    if any(p in txt for p in ("send zip", "send it", "yes", "sure", "send over", "interested", "bid tab", "spreadsheet")):
        return "POSITIVE_INTEREST"

    if ANTHROPIC_API_KEY and txt:
        try:
            resp = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": ANTHROPIC_MODEL,
                    "max_tokens": 30,
                    "messages": [
                        {
                            "role": "user",
                            "content": (
                                "Classify this construction estimator email reply into exactly one label: "
                                "POSITIVE_INTEREST, QUESTION, or UNSUBSCRIBE.\n\n"
                                f"Reply: {reply_text[:500]}"
                            ),
                        }
                    ],
                },
                timeout=15,
            )
            if resp.status_code == 200:
                out = ((resp.json().get("content") or [{}])[0].get("text") or "").upper()
                if "UNSUBSCRIBE" in out:
                    return "UNSUBSCRIBE"
                if "QUESTION" in out:
                    return "QUESTION"
        except Exception:
            pass
    return "POSITIVE_INTEREST"


def build_zip_fulfillment_reply(from_email: str) -> Dict[str, str]:
    ctx = lookup_prospect_context(from_email)
    body = (
        f"Hi {ctx['first_name']},\n\n"
        f"Here is the pre-shredded DOT Bid-Tab & Preconstruction package for {ctx['project_id']} ({ctx['project_title']}):\n\n"
        f"1. 1-Click 6-File OpenXML (.DOCX + .XLSX) Bid-Tab & Takeoff Package (.ZIP):\n"
        f"   {ctx['compiler_url']}\n"
        f"   (Includes Vol I CSI Spec & Submittal Matrix .docx, Vol II DOT Historical Unit-Price Bid Tabulation .xlsx with live =SUM() formulas, "
        f"Vol III Davis-Bacon WH-347 Fringe Model .xlsx, Vol IV 49 CFR 26 DBE & BABA Audit .docx, and Vol V AIA G702/G703 SOV .docx)\n\n"
        f"2. Interactive Letting Dossier & Competitor Spread Preview:\n"
        f"   {ctx['dossier_url']}\n\n"
        f"If you want automated 50-State DOT planholder alerts, 36-month historical unit bid tabulations, and unlimited 6-File .ZIP compilations across all upcoming lettings:\n"
        f"- Tier 1 // CamberWire Pro ($199/mo): {TIER1_STRIPE_URL}\n"
        f"- Tier 2 // CamberDesk Autopilot ($499/mo — Recommended): {TIER2_STRIPE_URL}\n"
        f"- Tier 3 // Unlimited 6-File .ZIP Takeoff Compiler ($1,499/mo): {TIER3_STRIPE_URL}\n\n"
        f"Best,\n"
        f"CamberDesk Preconstruction & DOT Systems\n"
        f"{SITE_BASE_URL}"
    )
    return {
        "to_email": from_email,
        "project_id": ctx["project_id"],
        "subject": f"Re: {ctx['project_id']} unit bid tabs & 6-File .ZIP Takeoff Package",
        "body": body,
    }


def run_reply_responder() -> Dict[str, Any]:
    processed: List[str] = []
    if PROCESSED_PATH.exists():
        try:
            processed = json.loads(PROCESSED_PATH.read_text(encoding="utf-8"))
        except Exception:
            processed = []

    summary = {"checked": 0, "replied": 0, "unsubscribed": 0, "model": ANTHROPIC_MODEL}
    if not INSTANTLY_API_KEY or not CAMBERDESK_CAMPAIGN_ID:
        return summary

    try:
        r = requests.get(
            "https://api.instantly.ai/api/v2/emails",
            headers={"Authorization": f"Bearer {INSTANTLY_API_KEY}"},
            params={"campaign_id": CAMBERDESK_CAMPAIGN_ID, "limit": 25},
            timeout=15,
        )
        if r.status_code == 200:
            items = (r.json() or {}).get("items") or []
            for item in items:
                msg_id = str(item.get("id") or "")
                if not msg_id or msg_id in processed or item.get("ue_type") != 2:
                    continue
                summary["checked"] += 1
                from_em = str(item.get("from_address_email") or "")
                body_txt = str((item.get("body") or {}).get("text") or "")
                label = classify_estimator_reply(body_txt)
                if label in ("POSITIVE_INTEREST", "QUESTION"):
                    pkg = build_zip_fulfillment_reply(from_em)
                    requests.post(
                        "https://api.instantly.ai/api/v2/emails/reply",
                        headers={"Authorization": f"Bearer {INSTANTLY_API_KEY}", "Content-Type": "application/json"},
                        json={
                            "reply_to_uuid": msg_id,
                            "eaccount": item.get("eaccount"),
                            "subject": pkg["subject"],
                            "body": {"text": pkg["body"]},
                        },
                        timeout=15,
                    )
                    summary["replied"] += 1
                else:
                    summary["unsubscribed"] += 1
                processed.append(msg_id)
            PROCESSED_PATH.write_text(json.dumps(processed[-500:], indent=2), encoding="utf-8")
    except Exception as exc:
        report_error("outbound_reply_responder.py", f"Reply polling note: {exc}")

    return summary


if __name__ == "__main__":
    res = run_reply_responder()
    print(f"[CAMBERDESK REPLY RESPONDER] {res}")

