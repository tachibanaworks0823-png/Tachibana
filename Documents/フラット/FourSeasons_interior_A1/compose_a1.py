#!/usr/bin/env python3
"""店内合成A1: 赤線でカット＋カウンター挿入＋黒オーバーレイ＋ロゴ最前面。"""

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
LOGO_MARK = ASSETS / "composite_logo_placement_mark.jpg"
LOGO_BLACK = ASSETS / "logo_four_seasons_blackbg.jpg"
LOGO_WHITE = ASSETS / "logo_four_seasons_whitebg.jpg"

PREVIEW = (1786, 2529)
PRINT150 = (3508, 4961)

# 黒オーバーレイ: 不透明度 50%（透過 50%）
BLACK_TRANSPARENCY = 0.50
BLACK_ALPHA = int(round(255 * (1.0 - BLACK_TRANSPARENCY)))


def red_cut_fraction(mark_path: Path) -> float:
    arr = np.array(Image.open(mark_path).convert("RGB"))
    h = arr.shape[0]
    r, g, b = arr[:, :, 0].astype(int), arr[:, :, 1].astype(int), arr[:, :, 2].astype(int)
    red = (r > 180) & (g < 100) & (b < 100) & ((r - g) > 80) & ((r - b) > 80)
    rows = np.where(red.any(axis=1))[0]
    if len(rows) == 0:
        raise SystemExit(f"red line not found in {mark_path}")
    return float(rows.min()) / h


def detect_red_box_frac(mark_path: Path) -> tuple[float, float, float, float]:
    """赤枠の内側を (x0,y0,x1,y1) の割合で返す。"""
    arr = np.array(Image.open(mark_path).convert("RGB"))
    h, w = arr.shape[:2]
    r, g, b = arr[:, :, 0].astype(int), arr[:, :, 1].astype(int), arr[:, :, 2].astype(int)
    red = (r > 180) & (g < 100) & (b < 100) & ((r - g) > 80) & ((r - b) > 80)
    row_counts = red.sum(axis=1)
    horiz = np.where(row_counts > w * 0.3)[0]
    gaps = np.where(np.diff(horiz) > 10)[0]
    if len(gaps) == 0:
        raise SystemExit(f"red rectangle not found in {mark_path}")
    top_band = horiz[: gaps[0] + 1]
    bot_band = horiz[gaps[0] + 1 :]
    top_inner = int(top_band.max()) + 2
    bot_inner = int(bot_band.min()) - 2
    band = red[top_band.min() : bot_band.max() + 1, :]
    col_c = band.sum(axis=0)
    left_peak = np.where(col_c[: w // 2] > band.shape[0] * 0.2)[0]
    right_peak = np.where(col_c[w // 2 :] > band.shape[0] * 0.2)[0] + w // 2
    left_inner = int(left_peak.max()) + 2
    right_inner = int(right_peak.min()) - 2
    return left_inner / w, top_inner / h, right_inner / w, bot_inner / h


def cover_bottom(im: Image.Image, tw: int, th: int) -> Image.Image:
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


def black_overlay_top(im: Image.Image) -> Image.Image:
    base = im.convert("RGBA")
    overlay = Image.new("RGBA", base.size, (0, 0, 0, BLACK_ALPHA))
    return Image.alpha_composite(base, overlay).convert("RGB")


def trim_margins(im: Image.Image, bg: str = "white", pad: int = 24) -> Image.Image:
    arr = np.array(im.convert("RGB"))
    if bg == "white":
        mask = arr.mean(axis=2) < 250
    else:
        mask = arr.mean(axis=2) > 15
    ys, xs = np.where(mask)
    if len(ys) == 0:
        return im.convert("RGBA")
    y0, y1 = max(0, ys.min() - pad), min(arr.shape[0], ys.max() + pad)
    x0, x1 = max(0, xs.min() - pad), min(arr.shape[1], xs.max() + pad)
    return im.crop((x0, y0, x1, y1)).convert("RGBA")


def fit_in_box(logo: Image.Image, max_w: int, max_h: int) -> Image.Image:
    lw, lh = logo.size
    scale = min(max_w / lw, max_h / lh)
    nw = max(1, int(round(lw * scale)))
    nh = max(1, int(round(lh * scale)))
    return logo.resize((nw, nh), Image.Resampling.LANCZOS)


def place_logos(
    base_rgb: Image.Image,
    box_frac: tuple[float, float, float, float],
    logo_left: Image.Image,
    logo_right: Image.Image,
) -> Image.Image:
    """赤枠内にロゴ2枚を左右配置（最前面）。"""
    W, H = base_rgb.size
    x0 = int(round(box_frac[0] * W))
    y0 = int(round(box_frac[1] * H))
    x1 = int(round(box_frac[2] * W))
    y1 = int(round(box_frac[3] * H))
    box_w, box_h = x1 - x0, y1 - y0
    pad = max(8, int(min(box_w, box_h) * 0.06))
    gap = max(12, int(box_w * 0.03))
    inner_w = box_w - 2 * pad
    inner_h = box_h - 2 * pad
    each_w = (inner_w - gap) // 2

    la = fit_in_box(logo_left, each_w, inner_h)
    lb = fit_in_box(logo_right, each_w, inner_h)
    canvas = base_rgb.convert("RGBA")
    ax = x0 + pad + (each_w - la.size[0]) // 2
    ay = y0 + pad + (inner_h - la.size[1]) // 2
    bx = x0 + pad + each_w + gap + (each_w - lb.size[0]) // 2
    by = y0 + pad + (inner_h - lb.size[1]) // 2
    canvas.alpha_composite(la.convert("RGBA"), (ax, ay))
    canvas.alpha_composite(lb.convert("RGBA"), (bx, by))
    return canvas.convert("RGB")


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


def write_chat(im: Image.Image, path: Path) -> None:
    chat_w = 900
    chat_h = int(round(chat_w * 841 / 594))
    chat = im.resize((chat_w, chat_h), Image.Resampling.LANCZOS)
    save_jpg(chat, path, 72)


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

    preview_ov = black_overlay_top(preview)
    print150_ov = black_overlay_top(print150)
    save_jpg(preview_ov, OUT / "FourSeasons_composite_A1_overlay_preview.jpg", 96)
    save_jpg(print150_ov, OUT / "FourSeasons_composite_A1_overlay_150dpi.jpg", 150)
    save_pdf(print150_ov, OUT / "FourSeasons_composite_A1_overlay.pdf")

    box = detect_red_box_frac(LOGO_MARK)
    logo_l = trim_margins(Image.open(LOGO_BLACK), bg="black", pad=16)
    logo_r = trim_margins(Image.open(LOGO_WHITE), bg="white", pad=32)
    print(f"logo box={box} left={logo_l.size} right={logo_r.size}")

    preview_logos = place_logos(preview_ov, box, logo_l, logo_r)
    print150_logos = place_logos(print150_ov, box, logo_l, logo_r)
    save_jpg(preview_logos, OUT / "FourSeasons_composite_A1_logos_preview.jpg", 96)
    save_jpg(print150_logos, OUT / "FourSeasons_composite_A1_logos_150dpi.jpg", 150)
    save_pdf(print150_logos, OUT / "FourSeasons_composite_A1_logos.pdf")

    write_chat(preview, OUT / "FourSeasons_composite_A1_chat.jpg")
    write_chat(preview_ov, OUT / "FourSeasons_composite_A1_overlay_chat.jpg")
    write_chat(preview_logos, OUT / "FourSeasons_composite_A1_logos_chat.jpg")
    print("wrote composite / overlay / logos A1 outputs")


if __name__ == "__main__":
    main()
