#!/usr/bin/env python3
"""A1看板プレビュー生成（本番反映前の確認用）。"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUT = ROOT / "output"
FONTS = ASSETS / "fonts"
PREV = OUT / "preview"
PREV.mkdir(parents=True, exist_ok=True)

JOSE = str(FONTS / "JosefinSans[wght].ttf")
JP = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"

PREVIEW = (1786, 2529)
CHAT = (900, 1274)
BLACK_OPACITY = 0.62

# ロゴ配置赤枠（ユーザー指定マークから検出した内側比率）
BOX = {"x0": 0.0922, "y0": 0.1240, "x1": 0.9211, "y1": 0.2920}
MAIN_SCALE_BOOST = 1.02
NUDGE_UP = 0.035
TEXT_NUDGE_DOWN = 0.035
DRINK_NUDGE_DOWN = 0.028

# 大きな花弁: 引き締め（間延び解消）＋スツール上の残光を避ける
PETAL_SCALE = 0.58
ERODE = 9
LARGE_PETAL_OPACITY = 0.15
BLUR_PASSES = ((5.5, 0.48), (2.4, 0.32), (1.0, 0.20))
CYAN = (168, 205, 210)


def font(path: str, size: int, weight: int | None = None) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(path, size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f


def extract_clean_logo() -> Image.Image:
    """黒プレートからロゴを切り出し、黒背景のみ透過。"""
    src = ImageOps.exif_transpose(Image.open(ASSETS / "logo_four_seasons_blackbg.jpg")).convert("RGB")
    arr = np.array(src)
    lum = arr.mean(axis=2)
    ys, xs = np.where(lum < 40)
    plate = src.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))
    parr = np.array(plate).astype(np.float32)
    pr, pg, pb = parr[:, :, 0], parr[:, :, 1], parr[:, :, 2]
    plum = (pr + pg + pb) / 3.0
    pmx = np.maximum(np.maximum(pr, pg), pb)
    alpha = np.clip((pmx - 6.0) / (36.0 - 6.0) * 255.0, 0, 255)
    alpha = np.where(plum > 42, 255, alpha)
    alpha = np.where((pb > 140) & (pg > 120) & (pb + 5 >= pr), 255, alpha)
    alpha = alpha.astype(np.uint8)
    logo = Image.fromarray(np.dstack([parr.astype(np.uint8), alpha]), "RGBA")
    logo.putalpha(logo.getchannel("A").filter(ImageFilter.GaussianBlur(0.3)))
    logo = logo.crop(logo.getbbox())
    logo.save(ASSETS / "logo_four_seasons_clean.png")
    return logo


def clean_main_mark(main: Image.Image) -> Image.Image:
    """メインマークから暗いグレーのプレート残りを除去。"""
    a = np.array(main).astype(np.float32)
    lum = a[:, :, :3].mean(axis=2)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    al = a[:, :, 3]
    keep_white = (lum > 160) & (al > 50)
    keep_cyan = (b > r + 12) & (g > r + 2) & (al > 70) & (lum > 90) & (lum < 230)
    keep = keep_white | keep_cyan
    keep_img = Image.fromarray((keep.astype(np.uint8) * 255)).filter(ImageFilter.MaxFilter(3))
    keep = np.array(keep_img) > 127
    out = a.copy()
    out[:, :, 3] = np.where(keep, al, 0)
    out[:, :, 3] = np.where(lum < 100, 0, out[:, :, 3])
    cleaned = Image.fromarray(out.astype(np.uint8), "RGBA")
    return cleaned.crop(cleaned.getbbox())


def build_logo_with_petals() -> tuple[Image.Image, tuple[int, int, int, int]]:
    """大きな花弁を引き締めてグロー化し、メインマークと合成。

    Returns:
        (logo_rgba, main_bbox_in_logo_coords)
    """
    clean = extract_clean_logo()
    main = clean_main_mark(Image.open(ASSETS / "logo_four_seasons_main.png").convert("RGBA"))

    c = np.array(clean)
    al = c[:, :, 3].astype(float)
    lum = c[:, :, :3].mean(axis=2)
    white = (lum > 170) & (al > 80)
    large_mask = (al > 20) & (lum >= 28) & (lum <= 95) & (~white)
    large_img = Image.fromarray((large_mask.astype(np.uint8) * 255)).filter(ImageFilter.MaxFilter(3))
    large_mask = np.array(large_img) > 127
    gray_a = np.where(large_mask, np.clip(al, 0, 255), 0).astype(np.uint8)

    shape = Image.fromarray(gray_a, "L")
    shape_bin = shape.point(lambda p: 255 if p > 30 else 0).filter(ImageFilter.MinFilter(ERODE))
    sw, sh = shape.size
    nw = max(1, int(round(sw * PETAL_SCALE)))
    nh = max(1, int(round(sh * PETAL_SCALE)))
    scaled_bin = shape_bin.resize((nw, nh), Image.Resampling.LANCZOS)
    scaled_soft = shape.resize((nw, nh), Image.Resampling.LANCZOS)
    ox, oy = int(round((sw - nw) / 2)), int(round((sh - nh) / 2))
    canvas_bin = Image.new("L", (sw, sh), 0)
    canvas_bin.paste(scaled_bin, (ox, oy))
    canvas_soft = Image.new("L", (sw, sh), 0)
    canvas_soft.paste(scaled_soft, (ox, oy))

    glow = np.zeros((sh, sw), np.float32)
    core = np.array(canvas_bin).astype(np.float32)
    body = np.array(canvas_soft).astype(np.float32)
    for radius, weight in BLUR_PASSES:
        blurred = np.array(canvas_bin.filter(ImageFilter.GaussianBlur(radius))).astype(np.float32)
        glow = np.maximum(glow, blurred * weight)
    combined = np.clip(np.maximum(glow, np.maximum(body * 0.45, core * 0.85)), 0, 255)
    peak = float(combined.max()) or 1.0
    petal_a = (combined / peak * (LARGE_PETAL_OPACITY * 255.0)).astype(np.uint8)

    # メイン文字帯より下へ伸びるグローをフェードアウト（スツール上の残光防止）
    ys = np.where(white.any(axis=1))[0]
    main_bottom = int(ys.max()) if len(ys) else sh // 2 + 40
    fade_start = main_bottom + int(sh * 0.02)
    fade_end = main_bottom + int(sh * 0.18)
    fade = np.ones(sh, np.float32)
    for y in range(sh):
        if y >= fade_end:
            fade[y] = 0.0
        elif y >= fade_start:
            fade[y] = 1.0 - (y - fade_start) / max(1, fade_end - fade_start)
    petal_a = (petal_a.astype(np.float32) * fade[:, None]).astype(np.uint8)

    petal_rgb = np.zeros((sh, sw, 3), dtype=np.uint8)
    petal_rgb[:, :, 0] = CYAN[0]
    petal_rgb[:, :, 1] = CYAN[1]
    petal_rgb[:, :, 2] = CYAN[2]
    large = Image.fromarray(np.dstack([petal_rgb, petal_a]), "RGBA")

    # メインをクリーン上の文字帯中心へ配置
    ys, xs = np.where(white)
    tx0, ty0, tx1, ty1 = int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1
    matched = Image.open(ASSETS / "logo_four_seasons_petals_matched.png").convert("RGBA")
    mm = np.array(matched)
    msmall = (
        (mm[:, :, 2] > mm[:, :, 0] + 15)
        & (mm[:, :, 1] > mm[:, :, 0] + 5)
        & (mm[:, :, 3] > 100)
        & (mm[:, :, :3].mean(axis=2) > 100)
    )
    tcx, tcy = (tx0 + tx1) / 2, (ty0 + ty1) / 2
    if msmall.any():
        pys = np.where(msmall.any(axis=1))[0]
        tcy = (min(ty0, int(pys.min())) + max(ty1, int(pys.max()) + 1)) / 2
    mw, mh = main.size
    mx = int(round(tcx - mw / 2))
    my = int(round(tcy - mh / 2))

    out_full = Image.new("RGBA", clean.size, (0, 0, 0, 0))
    out_full.alpha_composite(large)
    out_full.alpha_composite(main, (mx, my))
    cb = out_full.getbbox()
    assert cb is not None
    out = out_full.crop(cb)

    main_full = Image.new("RGBA", clean.size, (0, 0, 0, 0))
    main_full.alpha_composite(main, (mx, my))
    main_bbox = main_full.crop(cb).getbbox()
    assert main_bbox is not None

    out.save(ASSETS / "logo_four_seasons_cyan_petals.png")
    bg = Image.new("RGBA", (out.size[0] + 56, out.size[1] + 56), (16, 16, 20, 255))
    bg.alpha_composite(out, (28, 28))
    bg.convert("RGB").save(PREV / "logo_cyan_petals_preview.png")
    return out, main_bbox


def cover_bottom(im: Image.Image, tw: int, th: int) -> Image.Image:
    w, h = im.size
    scale = max(tw / w, th / h)
    nw, nh = int(round(w * scale)), int(round(h * scale))
    r = im.resize((nw, nh), Image.Resampling.LANCZOS)
    return r.crop(((nw - tw) // 2, nh - th, (nw - tw) // 2 + tw, nh))


def build_base(size: tuple[int, int]) -> Image.Image:
    """背面→前面寄り: 全体店内 → 下部店内。"""
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
    top = lounge.crop((0, 0, lounge.size[0], cut_y))
    top_c = cover_bottom(top, W, top_h)
    base = Image.new("RGB", (W, H))
    base.paste(top_c, (0, 0))
    base.paste(bar_r, (0, top_h))
    return base


def apply_black(base: Image.Image, opacity: float) -> Image.Image:
    rgba = base.convert("RGBA")
    ov = Image.new("RGBA", base.size, (0, 0, 0, int(round(255 * opacity))))
    return Image.alpha_composite(rgba, ov)


def center_text(draw, xy, text, fnt, fill) -> None:
    x, y = xy
    bb = draw.textbbox((0, 0), text, font=fnt)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    draw.text((x - w / 2, y - h / 2), text, font=fnt, fill=fill)


def draw_content(
    canvas: Image.Image,
    logo: Image.Image,
    main_bbox: tuple[int, int, int, int],
) -> Image.Image:
    """最前面: 店ロゴ＋テキスト。メインマーク基準で赤枠に合わせる。"""
    W, H = canvas.size
    img = canvas.convert("RGBA")
    draw = ImageDraw.Draw(img)
    white = (255, 255, 255, 255)
    s = W / 1786

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

    f_label = font(JP, int(82 * s))
    f_price = font(JOSE, int(168 * s), 650)
    f_mid = font(JOSE, int(70 * s), 500)
    f_mid_jp = font(JP, int(70 * s))
    f_body = font(JP, int(86 * s))

    cx = W / 2
    y = y1 + int(H * (0.04 + TEXT_NUDGE_DOWN))
    col = int(260 * s)  # 価格が重ならないよう間隔を確保

    center_text(draw, (cx - col, y), "カウンター", f_label, white)
    center_text(draw, (cx + col, y), "ボックス", f_label, white)
    div_h = int(70 * s)
    draw.line([(cx, y - div_h // 2), (cx, y + div_h // 2)], fill=white, width=max(2, int(3 * s)))

    y += int(120 * s)
    center_text(draw, (cx - col, y), "¥3,000", f_price, white)
    center_text(draw, (cx + col, y), "¥4,000", f_price, white)

    y += int(120 * s)
    center_text(draw, (cx, y), "1SET 50分", f_mid_jp, white)
    y += int(70 * s)
    center_text(draw, (cx, y), "TAX 20%", f_mid, white)

    y += int(H * DRINK_NUDGE_DOWN) + int(90 * s)
    for line in [
        "飲み放題",
        "焼酎・ウイスキー・リキュール各種",
        "割りもの(お茶類・炭酸など)",
        "キープボトル各種あり",
    ]:
        center_text(draw, (cx, y), line, f_body, white)
        y += int(78 * s)

    return img.convert("RGB")


def main() -> None:
    logo, main_bbox = build_logo_with_petals()
    base = build_base(PREVIEW)
    # レイヤー: 全体店内→下部店内→黒塗り→ロゴ+テキスト
    final = draw_content(apply_black(base, BLACK_OPACITY), logo, main_bbox)
    preview_path = PREV / "A1_signage_preview.jpg"
    chat_path = PREV / "A1_signage_preview_chat.jpg"
    final.save(preview_path, "JPEG", quality=95, optimize=True, dpi=(96, 96))
    final.resize(CHAT, Image.Resampling.LANCZOS).save(chat_path, "JPEG", quality=92, optimize=True)
    print(f"PREVIEW ONLY: {preview_path}")
    print(
        f"petals scale={PETAL_SCALE} erode={ERODE} opacity={LARGE_PETAL_OPACITY} "
        f"/ black={BLACK_OPACITY} / ROUNGE kept"
    )


if __name__ == "__main__":
    main()
