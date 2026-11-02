r"""
CamberDesk — Autonomous Outbound Reply Classifier, "SEND ZIP" Auto-Responder & 48h/96h Warm Follow-Up Engine
(`D:\CamberDesk\outbound_reply_responder.py`).
Polls for unread estimator replies (via Instantly.ai V2 `/api/v2/emails` with `email_type="received"`),
classifies each reply with `claude-sonnet-5-5` (after stripping quoted email history via `_strip_quoted_thread()`),
automatically answers specific estimator questions or `"SEND ZIP"` requests with the contractor's live DOT letting dossier,
the 1-Click 6-File OpenXML (.DOCX + .XLSX) Bid-Tab `.ZIP` download link, and pre-filled `?co=&state=&email=`
self-serve Stripe Checkout deep-links (`Tier 1 $199/mo`, `Tier 2 $499/mo`, `Tier 3 $1,499/mo`),
dispatches automated 48h and 96h post-`.ZIP` follow-up nudges via `warm_zip_followup_ledger.json`,
and permanently purges/archives any `UNSUBSCRIBE` requests.
"""

from error_telemetry import configure_utf8_stdio, report_error
configure_utf8_stdio()

import csv
import json
import os
import time
import urllib.parse
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
CAMBERDESK_DISCORD_WEBHOOK_URL = (os.getenv("CAMBERDESK_DISCORD_WEBHOOK_URL") or "").strip()
SITE_BASE_URL = os.getenv("CAMBERDESK_SITE_URL", "https://camberdesk.com").rstrip("/")
CSV_PATH = ROOT_DIR / "campaign_leads.csv"
MLOT_CSV_PATH = ROOT_DIR / "mlot_sniper_leads.csv"
PROCESSED_PATH = ROOT_DIR / "processed_outbound_replies.json"
ARCHIVE_PATH = ROOT_DIR / "completed_outreach_archive.json"
WARM_FOLLOWUP_PATH = ROOT_DIR / "warm_zip_followup_ledger.json"
TREASURY_LEDGER_PATH = ROOT_DIR / "reinvestment_treasury_ledger.json"

TIER1_STRIPE_URL = "https://buy.stripe.com/00wbJ08qS0h5cxa2sc7wA0a"
TIER2_STRIPE_URL = "https://buy.stripe.com/5kQ00i9uW5BpgNq6Is7wA0c"
TIER3_STRIPE_URL = "https://buy.stripe.com/cNidR8dLc2pdfJmgj27wA0e"
TIER4_STRIPE_URL = "https://buy.stripe.com/fZueVcePg5Bp2WA7Mw7wA0g"


def _append_prefilled_email(stripe_url: str, email: str) -> str:
    clean_em = str(email or "").strip()
    if not clean_em or "@" not in clean_em:
        return stripe_url
    sep = "&" if "?" in stripe_url else "?"
    return f"{stripe_url}{sep}prefilled_email={urllib.parse.quote(clean_em)}"


def _build_prefilled_site_url(base_path: str, company_name: str, state: str, email: str, hash_frag: str = "") -> str:
    q: Dict[str, str] = {}
    if company_name and company_name.lower() not in ("your estimating team", "chief estimator"):
        q["co"] = company_name
    if state:
        q["state"] = state
    if email and "@" in email:
        q["email"] = email
    qs = f"?{urllib.parse.urlencode(q)}" if q else ""
    frag = f"#{hash_frag.lstrip('#')}" if hash_frag else ""
    return f"{SITE_BASE_URL}{base_path}{qs}{frag}"


