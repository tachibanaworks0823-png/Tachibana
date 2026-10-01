#!/usr/bin/env python3
"""Render 謹告 A4 flyer to full-bleed PNG (A4 @ 300dpi)."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "index.html"
PNG = ROOT / "kinkoku-fuzoku-a4.png"
TMP = ROOT / "kinkoku-fuzoku-a4.capture.png"

# CSS reference size for 210mm×297mm at 96dpi
CSS_W = round(210 * 96 / 25.4)  # 794
CSS_H = round(297 * 96 / 25.4)  # 1123

# A4 @ 300dpi output
A4_W = 2480
A4_H = 3508
SCALE = A4_W / CSS_W  # ~3.1234 → capture ~2480×3509

CHROME = "/usr/local/bin/google-chrome"


def kill_after_file(proc: subprocess.Popen, path: Path, timeout: float = 45) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if path.exists() and path.stat().st_size > 50_000:
            time.sleep(0.8)
            proc.kill()
            break
        if proc.poll() is not None:
            break
        time.sleep(0.2)
    else:
        proc.kill()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()


def main() -> int:
    if not HTML.exists():
        print(f"Missing {HTML}", file=sys.stderr)
        return 1

    for p in (PNG, TMP):
        if p.exists():
            p.unlink()

    url = HTML.as_uri()
    user_data = ROOT / ".chrome-userdata"
    user_data.mkdir(exist_ok=True)

    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--allow-file-access-from-files",
        "--hide-scrollbars",
        f"--user-data-dir={user_data}",
        "--virtual-time-budget=6000",
        f"--window-size={CSS_W},{CSS_H}",
        f"--force-device-scale-factor={SCALE:.6f}",
        f"--screenshot={TMP}",
        url,
    ]
    print("+", " ".join(cmd))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    kill_after_file(proc, TMP)

    if not TMP.exists():
        err = (proc.stderr.read() if proc.stderr else b"").decode("utf-8", "replace")
        print("PNG was not created", file=sys.stderr)
        print(err[-2000:], file=sys.stderr)
        return 1

    from PIL import Image

    img = Image.open(TMP).convert("RGB")
    print(f"capture size: {img.size}")

    # Safety: if Chrome still left letterboxing, crop to non-empty content
    def is_bg(px):
        r, g, b = px
        return r < 40 and g < 30 and b < 30

    w, h = img.size
    pixels = img.load()
    minx, miny, maxx, maxy = w, h, 0, 0
    step = 3
    for y in range(0, h, step):
        for x in range(0, w, step):
            if not is_bg(pixels[x, y]):
                minx = min(minx, x)
                miny = min(miny, y)
                maxx = max(maxx, x)
                maxy = max(maxy, y)

    content_w = maxx - minx
    content_h = maxy - miny
    fill = (content_w / w) * (content_h / h)
    print(f"content bbox: {(minx, miny, maxx, maxy)} fill≈{fill:.2%}")

    if fill < 0.85:
        # Expand bbox a bit and crop — flyer was letterboxed
        pad = 2
        box = (
            max(0, minx - pad),
            max(0, miny - pad),
            min(w, maxx + pad + 1),
            min(h, maxy + pad + 1),
        )
        img = img.crop(box)
        print(f"cropped to: {img.size}")

    if img.size != (A4_W, A4_H):
        img = img.resize((A4_W, A4_H), Image.Resampling.LANCZOS)

    img.save(PNG, "PNG", optimize=True)
    TMP.unlink(missing_ok=True)
    print(f"PNG created: {PNG} ({A4_W}x{A4_H})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
