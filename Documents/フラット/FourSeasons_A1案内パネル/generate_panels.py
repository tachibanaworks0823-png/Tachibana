#!/usr/bin/env python3
"""Four Seasons — A1縦 無料案内所パネル サンプル20案生成"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUT = ROOT / "panels"
OUT.mkdir(exist_ok=True)

# A1 portrait preview (~76 dpi of 594×841 mm)
W, H = 1786, 2529
RATIO = H / W

TEAL = (126, 200, 212)
TEAL_D = (70, 150, 165)
GOLD = (212, 185, 120)
CREAM = (245, 240, 232)
IVORY = (252, 249, 244)
CHAR = (18, 18, 20)
WARM_BLK = (22, 18, 16)
WHITE = (255, 255, 255)
SOFT_GRAY = (230, 228, 224)

FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SANS = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
FONT_SANS_R = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
FONT_JP = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
FONT_LATIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_LATIN_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

PRICE_LINES = [
    "Set 50分",
    "カウンター席  ¥3,000",
    "ボックス席    ¥4,000",
    "TAX 20%",
]
DRINK_LINES = [
    "甲類、ウイスキー、リキュール各種",
    "割りもの、お茶類、炭酸",
]


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def load_bar() -> Image.Image:
    return Image.open(ASSETS / "interior_bar.jpg").convert("RGB")


def load_sofa() -> Image.Image:
    return Image.open(ASSETS / "interior_sofa.jpg").convert("RGB")


def load_logo(kind: str = "black") -> Image.Image:
    if kind == "clear":
        return Image.open(ASSETS / "logo.png").convert("RGBA")
    return Image.open(ASSETS / "logo_black.png").convert("RGBA")


def cover_crop(im: Image.Image, tw: int, th: int, focus=(0.5, 0.45)) -> Image.Image:
    """Scale-to-cover and crop with focus point (fx, fy in 0..1)."""
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    cx, cy = int(nw * focus[0]), int(nh * focus[1])
    left = max(0, min(nw - tw, cx - tw // 2))
    top = max(0, min(nh - th, cy - th // 2))
    return im.crop((left, top, left + tw, top + th))


def fit_contain(im: Image.Image, tw: int, th: int) -> Image.Image:
    sw, sh = im.size
    scale = min(tw / sw, th / sh)
    nw, nh = max(1, int(sw * scale)), max(1, int(sh * scale))
    return im.resize((nw, nh), Image.Resampling.LANCZOS)


def paste_center(base: Image.Image, overlay: Image.Image, box, mask=None):
    x, y, w, h = box
    ov = fit_contain(overlay, w, h)
    px = x + (w - ov.width) // 2
    py = y + (h - ov.height) // 2
    if ov.mode == "RGBA":
        base.paste(ov, (px, py), ov)
    else:
        base.paste(ov, (px, py), mask)


def draw_text_center(draw, xy, text, fnt, fill, stroke_fill=None, stroke_width=0):
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(
        (x - tw / 2, y - th / 2),
        text,
        font=fnt,
        fill=fill,
        stroke_fill=stroke_fill,
        stroke_width=stroke_width,
    )


def gradient(size, c1, c2, vertical=True):
    w, h = size
    im = Image.new("RGB", size)
    px = im.load()
    for i in range(h if vertical else w):
        t = i / max(1, (h if vertical else w) - 1)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        if vertical:
            for x in range(w):
                px[x, i] = (r, g, b)
        else:
            for y in range(h):
                px[i, y] = (r, g, b)
    return im


def darken(im: Image.Image, factor=0.55) -> Image.Image:
    return ImageEnhance.Brightness(im).enhance(factor)


def vignette(im: Image.Image, strength=0.45) -> Image.Image:
    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((-w * 0.15, -h * 0.1, w * 1.15, h * 1.1), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(max(w, h) // 8))
    dark = Image.new("RGB", (w, h), (0, 0, 0))
    # blend: where mask is low, more dark
    inv = ImageEval = ImageEnhance.Brightness(mask).enhance(1)
    # Use Image.composite with darkened
    darkened = darken(im, 1 - strength)
    return Image.composite(im, darkened, mask)


def price_block(draw, x, y, w, fill=WHITE, accent=TEAL, scale=1.0, drinks=True, compact=False):
    """料金＋飲み放題メニュー。戻り値は描画後のY。"""
    title_size = int((22 if compact else 28) * scale)
    line_size = int((26 if compact else 34) * scale)
    drink_size = int((22 if compact else 28) * scale)
    gap = int((14 if compact else 22) * scale)
    f_title = font(FONT_JP, title_size)
    f_line = font(FONT_JP, line_size)
    f_drink = font(FONT_JP, drink_size)

    draw.text((x, y), "料金", font=f_title, fill=accent)
    yy = y + int(title_size * 1.55)
    for line in PRICE_LINES:
        draw.text((x, yy), line, font=f_line, fill=fill)
        bb = draw.textbbox((x, yy), line, font=f_line)
        draw.line((bb[0], bb[3] + 4, min(x + w, bb[0] + max(w * 0.85, bb[2] - bb[0] + 40)), bb[3] + 4), fill=accent, width=2)
        yy = bb[3] + gap

    if drinks:
        yy += int(8 * scale)
        draw.text((x, yy), "飲み放題メニュー", font=f_title, fill=accent)
        yy += int(title_size * 1.55)
        for line in DRINK_LINES:
            draw.text((x, yy), line, font=f_drink, fill=fill)
            bb = draw.textbbox((x, yy), line, font=f_drink)
            yy = bb[3] + int(gap * 0.85)
    return yy


def tag_label(draw, text, xy, fnt, fill=WHITE, bg=(0, 0, 0, 160)):
    # unused helper kept for clarity
    pass


def save(im: Image.Image, name: str, title: str):
    path = OUT / name
    rgb = im.convert("RGB")
    rgb.save(path, "JPEG", quality=88, optimize=True)
    print(f"  wrote {path.name} — {title}")
    return path, title


# ---------- Layouts ----------

def layout_01():
    """フルブリードバー写真・中央ロゴ帯＋料金・下ソファ"""
    canvas = Image.new("RGB", (W, H), CHAR)
    top_h = int(H * 0.52)
    canvas.paste(darken(cover_crop(load_bar(), W, top_h, (0.55, 0.4)), 0.72), (0, 0))
    mid_band = int(H * 0.22)
    sofa_h = H - top_h - mid_band
    canvas.paste(gradient((W, mid_band), (10, 12, 14), (20, 24, 28)), (0, top_h))
    paste_center(canvas, load_logo("clear"), (int(W * 0.12), top_h + 8, int(W * 0.76), int(mid_band * 0.48)))
    d = ImageDraw.Draw(canvas)
    price_block(
        d,
        int(W * 0.08),
        top_h + int(mid_band * 0.48) + 2,
        int(W * 0.84),
        fill=WHITE,
        accent=TEAL,
        scale=0.7,
        compact=True,
    )
    canvas.paste(cover_crop(load_sofa(), W, sofa_h, (0.45, 0.4)), (0, top_h + mid_band))
    return canvas


def layout_02():
    """上下二等分・中央ロゴ帯＋下料金"""
    canvas = Image.new("RGB", (W, H), CHAR)
    mid = int(H * 0.34)
    band = int(H * 0.12)
    foot = int(H * 0.24)
    canvas.paste(cover_crop(load_bar(), W, mid, (0.5, 0.4)), (0, 0))
    canvas.paste(cover_crop(load_sofa(), W, H - mid - band - foot, (0.5, 0.45)), (0, mid + band))
    canvas.paste(gradient((W, band), (12, 14, 18), (28, 36, 42)), (0, mid))
    paste_center(canvas, load_logo("clear"), (int(W * 0.18), mid + int(band * 0.08), int(W * 0.64), int(band * 0.84)))
    canvas.paste(gradient((W, foot), (14, 16, 20), (8, 10, 12)), (0, H - foot))
    d = ImageDraw.Draw(canvas)
    price_block(d, int(W * 0.08), H - foot + 20, int(W * 0.84), fill=WHITE, accent=TEAL, scale=0.9, compact=True)
    return canvas


def layout_03():
    """マガジン：ロゴ上・大バー・下ソファ＋料金"""
    canvas = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(canvas)
    paste_center(canvas, load_logo("black"), (int(W * 0.15), 40, int(W * 0.7), 180))
    d.line((int(W * 0.2), 240, int(W * 0.8), 240), fill=TEAL_D, width=2)
    draw_text_center(d, (W // 2, 275), "GIRL'S BAR  /  LOUNGE PUB SNACK", font(FONT_SANS, 26), TEAL_D)
    y0 = 310
    bar_h = int(H * 0.30)
    canvas.paste(cover_crop(load_bar(), W - 80, bar_h, (0.55, 0.42)), (40, y0))
    y1 = y0 + bar_h + 22
    sofa_h = int(H * 0.24)
    canvas.paste(cover_crop(load_sofa(), W - 80, sofa_h, (0.5, 0.45)), (40, y1))
    price_block(d, 60, y1 + sofa_h + 28, W - 120, fill=(40, 35, 30), accent=TEAL_D, scale=0.95, compact=True)
    return canvas


def layout_04():
    """黒フレーム・積層写真・価格"""
    canvas = Image.new("RGB", (W, H), CHAR)
    margin = 48
    paste_center(canvas, load_logo("clear"), (margin, 40, W - 2 * margin, 170))
    y = 230
    gap = 22
    h1 = int(H * 0.24)
    canvas.paste(cover_crop(load_bar(), W - 2 * margin, h1, (0.55, 0.4)), (margin, y))
    y += h1 + gap
    h2 = int(H * 0.22)
    canvas.paste(cover_crop(load_sofa(), W - 2 * margin, h2, (0.45, 0.4)), (margin, y))
    y += h2 + 28
    d = ImageDraw.Draw(canvas)
    price_block(d, margin + 20, y, W - 2 * margin - 40, fill=WHITE, accent=TEAL, scale=1.05, compact=True)
    return canvas


def layout_05():
    """ティールラグジュアリー"""
    canvas = gradient((W, H), (18, 48, 55), (8, 18, 22))
    d = ImageDraw.Draw(canvas)
    d.rectangle((0, 0, W, 18), fill=TEAL)
    d.rectangle((0, H - 18, W, H), fill=TEAL)
    paste_center(canvas, load_logo("clear"), (int(W * 0.12), 40, int(W * 0.76), 180))
    y = 250
    bar_h = int(H * 0.28)
    canvas.paste(cover_crop(load_bar(), W - 100, bar_h, (0.55, 0.4)), (50, y))
    y += bar_h + 28
    left_w = int(W * 0.52)
    canvas.paste(cover_crop(load_sofa(), left_w - 50, H - y - 50, (0.4, 0.45)), (50, y))
    price_block(d, left_w + 20, y + 10, W - left_w - 70, fill=WHITE, accent=TEAL, scale=0.92, compact=True)
    return canvas


def layout_06():
    """斜め分割（非対称）＋下料金帯"""
    bar = cover_crop(load_bar(), W, H, (0.55, 0.4))
    sofa = cover_crop(load_sofa(), W, H, (0.45, 0.45))
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.polygon([(0, 0), (W, 0), (W, int(H * 0.48)), (0, int(H * 0.68))], fill=255)
    canvas = Image.composite(bar, sofa, mask)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((0, int(H * 0.32), W, int(H * 0.48)), fill=(0, 0, 0, 175))
    od.rectangle((0, int(H * 0.70), W, H), fill=(0, 0, 0, 200))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    paste_center(canvas, load_logo("clear"), (int(W * 0.1), int(H * 0.34), int(W * 0.8), int(H * 0.12)))
    d = ImageDraw.Draw(canvas)
    price_block(d, int(W * 0.08), int(H * 0.73), int(W * 0.84), fill=WHITE, accent=TEAL, scale=0.95, compact=True)
    return canvas


def layout_07():
    """クリーム地・ロゴヒーロー・二枚グリッド"""
    canvas = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(canvas)
    paste_center(canvas, load_logo("black"), (int(W * 0.1), 50, int(W * 0.8), 200))
    draw_text_center(d, (W // 2, 290), "落ち着いた大人のガールズバー", font(FONT_JP, 34), (60, 55, 50))
    gap = 24
    margin = 50
    cell_w = (W - 2 * margin - gap) // 2
    cell_h = int(H * 0.32)
    y = 340
    canvas.paste(cover_crop(load_bar(), cell_w, cell_h, (0.55, 0.4)), (margin, y))
    canvas.paste(cover_crop(load_sofa(), cell_w, cell_h, (0.45, 0.4)), (margin + cell_w + gap, y))
    price_block(d, margin, y + cell_h + 36, W - 2 * margin, fill=(40, 35, 30), accent=TEAL_D, scale=1.0, compact=True)
    return canvas


def layout_08():
    """フレーム写真（額縁）＋中央ロゴ・料金"""
    canvas = gradient((W, H), (32, 28, 26), (12, 10, 10))
    margin = 60
    d = ImageDraw.Draw(canvas)
    d.rectangle((40, 40, W - 40, H - 40), outline=GOLD, width=4)
    d.rectangle((52, 52, W - 52, H - 52), outline=(90, 75, 50), width=1)
    y = 80
    h1 = int(H * 0.26)
    canvas.paste(cover_crop(load_bar(), W - 2 * margin, h1, (0.55, 0.4)), (margin, y))
    y += h1 + 20
    paste_center(canvas, load_logo("clear"), (int(W * 0.15), y, int(W * 0.7), 150))
    y += 170
    h2 = int(H * 0.22)
    canvas.paste(cover_crop(load_sofa(), W - 2 * margin, h2, (0.45, 0.45)), (margin, y))
    y += h2 + 24
    price_block(d, margin + 10, y, W - 2 * margin - 20, fill=CREAM, accent=GOLD, scale=0.95, compact=True)
    return canvas


def layout_09():
    """全面コラージュ・中央ロゴバッジ＋下料金"""
    canvas = Image.new("RGB", (W, H))
    top_h = int(H * 0.48)
    canvas.paste(cover_crop(load_bar(), W, top_h, (0.5, 0.35)), (0, 0))
    canvas.paste(cover_crop(load_sofa(), W, H - top_h, (0.5, 0.5)), (0, top_h))
    badge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(badge)
    bw, bh = int(W * 0.78), int(H * 0.16)
    bx, by = (W - bw) // 2, int(H * 0.34)
    bd.rounded_rectangle((bx, by, bx + bw, by + bh), radius=36, fill=(0, 0, 0, 205))
    bd.rectangle((0, int(H * 0.72), W, H), fill=(0, 0, 0, 200))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), badge).convert("RGB")
    paste_center(canvas, load_logo("clear"), (bx + 40, by + 16, bw - 80, bh - 32))
    d = ImageDraw.Draw(canvas)
    price_block(d, int(W * 0.08), int(H * 0.74), int(W * 0.84), fill=WHITE, accent=TEAL, scale=0.95, compact=True)
    return canvas


def layout_10():
    """左縦ストリップ写真・右情報"""
    canvas = Image.new("RGB", (W, H), IVORY)
    left_w = int(W * 0.46)
    canvas.paste(cover_crop(load_bar(), left_w, int(H * 0.5), (0.6, 0.4)), (0, 0))
    canvas.paste(cover_crop(load_sofa(), left_w, H - int(H * 0.5), (0.4, 0.45)), (0, int(H * 0.5)))
    d = ImageDraw.Draw(canvas)
    rx = left_w + 36
    paste_center(canvas, load_logo("black"), (rx, 50, W - rx - 36, 170))
    d.line((rx + 10, 250, W - 50, 250), fill=TEAL_D, width=2)
    draw_text_center(d, ((left_w + W) // 2, 295), "GIRL'S BAR", font(FONT_SANS, 30), TEAL_D)
    price_block(d, rx + 4, 340, W - rx - 50, fill=(30, 28, 26), accent=TEAL_D, scale=0.95, compact=True)
    draw_text_center(d, ((left_w + W) // 2, H - 60), "ご来店お待ちしております", font(FONT_JP, 26), (80, 70, 60))
    return canvas


def layout_11():
    """上ロゴ帯・写真スタック・下料金帯"""
    canvas = Image.new("RGB", (W, H), CHAR)
    header = int(H * 0.12)
    foot = int(H * 0.22)
    head = gradient((W, header), (20, 24, 28), (10, 12, 14))
    canvas.paste(head, (0, 0))
    paste_center(canvas, load_logo("clear"), (int(W * 0.15), 12, int(W * 0.7), header - 24))
    rest = H - header - foot
    h1 = int(rest * 0.55)
    canvas.paste(cover_crop(load_bar(), W, h1, (0.55, 0.4)), (0, header))
    canvas.paste(cover_crop(load_sofa(), W, rest - h1, (0.45, 0.45)), (0, header + h1))
    foot_im = gradient((W, foot), (14, 16, 20), (6, 8, 10))
    canvas.paste(foot_im, (0, H - foot))
    d = ImageDraw.Draw(canvas)
    price_block(d, int(W * 0.08), H - foot + 20, int(W * 0.84), fill=WHITE, accent=TEAL, scale=0.9, compact=True)
    return canvas


def layout_12():
    """円形クロップ写真＋ロゴ"""
    canvas = gradient((W, H), (245, 242, 238), (220, 228, 230))
    d = ImageDraw.Draw(canvas)
    paste_center(canvas, load_logo("black"), (int(W * 0.15), 40, int(W * 0.7), 180))

    def circle_photo(src, cx, cy, r, focus):
        photo = cover_crop(src, 2 * r, 2 * r, focus)
        mask = Image.new("L", (2 * r, 2 * r), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
        canvas.paste(photo, (cx - r, cy - r), mask)
        d.ellipse((cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4), outline=TEAL_D, width=3)

    r = int(W * 0.22)
    circle_photo(load_bar(), int(W * 0.32), int(H * 0.38), r, (0.55, 0.4))
    circle_photo(load_sofa(), int(W * 0.68), int(H * 0.52), int(r * 0.9), (0.45, 0.45))
    price_block(d, int(W * 0.1), int(H * 0.68), int(W * 0.8), fill=(40, 40, 40), accent=TEAL_D, scale=0.95, compact=True)
    return canvas


def layout_13():
    """暖色ウッドトーン（バーに合わせる）"""
    canvas = gradient((W, H), (48, 32, 22), (18, 12, 10))
    d = ImageDraw.Draw(canvas)
    d.rectangle((0, 0, W, 12), fill=GOLD)
    paste_center(canvas, load_logo("clear"), (int(W * 0.1), 40, int(W * 0.8), 170))
    y = 230
    m = 40
    h1 = int(H * 0.26)
    canvas.paste(cover_crop(load_bar(), W - 2 * m, h1, (0.55, 0.42)), (m, y))
    d.rectangle((m - 2, y - 2, W - m + 2, y + h1 + 2), outline=GOLD, width=2)
    y += h1 + 28
    h2 = int(H * 0.20)
    canvas.paste(cover_crop(load_sofa(), W - 2 * m, h2, (0.45, 0.4)), (m, y))
    y += h2 + 28
    price_block(d, m + 10, y, W - 2 * m, fill=CREAM, accent=GOLD, scale=1.0, compact=True)
    return canvas


def layout_14():
    """ナイトライフ・ネオンエッジ"""
    canvas = Image.new("RGB", (W, H), (8, 8, 14))
    d = ImageDraw.Draw(canvas)
    for i, col in enumerate([(80, 200, 255), (255, 80, 160), (120, 255, 180)]):
        d.rectangle((8 + i * 4, 8 + i * 4, W - 9 - i * 4, H - 9 - i * 4), outline=col, width=2)
    bar = darken(cover_crop(load_bar(), W - 80, int(H * 0.28), (0.55, 0.4)), 0.85)
    canvas.paste(bar, (40, 50))
    paste_center(canvas, load_logo("clear"), (int(W * 0.12), int(H * 0.32), int(W * 0.76), 160))
    sofa = darken(cover_crop(load_sofa(), W - 80, int(H * 0.22), (0.45, 0.45)), 0.9)
    canvas.paste(sofa, (40, int(H * 0.42)))
    price_block(d, 60, int(H * 0.68), W - 120, fill=WHITE, accent=TEAL, scale=0.95, compact=True)
    return canvas


def layout_15():
    """ミニマル白・インセット写真"""
    canvas = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(canvas)
    d.rectangle((30, 30, W - 30, H - 30), outline=(200, 200, 200), width=1)
    paste_center(canvas, load_logo("black"), (int(W * 0.18), 50, int(W * 0.64), 170))
    draw_text_center(d, (W // 2, 250), "GIRL'S BAR / LOUNGE PUB SNACK", font(FONT_JP, 24), (140, 140, 140))
    gap = 20
    m = 70
    h1 = int(H * 0.26)
    canvas.paste(cover_crop(load_bar(), W - 2 * m, h1, (0.55, 0.4)), (m, 290))
    y = 290 + h1 + gap
    h2 = int(H * 0.20)
    canvas.paste(cover_crop(load_sofa(), W - 2 * m, h2, (0.45, 0.45)), (m, y))
    price_block(d, m, y + h2 + 28, W - 2 * m, fill=(50, 50, 50), accent=TEAL_D, scale=0.95, compact=True)
    return canvas


def layout_16():
    """下ロゴ＋料金フッター・上写真二段"""
    canvas = Image.new("RGB", (W, H), CHAR)
    foot = int(H * 0.28)
    h_each = (H - foot) // 2
    canvas.paste(cover_crop(load_bar(), W, h_each, (0.55, 0.38)), (0, 0))
    canvas.paste(cover_crop(load_sofa(), W, h_each, (0.45, 0.45)), (0, h_each))
    foot_im = gradient((W, foot), (14, 16, 20), (6, 8, 10))
    canvas.paste(foot_im, (0, H - foot))
    paste_center(canvas, load_logo("clear"), (int(W * 0.18), H - foot + 12, int(W * 0.64), 110))
    d = ImageDraw.Draw(canvas)
    price_block(d, int(W * 0.08), H - foot + 130, int(W * 0.84), fill=WHITE, accent=TEAL, scale=0.88, compact=True)
    return canvas


def layout_17():
    """オーバーラップ写真＋ロゴ・料金"""
    canvas = gradient((W, H), (28, 26, 30), (12, 10, 14))
    bar = cover_crop(load_bar(), int(W * 0.92), int(H * 0.36), (0.55, 0.4))
    canvas.paste(bar, (int(W * 0.04), 50))
    sofa = cover_crop(load_sofa(), int(W * 0.85), int(H * 0.30), (0.45, 0.45))
    shadow = Image.new("RGBA", (sofa.width + 20, sofa.height + 20), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rectangle((10, 10, sofa.width + 10, sofa.height + 10), fill=(0, 0, 0, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    sx, sy = int(W * 0.1), int(H * 0.34)
    canvas.paste(shadow, (sx - 10, sy - 10), shadow)
    canvas.paste(sofa, (sx, sy))
    paste_center(canvas, load_logo("clear"), (int(W * 0.15), int(H * 0.66), int(W * 0.7), 120))
    d = ImageDraw.Draw(canvas)
    price_block(d, int(W * 0.08), int(H * 0.76), int(W * 0.84), fill=WHITE, accent=TEAL, scale=0.9, compact=True)
    return canvas


def layout_18():
    """和モダン縦書きアクセント"""
    canvas = Image.new("RGB", (W, H), (248, 246, 242))
    d = ImageDraw.Draw(canvas)
    d.rectangle((0, 0, 28, H), fill=TEAL_D)
    paste_center(canvas, load_logo("black"), (80, 40, W - 120, 160))
    vfont = font(FONT_JP, 38)
    text = "四季を感じる大人の空間"
    x = W - 90
    y = 260
    for ch in text:
        d.text((x, y), ch, font=vfont, fill=(50, 48, 45))
        y += 48
    m = 70
    h1 = int(H * 0.24)
    canvas.paste(cover_crop(load_bar(), W - m - 140, h1, (0.55, 0.4)), (m, 230))
    canvas.paste(cover_crop(load_sofa(), W - m - 140, h1, (0.45, 0.45)), (m, 230 + h1 + 20))
    price_block(d, m, 230 + 2 * h1 + 40, W - m - 140, fill=(40, 40, 40), accent=TEAL_D, scale=0.92, compact=True)
    return canvas


def layout_19():
    """シネマ・レターボックス＋料金フッター"""
    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    top_h = int(H * 0.10)
    foot = int(H * 0.26)
    content_h = H - top_h - foot
    gap = 12
    each = (content_h - gap) // 2
    canvas.paste(cover_crop(load_bar(), W, each, (0.55, 0.4)), (0, top_h))
    canvas.paste(cover_crop(load_sofa(), W, each, (0.45, 0.45)), (0, top_h + each + gap))
    paste_center(canvas, load_logo("clear"), (int(W * 0.18), 8, int(W * 0.64), top_h - 16))
    d = ImageDraw.Draw(canvas)
    price_block(d, int(W * 0.08), H - foot + 24, int(W * 0.84), fill=WHITE, accent=TEAL, scale=0.92, compact=True)
    return canvas


def layout_20():
    """ソフトグラデ＋料金"""
    canvas = gradient((W, H), (30, 40, 48), (12, 16, 22))
    d = ImageDraw.Draw(canvas)
    paste_center(canvas, load_logo("clear"), (int(W * 0.12), 40, int(W * 0.76), 170))
    draw_text_center(d, (W // 2, 240), "無料案内所パネル サンプル", font(FONT_JP, 28), (180, 200, 210))
    m = 50
    h1 = int(H * 0.24)
    y = 280
    canvas.paste(cover_crop(load_bar(), W - 2 * m, h1, (0.55, 0.4)), (m, y))
    y += h1 + 22
    h2 = int(H * 0.20)
    canvas.paste(cover_crop(load_sofa(), W - 2 * m, h2, (0.45, 0.45)), (m, y))
    y += h2 + 28
    price_block(d, m + 10, y, W - 2 * m - 20, fill=WHITE, accent=TEAL, scale=1.0, compact=True)
    return canvas


LAYOUTS = [
    ("01_fullbleed_logo", "フルブリード・中央ロゴ", layout_01),
    ("02_split_band", "上下分割・中央ロゴ帯", layout_02),
    ("03_magazine", "マガジン構成", layout_03),
    ("04_black_stack", "黒フレーム積層＋料金", layout_04),
    ("05_teal_luxe", "ティールラグジュアリー", layout_05),
    ("06_diagonal", "斜め分割", layout_06),
    ("07_cream_grid", "クリーム・二枚グリッド", layout_07),
    ("08_gold_frame", "ゴールド額縁", layout_08),
    ("09_collage_badge", "コラージュ中央バッジ", layout_09),
    ("10_sidebar", "左写真・右情報", layout_10),
    ("11_header_stack", "上ロゴ帯・写真スタック", layout_11),
    ("12_circles", "円形クロップ", layout_12),
    ("13_warm_wood", "暖色ウッドトーン", layout_13),
    ("14_neon_night", "ネオンナイト", layout_14),
    ("15_minimal_white", "ミニマルホワイト", layout_15),
    ("16_footer_logo", "下ロゴフッター", layout_16),
    ("17_overlap", "オーバーラップ写真", layout_17),
    ("18_jp_modern", "和モダン縦書き", layout_18),
    ("19_cinema", "シネマ・レターボックス", layout_19),
    ("20_soft_gradient", "ソフトグラデ＋料金", layout_20),
]


def make_contact_sheet(items: list[tuple[Path, str]]):
    """5×4 contact sheet of all panels."""
    cols, rows = 5, 4
    thumb_w = 360
    thumb_h = int(thumb_w * RATIO)
    pad = 16
    label_h = 36
    sheet_w = cols * thumb_w + (cols + 1) * pad
    sheet_h = rows * (thumb_h + label_h) + (rows + 1) * pad + 70
    sheet = Image.new("RGB", (sheet_w, sheet_h), (245, 245, 245))
    d = ImageDraw.Draw(sheet)
    title_f = font(FONT_JP, 32)
    d.text((pad, 20), "Four Seasons — A1縦 案内パネル サンプル20案", font=title_f, fill=(30, 30, 30))
    small = font(FONT_JP, 16)
    for i, (path, title) in enumerate(items):
        r, c = divmod(i, cols)
        # wait, 5 cols 4 rows: index i -> row = i // cols
        row, col = i // cols, i % cols
        x = pad + col * (thumb_w + pad)
        y = 70 + pad + row * (thumb_h + label_h + pad)
        im = Image.open(path).convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(im, (x, y))
        d.text((x, y + thumb_h + 6), f"{i+1:02d} {title}", font=small, fill=(50, 50, 50))
    out = ROOT / "全候補_1枚まとめ.jpg"
    sheet.save(out, "JPEG", quality=85, optimize=True)
    print(f"contact sheet -> {out}")
    return out


def make_viewer(items: list[tuple[str, str]]):
    cards = "\n".join(
        f"""    <figure>
      <img src="panels/{name}.jpg" alt="{title}" loading="lazy"/>
      <figcaption>{i:02d}. {title}</figcaption>
    </figure>"""
        for i, (name, title, _) in enumerate(LAYOUTS, start=1)
    )
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Four Seasons A1案内パネル サンプル20案</title>
<style>
  :root {{ --bg:#111; --fg:#f2f2f2; --muted:#999; --accent:#7ec8d4; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; font-family: system-ui, sans-serif; background:var(--bg); color:var(--fg); }}
  header {{ padding:24px 20px 8px; max-width:1200px; margin:0 auto; }}
  h1 {{ font-size:1.4rem; margin:0 0 6px; }}
  p {{ color:var(--muted); margin:0 0 16px; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:18px; padding:16px 20px 40px; max-width:1200px; margin:0 auto; }}
  figure {{ margin:0; background:#1a1a1a; border-radius:8px; overflow:hidden; }}
  img {{ width:100%; height:auto; display:block; aspect-ratio:594/841; object-fit:cover; }}
  figcaption {{ padding:10px 12px; font-size:0.85rem; color:var(--accent); }}
  a.summary {{ color:var(--accent); }}
</style>
</head>
<body>
<header>
  <h1>Four Seasons — A1縦 無料案内所パネル</h1>
  <p>店内写真2枚＋ロゴで作成したサンプル20案。サイズ比 A1縦（594×841）。
  <a class="summary" href="全候補_1枚まとめ.jpg">1枚まとめを見る</a></p>
</header>
<div class="grid">
{cards}
</div>
</body>
</html>
"""
    path = ROOT / "見る.html"
    path.write_text(html, encoding="utf-8")
    print(f"viewer -> {path}")