def lookup_prospect_context(from_email: str) -> Dict[str, str]:
    clean_em = str(from_email or "").strip().lower()
    dom = clean_em.split("@", 1)[1] if "@" in clean_em else ""
    matched: Dict[str, str] = {}
    for csv_candidate in (CSV_PATH, MLOT_CSV_PATH):
        if csv_candidate.exists() and not matched:
            try:
                with open(csv_candidate, mode="r", encoding="utf-8", newline="") as f:
                    for row in csv.DictReader(f):
                        row_em = str(row.get("email") or "").strip().lower()
                        if row_em == clean_em or (dom and row_em.endswith("@" + dom)):
                            matched = dict(row)
                            break
            except Exception:
                pass
    verified_json = ROOT_DIR / "verified_public_dot_contacts.json"
    if not matched and verified_json.exists():
        try:
            for item in json.loads(verified_json.read_text(encoding="utf-8")) or []:
                row_em = str(item.get("email") or "").strip().lower()
                if row_em == clean_em or (dom and row_em.endswith("@" + dom)):
                    matched = dict(item)
                    break
        except Exception:
            pass
    fallback_co = dom.split(".")[0].replace("-", " ").title() if dom else "your estimating team"
    res_state = matched.get("state") or "TX"
    res_pid = matched.get("project_id") or "TXDOT-CSJ-0015-13-412"
    comp_name = matched.get("company_name") or fallback_co
    raw_compiler = matched.get("compiler_url") or ""
    if not raw_compiler or "project_id=" not in raw_compiler or "api.camberdesk.com" in raw_compiler:
        raw_compiler = f"https://camberdesk.com/v1/camber-autopilot/compile-bid-package?project_id={res_pid}&state_code={res_state}&format=binary"
    raw_dossier = matched.get("dossier_url") or _build_prefilled_site_url("/", comp_name, res_state, clean_em, "lettings")
    if "?" not in raw_dossier and (comp_name or clean_em):
        q_params = urllib.parse.urlencode({"co": comp_name, "state": res_state, "email": clean_em})
        if "#" in raw_dossier:
            base_part, hash_part = raw_dossier.split("#", 1)
            raw_dossier = f"{base_part}?{q_params}#{hash_part}"
        else:
            raw_dossier = f"{raw_dossier}?{q_params}"
    return {
        "first_name": matched.get("first_name") or "Chief Estimator",
        "company_name": comp_name,
        "state": res_state,
        "project_id": res_pid,
        "project_title": matched.get("project_title") or "IH-35 Bridge Deck Replacement & Superpave Overlay",
        "dossier_url": raw_dossier,
        "compiler_url": raw_compiler,
        "tier1_stripe_url": _append_prefilled_email(TIER1_STRIPE_URL, clean_em),
        "tier2_stripe_url": _append_prefilled_email(TIER2_STRIPE_URL, clean_em),
        "tier3_stripe_url": _append_prefilled_email(TIER3_STRIPE_URL, clean_em),
        "workspace_checkout_url": _build_prefilled_site_url("/", comp_name, res_state, clean_em, "checkout"),
    }


def _strip_quoted_thread(raw_text: str) -> str:
    """Strip quoted email history ('On ... wrote:', '> ...', '-----Original Message-----') before classifying."""
    lines: List[str] = []
    for ln in str(raw_text or "").splitlines():
        s = ln.strip()
        if s.startswith(">"):
            continue
        if s.lower().startswith("on ") and s.lower().endswith("wrote:"):
            break
        if s.startswith("-----Original Message-----") or s.startswith("From: "):
            break
        lines.append(ln)
    cleaned = "\n".join(lines).strip()
    return cleaned if cleaned else str(raw_text or "").strip()


def classify_estimator_reply(reply_text: str, subject: str = "", from_email: str = "") -> str:
    stripped = _strip_quoted_thread(reply_text)
    txt = stripped.lower()
    subj_low = str(subject or "").lower()
    em_low = str(from_email or "").lower()
    if (
        em_low.startswith(("mailer-daemon@", "postmaster@", "noreply-dmarc@", "bounces@"))
        or subj_low.startswith(("undeliverable:", "delivery status notification", "returned mail:", "mail delivery failed", "failure notice"))
        or any(
            b_p in txt
            for b_p in (
                "delivery to the following recipient failed",
                "550 5.1.1",
                "address not found",
                "user unknown",
                "mailbox unavailable",
            )
        )
    ):
        return "BOUNCE"
    if (
        subj_low.startswith(("automatic reply:", "auto-reply:", "out of office:", "out of the office:"))
        or any(
            ooo_p in txt
            for ooo_p in (
                "out of the office",
                "out of office",
                "currently away from",
                "limited access to email",
                "on vacation until",
                "on parental leave",
                "on medical leave",
                "away from my desk",
                "auto-reply",
                "automatic reply",
            )
        )
    ):
        return "OUT_OF_OFFICE"
    negated_unsub = any(
        neg in txt
        for neg in (
            "don't unsubscribe", "do not unsubscribe", "dont unsubscribe",
            "don't remove me", "do not remove me", "dont remove me",
            "don't take me off", "do not take me off", "dont take me off",
            "don't stop emailing", "do not stop emailing",
        )
    )
    if not negated_unsub and any(u in txt for u in ("unsubscribe", "remove me", "stop emailing", "not interested", "take me off", "no thanks", "off your list")):
        return "UNSUBSCRIBE"
    if "?" in stripped and not any(p in txt for p in ("send zip", "send it", "send over")):
        return "QUESTION"
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
                                f"Reply: {stripped[:500]}"
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


