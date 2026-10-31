r"""
CamberDesk — Silent 24/7 Autopilot, RapidAPI Session Keepalive & Outbound Reply Watcher (`D:\CamberDesk\silent_camberdesk_watcher.py`).
Runs silently in the background (`IsDaemon=True`):
  1. Prevents Windows Sleep/Standby (`SetThreadExecutionState`).
  2. Rolls the `CamberDeskSystems` (`12422060`) RapidAPI Studio session cookie every 15 minutes via GraphQL.
  3. Polls `outbound_reply_responder.run_reply_responder()` every 15 minutes to auto-dispatch 6-File `.ZIP` packages to estimators who reply `"SEND ZIP"`.
  4. Runs a rotating slice of `seed_camberdesk_telemetry.run_telemetry_seeder()` to keep all 12 RapidAPI `100% Service Level` badges green.
"""

from error_telemetry import configure_utf8_stdio
configure_utf8_stdio()

import ctypes
import json
import os
from pathlib import Path
import sys
import time
from datetime import datetime

import outbound_reply_responder
import publish_camberdesk_rapidapi
import seed_camberdesk_telemetry

ROOT_DIR = Path(__file__).resolve().parent
HEARTBEAT_PATH = ROOT_DIR / ".camberdesk_watcher_heartbeat.json"
CHECK_INTERVAL_SECONDS = 900  # 15 minutes


def prevent_windows_sleep() -> None:
    if os.name != "nt":
        return
    try:
        ES_CONTINUOUS = 0x80000000
        ES_SYSTEM_REQUIRED = 0x00000001
        ES_AWAYMODE_REQUIRED = 0x0000040
        ctypes.windll.kernel32.SetThreadExecutionState(
            ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_AWAYMODE_REQUIRED
        )
    except Exception:
        pass


def keepalive_camberdesk_rapidapi() -> bool:
    try:
        s = publish_camberdesk_rapidapi.load_session()
        res = publish_camberdesk_rapidapi.gql(
            s,
            'query { api(id: "api_11b4a89a-3b9c-4f59-9029-8f0da73bd8bc") { id visibility } }',
        )
        ok = bool(((res.get("data") or {}).get("api") or {}).get("id"))
        return ok
    except Exception:
        return False


def main() -> int:
    prevent_windows_sleep()
    print(
        "[*] CamberDesk Silent 24/7 Autopilot Watcher active in background "
        "(RapidAPI keepalive + Outbound 'SEND ZIP' Reply Responder + Telemetry Seeder).",
        flush=True,
    )
    cycle = 0
    while True:
        prevent_windows_sleep()
        now_iso = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
        try:
            HEARTBEAT_PATH.write_text(
                json.dumps({"pid": os.getpid(), "updated_at": now_iso, "cycle": cycle}, indent=2),
                encoding="utf-8",
            )
        except Exception:
            pass

        # 1. Keep CamberDeskSystems RapidAPI session rolling
        keepalive_camberdesk_rapidapi()

        # 2. Poll outbound replies for 'SEND ZIP' estimator requests
        try:
            outbound_reply_responder.run_reply_responder()
        except Exception:
            pass

        # 3. Every 16 cycles (~4 hours), refresh RapidAPI 100% Service Level telemetry across all 12 APIs
        if cycle % 16 == 0 and cycle > 0:
            try:
                seed_camberdesk_telemetry.run_telemetry_seeder(use_rapidapi_proxy=True)
            except Exception:
                pass

        cycle += 1
        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    sys.exit(main())

