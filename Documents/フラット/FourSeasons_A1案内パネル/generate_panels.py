#!/usr/bin/env python3
"""Four Seasons — ガールズスナック向け A1縦 おしゃれ案内パネル 20案"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
FONTS_DIR = ASSETS / "fonts"
OUT = ROOT / "panels"
OUT.mkdir(exist_ok=True)

W, H = 1786, 2529
RATIO = H / W

# Palette — soft glam, not neon-club / not template-menu
BLUSH = (232, 176, 168)
ROSE = (196, 120, 118)
CHAMP = (214, 188, 150)
PEARL = (248, 244, 240)
IVORY = (255, 250, 246)
INK = (28, 24, 26)
SOFT_BLK = (16, 14, 16)
WINE = (92, 36, 48)
MIST = (232, 228, 224)
TEAL_SOFT = (150, 186, 190)
WHITE = (255, 255, 255)

FONT_PLAY = str(FONTS_DIR / "PlayfairDisplay[wght].ttf")
FONT_PLAY_I = str(FONTS_DIR / "PlayfairDisplay-Italic[wght].ttf")
FONT_JOSE = str(FONTS_DIR / "JosefinSans[wght].ttf")
FONT_CORM = str(FONTS_DIR / "CormorantGaramond[wght].ttf")
FONT_SCRIPT = str(FONTS_DIR / "GreatVibes-Regular.ttf")
FONT_JP = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"

PRICE = [
    ("Set 50分", ""),
    ("カウンター席", "¥3,000"),
    ("ボックス席", "¥4,000"),
]
DRINKS = "甲類・ウイスキー・リキュール各種 ／ 割りもの・お茶・炭酸"


def F(path: str, size: int, weight: int | None = None) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(path, size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f


def load_bar() -> Image.Image:
    return Image.open(ASSETS / "interior_bar.jpg").convert("RGB")


def load_sofa() -> Image.Image:
    return Image.open(ASSETS / "interior_sofa.jpg").convert("RGB")


def load_logo(kind: str = "clear") -> Image.Image:
    name = "logo.png" if kind == "clear" else "logo_black.png"
    return Image.open(ASSETS / name).convert("RGBA")


def cover(im: Image.Image, tw: int, th: int, focus=(0.5, 0.42)) -> Image.Image:
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    cx, cy = int(nw * focus[0]), int(nh * focus[1])
    left = max(0, min(nw - tw, cx - tw // 2))
    top = max(0, min(nh - th, cy - th // 2))
    return im.crop((left, top, left + tw, top + th))


def contain(im: Image.Image, tw: int, th: int) -> Image.Image:
    sw, sh = im.size
    s = min(tw / sw, th / sh)
    return im.resize((max(1, int(sw * s)), max(1, int(sh * s))), Image.Resampling.LANCZOS)


def paste_c(base: Image.Image, ov: Image.Image, box):
    x, y, w, h = box
    o = contain(ov, w, h)
    px, py = x + (w - o.width) // 2, y + (h - o.height) // 2
    if o.mode == "RGBA":
        base.paste(o, (px, py), o)
    else:
        base.paste(o, (px, py))


def grad(size, c1, c2, vertical=True):
    w, h = size
    im = Image.new("RGB", size)
    px = im.load()
    n = (h if vertical else w) - 1 or 1
    for i in range(h if vertical else w):
        t = i / n
        rgb = tuple(int(c1[j] + (c2[j] - c1[j]) * t) for j in range(3))
        if vertical:
            for x in range(w):
                px[x, i] = rgb
        else:
            for y in range(h):
                px[i, y] = rgb
    return im


def soft(im: Image.Image, b=0.88, c=1.05) -> Image.Image:
    im = ImageEnhance.Brightness(im).enhance(b)
    return ImageEnhance.Color(im).enhance(c)


def veil(base: Image.Image, box, color=(0, 0, 0), alpha=120):
    """Soft translucent rectangle overlay."""
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle((x0, y0, x1, y1), fill=(*color, alpha))
    out = Image.alpha_composite(base.convert("RGBA"), layer)
    return out.convert("RGB")


def text_c(draw, xy, text, fnt, fill, stroke=None, sw=0):
    x, y = xy
    bb = draw.textbbox((0, 0), text, font=fnt)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    draw.text((x - tw / 2, y - th / 2), text, font=fnt, fill=fill, stroke_width=sw, stroke_fill=stroke)


def hairline(draw, y, x0, x1, fill, width=1):
    draw.line((x0, y, x1, y), fill=fill, width=width)


def chic_price(draw, x, y, w, fill=WHITE, accent=BLUSH, scale=1.0, center=False):
    """Refined price block — fashion editorial style, not menu dump."""
    f_label = F(FONT_JOSE, int(22 * scale), 300)
    f_jp = F(FONT_JP, int(28 * scale))
    f_num = F(FONT_PLAY, int(34 * scale), 500)
    f_tiny = F(FONT_JOSE, int(18 * scale), 300)

    draw.text((x, y), "料金", font=F(FONT_JP, int(24 * scale)), fill=accent)
    yy = y + int(36 * scale)
    hairline(draw, yy, x, x + int(w * 0.35), accent, 1)
    yy += int(20 * scale)

    for label, price in PRICE:
        if center:
            line = f"{label}  {price}".strip()
            text_c(draw, (x + w // 2, yy + int(14 * scale)), line, f_jp, fill)
            yy += int(44 * scale)
        else:
            draw.text((x, yy), label, font=f_jp, fill=fill)
            if price:
                bb = draw.textbbox((0, 0), price, font=f_num)
                draw.text((x + w - (bb[2] - bb[0]), yy - 2), price, font=f_num, fill=fill)
            yy += int(46 * scale)

    draw.text((x, yy + int(4 * scale)), "TAX 20%", font=f_tiny, fill=accent)
    yy += int(36 * scale)
    hairline(draw, yy, x, x + int(w * 0.35), accent, 1)
    yy += int(16 * scale)
    draw.text((x, yy), "飲み放題", font=F(FONT_JP, int(22 * scale)), fill=accent)
    yy += int(30 * scale)
    f_d = F(FONT_JP, int(21 * scale))
    draw.text((x, yy), DRINKS, font=f_d, fill=fill)
    return yy + int(28 * scale)


def save(im: Image.Image, name: str, title: str):
    path = OUT / name
    im.convert("RGB").save(path, "JPEG", quality=90, optimize=True)
    print(f"  {name} — {title}")
    return path, title


# ===================== 20 chic layouts =====================

def L01():
    """フルブリード夜景・中央セリフブランド"""
    canvas = soft(cover(load_bar(), W, H, (0.55, 0.4)), 0.55, 1.1)
    canvas = veil(canvas, (0, int(H * 0.28), W, int(H * 0.72)), (10, 8, 10), 140)
    d = ImageDraw.Draw(canvas)
    text_c(d, (W // 2, int(H * 0.34)), "GIRLS SNACK", F(FONT_JOSE, 28, 300), BLUSH)
    paste_c(canvas, load_logo("clear"), (int(W * 0.14), int(H * 0.38), int(W * 0.72), int(H * 0.14)))
    text_c(d, (W // 2, int(H * 0.58)), "大人のための、静かな夜。", F(FONT_JP, 32), PEARL)
    hairline(d, int(H * 0.63), int(W * 0.35), int(W * 0.65), CHAMP, 1)
    chic_price(d, int(W * 0.18), int(H * 0.68), int(W * 0.64), fill=PEARL, accent=BLUSH, scale=1.05)
    return canvas


def L02():
    """blush サイドパネル・写真大"""
    canvas = Image.new("RGB", (W, H), (244, 228, 224))
    photo_w = int(W * 0.62)
    canvas.paste(soft(cover(load_bar(), photo_w, int(H * 0.52), (0.55, 0.4)), 0.95), (0, 0))
    canvas.paste(soft(cover(load_sofa(), photo_w, H - int(H * 0.52), (0.45, 0.45)), 0.95), (0, int(H * 0.52)))
    d = ImageDraw.Draw(canvas)
    rx = photo_w + 36
    paste_c(canvas, load_logo("black"), (rx, 80, W - rx - 40, 160))
    text_c(d, ((photo_w + W) // 2, 300), "Girls Snack", F(FONT_SCRIPT, 52), ROSE)
    chic_price(d, rx + 8, 380, W - rx - 60, fill=INK, accent=ROSE, scale=0.95)
    text_c(d, ((photo_w + W) // 2, H - 70), "ご来店お待ちしております", F(FONT_JP, 22), ROSE)
    return canvas


def L03():
    """エディトリアル白・大写真1枚＋小"""
    canvas = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(canvas)
    text_c(d, (W // 2, 70), "FOUR SEASONS", F(FONT_JOSE, 26, 300), ROSE)
    paste_c(canvas, load_logo("black"), (int(W * 0.2), 100, int(W * 0.6), 140))
    m = 60
    canvas.paste(soft(cover(load_bar(), W - 2 * m, int(H * 0.38), (0.55, 0.4)), 0.98), (m, 270))
    # two small under
    gap = 20
    sw = (W - 2 * m - gap) // 2
    y = 270 + int(H * 0.38) + 24
    canvas.paste(soft(cover(load_sofa(), sw, int(H * 0.22), (0.4, 0.4)), 0.98), (m, y))
    # elegant quote panel instead of second small photo duplicate - use sofa crop different
    canvas.paste(soft(cover(load_sofa(), sw, int(H * 0.22), (0.7, 0.5)), 0.98), (m + sw + gap, y))
    chic_price(d, m + 20, y + int(H * 0.22) + 40, W - 2 * m - 40, fill=INK, accent=ROSE, scale=1.0)
    return canvas


def L04():
    """ワインカラーラグジュアリー"""
    canvas = grad((W, H), (60, 22, 34), (22, 10, 16))
    d = ImageDraw.Draw(canvas)
    d.rectangle((40, 40, W - 40, H - 40), outline=CHAMP, width=1)
    paste_c(canvas, load_logo("clear"), (int(W * 0.15), 70, int(W * 0.7), 150))
    text_c(d, (W // 2, 250), "Quiet nights, soft lights.", F(FONT_PLAY_I, 34, 400), CHAMP)
    y = 300
    canvas.paste(soft(cover(load_bar(), W - 160, int(H * 0.28), (0.55, 0.4)), 0.9), (80, y))
    y += int(H * 0.28) + 24
    canvas.paste(soft(cover(load_sofa(), W - 160, int(H * 0.24), (0.45, 0.45)), 0.9), (80, y))
    chic_price(d, 100, y + int(H * 0.24) + 36, W - 200, fill=PEARL, accent=CHAMP, scale=1.0)
    return canvas


def L05():
    """フルブリードソファ・下部グラス帯"""
    canvas = soft(cover(load_sofa(), W, H, (0.45, 0.4)), 0.62, 1.05)
    canvas = veil(canvas, (0, 0, W, int(H * 0.22)), (255, 250, 246), 40)
    canvas = veil(canvas, (0, int(H * 0.62), W, H), (20, 14, 16), 170)
    d = ImageDraw.Draw(canvas)
    paste_c(canvas, load_logo("clear"), (int(W * 0.16), 60, int(W * 0.68), 150))
    text_c(d, (W // 2, 240), "GIRLS SNACK  ·  LOUNGE", F(FONT_JOSE, 24, 300), WHITE)
    # tiny bar strip
    bar_strip = soft(cover(load_bar(), W, int(H * 0.16), (0.55, 0.45)), 0.85)
    canvas.paste(bar_strip, (0, int(H * 0.48)))
    chic_price(d, int(W * 0.14), int(H * 0.68), int(W * 0.72), fill=PEARL, accent=BLUSH, scale=1.05)
    return canvas


def L06():
    """非対称マガジン（大＋縦帯）"""
    canvas = Image.new("RGB", (W, H), PEARL)
    # large left photo
    lw = int(W * 0.68)
    canvas.paste(soft(cover(load_bar(), lw, int(H * 0.58), (0.55, 0.4)), 0.96), (0, 0))
    # right blush column
    d = ImageDraw.Draw(canvas)
    d.rectangle((lw, 0, W, int(H * 0.58)), fill=(236, 210, 204))
    # vertical text
    v = "GIRLS SNACK"
    f = F(FONT_JOSE, 28, 300)
    y = 80
    for ch in v:
        text_c(d, ((lw + W) // 2, y), ch, f, ROSE)
        y += 42
    # bottom sofa full width
    canvas.paste(soft(cover(load_sofa(), W, int(H * 0.22), (0.45, 0.45)), 0.96), (0, int(H * 0.58)))
    paste_c(canvas, load_logo("black"), (int(W * 0.25), int(H * 0.58) + int(H * 0.22) + 20, int(W * 0.5), 110))
    chic_price(d, int(W * 0.12), int(H * 0.58) + int(H * 0.22) + 140, int(W * 0.76), fill=INK, accent=ROSE, scale=0.9)
    return canvas


def L07():
    """シャンパンゴールド・フレームレス"""
    canvas = grad((W, H), (36, 30, 28), (18, 16, 16))
    d = ImageDraw.Draw(canvas)
    text_c(d, (W // 2, 80), "Four Seasons", F(FONT_SCRIPT, 72), CHAMP)
    text_c(d, (W // 2, 160), "GIRLS SNACK", F(FONT_JOSE, 22, 300), BLUSH)
    paste_c(canvas, load_logo("clear"), (int(W * 0.22), 190, int(W * 0.56), 120))
    y = 340
    for src, foc, hh in [(load_bar, (0.55, 0.4), 0.30), (load_sofa, (0.45, 0.45), 0.26)]:
        ph = int(H * hh)
        canvas.paste(soft(cover(src(), W - 120, ph, foc), 0.92), (60, y))
        y += ph + 28
    chic_price(d, 80, y + 10, W - 160, fill=PEARL, accent=CHAMP, scale=1.0)
    return canvas


def L08():
    """パール地・中央アーチ感（角丸なしで余白構成）"""
    canvas = Image.new("RGB", (W, H), (250, 246, 242))
    d = ImageDraw.Draw(canvas)
    # soft top wash
    top = grad((W, 280), (240, 220, 216), (250, 246, 242))
    canvas.paste(top, (0, 0))
    paste_c(canvas, load_logo("black"), (int(W * 0.18), 50, int(W * 0.64), 150))
    text_c(d, (W // 2, 230), "今夜は、少し贅沢な時間を。", F(FONT_JP, 30), ROSE)
    # stacked photos with wide margins
    m = 100
    canvas.paste(soft(cover(load_bar(), W - 2 * m, int(H * 0.32), (0.55, 0.4)), 1.0), (m, 290))
    canvas.paste(soft(cover(load_sofa(), W - 2 * m, int(H * 0.26), (0.45, 0.45)), 1.0), (m, 290 + int(H * 0.32) + 28))
    chic_price(d, m + 10, 290 + int(H * 0.32) + 28 + int(H * 0.26) + 36, W - 2 * m - 20, fill=INK, accent=ROSE, scale=0.95)
    return canvas


def L09():
    """写真全面・タイポ最小・料金フッター細帯"""
    canvas = soft(cover(load_bar(), W, int(H * 0.7), (0.55, 0.38)), 0.7, 1.08)
    bottom = soft(cover(load_sofa(), W, H - int(H * 0.7), (0.5, 0.45)), 0.75)
    full = Image.new("RGB", (W, H))
    full.paste(canvas, (0, 0))
    full.paste(bottom, (0, int(H * 0.7)))
    full = veil(full, (0, int(H * 0.55), W, H), (12, 10, 12), 160)
    d = ImageDraw.Draw(full)
    paste_c(full, load_logo("clear"), (int(W * 0.2), int(H * 0.58), int(W * 0.6), 130))
    text_c(d, (W // 2, int(H * 0.68)), "Girls Snack  Four Seasons", F(FONT_PLAY_I, 28, 400), BLUSH)
    chic_price(d, int(W * 0.14), int(H * 0.72), int(W * 0.72), fill=PEARL, accent=CHAMP, scale=0.92)
    return full


def L10():
    """ローズミスト・二段カードレス"""
    canvas = grad((W, H), (248, 236, 232), (236, 220, 216))
    d = ImageDraw.Draw(canvas)
    text_c(d, (W // 2, 60), "seasonal lounge", F(FONT_JOSE, 20, 300), ROSE)
    paste_c(canvas, load_logo("black"), (int(W * 0.16), 90, int(W * 0.68), 150))
    # photos edge to edge almost
    y = 270
    canvas.paste(soft(cover(load_bar(), W, int(H * 0.3), (0.55, 0.4)), 0.97), (0, y))
    y += int(H * 0.3) + 8
    canvas.paste(soft(cover(load_sofa(), W, int(H * 0.26), (0.45, 0.45)), 0.97), (0, y))
    # info on soft panel
    info_y = y + int(H * 0.26) + 20
    chic_price(d, int(W * 0.12), info_y, int(W * 0.76), fill=INK, accent=ROSE, scale=1.0)
    return canvas


def L11():
    """モノトーン＋ブラッシュアクセント"""
    canvas = Image.new("RGB", (W, H), SOFT_BLK)
    d = ImageDraw.Draw(canvas)
    # accent line
    d.rectangle((0, 0, 10, H), fill=BLUSH)
    paste_c(canvas, load_logo("clear"), (80, 60, W - 120, 150))
    text_c(d, (W // 2 + 20, 240), "大人ガールズスナック", F(FONT_JP, 28), BLUSH)
    y = 290
    canvas.paste(soft(cover(load_bar(), W - 100, int(H * 0.3), (0.55, 0.4)), 0.85), (70, y))
    y += int(H * 0.3) + 20
    canvas.paste(soft(cover(load_sofa(), W - 100, int(H * 0.26), (0.45, 0.45)), 0.85), (70, y))
    chic_price(d, 80, y + int(H * 0.26) + 30, W - 160, fill=PEARL, accent=BLUSH, scale=1.0)
    return canvas


def L12():
    """縦半分スプリット（写真／タイポ）"""
    canvas = Image.new("RGB", (W, H), IVORY)
    left = int(W * 0.52)
    canvas.paste(soft(cover(load_bar(), left, int(H * 0.5), (0.6, 0.4)), 0.95), (0, 0))
    canvas.paste(soft(cover(load_sofa(), left, H - int(H * 0.5), (0.4, 0.45)), 0.95), (0, int(H * 0.5)))
    d = ImageDraw.Draw(canvas)
    rx = left + 30
    text_c(d, ((left + W) // 2, 100), "Four", F(FONT_PLAY, 64, 500), ROSE)
    text_c(d, ((left + W) // 2, 170), "Seasons", F(FONT_PLAY, 64, 500), ROSE)
    paste_c(canvas, load_logo("black"), (rx, 220, W - rx - 30, 120))
    text_c(d, ((left + W) // 2, 380), "Girls Snack", F(FONT_SCRIPT, 48), ROSE)
    hairline(d, 440, rx + 20, W - 50, BLUSH, 1)
    chic_price(d, rx + 10, 480, W - rx - 50, fill=INK, accent=ROSE, scale=0.95)
    return canvas


def L13():
    """夜のシフォン — 暗め写真＋手書き感キャッチ"""
    canvas = soft(cover(load_bar(), W, H, (0.5, 0.4)), 0.45, 1.15)
    canvas = veil(canvas, (int(W * 0.08), int(H * 0.2), int(W * 0.92), int(H * 0.85)), (8, 6, 8), 150)
    d = ImageDraw.Draw(canvas)
    text_c(d, (W // 2, int(H * 0.28)), "Tonight", F(FONT_SCRIPT, 90), BLUSH)
    paste_c(canvas, load_logo("clear"), (int(W * 0.18), int(H * 0.36), int(W * 0.64), 140))
    # inset sofa
    inset = soft(cover(load_sofa(), int(W * 0.7), int(H * 0.18), (0.45, 0.45)), 0.9)
    canvas.paste(inset, ((W - inset.width) // 2, int(H * 0.52)))
    chic_price(d, int(W * 0.16), int(H * 0.74), int(W * 0.68), fill=PEARL, accent=BLUSH, scale=0.95)
    return canvas


def L14():
    """ミント×ブラッシュ（ロゴ葉色を活かす）"""
    canvas = grad((W, H), (236, 242, 240), (248, 236, 232))
    d = ImageDraw.Draw(canvas)
    paste_c(canvas, load_logo("black"), (int(W * 0.18), 50, int(W * 0.64), 150))
    text_c(d, (W // 2, 230), "soft night  ·  girls snack", F(FONT_JOSE, 24, 300), TEAL_SOFT)
    m = 50
    # overlapping feel via offset
    canvas.paste(soft(cover(load_bar(), W - 2 * m - 40, int(H * 0.32), (0.55, 0.4)), 0.98), (m, 280))
    canvas.paste(soft(cover(load_sofa(), W - 2 * m - 40, int(H * 0.28), (0.45, 0.45)), 0.98), (m + 40, 280 + int(H * 0.32) + 16))
    chic_price(d, m + 20, 280 + int(H * 0.32) + 16 + int(H * 0.28) + 30, W - 2 * m - 40, fill=INK, accent=TEAL_SOFT, scale=0.95)
    return canvas


def L15():
    """ハイファッション余白・写真は下半分"""
    canvas = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(canvas)
    text_c(d, (W // 2, 120), "Four Seasons", F(FONT_PLAY, 70, 600), INK)
    text_c(d, (W // 2, 200), "Girls Snack", F(FONT_SCRIPT, 56), ROSE)
    hairline(d, 250, int(W * 0.3), int(W * 0.7), BLUSH, 1)
    text_c(d, (W // 2, 300), "カウンターとボックス、ふたつの時間。", F(FONT_JP, 26), (90, 70, 70))
    paste_c(canvas, load_logo("black"), (int(W * 0.25), 340, int(W * 0.5), 100))
    # dual photos bottom
    y = 480
    gap = 16
    each = (H - y - 280) // 2
    canvas.paste(soft(cover(load_bar(), W, each, (0.55, 0.4)), 0.98), (0, y))
    canvas.paste(soft(cover(load_sofa(), W, each, (0.45, 0.45)), 0.98), (0, y + each + gap))
    chic_price(d, int(W * 0.12), y + 2 * each + gap + 20, int(W * 0.76), fill=INK, accent=ROSE, scale=0.9)
    return canvas


def L16():
    """ダークシネマなし・ぼかし背景＋クリア前景"""
    bg = soft(cover(load_bar(), W, H, (0.5, 0.4)), 0.4, 1.2).filter(ImageFilter.GaussianBlur(18))
    canvas = bg
    # sharp foreground photos
    fw, fh = int(W * 0.84), int(H * 0.28)
    p1 = soft(cover(load_bar(), fw, fh, (0.55, 0.4)), 0.95)
    p2 = soft(cover(load_sofa(), fw, fh, (0.45, 0.45)), 0.95)
    canvas.paste(p1, ((W - fw) // 2, int(H * 0.22)))
    canvas.paste(p2, ((W - fw) // 2, int(H * 0.22) + fh + 20))
    canvas = veil(canvas, (0, 0, W, int(H * 0.2)), (0, 0, 0), 80)
    d = ImageDraw.Draw(canvas)
    paste_c(canvas, load_logo("clear"), (int(W * 0.18), 40, int(W * 0.64), 140))
    canvas = veil(canvas, (0, int(H * 0.72), W, H), (12, 10, 12), 180)
    d = ImageDraw.Draw(canvas)
    chic_price(d, int(W * 0.14), int(H * 0.74), int(W * 0.72), fill=PEARL, accent=BLUSH, scale=0.95)
    return canvas


def L17():
    """ストリップコラージュおしゃれ"""
    canvas = Image.new("RGB", (W, H), (20, 16, 18))
    # three horizontal strips alternating
    h1, h2, h3 = int(H * 0.28), int(H * 0.22), int(H * 0.22)
    canvas.paste(soft(cover(load_bar(), W, h1, (0.55, 0.35)), 0.9), (0, 0))
    # middle brand band
    band = grad((W, int(H * 0.16)), (40, 28, 30), (24, 18, 20))
    canvas.paste(band, (0, h1))
    paste_c(canvas, load_logo("clear"), (int(W * 0.18), h1 + 20, int(W * 0.64), int(H * 0.12)))
    canvas.paste(soft(cover(load_sofa(), W, h2, (0.45, 0.45)), 0.9), (0, h1 + int(H * 0.16)))
    y = h1 + int(H * 0.16) + h2
    # bottom info on dark
    d = ImageDraw.Draw(canvas)
    text_c(d, (W // 2, y + 40), "Girls Snack", F(FONT_SCRIPT, 48), BLUSH)
    chic_price(d, int(W * 0.14), y + 90, int(W * 0.72), fill=PEARL, accent=CHAMP, scale=0.95)
    return canvas


def L18():
    """和モダンではなくフレンチシック縦書き風"""
    canvas = Image.new("RGB", (W, H), (252, 248, 244))
    d = ImageDraw.Draw(canvas)
    d.rectangle((0, 0, 16, H), fill=ROSE)
    paste_c(canvas, load_logo("black"), (60, 50, W - 160, 140))
    # vertical phrase
    phrase = "華やかな夜に"
    f = F(FONT_JP, 36)
    x = W - 80
    y = 220
    for ch in phrase:
        d.text((x, y), ch, font=f, fill=ROSE)
        y += 48
    m = 60
    canvas.paste(soft(cover(load_bar(), W - m - 120, int(H * 0.28), (0.55, 0.4)), 0.98), (m, 220))
    canvas.paste(soft(cover(load_sofa(), W - m - 120, int(H * 0.26), (0.45, 0.45)), 0.98), (m, 220 + int(H * 0.28) + 20))
    chic_price(d, m, 220 + int(H * 0.28) + 20 + int(H * 0.26) + 30, W - m - 120, fill=INK, accent=ROSE, scale=0.95)
    return canvas


def L19():
    """コントラスト強め・白抜きタイポ on 写真"""
    top = soft(cover(load_bar(), W, int(H * 0.55), (0.55, 0.4)), 0.6, 1.1)
    bot = soft(cover(load_sofa(), W, H - int(H * 0.55), (0.45, 0.45)), 0.65, 1.05)
    canvas = Image.new("RGB", (W, H))
    canvas.paste(top, (0, 0))
    canvas.paste(bot, (0, int(H * 0.55)))
    canvas = veil(canvas, (0, int(H * 0.35), W, int(H * 0.62)), (0, 0, 0), 130)
    d = ImageDraw.Draw(canvas)
    text_c(d, (W // 2, int(H * 0.4)), "GIRLS SNACK", F(FONT_JOSE, 30, 300), BLUSH)
    paste_c(canvas, load_logo("clear"), (int(W * 0.14), int(H * 0.44), int(W * 0.72), 140))
    chic_price(d, int(W * 0.14), int(H * 0.72), int(W * 0.72), fill=WHITE, accent=BLUSH, scale=1.0)
    return canvas


def L20():
    """ブティックポスター — 上余白タイポ、下写真コラージュ"""
    canvas = grad((W, H), (30, 24, 28), (14, 12, 14))
    d = ImageDraw.Draw(canvas)
    text_c(d, (W // 2, 70), "est. night lounge", F(FONT_JOSE, 18, 300), CHAMP)
    text_c(d, (W // 2, 140), "Four Seasons", F(FONT_PLAY, 68, 600), PEARL)
    text_c(d, (W // 2, 210), "Girls Snack", F(FONT_SCRIPT, 54), BLUSH)
    paste_c(canvas, load_logo("clear"), (int(W * 0.22), 250, int(W * 0.56), 110))
    # collage two photos with gap
    y = 400
    gap = 14
    pw = (W - 100 - gap) // 2
    ph = int(H * 0.34)
    canvas.paste(soft(cover(load_bar(), pw, ph, (0.55, 0.4)), 0.92), (50, y))
    canvas.paste(soft(cover(load_sofa(), pw, ph, (0.45, 0.45)), 0.92), (50 + pw + gap, y))
    chic_price(d, 70, y + ph + 40, W - 140, fill=PEARL, accent=CHAMP, scale=1.0)
    return canvas


LAYOUTS = [
    ("01_night_brand", "ナイトブランド中央", L01),
    ("02_blush_sidebar", "ブラッシュ・サイド情報", L02),
    ("03_editorial_white", "エディトリアル白", L03),
    ("04_wine_luxe", "ワインラグジュアリー", L04),
    ("05_sofa_hero", "ソファヒーロー", L05),
    ("06_asymmetric", "非対称マガジン", L06),
    ("07_champagne", "シャンパンゴールド", L07),
    ("08_pearl_calm", "パール・余白", L08),
    ("09_photo_footer", "写真全面・細フッター", L09),
    ("10_rose_mist", "ローズミスト", L10),
    ("11_mono_blush", "モノトーン＋ブラッシュ", L11),
    ("12_split_type", "縦半分タイポ", L12),
    ("13_tonight_script", "Tonightスクリプト", L13),
    ("14_mint_blush", "ミント×ブラッシュ", L14),
    ("15_fashion_space", "ファッション余白", L15),
    ("16_blur_focus", "ぼかし背景＋クリア", L16),
    ("17_strip_collage", "ストリップコラージュ", L17),
    ("18_french_chic", "フレンチシック", L18),
    ("19_type_on_photo", "写真上タイポ", L19),
    ("20_boutique", "ブティックポスター", L20),
]


def contact_sheet(items):
    cols, rows = 5, 4
    tw, th = 340, int(340 * RATIO)
    pad, lh = 14, 32
    sw = cols * tw + (cols + 1) * pad
    sh = 60 + rows * (th + lh + pad) + pad
    sheet = Image.new("RGB", (sw, sh), (245, 240, 238))
    d = ImageDraw.Draw(sheet)
    d.text((pad, 16), "Four Seasons Girls Snack — A1 おしゃれ案 20", font=F(FONT_JP, 28), fill=INK)
    small = F(FONT_JP, 15)
    for i, (path, title) in enumerate(items):
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = 55 + pad + r * (th + lh + pad)
        im = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(im, (x, y))
        d.text((x, y + th + 4), f"{i+1:02d} {title}", font=small, fill=(80, 60, 60))
    out = ROOT / "全候補_1枚まとめ.jpg"
    sheet.save(out, "JPEG", quality=88, optimize=True)
    return out


def make_viewer():
    cards = "\n".join(
        f'<figure><img src="panels/{n}.jpg" alt="{t}" loading="lazy"/><figcaption>{i:02d}. {t}</figcaption></figure>'
        for i, (n, t, _) in enumerate(LAYOUTS, 1)
    )
    html = f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Four Seasons Girls Snack A1 おしゃれ案20</title>
<style>
body{{margin:0;background:#1a1416;color:#f6eee8;font-family:system-ui,sans-serif}}
header{{padding:24px 20px;max-width:1200px;margin:0 auto}}
h1{{font-size:1.35rem;font-weight:500;margin:0 0 8px}}
p{{color:#c4a8a0;margin:0}}
a{{color:#e8b0a8}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px;padding:16px 20px 48px;max-width:1200px;margin:0 auto}}
figure{{margin:0;background:#241c1e;overflow:hidden}}
img{{width:100%;display:block;aspect-ratio:594/841;object-fit:cover}}
figcaption{{padding:10px;font-size:.8rem;color:#e8b0a8}}
</style></head><body>
<header>
<h1>Four Seasons — ガールズスナック A1 おしゃれ案</h1>
<p>方向性を刷新。写真と余白・タイポ中心の20案。
<a href="全候補_1枚まとめ.jpg">1枚まとめ</a></p>
</header>
<div class="grid">{cards}</div>
</body></html>"""
    (ROOT / "見る.html").write_text(html, encoding="utf-8")


def main():
    print(f"Generating chic girls-snack panels {W}×{H}…")
    items = []
    for name, title, fn in LAYOUTS:
        im = fn()
        assert im.size == (W, H), (name, im.size)
        items.append(save(im, f"{name}.jpg", title))
    contact_sheet(items)
    make_viewer()
    (ROOT / "README.md").write_text(
        """# Four Seasons — ガールズスナック A1縦 おしゃれ案20

無料案内所向け A1縦パネル。**ガールズスナックらしい上品さ**を軸に、写真・余白・タイポ中心で20案。

## 掲載
- Set 50分 / カウンター席 ¥3,000 / ボックス席 ¥4,000 / TAX 20%
- 飲み放題：甲類・ウイスキー・リキュール各種 ／ 割りもの・お茶・炭酸

## 見方
1. `見る.html`
2. `全候補_1枚まとめ.jpg`
3. `panels/`

```bash
python3 generate_panels.py
```
""",
        encoding="utf-8",
    )
    print("done")


if __name__ == "__main__":
    main()