def build_zip_fulfillment_reply(from_email: str, reply_text: str = "", label: str = "POSITIVE_INTEREST") -> Dict[str, str]:
    ctx = lookup_prospect_context(from_email)
    custom_answer_block = ""
    stripped_q = _strip_quoted_thread(reply_text)
    if label == "QUESTION" and stripped_q and ANTHROPIC_API_KEY:
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
                    "max_tokens": 220,
                    "system": (
                        "You are Aaron at the CamberDesk Preconstruction & DOT Desk. "
                        "Directly answer the estimator's question in 2-3 concise plain-text sentences (no markdown asterisks or hashtags). "
                        "Facts: CamberDesk monitors all 50 U.S. State DOT portals + Federal USACE Civil Works + Municipal Public Works (52 portals total), "
                        "benchmarks 36 months of historical winning unit-price bid tabulations (1.42M+ pay items), calculates county-specific Davis-Bacon WH-347 wages, "
                        "and compiles 6-File OpenXML (.DOCX + .XLSX with live =ROUND(D6*G6,2) and =SUM() Excel formulas) bid packages compatible with HCSS HeavyBid, Procore, and Excel."
                    ),
                    "messages": [{"role": "user", "content": f"Estimator question: {stripped_q[:500]}"}],
                },
                timeout=15,
            )
            if resp.status_code == 200:
                ans = ((resp.json().get("content") or [{}])[0].get("text") or "").strip().replace("**", "")
                if len(ans) >= 15:
                    custom_answer_block = f"{ans}\n\n"
        except Exception:
            pass

    body = (
        f"Hi {ctx['first_name']},\n\n"
        f"{custom_answer_block}"
        f"Here is the pre-shredded DOT Bid-Tab & Preconstruction package for {ctx['project_id']} ({ctx['project_title']}):\n\n"
        f"1. 1-Click 6-File OpenXML (.DOCX + .XLSX) Bid-Tab & Takeoff Package (.ZIP):\n"
        f"   {ctx['compiler_url']}\n"
        f"   (Includes Vol I CSI Spec & Submittal Matrix .docx, Vol II DOT Historical Unit-Price Bid Tabulation .xlsx with live =SUM() formulas, "
        f"Vol III Davis-Bacon WH-347 Fringe Model .xlsx, Vol IV 49 CFR 26 DBE & BABA Audit .docx, and Vol V AIA G702/G703 SOV .docx)\n\n"
        f"2. Interactive Letting Dossier & Competitor Spread Preview (Pre-Configured for {ctx['company_name']}):\n"
        f"   {ctx['dossier_url']}\n\n"
        f"If you want automated 50-State DOT planholder alerts, 36-month historical unit bid tabulations, and unlimited 6-File .ZIP compilations across all upcoming lettings:\n"
        f"- Tier 1 // CamberWire Pro ($199/mo): {ctx['tier1_stripe_url']}\n"
        f"- Tier 2 // CamberDesk Autopilot ($499/mo — Recommended): {ctx['tier2_stripe_url']}\n"
        f"- Tier 3 // Unlimited 6-File .ZIP Takeoff Compiler ($1,499/mo): {ctx['tier3_stripe_url']}\n\n"
        f"Best,\n"
        f"Aaron // CamberDesk Preconstruction & DOT Systems\n"
        f"{ctx['workspace_checkout_url']}"
    )
    return {
        "to_email": from_email,
        "project_id": ctx["project_id"],
        "subject": f"Re: {ctx['project_id']} unit bid tabs & 6-File .ZIP Takeoff Package",
        "body": body,
        "context": ctx,
    }


