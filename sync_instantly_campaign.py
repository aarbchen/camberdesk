r"""
CamberDesk — Dedicated Instantly.ai V2 Campaign Provisioner & Planholder Lead Sync (`D:\CamberDesk\sync_instantly_campaign.py`).
Creates or locates the standalone `"CamberDesk — 50-State DOT Planholder & Unit Bid-Tab Outreach"` campaign
in Instantly.ai V2 (separate from any other campaign), configures the 2-step zero-link plain-text sequence
scheduled for Monday–Friday 07:00–17:00 Central, uploads the 24 DOT Planholder Chief Estimator leads from
`D:\CamberDesk\campaign_leads.csv`, and saves `CAMBERDESK_INSTANTLY_CAMPAIGN_ID` to `D:\CamberDesk\.env`.
"""

from error_telemetry import configure_utf8_stdio
configure_utf8_stdio()

import csv
import json
import os
from pathlib import Path
from typing import Any, Dict, List
import requests
from dotenv import load_dotenv

from outreach_generator import generate_outreach_queue

ROOT_DIR = Path(__file__).resolve().parent
ENV_PATH = ROOT_DIR / ".env"
CSV_PATH = ROOT_DIR / "campaign_leads.csv"
load_dotenv(dotenv_path=str(ENV_PATH))

INSTANTLY_API_KEY = (os.getenv("INSTANTLY_API_KEY") or "").strip()
CAMPAIGN_NAME = "CamberDesk — 50-State DOT Planholder & Unit Bid-Tab Outreach"


def ensure_camberdesk_campaign() -> str:
    headers = {
        "Authorization": f"Bearer {INSTANTLY_API_KEY}",
        "Content-Type": "application/json",
    }
    existing_id = (os.getenv("CAMBERDESK_INSTANTLY_CAMPAIGN_ID") or "").strip()
    if existing_id:
        r_check = requests.get(f"https://api.instantly.ai/api/v2/campaigns/{existing_id}", headers=headers, timeout=15)
        if r_check.status_code == 200 and (r_check.json() or {}).get("id"):
            return existing_id

    r_list = requests.get("https://api.instantly.ai/api/v2/campaigns?limit=50", headers=headers, timeout=15)
    if r_list.status_code == 200:
        for item in (r_list.json() or {}).get("items") or []:
            if (item.get("name") or "").strip() == CAMPAIGN_NAME:
                cid = item["id"]
                _save_campaign_id(cid)
                return cid

    payload = {
        "name": CAMPAIGN_NAME,
        "campaign_schedule": {
            "schedules": [
                {
                    "name": "Monday-Friday Estimating Hours",
                    "timing": {"from": "07:00", "to": "17:00"},
                    "days": {"1": True, "2": True, "3": True, "4": True, "5": True, "6": False, "0": False},
                    "timezone": "America/Chicago",
                }
            ]
        },
        "sequences": [
            {
                "steps": [
                    {
                        "type": "email",
                        "delay": 0,
                        "variants": [
                            {
                                "subject": "{{step1_subject}}",
                                "body": "{{step1_body_zero_link}}",
                            }
                        ],
                    },
                    {
                        "type": "email",
                        "delay": 3,
                        "variants": [
                            {
                                "subject": "Re: {{step1_subject}}",
                                "body": "{{step2_body_dossier_link}}",
                            }
                        ],
                    },
                ]
            }
        ],
        "text_only": True,
        "stop_on_reply": True,
        "link_tracking": False,
        "open_tracking": False,
        "daily_limit": 25,
    }
    r_create = requests.post("https://api.instantly.ai/api/v2/campaigns", headers=headers, json=payload, timeout=20)
    if r_create.status_code in (200, 201):
        cid = (r_create.json() or {}).get("id") or ""
        if cid:
            _save_campaign_id(cid)
            return cid
    print(f"[!] Note creating Instantly campaign: HTTP {r_create.status_code} {r_create.text[:250]}")
    return ""


def _save_campaign_id(cid: str) -> None:
    if not ENV_PATH.exists():
        return
    txt = ENV_PATH.read_text(encoding="utf-8")
    if "CAMBERDESK_INSTANTLY_CAMPAIGN_ID=" in txt:
        lines = [
            f"CAMBERDESK_INSTANTLY_CAMPAIGN_ID={cid}" if ln.startswith("CAMBERDESK_INSTANTLY_CAMPAIGN_ID=") else ln
            for ln in txt.splitlines()
        ]
        ENV_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    else:
        ENV_PATH.write_text(txt.rstrip() + f"\nCAMBERDESK_INSTANTLY_CAMPAIGN_ID={cid}\n", encoding="utf-8")


def sync_leads_to_instantly() -> Dict[str, Any]:
    leads = generate_outreach_queue()
    if not INSTANTLY_API_KEY:
        return {"status": "skipped_no_key", "leads_local": len(leads)}

    cid = ensure_camberdesk_campaign()
    if not cid:
        return {"status": "local_only", "leads_local": len(leads)}

    headers = {
        "Authorization": f"Bearer {INSTANTLY_API_KEY}",
        "Content-Type": "application/json",
    }

    # Purge any legacy synthetic domains from the campaign if present
    valid_email_set = {l["email"].strip().lower() for l in leads}
    try:
        r_existing = requests.post(
            "https://api.instantly.ai/api/v2/leads/list",
            headers=headers,
            json={"campaign": cid, "limit": 100},
            timeout=15,
        )
        if r_existing.status_code == 200:
            for item in (r_existing.json() or {}).get("items") or []:
                em_existing = str(item.get("email") or "").strip().lower()
                lid = item.get("id")
                if lid and em_existing not in valid_email_set:
                    requests.delete(f"https://api.instantly.ai/api/v2/leads/{lid}", headers=headers, timeout=10)
    except Exception:
        pass

    uploaded = 0
    for lead in leads:
        payload = {
            "campaign": cid,
            "email": lead["email"],
            "first_name": lead["first_name"],
            "company_name": lead["company_name"],
            "custom_variables": {
                "license_or_dot_id": lead["license_or_dot_id"],
                "state": lead["state"],
                "project_id": lead["project_id"],
                "project_title": lead["project_title"],
                "letting_date": lead["letting_date"],
                "dossier_url": lead["dossier_url"],
                "compiler_url": lead["compiler_url"],
                "step1_subject": lead["step1_subject"],
                "step1_body_zero_link": lead["step1_body_zero_link"],
                "step2_body_dossier_link": lead["step2_body_dossier_link"],
            },
            "skip_if_in_workspace": False,
        }
        try:
            r = requests.post("https://api.instantly.ai/api/v2/leads", headers=headers, json=payload, timeout=15)
            if r.status_code in (200, 201):
                uploaded += 1
        except Exception:
            pass

    print(f"[CAMBERDESK INSTANTLY] Campaign {cid}: synced {uploaded}/{len(leads)} DOT Planholder leads.")
    return {"status": "synced", "campaign_id": cid, "uploaded": uploaded, "total": len(leads)}


if __name__ == "__main__":
    res = sync_leads_to_instantly()
    print(json.dumps(res, indent=2))

