#!/usr/bin/env python3
"""Four Seasons Girls Snack — A1縦 おしゃれ案20（ロゴなし・タイポ中心）"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
FONTS = ASSETS / "fonts"
OUT = ROOT / "panels"
OUT.mkdir(exist_ok=True)

W, H = 1786, 2529
RATIO = H / W

# Soft glam palette
BLUSH = (236, 186, 178)
ROSE = (188, 112, 118)
DUST = (196, 148, 142)
CHAMP = (214, 188, 152)
PEARL = (252, 248, 244)
IVORY = (255, 252, 248)
INK = (32, 26, 28)
SOFT = (18, 14, 16)
MIST = (236, 228, 224)
WHITE = (255, 255, 255)

PLAY = str(FONTS / "PlayfairDisplay[wght].ttf")
PLAY_I = str(FONTS / "PlayfairDisplay-Italic[wght].ttf")
JOSE = str(FONTS / "JosefinSans[wght].ttf")
CORM = str(FONTS / "CormorantGaramond[wght].ttf")
SCRIPT = str(FONTS / "GreatVibes-Regular.ttf")
JP = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"


def F(path: str, size: int, weight: int | None = None) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(path, size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f


def bar() -> Image.Image:
    return Image.open(ASSETS / "interior_bar.jpg").convert("RGB")


def sofa() -> Image.Image:
    return Image.open(ASSETS / "interior_sofa.jpg").convert("RGB")


def cover(im: Image.Image, tw: int, th: int, focus=(0.5, 0.42)) -> Image.Image:
    sw, sh = im.size
    s = max(tw / sw, th / sh)
    nw, nh = int(sw * s + 0.5), int(sh * s + 0.5)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    cx, cy = int(nw * focus[0]), int(nh * focus[1])
    left = max(0, min(nw - tw, cx - tw // 2))
    top = max(0, min(nh - th, cy - th // 2))
    return im.crop((left, top, left + tw, top + th))


def tone(im: Image.Image, b=0.9, c=1.08, contrast=1.05) -> Image.Image:
    im = ImageEnhance.Brightness(im).enhance(b)
    im = ImageEnhance.Color(im).enhance(c)
    return ImageEnhance.Contrast(im).enhance(contrast)


def grad(size, c1, c2, vertical=True):
    w, h = size
    im = Image.new("RGB", size)
    px = im.load()
    n = max(1, (h if vertical else w) - 1)
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


def veil(base: Image.Image, box, color=(0, 0, 0), alpha=120) -> Image.Image:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rectangle(box, fill=(*color, alpha))
    return Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB")


def tcenter(d, xy, text, fnt, fill, sw=0, stroke=None):
    x, y = xy
    bb = d.textbbox((0, 0), text, font=fnt)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text((x - tw / 2, y - th / 2), text, font=fnt, fill=fill, stroke_width=sw, stroke_fill=stroke)


def line(d, y, x0, x1, fill, w=1):
    d.line((x0, y, x1, y), fill=fill, width=w)


def brand_mark(d, cx, y, fill=WHITE, accent=BLUSH, scale=1.0):
    """Typography brand — no logo image."""
    tcenter(d, (cx, y), "Girls Snack", F(SCRIPT, int(54 * scale)), accent)
    tcenter(d, (cx, y + int(70 * scale)), "Four Seasons", F(PLAY, int(64 * scale), 600), fill)
    line(d, y + int(110 * scale), cx - int(60 * scale), cx + int(60 * scale), accent, 1)


def price_slim(d, x, y, w, fill=WHITE, accent=BLUSH, scale=1.0, center=False):
    """Minimal price — fashion caption style."""
    f_s = F(JOSE, int(18 * scale), 300)
    f_j = F(JP, int(24 * scale))
    f_n = F(PLAY, int(28 * scale), 500)
    rows = [
        ("Set 50分", ""),
        ("カウンター席", "¥3,000"),
        ("ボックス席", "¥4,000"),
        ("TAX 20%", ""),
    ]
    yy = y
    if center:
        tcenter(d, (x + w // 2, yy), "料金", F(JP, int(20 * scale)), accent)
        yy += int(36 * scale)
        for a, b in rows:
            t = f"{a}  {b}".strip()
            tcenter(d, (x + w // 2, yy), t, f_j if any(ord(c) > 127 for c in a) else f_n, fill)
            yy += int(38 * scale)
        yy += int(8 * scale)
        tcenter(d, (x + w // 2, yy), "飲み放題  甲類・ウイスキー・リキュール / お茶・炭酸", F(JP, int(18 * scale)), accent)
        return yy + int(24 * scale)

    d.text((x, yy), "料金", font=F(JP, int(20 * scale)), fill=accent)
    yy += int(32 * scale)
    for a, b in rows:
        d.text((x, yy), a, font=f_j, fill=fill)
        if b:
            bb = d.textbbox((0, 0), b, font=f_n)
            d.text((x + w - (bb[2] - bb[0]), yy), b, font=f_n, fill=fill)
        yy += int(40 * scale)
    yy += int(10 * scale)
    d.text((x, yy), "飲み放題", font=f_s, fill=accent)
    yy += int(26 * scale)
    d.text((x, yy), "甲類・ウイスキー・リキュール各種", font=F(JP, int(18 * scale)), fill=fill)
    yy += int(26 * scale)
    d.text((x, yy), "割りもの・お茶類・炭酸", font=F(JP, int(18 * scale)), fill=fill)
    return yy + int(20 * scale)


def save(im: Image.Image, name: str, title: str):
    p = OUT / name
    im.convert("RGB").save(p, "JPEG", quality=90, optimize=True)
    print(f"  {name} — {title}")
    return p, title


# ---------- 20 layouts (no logo) ----------

def L01():
    """フルブリード・タイポ中央"""
    c = tone(cover(bar(), W, H, (0.55, 0.4)), 0.48, 1.15, 1.1)
    c = veil(c, (0, int(H * 0.3), W, int(H * 0.78)), (12, 8, 10), 150)
    d = ImageDraw.Draw(c)
    brand_mark(d, W // 2, int(H * 0.38), PEARL, BLUSH, 1.15)
    tcenter(d, (W // 2, int(H * 0.58)), "大人のための、やさしい夜。", F(JP, 30), PEARL)
    price_slim(d, int(W * 0.2), int(H * 0.66), int(W * 0.6), PEARL, BLUSH, 1.0, center=True)
    return c


def L02():
    """明るい雑誌・写真上下＋中央タイポ帯"""
    c = Image.new("RGB", (W, H), PEARL)
    c.paste(tone(cover(bar(), W, int(H * 0.4), (0.55, 0.4)), 1.0, 1.05), (0, 0))
    band_h = int(H * 0.2)
    c.paste(grad((W, band_h), (252, 240, 236), (248, 228, 224)), (0, int(H * 0.4)))
    d = ImageDraw.Draw(c)
    brand_mark(d, W // 2, int(H * 0.4) + 40, INK, ROSE, 1.0)
    c.paste(tone(cover(sofa(), W, H - int(H * 0.4) - band_h, (0.45, 0.45)), 1.0, 1.05), (0, int(H * 0.4) + band_h))
    # price overlay bottom of sofa
    c = veil(c, (0, int(H * 0.82), W, H), (255, 248, 244), 210)
    d = ImageDraw.Draw(c)
    price_slim(d, int(W * 0.12), int(H * 0.84), int(W * 0.76), INK, ROSE, 0.9, center=True)
    return c


def L03():
    """片側大きな余白・フレンチポスター"""
    c = Image.new("RGB", (W, H), IVORY)
    pw = int(W * 0.58)
    c.paste(tone(cover(bar(), pw, int(H * 0.55), (0.6, 0.4)), 0.98), (0, 0))
    c.paste(tone(cover(sofa(), pw, H - int(H * 0.55), (0.4, 0.45)), 0.98), (0, int(H * 0.55)))
    d = ImageDraw.Draw(c)
    rx = (pw + W) // 2
    tcenter(d, (rx, 160), "Four", F(PLAY_I, 72, 400), ROSE)
    tcenter(d, (rx, 250), "Seasons", F(PLAY, 68, 600), INK)
    tcenter(d, (rx, 340), "Girls Snack", F(SCRIPT, 48), DUST)
    line(d, 400, pw + 50, W - 50, BLUSH, 1)
    price_slim(d, pw + 40, 450, W - pw - 80, INK, ROSE, 0.95)
    tcenter(d, (rx, H - 80), "ご来店お待ちしております", F(JP, 22), ROSE)
    return c


def L04():
    """ソファ全画面・上に店名のみ"""
    c = tone(cover(sofa(), W, H, (0.48, 0.42)), 0.7, 1.08)
    c = veil(c, (0, 0, W, int(H * 0.28)), (255, 250, 246), 55)
    c = veil(c, (0, int(H * 0.68), W, H), (20, 12, 16), 165)
    d = ImageDraw.Draw(c)
    tcenter(d, (W // 2, 90), "Girls Snack", F(SCRIPT, 58), WHITE)
    tcenter(d, (W // 2, 170), "Four Seasons", F(PLAY, 60, 600), WHITE)
    # thin bar ribbon
    strip = tone(cover(bar(), W, int(H * 0.14), (0.55, 0.5)), 0.85)
    c.paste(strip, (0, int(H * 0.55)))
    d = ImageDraw.Draw(c)
    price_slim(d, int(W * 0.16), int(H * 0.72), int(W * 0.68), PEARL, BLUSH, 1.0, center=True)
    return c


def L05():
    """ローズウォッシュ全面"""
    c = grad((W, H), (248, 228, 224), (236, 200, 196))
    d = ImageDraw.Draw(c)
    tcenter(d, (W // 2, 80), "seasonal night", F(JOSE, 20, 300), ROSE)
    brand_mark(d, W // 2, 130, INK, ROSE, 1.05)
    m = 48
    y = 320
    c.paste(tone(cover(bar(), W - 2 * m, int(H * 0.32), (0.55, 0.4)), 1.02), (m, y))
    y += int(H * 0.32) + 20
    c.paste(tone(cover(sofa(), W - 2 * m, int(H * 0.28), (0.45, 0.45)), 1.02), (m, y))
    d = ImageDraw.Draw(c)
    price_slim(d, m + 20, y + int(H * 0.28) + 36, W - 2 * m - 40, INK, ROSE, 0.95)
    return c


def L06():
    """斜めカット・モード感"""
    a = tone(cover(bar(), W, H, (0.55, 0.4)), 0.75, 1.1)
    b = tone(cover(sofa(), W, H, (0.45, 0.45)), 0.8, 1.05)
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).polygon([(0, 0), (W, 0), (W, int(H * 0.5)), (0, int(H * 0.72))], fill=255)
    c = Image.composite(a, b, mask)
    c = veil(c, (0, int(H * 0.28), W, int(H * 0.52)), (255, 240, 236), 40)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(overlay).rectangle((0, int(H * 0.32), W, int(H * 0.5)), fill=(255, 248, 244, 200))
    c = Image.alpha_composite(c.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(c)
    brand_mark(d, W // 2, int(H * 0.35), INK, ROSE, 0.95)
    c = veil(c, (0, int(H * 0.75), W, H), (16, 12, 14), 175)
    d = ImageDraw.Draw(c)
    price_slim(d, int(W * 0.14), int(H * 0.78), int(W * 0.72), PEARL, BLUSH, 0.95, center=True)
    return c


def L07():
    """上タイポ余白多め・下写真二連"""
    c = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(c)
    tcenter(d, (W // 2, 140), "Four Seasons", F(PLAY, 78, 500), INK)
    tcenter(d, (W // 2, 230), "Girls Snack", F(SCRIPT, 60), ROSE)
    line(d, 290, int(W * 0.35), int(W * 0.65), BLUSH, 1)
    tcenter(d, (W // 2, 340), "カウンターとボックス、ふたつの夜。", F(JP, 28), (100, 70, 75))
    y = 420
    gap = 12
    each = int((H - y - 260) / 2)
    c.paste(tone(cover(bar(), W, each, (0.55, 0.38)), 1.0), (0, y))
    c.paste(tone(cover(sofa(), W, each, (0.45, 0.45)), 1.0), (0, y + each + gap))
    d = ImageDraw.Draw(c)
    price_slim(d, int(W * 0.12), y + 2 * each + gap + 24, int(W * 0.76), INK, ROSE, 0.9, center=True)
    return c


def L08():
    """ダークシフォン・手書き感店名"""
    c = tone(cover(bar(), W, H, (0.5, 0.38)), 0.42, 1.2).filter(ImageFilter.GaussianBlur(2))
    sharp = tone(cover(sofa(), int(W * 0.78), int(H * 0.28), (0.45, 0.45)), 0.95)
    c = veil(c, (0, 0, W, H), (20, 10, 16), 80)
    c.paste(sharp, ((W - sharp.width) // 2, int(H * 0.42)))
    d = ImageDraw.Draw(c)
    tcenter(d, (W // 2, int(H * 0.22)), "Tonight", F(SCRIPT, 96), BLUSH)
    tcenter(d, (W // 2, int(H * 0.32)), "Four Seasons", F(PLAY, 52, 500), WHITE)
    tcenter(d, (W // 2, int(H * 0.38)), "GIRLS SNACK", F(JOSE, 22, 300), CHAMP)
    price_slim(d, int(W * 0.16), int(H * 0.74), int(W * 0.68), PEARL, BLUSH, 0.95, center=True)
    return c


def L09():
    """二枚横並び・上に店名（明るい）"""
    c = grad((W, H), (255, 248, 246), (244, 220, 216))
    d = ImageDraw.Draw(c)
    brand_mark(d, W // 2, 70, INK, ROSE, 1.0)
    y = 280
    gap = 18
    pw = (W - 80 - gap) // 2
    ph = int(H * 0.42)
    c.paste(tone(cover(bar(), pw, ph, (0.55, 0.4)), 1.0), (40, y))
    c.paste(tone(cover(sofa(), pw, ph, (0.45, 0.45)), 1.0), (40 + pw + gap, y))
    d = ImageDraw.Draw(c)
    tcenter(d, (W // 2, y + ph + 50), "やさしく過ごす、大人のスナック。", F(JP, 28), ROSE)
    price_slim(d, int(W * 0.14), y + ph + 100, int(W * 0.72), INK, ROSE, 0.95, center=True)
    return c


def L10():
    """縦ストリップ＋大きな店名"""
    c = Image.new("RGB", (W, H), SOFT)
    left = int(W * 0.42)
    c.paste(tone(cover(bar(), left, H, (0.65, 0.4)), 0.85), (0, 0))
    # right soft panel
    d = ImageDraw.Draw(c)
    d.rectangle((left, 0, W, H), fill=(40, 28, 32))
    cx = (left + W) // 2
    tcenter(d, (cx, 200), "Four", F(PLAY_I, 70, 400), BLUSH)
    tcenter(d, (cx, 290), "Seasons", F(PLAY, 66, 600), WHITE)
    tcenter(d, (cx, 380), "Girls Snack", F(SCRIPT, 50), CHAMP)
    line(d, 440, left + 50, W - 50, ROSE, 1)
    # small sofa insert
    ins = tone(cover(sofa(), W - left - 60, int(H * 0.22), (0.45, 0.45)), 0.9)
    c.paste(ins, (left + 30, 480))
    d = ImageDraw.Draw(c)
    price_slim(d, left + 36, 480 + ins.height + 40, W - left - 72, PEARL, BLUSH, 0.92)
    return c


def L11():
    """ほぼ写真・店名は小さく上品に"""
    c = Image.new("RGB", (W, H))
    c.paste(tone(cover(bar(), W, int(H * 0.58), (0.55, 0.38)), 0.88, 1.1), (0, 0))
    c.paste(tone(cover(sofa(), W, H - int(H * 0.58), (0.5, 0.45)), 0.88, 1.05), (0, int(H * 0.58)))
    c = veil(c, (0, 0, W, 160), (0, 0, 0), 90)
    c = veil(c, (0, int(H * 0.78), W, H), (0, 0, 0), 160)
    d = ImageDraw.Draw(c)
    tcenter(d, (W // 2, 70), "FOUR SEASONS  ·  GIRLS SNACK", F(JOSE, 24, 300), PEARL)
    price_slim(d, int(W * 0.14), int(H * 0.82), int(W * 0.72), PEARL, BLUSH, 0.9, center=True)
    return c


def L12():
    """シャンパンベージュ・ブティック"""
    c = grad((W, H), (48, 40, 36), (24, 20, 18))
    d = ImageDraw.Draw(c)
    tcenter(d, (W // 2, 90), "Four Seasons", F(SCRIPT, 78), CHAMP)
    tcenter(d, (W // 2, 180), "GIRLS SNACK", F(JOSE, 24, 300), BLUSH)
    line(d, 220, int(W * 0.4), int(W * 0.6), CHAMP, 1)
    y = 260
    for src, foc, hh in [(bar, (0.55, 0.4), 0.32), (sofa, (0.45, 0.45), 0.28)]:
        ph = int(H * hh)
        c.paste(tone(cover(src(), W - 100, ph, foc), 0.92), (50, y))
        y += ph + 24
    d = ImageDraw.Draw(c)
    price_slim(d, 70, y + 10, W - 140, PEARL, CHAMP, 0.95)
    return c


def L13():
    """淡いピンク地・写真は角なしフル幅"""
    c = Image.new("RGB", (W, H), (250, 236, 232))
    d = ImageDraw.Draw(c)
    tcenter(d, (W // 2, 100), "Girls Snack", F(SCRIPT, 64), ROSE)
    tcenter(d, (W // 2, 180), "Four Seasons", F(PLAY, 56, 500), INK)
    c.paste(tone(cover(bar(), W, int(H * 0.3), (0.55, 0.4)), 1.02), (0, 240))
    c.paste(tone(cover(sofa(), W, int(H * 0.28), (0.45, 0.45)), 1.02), (0, 240 + int(H * 0.3) + 10))
    d = ImageDraw.Draw(c)
    price_slim(d, int(W * 0.12), 240 + int(H * 0.3) + 10 + int(H * 0.28) + 40, int(W * 0.76), INK, ROSE, 0.95, center=True)
    return c


def L14():
    """レイヤー重ね・モード"""
    c = grad((W, H), (30, 22, 26), (14, 10, 12))
    p1 = tone(cover(bar(), int(W * 0.88), int(H * 0.36), (0.55, 0.4)), 0.9)
    p2 = tone(cover(sofa(), int(W * 0.8), int(H * 0.32), (0.45, 0.45)), 0.9)
    c.paste(p1, (int(W * 0.06), 180))
    # soft shadow for p2
    sh = Image.new("RGBA", (p2.width + 30, p2.height + 30), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((8, 8, p2.width + 8, p2.height + 8), fill=(0, 0, 0, 100))
    sh = sh.filter(ImageFilter.GaussianBlur(10))
    sx, sy = int(W * 0.12), int(H * 0.38)
    c.paste(sh, (sx - 8, sy - 8), sh)
    c.paste(p2, (sx, sy))
    d = ImageDraw.Draw(c)
    tcenter(d, (W // 2, 80), "Four Seasons", F(PLAY, 48, 600), PEARL)
    tcenter(d, (W // 2, 140), "Girls Snack", F(SCRIPT, 44), BLUSH)
    price_slim(d, int(W * 0.14), int(H * 0.74), int(W * 0.72), PEARL, BLUSH, 0.92, center=True)
    return c


def L15():
    """超余白・店名大・写真は下だけ"""
    c = Image.new("RGB", (W, H), PEARL)
    d = ImageDraw.Draw(c)
    tcenter(d, (W // 2, 180), "Four Seasons", F(PLAY, 86, 500), INK)
    tcenter(d, (W // 2, 280), "Girls Snack", F(SCRIPT, 64), ROSE)
    line(d, 340, int(W * 0.3), int(W * 0.7), BLUSH, 1)
    tcenter(d, (W // 2, 400), "静かに、きれいに、楽しく。", F(JP, 30), (120, 90, 95))
    y = 500
    half = (H - y) // 2 - 8
    c.paste(tone(cover(bar(), W, half, (0.55, 0.4)), 1.0), (0, y))
    c.paste(tone(cover(sofa(), W, H - y - half, (0.45, 0.45)), 1.0), (0, y + half + 8))
    # tiny price on bottom veil
    c = veil(c, (0, H - 200, W, H), (255, 250, 246), 200)
    d = ImageDraw.Draw(c)
    price_slim(d, int(W * 0.1), H - 180, int(W * 0.8), INK, ROSE, 0.85, center=True)
    return c


def L16():
    """ぼかし背景＋中央クリア写真一枚＋店名"""
    bg = tone(cover(bar(), W, H, (0.5, 0.4)), 0.5, 1.15).filter(ImageFilter.GaussianBlur(22))
    c = bg
    fg = tone(cover(sofa(), int(W * 0.82), int(H * 0.4), (0.45, 0.42)), 1.0)
    c.paste(fg, ((W - fg.width) // 2, int(H * 0.28)))
    d = ImageDraw.Draw(c)
    tcenter(d, (W // 2, 100), "Four Seasons", F(PLAY, 56, 600), WHITE)
    tcenter(d, (W // 2, 170), "Girls Snack", F(SCRIPT, 50), BLUSH)
    c = veil(c, (0, int(H * 0.72), W, H), (16, 12, 14), 170)
    d = ImageDraw.Draw(c)
    # small bar strip above price
    strip = tone(cover(bar(), int(W * 0.7), int(H * 0.1), (0.55, 0.5)), 0.9)
    c.paste(strip, ((W - strip.width) // 2, int(H * 0.7)))
    d = ImageDraw.Draw(c)
    price_slim(d, int(W * 0.16), int(H * 0.82), int(W * 0.68), PEARL, BLUSH, 0.9, center=True)
    return c


def L17():
    """横帯3段・中央に店名"""
    c = Image.new("RGB", (W, H), (22, 16, 18))
    h1 = int(H * 0.3)
    mid = int(H * 0.18)
    h2 = H - h1 - mid
    c.paste(tone(cover(bar(), W, h1, (0.55, 0.35)), 0.9), (0, 0))
    c.paste(grad((W, mid), (252, 236, 232), (244, 216, 210)), (0, h1))
    d = ImageDraw.Draw(c)
    brand_mark(d, W // 2, h1 + 30, INK, ROSE, 0.9)
    c.paste(tone(cover(sofa(), W, h2, (0.45, 0.45)), 0.88), (0, h1 + mid))
    c = veil(c, (0, H - 280, W, H), (12, 8, 10), 170)
    d = ImageDraw.Draw(c)
    price_slim(d, int(W * 0.14), H - 250, int(W * 0.72), PEARL, BLUSH, 0.92, center=True)
    return c


def L18():
    """左ローズ線・右写真・上品"""
    c = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(c)
    d.rectangle((0, 0, 18, H), fill=ROSE)
    tcenter(d, (W // 2 + 10, 90), "Four Seasons", F(PLAY, 58, 500), INK)
    tcenter(d, (W // 2 + 10, 165), "Girls Snack", F(SCRIPT, 52), ROSE)
    m = 50
    c.paste(tone(cover(bar(), W - m - 40, int(H * 0.3), (0.55, 0.4)), 1.0), (m, 220))
    c.paste(tone(cover(sofa(), W - m - 40, int(H * 0.28), (0.45, 0.45)), 1.0), (m, 220 + int(H * 0.3) + 18))
    # vertical phrase
    phrase = "華やかな夜に"
    f = F(JP, 34)
    x, y = W - 70, 240
    for ch in phrase:
        d.text((x, y), ch, font=f, fill=ROSE)
        y += 46
    d = ImageDraw.Draw(c)
    price_slim(d, m, 220 + int(H * 0.3) + 18 + int(H * 0.28) + 36, W - m - 100, INK, ROSE, 0.95)
    return c


def L19():
    """写真上に大きなセリフ店名"""
    c = tone(cover(bar(), W, int(H * 0.62), (0.55, 0.4)), 0.55, 1.15)
    bottom = tone(cover(sofa(), W, H - int(H * 0.62), (0.45, 0.45)), 0.7)
    full = Image.new("RGB", (W, H))
    full.paste(c, (0, 0))
    full.paste(bottom, (0, int(H * 0.62)))
    full = veil(full, (0, int(H * 0.2), W, int(H * 0.55)), (0, 0, 0), 110)
    d = ImageDraw.Draw(full)
    tcenter(d, (W // 2, int(H * 0.3)), "FOUR SEASONS", F(PLAY, 70, 700), WHITE)
    tcenter(d, (W // 2, int(H * 0.4)), "Girls Snack", F(SCRIPT, 56), BLUSH)
    tcenter(d, (W // 2, int(H * 0.48)), "大人の隠れ家スナック", F(JP, 28), PEARL)
    full = veil(full, (0, int(H * 0.78), W, H), (10, 8, 10), 175)
    d = ImageDraw.Draw(full)
    price_slim(d, int(W * 0.14), int(H * 0.82), int(W * 0.72), PEARL, BLUSH, 0.9, center=True)
    return full


def L20():
    """ブティックポスター完成形"""
    c = grad((W, H), (252, 242, 238), (236, 208, 204))
    d = ImageDraw.Draw(c)
    tcenter(d, (W // 2, 70), "est. girls snack", F(JOSE, 18, 300), ROSE)
    tcenter(d, (W // 2, 150), "Four Seasons", F(PLAY, 74, 600), INK)
    tcenter(d, (W // 2, 235), "Girls Snack", F(SCRIPT, 58), ROSE)
    line(d, 290, int(W * 0.38), int(W * 0.62), BLUSH, 1)
    y = 330
    gap = 14
    pw = (W - 90 - gap) // 2
    ph = int(H * 0.36)
    c.paste(tone(cover(bar(), pw, ph, (0.55, 0.4)), 1.0), (45, y))
    c.paste(tone(cover(sofa(), pw, ph, (0.45, 0.45)), 1.0), (45 + pw + gap, y))
    d = ImageDraw.Draw(c)
    tcenter(d, (W // 2, y + ph + 45), "Set 50分 ／ カウンター ¥3,000 ／ ボックス ¥4,000", F(JP, 24), INK)
    tcenter(d, (W // 2, y + ph + 90), "TAX 20%  ·  飲み放題あり", F(JP, 22), ROSE)
    tcenter(d, (W // 2, y + ph + 140), "甲類・ウイスキー・リキュール ／ お茶・炭酸", F(JP, 20), (120, 90, 90))
    return c


LAYOUTS = [
    ("01_full_type", "フルブリード・中央タイポ", L01),
    ("02_magazine_band", "明るい雑誌・中央帯", L02),
    ("03_french_side", "フレンチ余白サイド", L03),
    ("04_sofa_hero", "ソファ全画面", L04),
    ("05_rose_wash", "ローズウォッシュ", L05),
    ("06_diagonal_mode", "斜めカット・モード", L06),
    ("07_space_top", "上余白・下写真", L07),
    ("08_tonight", "Tonightシフォン", L08),
    ("09_dual_bright", "明るい二枚並び", L09),
    ("10_strip_type", "縦ストリップ＋店名", L10),
    ("11_photo_quiet", "写真主役・控えめ店名", L11),
    ("12_champagne", "シャンパンブティック", L12),
    ("13_soft_pink", "ソフトピンク", L13),
    ("14_layered", "レイヤー重ね", L14),
    ("15_max_space", "最大余白", L15),
    ("16_blur_focus", "ぼかし＋クリア", L16),
    ("17_tri_band", "三帯構成", L17),
    ("18_rose_line", "ローズライン", L18),
    ("19_serif_hero", "大セリフ店名", L19),
    ("20_boutique", "ブティック完成形", L20),
]


def contact_sheet(items):
    cols, rows = 5, 4
    tw = 340
    th = int(tw * RATIO)
    pad, lh = 14, 34
    sw = cols * tw + (cols + 1) * pad
    sh = 70 + rows * (th + lh + pad) + pad
    sheet = Image.new("RGB", (sw, sh), (250, 242, 238))
    d = ImageDraw.Draw(sheet)
    d.text((pad, 18), "Four Seasons Girls Snack — ロゴなしおしゃれ案20", font=F(JP, 28), fill=INK)
    small = F(JP, 14)
    for i, (path, title) in enumerate(items):
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = 60 + pad + r * (th + lh + pad)
        im = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(im, (x, y))
        d.text((x, y + th + 5), f"{i+1:02d} {title}", font=small, fill=(90, 60, 65))
    out = ROOT / "全候補_1枚まとめ.jpg"
    sheet.save(out, "JPEG", quality=88, optimize=True)
    return out


def make_viewer():
    cards = "\n".join(
        f'<figure><img src="panels/{n}.jpg" alt="{t}" loading="lazy"/><figcaption>{i:02d}. {t}</figcaption></figure>'
        for i, (n, t, _) in enumerate(LAYOUTS, 1)
    )
    (ROOT / "見る.html").write_text(
        f"""<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Four Seasons おしゃれ案20（ロゴなし）</title>
