#!/usr/bin/env python3
"""Render 謹告 A4 flyer to PNG (A4 @ 300dpi) via headless Chrome."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "index.html"
PNG = ROOT / "kinkoku-fuzoku-a4.png"

# A4 @ 300dpi
A4_W = 2480
A4_H = 3508

CHROME = "/usr/local/bin/google-chrome"


def main() -> int:
    if not HTML.exists():
        print(f"Missing {HTML}", file=sys.stderr)
        return 1

    url = HTML.as_uri()
    user_data = ROOT / ".chrome-userdata"
    user_data.mkdir(exist_ok=True)

    # Allow Google Fonts a moment; virtual-time-budget also advances timers
    time.sleep(0.5)

    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--allow-file-access-from-files",
        "--hide-scrollbars",
        f"--user-data-dir={user_data}",
        "--virtual-time-budget=5000",
        f"--window-size={A4_W},{A4_H}",
        f"--screenshot={PNG}",
        "--force-device-scale-factor=1",
        url,
    ]
    print("+", " ".join(cmd))
    # Chrome sometimes hangs after screenshot; kill after success window
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    deadline = time.time() + 45
    while time.time() < deadline:
        if PNG.exists() and PNG.stat().st_size > 50_000:
            time.sleep(1.0)  # let write finish
            proc.kill()
            break
        if proc.poll() is not None:
            break
        time.sleep(0.3)
    else:
        proc.kill()

    proc.wait(timeout=10)

    if not PNG.exists():
        print("PNG was not created", file=sys.stderr)
        err = (proc.stderr.read() if proc.stderr else b"").decode("utf-8", "replace")
        print(err[-2000:], file=sys.stderr)
        return 1

    try:
        from PIL import Image

        img = Image.open(PNG)
        if img.size != (A4_W, A4_H):
            img = img.resize((A4_W, A4_H), Image.Resampling.LANCZOS)
            img.save(PNG, "PNG", optimize=True)
        print(f"PNG created: {PNG} ({img.size[0]}x{img.size[1]})")
    except Exception as e:
        print(f"PNG created: {PNG} (size normalize skipped: {e})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
