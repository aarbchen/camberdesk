"""
CamberDesk — Closed-Loop Autonomous Error Telemetry & UTF-8 Stdio Helper.
"""

import os
import sys
from datetime import datetime, timezone
from typing import Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ERROR_LOG_PATH = os.path.join(BASE_DIR, "error_log.txt")


def configure_utf8_stdio() -> None:
    """Ensure stdout and stderr use UTF-8 encoding across Windows PowerShell and Linux containers."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is not None and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def report_error(
    source: str,
    message: str,
    severity: str = "ERROR",
    context: Optional[dict] = None,
) -> None:
    """Log error to local error_log.txt cleanly without throwing."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{ts}] [{severity.upper()}] [{source}] {message}"
    if context:
        line += f" | context={context}"
    try:
        with open(ERROR_LOG_PATH, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception:
        pass

