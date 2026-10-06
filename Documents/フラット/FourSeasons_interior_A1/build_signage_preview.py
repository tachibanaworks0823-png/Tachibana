#!/usr/bin/env python3
"""A1看板プレビュー生成（本番反映前の確認用）。

本文テキストは直前の正常プレビューを保持し、ロゴ層だけ差し替える。
花弁の大きさは変更しない（下方向ソフトグローの弱めのみ）。
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUT = ROOT / "output"
PREV = OUT / "preview"
PREV.mkdir(parents=True, exist_ok=True)

PREVIEW = (1786, 2529)
CHAT = (900, 1274)
BLACK_OPACITY = 0.62
BOX = {"x0": 0.0922, "y0": 0.1240, "x1": 0.9211, "y1": 0.2920}
MAIN_SCALE_BOOST = 1.02
NUDGE_UP = 0.035
MAIN_W, MAIN_H = 364, 91
# 本文開始位置（ここより下は前回プレビューのテキストをそのまま使う）
TEXT_CUT_FRAC = 0.310
BLEND_BAND = 40

# 花弁大きさ変更なし。下方向グローだけ弱める。
SOURCE_LOGO = ASSETS / "logo_four_seasons_cyan_petals_source.png"
# 本文を保持する基準プレビュー（テキストが正常な版）
BASELINE_PREVIEW = PREV / "A1_signage_preview_baseline.jpg"


def cover_bottom(im: Image.Image, tw: int, th: int) -> Image.Image:
    w, h = im.size
    scale = max(tw / w, th / h)
    nw, nh = int(round(w * scale)), int(round(h * scale))
    r = im.resize((nw, nh), Image.Resampling.LANCZOS)
    return r.crop(((nw - tw) // 2, nh - th, (nw - tw) // 2 + tw, nh))


def build_base(size: tuple[int, int]) -> Image.Image:
    W, H = size
    lounge = Image.open(OUT / "FourSeasons_interior_A1_150dpi.jpg").convert("RGB")
    bar = Image.open(ASSETS / "interior_bar_counter.jpg").convert("RGB")
    mark = np.array(Image.open(ASSETS / "interior_lounge_redline_mark.jpg").convert("RGB"))
    r, g, b = mark[:, :, 0].astype(int), mark[:, :, 1].astype(int), mark[:, :, 2].astype(int)
    red = (r > 180) & (g < 100) & (b < 100) & ((r - g) > 80) & ((r - b) > 80)
    cut_frac = float(np.where(red.any(axis=1))[0].min()) / mark.shape[0]
    bar_h = int(round(W * bar.size[1] / bar.size[0]))
    bar_r = bar.resize((W, bar_h), Image.Resampling.LANCZOS)
    top_h = H - bar_h
    cut_y = int(round(lounge.size[1] * cut_frac))
    top = cover_bottom(lounge.crop((0, 0, lounge.size[0], cut_y)), W, top_h)
    base = Image.new("RGB", (W, H))
    base.paste(top, (0, 0))
    base.paste(bar_r, (0, top_h))
    return base


def apply_black(base: Image.Image, opacity: float) -> Image.Image:
    rgba = base.convert("RGBA")
    ov = Image.new("RGBA", base.size, (0, 0, 0, int(round(255 * opacity))))
    return Image.alpha_composite(rgba, ov)


def load_logo_no_size_change() -> Image.Image:
    """ソースロゴを読み、大きさはそのまま下方向グローだけ弱める。"""
    src_path = SOURCE_LOGO if SOURCE_LOGO.exists() else ASSETS / "logo_four_seasons_cyan_petals.png"
    src = Image.open(src_path).convert("RGBA")
    arr = np.array(src).astype(np.float32)
    al = arr[:, :, 3]
    sh = src.size[1]
    fade_start = int(sh * 0.55)
    fade_end = int(sh * 0.92)
    fade = np.ones(sh, np.float32)
    for y in range(sh):
        if y >= fade_end:
            fade[y] = 0.20
        elif y >= fade_start:
            t = (y - fade_start) / max(1, fade_end - fade_start)
            fade[y] = 1.0 - 0.80 * t
    protect = al >= 100
    arr[:, :, 3] = np.where(protect, al, al * fade[:, None])
    out = Image.fromarray(arr.astype(np.uint8), "RGBA")
    assert out.size == src.size  # 大きさ変更なし
    out.save(ASSETS / "logo_four_seasons_cyan_petals.png")
    return out


def main_bbox_in_logo(logo: Image.Image) -> tuple[int, int, int, int]:
    arr = np.array(logo)
    lum = arr[:, :, :3].astype(np.float32).mean(axis=2)
    bright = (lum > 180) & (arr[:, :, 3] > 80)
    ys = np.where(bright.any(axis=1))[0]
    xs = np.where(bright.any(axis=0))[0]
    bcx = (float(xs.min()) + float(xs.max())) / 2.0
    bcy = (float(ys.min()) + float(ys.max())) / 2.0
    x0 = int(round(bcx - MAIN_W / 2))
    y0 = int(round(bcy - MAIN_H / 2))
    return (
        max(0, x0),
        max(0, y0),
        min(logo.size[0], x0 + MAIN_W),
        min(logo.size[1], y0 + MAIN_H),
    )


def place_logo(canvas: Image.Image, logo: Image.Image, main_bbox: tuple[int, int, int, int]) -> Image.Image:
    W, H = canvas.size
    img = canvas.convert("RGBA")
    x0 = int(round(BOX["x0"] * W))
    y0 = int(round(BOX["y0"] * H))
    x1 = int(round(BOX["x1"] * W))
    y1 = int(round(BOX["y1"] * H))
    box_w, box_h = x1 - x0, y1 - y0
    mx0, my0, mx1, my1 = main_bbox
    mw, mh = max(1, mx1 - mx0), max(1, my1 - my0)
    scale = min(box_w / mw, box_h / mh) * MAIN_SCALE_BOOST
    logo_r = logo.resize(
        (max(1, int(round(logo.size[0] * scale))), max(1, int(round(logo.size[1] * scale)))),
        Image.Resampling.LANCZOS,
    )
    sm = tuple(int(round(v * scale)) for v in main_bbox)
    lx = int(round(x0 + box_w / 2 - (sm[0] + sm[2]) / 2))
    ly = int(round(y0 + box_h / 2 - (sm[1] + sm[3]) / 2 - H * NUDGE_UP))
    img.alpha_composite(logo_r, (lx, ly))
    return img


def merge_keep_baseline_text(baseline: Image.Image, with_new_logo: Image.Image) -> Image.Image:
    """上＝新ロゴ、下＝基準プレビューの本文（ピクセル一致）。"""
    W, H = baseline.size
    before = np.array(baseline.convert("RGB")).astype(np.float32)
    new_rgb = np.array(with_new_logo.convert("RGB")).astype(np.float32)
    text_cut = int(TEXT_CUT_FRAC * H)
    out = before.copy()
    out[:text_cut, :, :] = new_rgb[:text_cut, :, :]
    band = BLEND_BAND
    for i in range(band):
        y = text_cut - band + i
        if y < 0:
            continue
        t = i / band
        out[y] = new_rgb[y] * (1.0 - t) + before[y] * t
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def main() -> None:
    if not BASELINE_PREVIEW.exists():
        raise SystemExit(
            f"Missing baseline preview with good text: {BASELINE_PREVIEW}\n"
            "Copy a known-good A1_signage_preview.jpg there first."
        )
    if not SOURCE_LOGO.exists():
        raise SystemExit(f"Missing source logo (size-locked): {SOURCE_LOGO}")

    logo = load_logo_no_size_change()
    main_bbox = main_bbox_in_logo(logo)
    canvas = apply_black(build_base(PREVIEW), BLACK_OPACITY)
    with_logo = place_logo(canvas, logo, main_bbox)
    baseline = Image.open(BASELINE_PREVIEW)
    final = merge_keep_baseline_text(baseline, with_logo)

    preview_path = PREV / "A1_signage_preview.jpg"
    chat_path = PREV / "A1_signage_preview_chat.jpg"
    final.save(preview_path, "JPEG", quality=95, optimize=True, dpi=(96, 96))
    final.resize(CHAT, Image.Resampling.LANCZOS).save(chat_path, "JPEG", quality=92, optimize=True)
    print(f"PREVIEW ONLY: {preview_path}")
    print(f"logo size unchanged={logo.size} / body text from baseline / black={BLACK_OPACITY}")


if __name__ == "__main__":
    main()
