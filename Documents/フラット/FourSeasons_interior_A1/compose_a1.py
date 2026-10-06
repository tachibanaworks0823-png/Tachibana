#!/usr/bin/env python3
"""店内席写真の赤線位置にカウンター写真を挿入し、A1用紙に合わせる。"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageOps
from reportlab.lib.pagesizes import A1
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

LOUNGE_HI = OUT / "FourSeasons_interior_A1_150dpi.jpg"
LOUNGE_MARK = ASSETS / "interior_lounge_redline_mark.jpg"
BAR = ASSETS / "interior_bar_counter.jpg"

PREVIEW = (1786, 2529)
PRINT150 = (3508, 4961)


def red_cut_fraction(mark_path: Path) -> float:
    arr = np.array(Image.open(mark_path).convert("RGB"))
    h = arr.shape[0]
    r, g, b = arr[:, :, 0].astype(int), arr[:, :, 1].astype(int), arr[:, :, 2].astype(int)
    red = (r > 180) & (g < 100) & (b < 100) & ((r - g) > 80) & ((r - b) > 80)
    rows = np.where(red.any(axis=1))[0]
    if len(rows) == 0:
        raise SystemExit(f"red line not found in {mark_path}")
    return float(rows.min()) / h


def cover_bottom(im: Image.Image, tw: int, th: int) -> Image.Image:
    """Cover-fit, keep bottom edge (near red line) aligned."""
    w, h = im.size
    scale = max(tw / w, th / h)
    nw, nh = int(round(w * scale)), int(round(h * scale))
    r = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = nh - th
    return r.crop((left, top, left + tw, top + th))


def compose(lounge_top: Image.Image, bar: Image.Image, size: tuple[int, int]) -> Image.Image:
    W, H = size
    bw, bh = bar.size
    bar_h = int(round(W * bh / bw))
    bar_r = bar.resize((W, bar_h), Image.Resampling.LANCZOS)
    top_h = H - bar_h
    top_c = cover_bottom(lounge_top, W, top_h)
    out = Image.new("RGB", (W, H))
    out.paste(top_c, (0, 0))
    out.paste(bar_r, (0, top_h))
    return out


def save_jpg(im: Image.Image, path: Path, dpi: int) -> None:
    im.save(path, "JPEG", quality=95, optimize=True, dpi=(dpi, dpi))


def save_pdf(im: Image.Image, path: Path) -> None:
    tmp = OUT / "_embed_tmp.jpg"
    save_jpg(im, tmp, 150)
    c = canvas.Canvas(str(path), pagesize=A1)
    pw, ph = A1
    c.drawImage(str(tmp), 0, 0, width=pw, height=ph, preserveAspectRatio=False)
    c.showPage()
    c.save()
    tmp.unlink(missing_ok=True)


def main() -> None:
    cut = red_cut_fraction(LOUNGE_MARK)
    lounge = ImageOps.exif_transpose(Image.open(LOUNGE_HI)).convert("RGB")
    bar = ImageOps.exif_transpose(Image.open(BAR)).convert("RGB")
    cut_y = int(round(lounge.size[1] * cut))
    top = lounge.crop((0, 0, lounge.size[0], cut_y))
    print(f"cut_frac={cut:.4f} top={top.size} bar={bar.size}")

    preview = compose(top, bar, PREVIEW)
    print150 = compose(top, bar, PRINT150)

    save_jpg(preview, OUT / "FourSeasons_composite_A1_preview.jpg", 96)
    save_jpg(print150, OUT / "FourSeasons_composite_A1_150dpi.jpg", 150)
    save_pdf(print150, OUT / "FourSeasons_composite_A1.pdf")

    chat_w = 900
    chat_h = int(round(chat_w * 841 / 594))
    chat = preview.resize((chat_w, chat_h), Image.Resampling.LANCZOS)
    save_jpg(chat, OUT / "FourSeasons_composite_A1_chat.jpg", 72)
    print("wrote composite A1 outputs")


if __name__ == "__main__":
    main()
