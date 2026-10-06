#!/usr/bin/env python3
"""A1看板プレビュー生成（本番反映前の確認用）。

本文はフォントでテキスト描画（JPEGコピー／帯ずらしはしない）。
ロゴ（花弁＋マーク）は透過PNGを配置する。
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

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

BOX = {"x0": 0.0922, "y0": 0.1240, "x1": 0.9211, "y1": 0.2920}
MAIN_SCALE_BOOST = 1.02
NUDGE_UP = 0.035
TEXT_NUDGE_DOWN = 0.035
# 以前プレビューの行間を基準に、TAX→飲み放題は視認で少し広め
TAX_TO_NOMI = 230 / 2529  # TAX → 飲み放題（以前186 + 余白）
NOMI_GAP = 150 / 2529  # 飲み放題 → 詳細1行目
LINE_GAP = 90 / 2529  # 詳細行どうし

SOURCE_LOGO = ASSETS / "logo_four_seasons_cyan_petals_source.png"
LOGO_ASSET = ASSETS / "logo_four_seasons_cyan_petals.png"
MAIN_W, MAIN_H = 364, 91
# ソフト背景花弁＋中央マーク花弁をそれぞれ一回り小さく（文字は触らない）
SOFT_PETAL_SCALE = 0.82
SOFT_PETAL_BLUR = 3.5
MARK_PETAL_SCALE = 0.82


def font(path: str, size: int, weight: int | None = None) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(path, size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f


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


def load_logo() -> Image.Image:
    """ソフト背景花弁を縮小し、赤丸の中央マーク花弁も一回り小さくする。文字は不変。"""
    src_path = SOURCE_LOGO if SOURCE_LOGO.exists() else LOGO_ASSET
    src = Image.open(src_path).convert("RGBA")
    arr = np.array(src).astype(np.float32)
    al = arr[:, :, 3]
    lum = arr[:, :, :3].mean(axis=2)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    sw, sh = src.size

    white = (lum > 155) & (al > 60)
    # 中央のソリッド花弁（赤丸のロゴマーク）
    mark = (
        (b > r + 8)
        & (g > r - 2)
        & (al > 120)
        & (lum > 100)
        & (lum < 240)
        & (~white)
    )
    mark_img_mask = Image.fromarray((mark.astype(np.uint8) * 255), "L").filter(ImageFilter.MaxFilter(3))
    mark = np.array(mark_img_mask) > 0

    # --- ソフト背景花弁 ---
    protect_soft = white | mark
    soft = arr.copy()
    soft[:, :, 3] = np.where(protect_soft, 0, al)
    soft[:, :, 3] = np.where(soft[:, :, 3] < 10, 0, soft[:, :, 3])
    soft_img = Image.fromarray(soft.astype(np.uint8), "RGBA")
    nw = max(1, int(round(sw * SOFT_PETAL_SCALE)))
    nh = max(1, int(round(sh * SOFT_PETAL_SCALE)))
    soft_s = soft_img.resize((nw, nh), Image.Resampling.LANCZOS)
    sa = np.array(soft_s.getchannel("A")).astype(np.float32)
    yy, xx = np.mgrid[0:nh, 0:nw]
    cy, cx = (nh - 1) / 2.0, (nw - 1) / 2.0
    ry, rx = max(1.0, nh * 0.48), max(1.0, nw * 0.48)
    ell = ((yy - cy) / ry) ** 2 + ((xx - cx) / rx) ** 2
    feather = np.clip(1.0 - np.maximum(0.0, ell - 0.55) / 0.45, 0.0, 1.0)
    sa *= feather
    sa_img = Image.fromarray(np.clip(sa, 0, 255).astype(np.uint8), "L")
    sa_img = sa_img.filter(ImageFilter.GaussianBlur(SOFT_PETAL_BLUR))
    soft_s.putalpha(sa_img)

    canvas = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    canvas.alpha_composite(soft_s, (int(round((sw - nw) / 2)), int(round((sh - nh) / 2))))

    c_arr = np.array(canvas).astype(np.float32)
    fade_start = int(sh * 0.48)
    fade_end = int(sh * 0.78)
    fade = np.ones(sh, np.float32)
    for y in range(sh):
        if y >= fade_end:
            fade[y] = 0.0
        elif y >= fade_start:
            t = (y - fade_start) / max(1, fade_end - fade_start)
            fade[y] = 1.0 - t
    c_arr[:, :, 3] *= fade[:, None]
    canvas = Image.fromarray(c_arr.astype(np.uint8), "RGBA")

    # --- 白文字（縮小なし） ---
    text_layer = arr.copy()
    text_layer[:, :, 3] = np.where(white, al, 0)
    canvas.alpha_composite(Image.fromarray(text_layer.astype(np.uint8), "RGBA"))

    # --- 中央マーク花弁を一回り小さく（中心基準） ---
    mb = Image.fromarray((mark.astype(np.uint8) * 255), "L").getbbox()
    if mb is not None:
        mark_rgba = arr.copy()
        mark_rgba[:, :, 3] = np.where(mark, al, 0)
        mark_img = Image.fromarray(mark_rgba.astype(np.uint8), "RGBA").crop(mb)
        mw, mh = mark_img.size
        mnw = max(1, int(round(mw * MARK_PETAL_SCALE)))
        mnh = max(1, int(round(mh * MARK_PETAL_SCALE)))
        mark_s = mark_img.resize((mnw, mnh), Image.Resampling.LANCZOS)
        # 元bbox中心へ配置
        mcx = (mb[0] + mb[2]) / 2.0
        mcy = (mb[1] + mb[3]) / 2.0
        mx = int(round(mcx - mnw / 2))
        my = int(round(mcy - mnh / 2))
        canvas.alpha_composite(mark_s, (mx, my))

    canvas.save(LOGO_ASSET)
    return canvas


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
    # 本文開始より下へ伸びるロゴ画素は捨てる（背景崩れ防止）
    max_bottom = y1 + int(H * 0.02)
    if ly + logo_r.size[1] > max_bottom:
        keep_h = max(1, max_bottom - ly)
        logo_r = logo_r.crop((0, 0, logo_r.size[0], keep_h))
    img.alpha_composite(logo_r, (lx, ly))
    return img


def center_text(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str, fnt, fill) -> None:
    x, y = xy
    bb = draw.textbbox((0, 0), text, font=fnt)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    draw.text((x - w / 2 - bb[0], y - h / 2 - bb[1]), text, font=fnt, fill=fill)


def draw_text_layer(size: tuple[int, int], logo_bottom_y: int) -> Image.Image:
    """本文だけを透明レイヤーにフォント描画する。"""
    W, H = size
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    white = (255, 255, 255, 255)
    s = W / 1786.0

    f_label = font(JP, int(82 * s))
    f_price = font(JOSE, int(168 * s), 650)
    f_mid = font(JOSE, int(70 * s), 500)
    f_mid_jp = font(JP, int(70 * s))
    f_nomi = font(JP, int(86 * s))
    f_body = font(JP, int(78 * s))

    cx = W / 2
    y = logo_bottom_y + int(H * (0.04 + TEXT_NUDGE_DOWN))
    # 基準プレビューの価格中心（canvas中央から約330px）に合わせる
    col_label = int(260 * s)
    col_price = int(330 * s)

    center_text(draw, (cx - col_label, y), "カウンター", f_label, white)
    center_text(draw, (cx + col_label, y), "ボックス", f_label, white)
    div_h = int(70 * s)
    draw.line([(cx, y - div_h // 2), (cx, y + div_h // 2)], fill=white, width=max(2, int(3 * s)))

    y += int(120 * s)
    center_text(draw, (cx - col_price, y), "¥3,000", f_price, white)
    center_text(draw, (cx + col_price, y), "¥4,000", f_price, white)

    y += int(120 * s)
    center_text(draw, (cx, y), "1SET 50分", f_mid_jp, white)
    y += int(70 * s)
    center_text(draw, (cx, y), "TAX 20%", f_mid, white)

    y += int(H * TAX_TO_NOMI)
    center_text(draw, (cx, y), "飲み放題", f_nomi, white)

    y += int(H * NOMI_GAP)
    for line in [
        "焼酎・ウイスキー・リキュール各種",
        "割りもの(お茶類・炭酸など)",
        "キープボトル各種あり",
    ]:
        center_text(draw, (cx, y), line, f_body, white)
        y += int(H * LINE_GAP)

    return layer


def soft_text_glow(text_layer: Image.Image) -> Image.Image:
    """視認用の軽い外側グロー（テキスト自体はシャープなまま）。"""
    alpha = text_layer.getchannel("A")
    glow = alpha.filter(ImageFilter.GaussianBlur(5))
    glow = glow.point(lambda p: min(255, int(p * 0.45)))
    glow_rgba = Image.merge(
        "RGBA",
        (
            Image.new("L", text_layer.size, 255),
            Image.new("L", text_layer.size, 255),
            Image.new("L", text_layer.size, 255),
            glow,
        ),
    )
    out = Image.new("RGBA", text_layer.size, (0, 0, 0, 0))
    out = Image.alpha_composite(out, glow_rgba)
    out = Image.alpha_composite(out, text_layer)
    return out


def render_body_text(size: tuple[int, int], logo_bottom_y: int) -> Image.Image:
    """本文を2倍解像度で描画してから縮小し、シャープなテキストレイヤーにする。"""
    W, H = size
    hi = (W * 2, H * 2)
    layer_hi = draw_text_layer(hi, logo_bottom_y * 2)
    layer_hi = soft_text_glow(layer_hi)
    return layer_hi.resize(size, Image.Resampling.LANCZOS)


def main() -> None:
    logo = load_logo()
    main_bbox = main_bbox_in_logo(logo)
    canvas = apply_black(build_base(PREVIEW), BLACK_OPACITY)
    with_logo = place_logo(canvas, logo, main_bbox)

    y1 = int(round(BOX["y1"] * PREVIEW[1]))
    text_layer = render_body_text(PREVIEW, y1)
    final = Image.alpha_composite(with_logo.convert("RGBA"), text_layer).convert("RGB")

    preview_path = PREV / "A1_signage_preview.jpg"
    chat_path = PREV / "A1_signage_preview_chat.jpg"
    final.save(preview_path, "JPEG", quality=95, optimize=True, dpi=(96, 96))
    final.resize(CHAT, Image.Resampling.LANCZOS).save(chat_path, "JPEG", quality=92, optimize=True)
    print(f"PREVIEW ONLY: {preview_path}")
    print(
        f"soft={SOFT_PETAL_SCALE} mark-petals={MARK_PETAL_SCALE} "
        f"/ body text = font layers / logo mark unchanged"
    )


if __name__ == "__main__":
    main()