def main():
    print(f"Generating {len(LAYOUTS)} A1 panels at {W}×{H}…")
    items: list[tuple[Path, str]] = []
    for name, title, fn in LAYOUTS:
        im = fn()
        assert im.size == (W, H), f"{name} size {im.size}"
        path, _ = save(im, f"{name}.jpg", title)
        items.append((path, title))
    make_contact_sheet(items)
    make_viewer([(n, t) for n, t, _ in LAYOUTS])
    # README
    readme = ROOT / "README.md"
    readme.write_text(
        """# Four Seasons — A1縦 無料案内所パネル サンプル20案

店内写真2枚と店舗ロゴで、**A1縦（594×841mm 相当比）**の案内所掲載用パネル案を20種類作成しました。

## 素材
- `assets/interior_bar.jpg` … カウンター店内
- `assets/interior_sofa.jpg` … ソファ席店内
- `assets/logo_black.png` … 黒オーバル付きロゴ
- `assets/logo.png` … 黒背景を透過したロゴ（写真上載せ用）

## 掲載内容（全案共通）
- Girl's Bar / Lounge Pub Snack **Four Seasons**
- **料金** Set 50分 / カウンター席 ¥3,000 / ボックス席 ¥4,000 / TAX 20%
- **飲み放題メニュー** 甲類・ウイスキー・リキュール各種 / 割りもの・お茶類・炭酸

## 見方
1. **`見る.html`** をブラウザで開く
2. または **`全候補_1枚まとめ.jpg`** で20案を一望
3. 個別は `panels/XX_*.jpg`

## 再出力
```bash
cd Documents/フラット/FourSeasons_A1案内パネル
python3 generate_panels.py
```
""",
        encoding="utf-8",
    )
    print("done.")


if __name__ == "__main__":
    main()