def _is_converted_or_unsubscribed(email: str) -> bool:
    clean = str(email or "").strip().lower()
    if not clean:
        return True
    if ARCHIVE_PATH.exists():
        try:
            raw = json.loads(ARCHIVE_PATH.read_text(encoding="utf-8"))
            if isinstance(raw, list) and clean in {str(x).strip().lower() for x in raw if x}:
                return True
        except Exception:
            pass
    if TREASURY_LEDGER_PATH.exists():
        try:
            t_data = json.loads(TREASURY_LEDGER_PATH.read_text(encoding="utf-8")) or {}
            for ev in (t_data.get("payment_events") or []):
                if str(ev.get("customer_email") or "").strip().lower() == clean:
                    return True
        except Exception:
            pass
    return False


def _record_warm_zip_delivery(from_email: str, eaccount: str, msg_id: str, subject: str, ctx: Dict[str, str]) -> None:
    clean_em = str(from_email or "").strip().lower()
    if not clean_em or "@" not in clean_em:
        return
    entries: Dict[str, Any] = {}
    if WARM_FOLLOWUP_PATH.exists():
        try:
            loaded = json.loads(WARM_FOLLOWUP_PATH.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                entries = loaded
        except Exception:
            entries = {}
    if clean_em not in entries:
        entries[clean_em] = {
            "email": clean_em,
            "eaccount": eaccount,
            "reply_to_uuid": msg_id,
            "subject": subject,
            "first_name": ctx.get("first_name") or "Chief Estimator",
            "company_name": ctx.get("company_name") or "your estimating team",
            "state": ctx.get("state") or "TX",
            "project_id": ctx.get("project_id") or "TXDOT-CSJ-0015-13-412",
            "compiler_url": ctx.get("compiler_url") or "",
            "dossier_url": ctx.get("dossier_url") or "",
            "tier2_stripe_url": ctx.get("tier2_stripe_url") or TIER2_STRIPE_URL,
            "workspace_checkout_url": ctx.get("workspace_checkout_url") or f"{SITE_BASE_URL}/#checkout",
            "sent_at_epoch": time.time(),
            "nudge_48h_sent": False,
            "nudge_96h_sent": False,
        }
        try:
            WARM_FOLLOWUP_PATH.write_text(json.dumps(entries, indent=2), encoding="utf-8")
        except Exception:
            pass


def _process_warm_zip_followups() -> int:
    if not WARM_FOLLOWUP_PATH.exists() or not INSTANTLY_API_KEY:
        return 0
    try:
        entries = json.loads(WARM_FOLLOWUP_PATH.read_text(encoding="utf-8"))
        if not isinstance(entries, dict):
            return 0
    except Exception:
        return 0

    now = time.time()
    nudges_sent = 0
    dirty = False
    headers = {"Authorization": f"Bearer {INSTANTLY_API_KEY}", "Content-Type": "application/json"}

    for em, info in list(entries.items()):
        if not isinstance(info, dict) or _is_converted_or_unsubscribed(em):
            continue
        sent_at = float(info.get("sent_at_epoch") or 0)
        if sent_at <= 0:
            continue
        elapsed_hrs = (now - sent_at) / 3600.0
        msg_id = str(info.get("reply_to_uuid") or "").strip()
        eaccount = str(info.get("eaccount") or "").strip()
        if not msg_id or not eaccount or "camberdesk" not in eaccount.lower():
            continue
        fname = info.get("first_name") or "Chief Estimator"
        pid = info.get("project_id") or "TXDOT-CSJ-0015-13-412"
        comp = info.get("company_name") or "your estimating team"
        t2_url = info.get("tier2_stripe_url") or TIER2_STRIPE_URL
        ws_url = info.get("workspace_checkout_url") or f"{SITE_BASE_URL}/#checkout"
        subj = str(info.get("subject") or f"Re: {pid} unit bid tabs & 6-File .ZIP Takeoff Package")
        if not subj.lower().startswith("re:"):
            subj = f"Re: {subj}"

        if elapsed_hrs >= 48.0 and not info.get("nudge_48h_sent"):
            body_48 = (
                f"Hi {fname},\n\n"
                f"Quick check-in on the 6-file OpenXML (.DOCX + .XLSX) DOT Bid-Tab & Takeoff package I sent over for {pid} — "
                f"did the live =ROUND(D6*G6,2) unit-price formulas in Volume II and the Davis-Bacon WH-347 wage schedule in Volume III open cleanly in Excel/HeavyBid for {comp}?\n\n"
                f"If your estimating desk wants automated 50-State DOT planholder alerts, 36-month winning low unit bid tabulations, and unlimited 6-File .ZIP compilations:\n"
                f"- Instant Tier 2 Autopilot Activation ($499/mo): {t2_url}\n"
                f"- Pre-Configured Estimating Workspace: {ws_url}\n\n"
                f"Best,\nAaron // CamberDesk Preconstruction & DOT Systems"
            )
            try:
                r_nudge = requests.post(
                    "https://api.instantly.ai/api/v2/emails/reply",
                    headers=headers,
                    json={"reply_to_uuid": msg_id, "eaccount": eaccount, "subject": subj, "body": {"text": body_48}},
                    timeout=15,
                )
                if 200 <= r_nudge.status_code < 300:
                    info["nudge_48h_sent"] = True
                    info["nudge_48h_at"] = now
                    nudges_sent += 1
                    dirty = True
            except Exception:
                pass
        elif elapsed_hrs >= 96.0 and info.get("nudge_48h_sent") and not info.get("nudge_96h_sent"):
            body_96 = (
                f"Hi {fname},\n\n"
                f"Closing the loop on {pid} before the upcoming letting deadline — if {comp} wants ongoing 36-month State DOT unit-price bid tabulations, "
                f"competitor Money-Left-On-Table (MLOT) spread models, and 1-click 6-file OpenXML .ZIP packages across all upcoming lettings, "
                f"you can lock in your territory seat anytime here:\n"
                f"{t2_url}\n\n"
                f"Best,\nAaron // CamberDesk Preconstruction & DOT Systems"
            )
            try:
                r_nudge = requests.post(
                    "https://api.instantly.ai/api/v2/emails/reply",
                    headers=headers,
                    json={"reply_to_uuid": msg_id, "eaccount": eaccount, "subject": subj, "body": {"text": body_96}},
                    timeout=15,
                )
                if 200 <= r_nudge.status_code < 300:
                    info["nudge_96h_sent"] = True
                    info["nudge_96h_at"] = now
                    nudges_sent += 1
                    dirty = True
            except Exception:
                pass

    if dirty:
        try:
            WARM_FOLLOWUP_PATH.write_text(json.dumps(entries, indent=2), encoding="utf-8")
        except Exception:
            pass
    return nudges_sent


def _archive_and_purge_unsubscribed_lead(from_email: str) -> None:
    clean_unsub = str(from_email or "").strip().lower()
    if not clean_unsub or "@" not in clean_unsub:
        return
    try:
        archived: List[str] = []
        if ARCHIVE_PATH.exists():
            raw = json.loads(ARCHIVE_PATH.read_text(encoding="utf-8"))
            if isinstance(raw, list):
                archived = [str(x).strip().lower() for x in raw if x]
        if clean_unsub not in archived:
            archived.append(clean_unsub)
            ARCHIVE_PATH.write_text(json.dumps(sorted(set(archived)), indent=2), encoding="utf-8")
    except Exception:
        pass

    if INSTANTLY_API_KEY and CAMBERDESK_CAMPAIGN_ID:
        try:
            headers = {"Authorization": f"Bearer {INSTANTLY_API_KEY}", "Content-Type": "application/json"}
            l_resp = requests.post(
                "https://api.instantly.ai/api/v2/leads/list",
                headers=headers,
                json={"campaign": CAMBERDESK_CAMPAIGN_ID, "search": clean_unsub, "limit": 20},
                timeout=10,
            )
            if l_resp.status_code == 200:
                for l_it in (l_resp.json().get("items") or []):
                    if str(l_it.get("email") or "").strip().lower() == clean_unsub and l_it.get("id"):
                        requests.delete(
                            f"https://api.instantly.ai/api/v2/leads/{l_it['id']}",
                            headers={"Authorization": f"Bearer {INSTANTLY_API_KEY}"},
                            timeout=10,
                        )
        except Exception:
            pass


def run_reply_responder() -> Dict[str, Any]:
    processed: List[str] = []
    if PROCESSED_PATH.exists():
        try:
            processed = json.loads(PROCESSED_PATH.read_text(encoding="utf-8"))
        except Exception:
            processed = []

    summary = {"checked": 0, "replied": 0, "nudges_sent": 0, "unsubscribed": 0, "model": ANTHROPIC_MODEL}
    if not INSTANTLY_API_KEY or not CAMBERDESK_CAMPAIGN_ID:
        return summary

    try:
        r = None
        for attempt in range(3):
            try:
                r = requests.get(
                    "https://api.instantly.ai/api/v2/emails",
                    headers={"Authorization": f"Bearer {INSTANTLY_API_KEY}"},
                    params={"campaign_id": CAMBERDESK_CAMPAIGN_ID, "email_type": "received", "limit": 50},
                    timeout=20,
                )
                break
            except requests.exceptions.RequestException:
                if attempt < 2:
                    time.sleep(1.5 * (attempt + 1))

        if r is not None and r.status_code == 200:
            items = (r.json() or {}).get("items") or []
            for item in items:
                msg_id = str(item.get("id") or "")
                if not msg_id or msg_id in processed or item.get("ue_type") != 2:
                    continue
                eaccount = str(item.get("eaccount") or "").strip().lower()
                from_em = str(item.get("from_address_email") or item.get("lead") or "").strip()
                if "camberdesk" not in eaccount or "signaltender" in eaccount or "rubricward" in eaccount or "signaltender" in from_em.lower() or "camberdesk" in from_em.lower() or "rubricward" in from_em.lower():
                    continue
                summary["checked"] += 1
                body_obj = item.get("body") or {}
                body_txt = str(body_obj.get("text") or body_obj.get("html") or "").strip()
                if not body_txt:
                    processed.append(msg_id)
                    continue
                subj_in = str(item.get("subject") or "")
                label = classify_estimator_reply(body_txt, subject=subj_in, from_email=from_em)
                if label in ("POSITIVE_INTEREST", "QUESTION"):
                    pkg = build_zip_fulfillment_reply(from_em, reply_text=body_txt, label=label)
                    r_send = requests.post(
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
                    if 200 <= r_send.status_code < 300:
                        summary["replied"] += 1
                        _record_warm_zip_delivery(from_em, str(item.get("eaccount") or ""), msg_id, pkg["subject"], pkg.get("context") or {})
                        discord_url = (os.getenv("DISCORD_WEBHOOK_URL") or "").strip()
                        if discord_url:
                            try:
                                requests.post(
                                    discord_url,
                                    json={
                                        "content": (
                                            f"**[CAMBERDESK HOT REPLY — AUTO-ANSWERED BY CLAUDE SONNET 5.5]**\n"
                                            f"• **Estimator:** `{from_em}` (`{label}`)\n"
                                            f"• **Their Reply:** {body_txt[:300]}\n"
                                            f"• **Auto-Sent Response:** Delivered 6-File OpenXML Bid-Tab `.ZIP` + pre-filled `/#checkout` link."
                                        ),
                                        "flags": 4,
                                    },
                                    timeout=8,
                                )
                            except Exception:
                                pass
                elif label in ("UNSUBSCRIBE", "BOUNCE"):
                    summary["unsubscribed"] += 1
                    _archive_and_purge_unsubscribed_lead(from_em)
                processed.append(msg_id)
            PROCESSED_PATH.write_text(json.dumps(processed[-500:], indent=2), encoding="utf-8")
        summary["nudges_sent"] = _process_warm_zip_followups()
    except Exception as exc:
        report_error("outbound_reply_responder.py", f"Reply polling note: {exc}")

    return summary


if __name__ == "__main__":
    res = run_reply_responder()
    print(f"[CAMBERDESK REPLY RESPONDER] {res}")
