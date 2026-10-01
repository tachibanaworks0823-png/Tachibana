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


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> int:
    if not HTML.exists():
        print(f"Missing {HTML}", file=sys.stderr)
        return 1

    url = HTML.as_uri()
    # Allow Google Fonts to load
    time.sleep(1.5)

    user_data = ROOT / ".chrome-user"
    user_data.mkdir(exist_ok=True)

    # Virtual time budget helps fonts settle before capture
    run(
        [
            CHROME,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--allow-file-access-from-files",
            "--hide-scrollbars",
            f"--user-data-dir={user_data}",
            "--virtual-time-budget=8000",
            f"--window-size={A4_W},{A4_H}",
            f"--screenshot={PNG}",
            "--force-device-scale-factor=1",
            "--timeout=30000",
            url,
        ],
    )

    if not PNG.exists():
        print("PNG was not created", file=sys.stderr)
        return 1

    # Normalize exact A4 pixel size if Chrome viewport differs
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
