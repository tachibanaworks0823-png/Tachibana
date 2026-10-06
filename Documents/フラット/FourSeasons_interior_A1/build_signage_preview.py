#!/usr/bin/env python3
"""A1看板プレビュー生成（本番反映前の確認用）。"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUT = ROOT / "output"
FONTS = ASSETS / "fonts"
PREV = OUT / "preview"
PREV.mkdir(exist_ok=True)

PLAY = str(FONTS / "PlayfairDisplay[wght].ttf")
JOSE = str(FONTS / "JosefinSans[wght].ttf")
JP = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"

PREVIEW = (1786, 2529)
CHAT = (900, 1274)
BLACK_OPACITY = 0.62  # プレビュー値。承認後に本番調整可


def font(path: str, size: int, weight: int | None = None) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(path, size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f


def build_logo() -> Image.Image:
    """店ロゴ原寸を使用。白枠内の黒プレートを切り出し、黒背景のみ透過。

    文字・花びらは再描画せず元ピクセルを保持（参考画像と同じ見た目）。
    ※元データは ROUNGE 表記。LOUNGE 修正は別途確認のうえ実施。
    """
    from PIL import ImageFilter, ImageOps

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
    logo.save(PREV / "logo_transparent_preview.png")
    return logo


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


def draw_content(canvas: Image.Image, logo: Image.Image) -> Image.Image:
    """最前面: 店ロゴ＋テキスト。"""
    W, H = canvas.size
    img = canvas.convert("RGBA")
    draw = ImageDraw.Draw(img)
    white = (255, 255, 255, 255)
    s = W / 1786

    logo_w = int(W * 0.72)
    logo_r = logo.resize(
        (logo_w, max(1, int(logo.size[1] * logo_w / logo.size[0]))),
        Image.Resampling.LANCZOS,
    )
    img.alpha_composite(logo_r, ((W - logo_r.size[0]) // 2, int(H * 0.055)))

    f_label = font(JP, int(50 * s))
    f_price = font(JOSE, int(108 * s), 650)
    f_mid = font(JOSE, int(46 * s), 500)
    f_mid_jp = font(JP, int(46 * s))
    f_body = font(JP, int(40 * s))

    cx = W / 2
    y = int(H * 0.36)
    col = int(140 * s)

    center_text(draw, (cx - col, y), "カウンター", f_label, white)
    center_text(draw, (cx + col, y), "ボックス", f_label, white)
    div_h = int(52 * s)
    draw.line([(cx, y - div_h // 2), (cx, y + div_h // 2)], fill=white, width=max(2, int(3 * s)))

    y += int(95 * s)
    center_text(draw, (cx - col, y), "¥3,000", f_price, white)
    center_text(draw, (cx + col, y), "¥4,000", f_price, white)

    y += int(105 * s)
    center_text(draw, (cx, y), "1SET 50分", f_mid_jp, white)
    y += int(56 * s)
    center_text(draw, (cx, y), "TAX 20%", f_mid, white)

    y += int(78 * s)
    for line in [
        "飲み放題",
        "焼酎・ウイスキー・リキュール各種",
        "割りもの(お茶類・炭酸など)",
        "キープボトル各種あり",
    ]:
        center_text(draw, (cx, y), line, f_body, white)
        y += int(54 * s)

    return img.convert("RGB")


def main() -> None:
    logo = build_logo()
    base = build_base(PREVIEW)
    # レイヤー: 全体店内→下部店内→黒塗り→ロゴ+テキスト
    final = draw_content(apply_black(base, BLACK_OPACITY), logo)
    preview_path = PREV / "A1_signage_preview.jpg"
    chat_path = PREV / "A1_signage_preview_chat.jpg"
    final.save(preview_path, "JPEG", quality=95, optimize=True, dpi=(96, 96))
    final.resize(CHAT, Image.Resampling.LANCZOS).save(chat_path, "JPEG", quality=92, optimize=True)
    print(f"PREVIEW ONLY: {preview_path}")
    print(f"layers OK / black_opacity={BLACK_OPACITY} / no karaoke / LOUNGE")


if __name__ == "__main__":
    main()