<style>
body{{margin:0;background:#1c1416;color:#f8eee8;font-family:system-ui,sans-serif}}
header{{padding:24px;max-width:1200px;margin:0 auto}}
a{{color:#e8b0a8}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px;padding:16px 20px 40px;max-width:1200px;margin:0 auto}}
figure{{margin:0;background:#24181a}}
img{{width:100%;display:block;aspect-ratio:594/841;object-fit:cover}}
figcaption{{padding:8px 10px;font-size:.8rem;color:#e8b0a8}}
</style></head><body>
<header><h1>Four Seasons Girls Snack — ロゴなしおしゃれ案</h1>
<p>店ロゴ画像は使用せず、タイポのみ。<a href="全候補_1枚まとめ.jpg">1枚まとめ</a></p></header>
<div class="grid">{cards}</div></body></html>""",
        encoding="utf-8",
    )


def main():
    print("Generating no-logo chic panels…")
    # clear old panels with different names
    for p in OUT.glob("*.jpg"):
        p.unlink()
    items = []
    for name, title, fn in LAYOUTS:
        im = fn()
        assert im.size == (W, H), (name, im.size)
        items.append(save(im, f"{name}.jpg", title))
    contact_sheet(items)
    make_viewer()
    (ROOT / "README.md").write_text(
        """# Four Seasons Girls Snack — A1おしゃれ案20（ロゴなし）

店ロゴ画像は外し、**Four Seasons / Girls Snack をタイポのみ**で構成。

## 掲載
- Set 50分 / カウンター席 ¥3,000 / ボックス席 ¥4,000 / TAX 20%
- 飲み放題：甲類・ウイスキー・リキュール各種／割りもの・お茶・炭酸

## 見方
`見る.html` / `全候補_1枚まとめ.jpg` / `panels/`
""",
        encoding="utf-8",
    )
    print("done")


if __name__ == "__main__":
    main()
