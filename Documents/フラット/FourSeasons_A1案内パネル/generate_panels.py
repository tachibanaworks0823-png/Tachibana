#!/usr/bin/env python3
"""
Four Seasons — ガールズバー／スナック A1案内パネル 華やか案20
参考: サインモール等（ピンク×ゴールド・煌めき・料金大・華やかフレーム）
制約: 写真なし / 暗め背景NG / スカスカ禁止（面を埋める）
"""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont

ROOT = Path(__file__).resolve().parent
FONTS = ROOT / "assets" / "fonts"
OUT = ROOT / "panels"
OUT.mkdir(exist_ok=True)

W, H = 1786, 2529
RATIO = H / W

# Bright glam palette
HOT = (255, 72, 148)
HOT2 = (255, 40, 120)
ROSE = (255, 110, 160)
PINK = (255, 160, 190)
SOFT_P = (255, 210, 225)
BLUSH = (255, 230, 238)
CREAM = (255, 248, 240)
IVORY = (255, 252, 248)
GOLD = (212, 168, 72)
GOLD_L = (255, 224, 140)
GOLD_D = (176, 128, 48)
WHITE = (255, 255, 255)
INK = (72, 28, 48)
SOFT = (120, 55, 80)

PLAY = str(FONTS / "PlayfairDisplay[wght].ttf")
PLAY_I = str(FONTS / "PlayfairDisplay-Italic[wght].ttf")
JOSE = str(FONTS / "JosefinSans[wght].ttf")
SCRIPT = str(FONTS / "GreatVibes-Regular.ttf")
CORM = str(FONTS / "CormorantGaramond[wght].ttf")
JP = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"


def F(path: str, size: int, weight: int | None = None) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(path, size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f


def tcenter(d, xy, text, fnt, fill, stroke=None, sw=0):
    x, y = xy
    bb = d.textbbox((0, 0), text, font=fnt)
    d.text(
        (x - (bb[2] - bb[0]) / 2, y - (bb[3] - bb[1]) / 2),
        text,
        font=fnt,
        fill=fill,
        stroke_width=sw,
        stroke_fill=stroke,
    )


def grad_v(size, c1, c2):
    w, h = size
    im = Image.new("RGB", size)
    px = im.load()
    for y in range(h):
        t = y / max(1, h - 1)
        rgb = tuple(int(c1[j] + (c2[j] - c1[j]) * t) for j in range(3))
        for x in range(w):
            px[x, y] = rgb
    return im


def grad_h(size, c1, c2):
    w, h = size
    im = Image.new("RGB", size)
    px = im.load()
    for x in range(w):
        t = x / max(1, w - 1)
        rgb = tuple(int(c1[j] + (c2[j] - c1[j]) * t) for j in range(3))
        for y in range(h):
            px[x, y] = rgb
    return im


def radial(size, c_center, c_edge, cx=None, cy=None):
    w, h = size
    im = Image.new("RGB", size)
    px = im.load()
    cx = w / 2 if cx is None else cx
    cy = h / 2 if cy is None else cy
    maxd = math.hypot(max(cx, w - cx), max(cy, h - cy))
    for y in range(h):
        for x in range(w):
            t = min(1.0, math.hypot(x - cx, y - cy) / maxd)
            px[x, y] = tuple(int(c_center[j] + (c_edge[j] - c_center[j]) * t) for j in range(3))
    return im


def glitter_layer(seed=1, n=220, color=(255, 230, 160)):
    """キラキラ粒子レイヤ（合成用RGBA）"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rng = random.Random(seed)
    for _ in range(n):
        x, y = rng.randint(40, W - 40), rng.randint(40, H - 40)
        s = rng.randint(2, 9)
        a = rng.randint(90, 220)
        col = (*color, a)
        d.line((x - s, y, x + s, y), fill=col, width=2)
        d.line((x, y - s, x, y + s), fill=col, width=2)
        if s > 5:
            d.line((x - s // 2, y - s // 2, x + s // 2, y + s // 2), fill=col, width=1)
            d.line((x - s // 2, y + s // 2, x + s // 2, y - s // 2), fill=col, width=1)
    # soft bokeh circles
    for _ in range(35):
        x, y = rng.randint(0, W), rng.randint(0, H)
        r = rng.randint(8, 40)
        a = rng.randint(25, 70)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(*color, a))
    return im.filter(ImageFilter.GaussianBlur(0.6))


def apply_glitter(base: Image.Image, seed=1) -> Image.Image:
    out = base.convert("RGBA")
    out = Image.alpha_composite(out, glitter_layer(seed))
    out = Image.alpha_composite(out, glitter_layer(seed + 77, n=80, color=(255, 180, 210)))
    return out.convert("RGB")


def diamond(d, cx, cy, s, fill=GOLD_L, outline=GOLD):
    pts = [(cx, cy - s), (cx + s * 0.72, cy), (cx, cy + s), (cx - s * 0.72, cy)]
    d.polygon(pts, fill=fill, outline=outline)


def starburst(d, cx, cy, r=28, color=GOLD):
    for a in range(0, 360, 30):
        rad = math.radians(a)
        d.line(
            (cx + math.cos(rad) * 4, cy + math.sin(rad) * 4, cx + math.cos(rad) * r, cy + math.sin(rad) * r),
            fill=color,
            width=2,
        )
    diamond(d, cx, cy, 8, GOLD_L, color)


def ornate_frame(d, m=28):
    """厚めの三重フレーム＋コーナー飾り"""
    d.rectangle((m, m, W - m, H - m), outline=GOLD_D, width=14)
    d.rectangle((m + 18, m + 18, W - m - 18, H - m - 18), outline=GOLD_L, width=5)
    d.rectangle((m + 32, m + 32, W - m - 32, H - m - 32), outline=HOT, width=3)
    # corner medallions
    for cx, cy in [
        (m + 70, m + 70),
        (W - m - 70, m + 70),
        (m + 70, H - m - 70),
        (W - m - 70, H - m - 70),
    ]:
        d.ellipse((cx - 38, cy - 38, cx + 38, cy + 38), outline=GOLD, width=4)
        starburst(d, cx, cy, 26, GOLD)
    # side diamonds
    for y in range(220, H - 200, 160):
        diamond(d, m + 55, y, 10)
        diamond(d, W - m - 55, y, 10)


def flourish(d, cx, cy, scale=1.0, color=GOLD):
    for sign in (-1, 1):
        pts = []
        for i in range(24):
            t = i / 23
            x = cx + sign * (30 + t * 110) * scale
            y = cy + math.sin(t * math.pi * 1.6) * 28 * scale * sign
            pts.append((x, y))
        d.line(pts, fill=color, width=3)
    diamond(d, cx, cy, 9)


def ribbon(d, y, text, fill=HOT, h=96):
    """横断リボン（影つき）"""
    d.polygon(
        [(90, y + 12), (W - 90, y + 12), (W - 55, y + h // 2 + 12), (W - 90, y + h + 12), (90, y + h + 12), (55, y + h // 2 + 12)],
        fill=GOLD_D,
    )
    d.polygon(
        [(90, y), (W - 90, y), (W - 55, y + h // 2), (W - 90, y + h), (90, y + h), (55, y + h // 2)],
        fill=fill,
    )
    # folds
    d.polygon([(90, y), (55, y + h // 2), (90, y + 28)], fill=GOLD_D)
    d.polygon([(W - 90, y), (W - 55, y + h // 2), (W - 90, y + 28)], fill=GOLD_D)
    tcenter(d, (W // 2, y + h // 2), text, F(JP, 38), WHITE)


def champagne(d, cx, cy, scale=1.0):
    """簡易シャンパングラス装飾"""
    s = scale
    d.polygon(
        [
            (cx - 22 * s, cy - 70 * s),
            (cx + 22 * s, cy - 70 * s),
            (cx + 14 * s, cy),
            (cx - 14 * s, cy),
        ],
        outline=GOLD,
        fill=GOLD_L,
    )
    d.line((cx, cy, cx, cy + 55 * s), fill=GOLD, width=3)
    d.ellipse((cx - 28 * s, cy + 50 * s, cx + 28 * s, cy + 68 * s), outline=GOLD, width=3)
    # bubbles
    for dx, dy in [(-8, -50), (6, -40), (-2, -30)]:
        d.ellipse((cx + dx * s - 3, cy + dy * s - 3, cx + dx * s + 3, cy + dy * s + 3), outline=WHITE, width=1)


def rose(d, cx, cy, s=40, color=HOT):
    """簡易バラ"""
    for i, (dx, dy) in enumerate([(0, -8), (-10, 2), (10, 2), (-6, 10), (6, 10)]):
        d.ellipse((cx + dx - s // 2, cy + dy - s // 2, cx + dx + s // 2, cy + dy + s // 2), fill=color if i % 2 == 0 else ROSE)
    d.ellipse((cx - s // 4, cy - s // 4, cx + s // 4, cy + s // 4), fill=GOLD_L)


def silhouette(d, cx, cy, scale=1.0, color=(255, 170, 195)):
    r = 30 * scale
    d.ellipse((cx - r, cy - r * 3.4, cx + r, cy - r * 1.3), fill=color)
    d.ellipse((cx - r * 1.35, cy - r * 3.55, cx + r * 0.95, cy - r * 1.5), outline=HOT, width=3)
    d.polygon(
        [
            (cx - 60 * scale, cy + 100 * scale),
            (cx - 32 * scale, cy - 8 * scale),
            (cx + 32 * scale, cy - 8 * scale),
            (cx + 60 * scale, cy + 100 * scale),
            (cx, cy + 135 * scale),
        ],
        fill=color,
    )


def header_block(d, y=120, script=False):
    tcenter(d, (W // 2, y), "GIRLS BAR  ★  GIRLS SNACK", F(JOSE, 30, 500), HOT)
    flourish(d, W // 2, y + 48, 1.15, GOLD)
    name_font = F(SCRIPT, 96) if script else F(PLAY, 82, 700)
    tcenter(d, (W // 2, y + 130), "Four Seasons", name_font, INK, GOLD_L, 1)
    for dx in (-100, -50, 0, 50, 100):
        diamond(d, W // 2 + dx, y + 200, 11)


def system_banner(d, y, text="★  SYSTEM / 料金案内  ★"):
    d.rounded_rectangle((110, y, W - 110, y + 78), radius=14, fill=HOT, outline=GOLD_L, width=4)
    tcenter(d, (W // 2, y + 39), text, F(JP, 36), WHITE)


def price_rows(d, y, accent=HOT):
    """密な料金行"""
    rows = [
        ("Set 時間", "50分"),
        ("カウンター席", "¥3,000"),
        ("ボックス席", "¥4,000"),
        ("TAX", "20%"),
    ]
    yy = y
    for i, (label, price) in enumerate(rows):
        bg = WHITE if i % 2 == 0 else (255, 240, 246)
        d.rounded_rectangle((130, yy, W - 130, yy + 92), radius=12, fill=bg, outline=GOLD, width=3)
        # left accent bar
        d.rounded_rectangle((130, yy + 8, 155, yy + 84), radius=6, fill=accent)
        d.text((180, yy + 24), label, font=F(JP, 36), fill=INK)
        bb = d.textbbox((0, 0), price, font=F(PLAY, 44, 700))
        # use JP for 分
        if "分" in price:
            fnt = F(JP, 42)
            bb = d.textbbox((0, 0), price, font=fnt)
            d.text((W - 170 - (bb[2] - bb[0]), yy + 22), price, font=fnt, fill=accent)
        else:
            d.text((W - 170 - (bb[2] - bb[0]), yy + 18), price, font=F(PLAY, 44, 700), fill=accent)
        yy += 102
    return yy


def drink_box(d, y, h=260):
    d.rounded_rectangle((130, y, W - 130, y + h), radius=16, fill=(255, 236, 244), outline=HOT, width=4)
    # top gold strip
    d.rectangle((130, y, W - 130, y + 12), fill=GOLD)
    tcenter(d, (W // 2, y + 55), "★ 飲み放題メニュー ★", F(JP, 34), HOT)
    tcenter(d, (W // 2, y + 120), "甲類・ウイスキー・リキュール各種", F(JP, 30), INK)
    tcenter(d, (W // 2, y + 175), "割りもの・お茶類・炭酸", F(JP, 30), INK)
    # bottom ornaments
    for dx in (-120, -60, 0, 60, 120):
        diamond(d, W // 2 + dx, y + h - 35, 8)
    return y + h


def footer_band(d, y=None):
    y = H - 160 if y is None else y
    d.rectangle((70, y, W - 70, y + 90), fill=HOT)
    d.rectangle((70, y, W - 70, y + 8), fill=GOLD_L)
    d.rectangle((70, y + 82, W - 70, y + 90), fill=GOLD_L)
    tcenter(d, (W // 2, y + 45), "Four Seasons  ガールズバー＆スナック", F(JP, 30), WHITE)


def save(im, name, title):
    p = OUT / name
    im.convert("RGB").save(p, "JPEG", quality=91, optimize=True)
    print(f"  {name} — {title}")
    return p, title


# ---------- 20 dense glamorous layouts ----------


def L01():
    """ピンクゴールド王道・面埋め"""
    c = radial((W, H), (255, 242, 248), (255, 150, 185), cy=H * 0.35)
    d = ImageDraw.Draw(c)
    # decorative top band
    d.rectangle((0, 0, W, 90), fill=HOT)
    tcenter(d, (W // 2, 45), "★  WELCOME TO  ★", F(JOSE, 26, 500), GOLD_L)
    ornate_frame(d)
    header_block(d, 160)
    ribbon(d, 420, "初めてでも安心 ◎ 明朗会計")
    system_banner(d, 560)
    yy = price_rows(d, 660)
    yy = drink_box(d, yy + 20)
    # fill lower area — no empty pink void
    d.rounded_rectangle((110, yy + 30, W - 110, H - 180), radius=20, fill=(255, 220, 232), outline=GOLD, width=4)
    for i, x in enumerate(range(280, W - 240, 200)):
        silhouette(d, x, yy + 220, 1.15, (255, 170 + i * 8, 198))
    champagne(d, 200, yy + 280, 1.0)
    champagne(d, W - 200, yy + 280, 1.0)
    for i, x in enumerate(range(260, W - 220, 160)):
        rose(d, x, yy + 90, 30, HOT if i % 2 == 0 else ROSE)
    tcenter(d, (W // 2, yy + 380), "かわいい女の子がお出迎えします", F(JP, 28), SOFT)
    footer_band(d)
    return apply_glitter(c, 1)


def L02():
    """ヒーロー料金円＋下部密情報"""
    c = grad_v((W, H), CREAM, (255, 190, 210))
    d = ImageDraw.Draw(c)
    ornate_frame(d, 32)
    tcenter(d, (W // 2, 140), "Four Seasons", F(SCRIPT, 100), HOT)
    tcenter(d, (W // 2, 250), "GIRLS BAR  ★  GIRLS SNACK", F(JOSE, 28, 500), GOLD_D)
    # hero circle
    d.ellipse((W // 2 - 280, 300, W // 2 + 280, 860), fill=HOT, outline=GOLD_L, width=12)
    d.ellipse((W // 2 - 250, 330, W // 2 + 250, 830), outline=GOLD, width=4)
    tcenter(d, (W // 2, 420), "いちばん人気", F(JP, 30), GOLD_L)
    tcenter(d, (W // 2, 520), "カウンター席", F(JP, 34), WHITE)
    tcenter(d, (W // 2, 630), "¥3,000", F(PLAY, 78, 700), GOLD_L)
    tcenter(d, (W // 2, 730), "Set 50分", F(JP, 32), WHITE)
    # side pills
    for label, price, x in [("ボックス", "¥4,000", 200), ("TAX", "20%", W - 200)]:
        d.rounded_rectangle((x - 130, 900, x + 130, 1020), radius=20, fill=WHITE, outline=GOLD, width=4)
        tcenter(d, (x, 940), label, F(JP, 26), SOFT)
        tcenter(d, (x, 990), price, F(PLAY if "¥" in price or "%" in price else JP, 34, 700), HOT)
    d.rounded_rectangle((120, 1080, W - 120, 1480), radius=18, fill=WHITE, outline=HOT, width=5)
    tcenter(d, (W // 2, 1160), "★ 飲み放題つきセット ★", F(JP, 36), HOT)
    tcenter(d, (W // 2, 1260), "甲類・ウイスキー・リキュール各種", F(JP, 30), INK)
    tcenter(d, (W // 2, 1340), "割りもの・お茶類・炭酸", F(JP, 30), INK)
    tcenter(d, (W // 2, 1420), "Set 50分 ／ 明朗会計", F(JP, 28), GOLD_D)
    # bottom ornament strip
    d.rectangle((90, 1580, W - 90, 2100), fill=(255, 230, 240))
    for i, x in enumerate(range(220, W - 180, 220)):
        silhouette(d, x, 1850, 1.15 + (i % 2) * 0.1, (255, 175 + i * 8, 200))
    tcenter(d, (W // 2, 2050), "Girls Night Out", F(SCRIPT, 48), HOT)
    footer_band(d)
    return apply_glitter(c, 2)


def L03():
    """シルエット舞台＋料金"""
    c = grad_v((W, H), (255, 235, 245), (255, 175, 200))
    d = ImageDraw.Draw(c)
    ornate_frame(d)
    header_block(d, 130, script=False)
    ribbon(d, 380, "かわいい女の子がお出迎え")
    # stage platform
    d.ellipse((180, 520, W - 180, 780), fill=(255, 200, 220), outline=GOLD, width=5)
    for i, x in enumerate([340, 560, 780, 1000, 1220, 1440]):
        silhouette(d, x, 620, 1.0 + (i % 3) * 0.12, (255, 165 + i * 10, 195))
    system_banner(d, 820)
    yy = price_rows(d, 920)
    yy = drink_box(d, yy + 16, 240)
    rose(d, 200, yy + 100, 42)
    rose(d, W - 200, yy + 100, 42)
    footer_band(d)
    return apply_glitter(c, 3)


def L04():
    """左右分割・密充填"""
    c = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(c)
    mid = int(W * 0.46)
    left = grad_v((mid, H), HOT, ROSE)
    c.paste(left, (0, 0))
    d = ImageDraw.Draw(c)
    # left brand column
    for y in range(80, H - 80, 90):
        diamond(d, 60, y, 8, GOLD_L, GOLD)
    tcenter(d, (mid // 2, 220), "Girls", F(SCRIPT, 78), WHITE)
    tcenter(d, (mid // 2, 340), "Bar", F(SCRIPT, 78), GOLD_L)
    tcenter(d, (mid // 2, 460), "&", F(PLAY, 50, 400), WHITE)
    tcenter(d, (mid // 2, 580), "Snack", F(SCRIPT, 78), WHITE)
    d.line((120, 680, mid - 120, 680), fill=GOLD_L, width=3)
    tcenter(d, (mid // 2, 780), "Four", F(PLAY, 56, 700), GOLD_L)
    tcenter(d, (mid // 2, 870), "Seasons", F(PLAY, 56, 700), GOLD_L)
    for i in range(5):
        rose(d, mid // 2 - 80 + i * 40, 1050, 28, PINK if i % 2 else HOT)
    champagne(d, mid // 2, 1300, 1.3)
    tcenter(d, (mid // 2, 1550), "WELCOME", F(JOSE, 28, 500), GOLD_L)
    tcenter(d, (mid // 2, 1650), "初めての方も安心", F(JP, 26), WHITE)
    # right info
    rx = mid + 30
    tcenter(d, ((rx + W) // 2, 140), "料金 SYSTEM", F(JP, 38), HOT)
    flourish(d, (rx + W) // 2, 200, 0.9, GOLD)
    rows = [("Set", "50分"), ("カウンター席", "¥3,000"), ("ボックス席", "¥4,000"), ("TAX", "20%")]
    yy = 260
    for a, b in rows:
        d.rounded_rectangle((rx, yy, W - 50, yy + 130), radius=16, outline=GOLD, width=4, fill=WHITE)
        d.rectangle((rx, yy, rx + 18, yy + 130), fill=HOT)
        d.text((rx + 40, yy + 40), a, font=F(JP, 34), fill=INK)
        fnt = F(JP, 40) if "分" in b else F(PLAY, 44, 700)
        bb = d.textbbox((0, 0), b, font=fnt)
        d.text((W - 80 - (bb[2] - bb[0]), yy + 38), b, font=fnt, fill=HOT)
        yy += 150
    d.rounded_rectangle((rx, yy + 10, W - 50, yy + 380), radius=16, fill=(255, 230, 240), outline=HOT, width=4)
    tcenter(d, ((rx + W) // 2, yy + 80), "★ 飲み放題 ★", F(JP, 34), HOT)
    tcenter(d, ((rx + W) // 2, yy + 170), "甲類・ウイスキー・リキュール各種", F(JP, 26), INK)
    tcenter(d, ((rx + W) // 2, yy + 250), "割りもの・お茶類・炭酸", F(JP, 26), INK)
    tcenter(d, ((rx + W) // 2, yy + 330), "Set 50分", F(JP, 28), GOLD_D)
    # gold divider
    d.rectangle((mid - 6, 40, mid + 6, H - 40), fill=GOLD)
    return apply_glitter(c, 4)


def L05():
    """放射キラキラ全面"""
    c = radial((W, H), WHITE, (255, 150, 190), cy=H * 0.3)
    d = ImageDraw.Draw(c)
    cx, cy = W // 2, int(H * 0.28)
    for a in range(0, 360, 6):
        rad = math.radians(a)
        col = (255, 200, 220) if a % 12 else (255, 220, 180)
        d.line((cx, cy, cx + math.cos(rad) * 1200, cy + math.sin(rad) * 1200), fill=col, width=4)
    ornate_frame(d, 24)
    header_block(d, 140, script=True)
    chips = [
        ("Set 50分", 480),
        ("カウンター席  ¥3,000", 640),
        ("ボックス席  ¥4,000", 800),
        ("TAX  20%", 960),
    ]
    for text, y in chips:
        d.rounded_rectangle((160, y, W - 160, y + 120), radius=60, fill=HOT, outline=GOLD_L, width=6)
        tcenter(d, (W // 2, y + 60), text, F(JP, 40), WHITE)
    d.rounded_rectangle((140, 1140, W - 140, 1580), radius=20, fill=WHITE, outline=GOLD, width=5)
    tcenter(d, (W // 2, 1230), "★ 飲み放題メニュー ★", F(JP, 36), HOT)
    tcenter(d, (W // 2, 1340), "甲類・ウイスキー・リキュール各種", F(JP, 30), INK)
    tcenter(d, (W // 2, 1440), "割りもの・お茶類・炭酸", F(JP, 30), INK)
    tcenter(d, (W // 2, 1520), "明朗会計で安心", F(JP, 28), GOLD_D)
    for x in range(200, W - 150, 180):
        starburst(d, x, 1700, 22)
    footer_band(d)
    return apply_glitter(c, 5)


def L06():
    """超厚ゴールド枠リッチ"""
    c = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(c)
    for i, (col, w) in enumerate([(GOLD_D, 36), (GOLD, 22), (GOLD_L, 10), (HOT, 4)]):
        o = 20 + i * 22
        d.rectangle((o, o, W - o, H - o), outline=col, width=w)
    # corner roses
    for cx, cy in [(120, 120), (W - 120, 120), (120, H - 120), (W - 120, H - 120)]:
        rose(d, cx, cy, 48)
    tcenter(d, (W // 2, 180), "PREMIUM GIRLS SPACE", F(JOSE, 26, 400), GOLD_D)
    tcenter(d, (W // 2, 300), "Four Seasons", F(PLAY, 84, 700), INK)
    flourish(d, W // 2, 390, 1.4, GOLD)
    tcenter(d, (W // 2, 470), "Girls Bar  &  Girls Snack", F(SCRIPT, 54), HOT)
    ribbon(d, 540, "飲み放題付きセットあり")
    system_banner(d, 680)
    yy = price_rows(d, 780)
    yy = drink_box(d, yy + 20, 250)
    champagne(d, 260, yy + 140, 1.2)
    champagne(d, W - 260, yy + 140, 1.2)
    tcenter(d, (W // 2, yy + 140), "Luxury Night", F(SCRIPT, 44), GOLD_D)
    footer_band(d)
    return apply_glitter(c, 6)


def L07():
    """二席種カード＋下部飲み放題"""
    c = grad_v((W, H), (255, 210, 225), CREAM)
    d = ImageDraw.Draw(c)
    ornate_frame(d, 26)
    d.rectangle((70, 70, W - 70, 380), fill=HOT)
    for x in range(120, W - 100, 100):
        diamond(d, x, 100, 8, GOLD_L, GOLD)
    tcenter(d, (W // 2, 180), "Four Seasons", F(SCRIPT, 90), GOLD_L)
    tcenter(d, (W // 2, 290), "GIRLS BAR / SNACK", F(JOSE, 32, 500), WHITE)
    tcenter(d, (W // 2, 340), "大人女子の楽しい夜を", F(JP, 28), WHITE)
    # two seat cards
    for x0, title, price, sub in [
        (90, "カウンター席", "¥3,000", "気軽に楽しめる"),
        (W // 2 + 20, "ボックス席", "¥4,000", "ゆったりプライベート"),
    ]:
        d.rounded_rectangle((x0, 440, x0 + W // 2 - 110, 1180), radius=24, fill=WHITE, outline=GOLD, width=6)
        d.rectangle((x0, 440, x0 + W // 2 - 110, 540), fill=HOT)
        tcenter(d, (x0 + (W // 2 - 110) // 2, 490), title, F(JP, 34), WHITE)
        tcenter(d, (x0 + (W // 2 - 110) // 2, 680), "Set 50分", F(JP, 30), GOLD_D)
        tcenter(d, (x0 + (W // 2 - 110) // 2, 820), price, F(PLAY, 64, 700), HOT)
        tcenter(d, (x0 + (W // 2 - 110) // 2, 940), "TAX 20%", F(JP, 28), SOFT)
        tcenter(d, (x0 + (W // 2 - 110) // 2, 1060), sub, F(JP, 26), INK)
        rose(d, x0 + (W // 2 - 110) // 2, 1140, 30)
    d.rounded_rectangle((90, 1240, W - 90, 1780), radius=20, fill=(255, 235, 245), outline=HOT, width=5)
    tcenter(d, (W // 2, 1340), "★ 飲み放題メニュー ★", F(JP, 38), HOT)
    tcenter(d, (W // 2, 1480), "甲類・ウイスキー・リキュール各種", F(JP, 32), INK)
    tcenter(d, (W // 2, 1580), "割りもの・お茶類・炭酸", F(JP, 32), INK)
    tcenter(d, (W // 2, 1680), "初めてでも安心・明朗会計", F(JP, 28), GOLD_D)
    footer_band(d)
    return apply_glitter(c, 7)


def L08():
    """リボン連打ポップ"""
    c = Image.new("RGB", (W, H), (255, 242, 248))
    d = ImageDraw.Draw(c)
    # stripe bg
    for i in range(0, H, 28):
        if i // 28 % 2 == 0:
            d.rectangle((0, i, W, i + 28), fill=(255, 228, 238))
    ornate_frame(d, 22)
    header_block(d, 130)
    ribbons = [
        ("NEW OPEN 歓迎", HOT),
        ("女性スタッフ在籍", HOT2),
        ("飲み放題あり", GOLD_D),
        ("初めてでも安心", ROSE),
    ]
    for i, (txt, col) in enumerate(ribbons):
        ribbon(d, 400 + i * 120, txt, col, h=88)
    system_banner(d, 920)
    yy = price_rows(d, 1020)
    yy = drink_box(d, yy + 12, 230)
    footer_band(d)
    return apply_glitter(c, 8)


def L09():
    """ダイヤ散りばめメダル"""
    c = grad_v((W, H), (255, 236, 220), (255, 185, 205))
    d = ImageDraw.Draw(c)
    ornate_frame(d, 30)
    rng = random.Random(9)
    for _ in range(55):
        diamond(d, rng.randint(90, W - 90), rng.randint(90, H - 90), rng.randint(7, 16))
    tcenter(d, (W // 2, 170), "Four Seasons", F(PLAY, 78, 700), INK, GOLD_L, 2)
    tcenter(d, (W // 2, 270), "Girls Bar  ★  Girls Snack", F(JOSE, 28, 400), HOT)
    # medal
    d.ellipse((W // 2 - 290, 320, W // 2 + 290, 900), outline=GOLD, width=12)
    d.ellipse((W // 2 - 255, 355, W // 2 + 255, 865), outline=HOT, width=5)
    d.ellipse((W // 2 - 220, 390, W // 2 + 220, 830), fill=(255, 245, 250))
    tcenter(d, (W // 2, 480), "いちばん人気", F(JP, 30), HOT)
    tcenter(d, (W // 2, 580), "¥3,000〜", F(PLAY, 72, 700), INK)
    tcenter(d, (W // 2, 680), "カウンター Set 50分", F(JP, 30), SOFT)
    tcenter(d, (W // 2, 760), "ボックス ¥4,000", F(JP, 28), SOFT)
    # info strip
    d.rounded_rectangle((120, 960, W - 120, 1180), radius=18, fill=HOT, outline=GOLD_L, width=5)
    tcenter(d, (W // 2, 1020), "TAX 20%  ／  明朗会計", F(JP, 34), WHITE)
    tcenter(d, (W // 2, 1110), "Set 50分で気軽にどうぞ", F(JP, 28), GOLD_L)
    d.rounded_rectangle((120, 1240, W - 120, 1680), radius=18, fill=WHITE, outline=GOLD, width=5)
    tcenter(d, (W // 2, 1340), "★ 飲み放題 ★", F(JP, 38), HOT)
    tcenter(d, (W // 2, 1460), "甲類・ウイスキー・リキュール各種", F(JP, 30), INK)
    tcenter(d, (W // 2, 1560), "割りもの・お茶類・炭酸", F(JP, 30), INK)
    footer_band(d)
    return apply_glitter(c, 9)


def L10():
    """アーチステージ全面"""
    c = radial((W, H), (255, 250, 245), (255, 155, 185), cy=400)
    d = ImageDraw.Draw(c)
    ornate_frame(d)
    # arches
    for i, (inset, col, w) in enumerate([(160, GOLD, 14), (200, HOT, 7), (240, GOLD_L, 4)]):
        d.arc((inset, 80, W - inset, 720), 200, 340, fill=col, width=w)
    tcenter(d, (W // 2, 220), "Four Seasons", F(PLAY, 72, 700), INK)
    tcenter(d, (W // 2, 320), "Girls Bar / Girls Snack", F(SCRIPT, 46), HOT)
    # curtain-ish side panels
    for x0 in [80, W - 200]:
        d.rectangle((x0, 400, x0 + 120, 1100), fill=ROSE)
        for y in range(420, 1080, 40):
            d.ellipse((x0 + 10, y, x0 + 110, y + 50), outline=GOLD_L, width=2)
    for i, x in enumerate([400, 620, 840, 1060, 1280]):
        silhouette(d, x, 700, 1.2 + (i % 2) * 0.15, (255, 170 + i * 8, 198))
    ribbon(d, 980, "ステージのような華やかな夜を")
    system_banner(d, 1120)
    yy = price_rows(d, 1220)
    yy = drink_box(d, yy + 10, 220)
    footer_band(d)
    return apply_glitter(c, 10)


def L11():
    """4マス料金＋下部ワイド飲み放題"""
    c = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(c)
    for i, col in enumerate([HOT, GOLD, FUCHSIA := (255, 80, 160), GOLD_L, PINK]):
        d.rectangle((16 + i * 10, 16 + i * 10, W - 16 - i * 10, H - 16 - i * 10), outline=col, width=3)
    tcenter(d, (W // 2, 120), "TONIGHT", F(JOSE, 24, 300), GOLD_D)
    tcenter(d, (W // 2, 220), "Four Seasons", F(SCRIPT, 96), HOT)
    tcenter(d, (W // 2, 340), "ガールズバー ＆ ガールズスナック", F(JP, 32), INK)
    flourish(d, W // 2, 400, 1.2, GOLD)
    items = [("Set", "50分"), ("Counter", "¥3,000"), ("Box", "¥4,000"), ("TAX", "20%")]
    positions = [(100, 460), (W // 2 + 10, 460), (100, 900), (W // 2 + 10, 900)]
    for (x, y), (a, b) in zip(positions, items):
        d.rounded_rectangle((x, y, x + W // 2 - 120, y + 380), radius=22, fill=(255, 232, 242), outline=GOLD, width=5)
        starburst(d, x + 50, y + 50, 20)
        tcenter(d, (x + (W // 2 - 120) // 2, y + 130), a, F(JOSE, 30, 400), GOLD_D)
        fnt = F(JP, 52) if "分" in b else F(PLAY, 56, 700)
        tcenter(d, (x + (W // 2 - 120) // 2, y + 240), b, fnt, HOT)
    d.rounded_rectangle((100, 1360, W - 100, 1880), radius=22, fill=HOT)
    for x in range(160, W - 140, 90):
        diamond(d, x, 1400, 9, GOLD_L, GOLD)
    tcenter(d, (W // 2, 1520), "飲み放題メニュー", F(JP, 40), WHITE)
    tcenter(d, (W // 2, 1640), "甲類・ウイスキー・リキュール各種", F(JP, 30), GOLD_L)
    tcenter(d, (W // 2, 1740), "割りもの・お茶類・炭酸", F(JP, 30), GOLD_L)
    footer_band(d)
    return apply_glitter(c, 11)


def L12():
    """ネオン風ピンク全面"""
    c = Image.new("RGB", (W, H), (255, 210, 230))
    d = ImageDraw.Draw(c)
    # glow panels
    for y in range(100, H - 100, 180):
        d.rounded_rectangle((90, y, W - 90, y + 140), radius=20, outline=HOT, width=2)
    ornate_frame(d, 28)
    for sw, col in [(14, (255, 180, 210)), (6, HOT)]:
        tcenter(d, (W // 2, 200), "Four Seasons", F(PLAY, 76, 700), HOT, col, sw)
    tcenter(d, (W // 2, 320), "GIRLS BAR", F(JOSE, 44, 600), HOT2)
    tcenter(d, (W // 2, 400), "GIRLS SNACK", F(JOSE, 44, 600), GOLD_D)
    ribbon(d, 460, "キラキラ楽しい夜をどうぞ")
    system_banner(d, 600)
    yy = price_rows(d, 700)
    yy = drink_box(d, yy + 16, 250)
    for x in (220, W // 2, W - 220):
        champagne(d, x, yy + 160, 1.0)
    footer_band(d)
    return apply_glitter(c, 12)


def L13():
    """ティアラ王冠リッチ"""
    c = grad_v((W, H), CREAM, (255, 200, 225))
    d = ImageDraw.Draw(c)
    ornate_frame(d)
    # crown
    cx, cy = W // 2, 180
    d.polygon(
        [
            (cx - 140, cy + 50),
            (cx - 115, cy - 50),
            (cx - 55, cy + 15),
            (cx, cy - 80),
            (cx + 55, cy + 15),
            (cx + 115, cy - 50),
            (cx + 140, cy + 50),
        ],
        fill=GOLD_L,
        outline=GOLD,
    )
    d.rectangle((cx - 140, cy + 45, cx + 140, cy + 70), fill=GOLD)
    for dx in (-115, 0, 115):
        diamond(d, cx + dx, cy - 10, 14, HOT, GOLD)
    tcenter(d, (W // 2, 320), "Four Seasons", F(PLAY, 74, 700), INK)
    tcenter(d, (W // 2, 420), "Girls Bar  /  Girls Snack", F(SCRIPT, 50), HOT)
    ribbon(d, 500, "特別な一夜を、ここで。")
    system_banner(d, 640)
    yy = price_rows(d, 740)
    yy = drink_box(d, yy + 16, 240)
    # bottom rose garland
    for i, x in enumerate(range(200, W - 160, 120)):
        rose(d, x, yy + 120, 34, HOT if i % 2 == 0 else ROSE)
    footer_band(d)
    return apply_glitter(c, 13)


def L14():
    """横帯ストライプ全面使用"""
    c = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(c)
    band_h = 70
    colors = [HOT, GOLD_L, ROSE, PEACH := (255, 210, 190), PINK, GOLD, SOFT_P]
    for i in range(0, H, band_h):
        d.rectangle((0, i, W, i + band_h - 8), fill=colors[(i // band_h) % len(colors)])
    # content card covering most area
    d.rounded_rectangle((70, 160, W - 70, H - 160), radius=28, fill=IVORY, outline=GOLD_D, width=8)
    d.rounded_rectangle((95, 185, W - 95, H - 185), radius=20, outline=HOT, width=3)
    header_block(d, 240)
    ribbon(d, 500, "華やかな時間をあなたに")
    system_banner(d, 640)
    yy = price_rows(d, 740)
    yy = drink_box(d, yy + 16, 250)
    tcenter(d, (W // 2, yy + 100), "Four Seasons", F(SCRIPT, 52), HOT)
    footer_band(d, H - 140)
    return apply_glitter(c, 14)


def L15():
    """ハート装飾かわいい強め・面埋め"""
    c = radial((W, H), WHITE, (255, 165, 195))
    d = ImageDraw.Draw(c)
    ornate_frame(d, 26)

    def heart(cx, cy, s, fill):
        d.ellipse((cx - s, cy - s // 2, cx, cy + s // 2), fill=fill)
        d.ellipse((cx, cy - s // 2, cx + s, cy + s // 2), fill=fill)
        d.polygon([(cx - s, cy), (cx + s, cy), (cx, cy + int(s * 1.25))], fill=fill)

    for cx, cy, s in [
        (180, 180, 44),
        (W - 180, 200, 40),
        (200, H - 220, 48),
        (W - 200, H - 240, 42),
        (160, 900, 30),
        (W - 160, 900, 30),
        (300, 1600, 34),
        (W - 300, 1600, 34),
    ]:
        heart(cx, cy, s, PINK if (cx + cy) % 3 else HOT)
    header_block(d, 200)
    ribbon(d, 460, "LOVE ＆ SMILE な夜に")
    system_banner(d, 600)
    yy = price_rows(d, 700)
    yy = drink_box(d, yy + 16, 240)
    tcenter(d, (W // 2, yy + 100), "かわいく・楽しく・安心して", F(JP, 30), SOFT)
    footer_band(d)
    return apply_glitter(c, 15)


def L16():
    """高級感テーブル全面"""
    c = grad_v((W, H), (255, 245, 230), (255, 205, 195))
    d = ImageDraw.Draw(c)
    for i in range(5):
        d.rectangle((20 + i * 14, 20 + i * 14, W - 20 - i * 14, H - 20 - i * 14), outline=GOLD if i % 2 == 0 else GOLD_L, width=5)
    tcenter(d, (W // 2, 140), "LUXURY NIGHT", F(JOSE, 26, 300), GOLD_D)
    tcenter(d, (W // 2, 250), "Four Seasons", F(PLAY, 82, 700), INK)
    flourish(d, W // 2, 340, 1.5, GOLD)
    tcenter(d, (W // 2, 420), "Girls Bar & Snack", F(SCRIPT, 52), HOT)
    d.rounded_rectangle((100, 500, W - 100, 1750), radius=18, fill=WHITE, outline=GOLD, width=7)
    d.rectangle((100, 500, W - 100, 600), fill=HOT)
    tcenter(d, (W // 2, 550), "★ SYSTEM / 料金表 ★", F(JP, 36), WHITE)
    tcenter(d, (W // 4 + 40, 680), "内容", F(JP, 30), GOLD_D)
    tcenter(d, (3 * W // 4 - 40, 680), "料金", F(JP, 30), GOLD_D)
    d.line((140, 740, W - 140, 740), fill=GOLD, width=3)
    data = [
        ("Set 時間", "50分"),
        ("カウンター席", "¥3,000"),
        ("ボックス席", "¥4,000"),
        ("TAX", "20%"),
        ("飲み放題", "あり"),
    ]
    yy = 800
    for a, b in data:
        d.text((180, yy), a, font=F(JP, 36), fill=INK)
        fnt = F(JP, 38) if any(ord(ch) > 127 for ch in b) else F(PLAY, 40, 700)
        bb = d.textbbox((0, 0), b, font=fnt)
        d.text((W - 180 - (bb[2] - bb[0]), yy), b, font=fnt, fill=HOT)
        yy += 110
        d.line((160, yy - 40, W - 160, yy - 40), fill=(255, 220, 180), width=2)
    tcenter(d, (W // 2, 1500), "飲み放題メニュー", F(JP, 32), HOT)
    tcenter(d, (W // 2, 1580), "甲類・ウイスキー・リキュール各種", F(JP, 28), INK)
    tcenter(d, (W // 2, 1650), "割りもの・お茶類・炭酸", F(JP, 28), INK)
    for x in range(200, W - 160, 140):
        rose(d, x, 1900, 32)
    footer_band(d)
    return apply_glitter(c, 16)


def L17():
    """円形バッジ密集"""
    c = Image.new("RGB", (W, H), (255, 235, 242))
    d = ImageDraw.Draw(c)
    ornate_frame(d, 24)
    header_block(d, 120)
    badges = [
        (320, 520, "Set", "50分", HOT),
        (900, 520, "Counter", "¥3,000", HOT2),
        (1480, 520, "Box", "¥4,000", GOLD_D),
        (500, 920, "TAX", "20%", ROSE),
        (1100, 920, "Drink", "飲み放題", FUCHSIA := (255, 80, 160)),
        (900, 1280, "OK", "初めて歓迎", HOT),
    ]
    for cx, cy, en, jp, col in badges:
        d.ellipse((cx - 175, cy - 175, cx + 175, cy + 175), fill=col, outline=GOLD_L, width=8)
        d.ellipse((cx - 150, cy - 150, cx + 150, cy + 150), outline=WHITE, width=2)
        tcenter(d, (cx, cy - 40), en, F(JOSE, 24, 400), GOLD_L)
        fnt = F(JP, 36) if any(ord(ch) > 127 for ch in jp) else F(PLAY, 40, 700)
        tcenter(d, (cx, cy + 30), jp, fnt, WHITE)
    d.rounded_rectangle((120, 1520, W - 120, 1980), radius=20, fill=WHITE, outline=GOLD, width=5)
    tcenter(d, (W // 2, 1620), "飲み放題メニュー", F(JP, 36), HOT)
    tcenter(d, (W // 2, 1740), "甲類・ウイスキー・リキュール各種", F(JP, 30), INK)
    tcenter(d, (W // 2, 1840), "割りもの・お茶類・炭酸", F(JP, 30), INK)
    tcenter(d, (W // 2, 1920), "Set 50分 ／ TAX 20%", F(JP, 28), GOLD_D)
    footer_band(d)
    return apply_glitter(c, 17)


def L18():
    """上品×派手・装飾線＋シルエット"""
    c = grad_v((W, H), (255, 248, 252), (255, 190, 215))
    d = ImageDraw.Draw(c)
    ornate_frame(d, 36)
    flourish(d, W // 2, 140, 1.7, GOLD)
    tcenter(d, (W // 2, 230), "Four Seasons", F(PLAY_I, 74, 500), INK)
    tcenter(d, (W // 2, 330), "Girls Bar  ·  Girls Snack", F(SCRIPT, 50), HOT)
    yy = 420
    for label, price in [
        ("Set 50分", ""),
        ("カウンター席", "¥3,000"),
        ("ボックス席", "¥4,000"),
        ("TAX", "20%"),
    ]:
        d.line((180, yy, W - 180, yy), fill=GOLD, width=3)
        d.text((210, yy + 30), label, font=F(JP, 38), fill=INK)
        if price:
            fnt = F(PLAY, 46, 700)
            bb = d.textbbox((0, 0), price, font=fnt)
            d.text((W - 210 - (bb[2] - bb[0]), yy + 24), price, font=fnt, fill=HOT)
        else:
            tcenter(d, (W // 2 + 160, yy + 55), "50min", F(PLAY, 36, 600), GOLD_D)
        # side stars
        starburst(d, 150, yy + 55, 16)
        starburst(d, W - 150, yy + 55, 16)
        yy += 130
    d.line((180, yy, W - 180, yy), fill=GOLD, width=3)
    ribbon(d, yy + 30, "飲み放題  甲類・ウイスキー・リキュール")
    tcenter(d, (W // 2, yy + 180), "割りもの・お茶類・炭酸", F(JP, 30), INK)
    # bottom silhouettes fill
    d.rectangle((100, yy + 240, W - 100, H - 180), fill=(255, 220, 232))
    for i, x in enumerate(range(280, W - 240, 200)):
        silhouette(d, x, yy + 420, 1.25, (255, 175 + i * 6, 200))
    footer_band(d)
    return apply_glitter(c, 18)


def L19():
    """大文字インパクト＋白パネル密"""
    c = Image.new("RGB", (W, H), HOT)
    d = ImageDraw.Draw(c)
    d.rectangle((36, 36, W - 36, H - 36), outline=GOLD_L, width=12)
    d.rectangle((58, 58, W - 58, H - 58), outline=WHITE, width=3)
    # diagonal glitter bands
    for i in range(-H, W, 80):
        d.line((i, 0, i + H, H), fill=(255, 100, 160), width=2)
    tcenter(d, (W // 2, 160), "GIRLS", F(JOSE, 78, 600), WHITE)
    tcenter(d, (W // 2, 280), "BAR", F(JOSE, 78, 600), GOLD_L)
    tcenter(d, (W // 2, 400), "& SNACK", F(JOSE, 52, 500), WHITE)
    tcenter(d, (W // 2, 530), "Four Seasons", F(SCRIPT, 84), GOLD_L)
    for dx in (-90, -45, 0, 45, 90):
        diamond(d, W // 2 + dx, 610, 12, GOLD_L, GOLD)
    d.rounded_rectangle((90, 680, W - 90, H - 120), radius=28, fill=WHITE)
    system_banner(d, 740)
    yy = price_rows(d, 850)
    yy = drink_box(d, yy + 16, 280)
    tcenter(d, (W // 2, yy + 80), "WELCOME — 明朗会計", F(JP, 28), SOFT)
    return apply_glitter(c, 19)


def L20():
    """全部盛り・最密度"""
    c = radial((W, H), (255, 245, 250), (255, 140, 180), cy=H * 0.25)
    d = ImageDraw.Draw(c)
    ornate_frame(d, 20)
    for i in range(14):
        diamond(d, 110 + i * 120, 95, 12)
        diamond(d, 110 + i * 120, H - 95, 12)
    header_block(d, 140)
    ribbon(d, 400, "★ ガールズバー＆スナック ★")
    # triple medals
    medals = [("50分", "SET", 380), ("¥3,000", "COUNTER", 900), ("¥4,000", "BOX", 1420)]
    for price, label, cx in medals:
        d.ellipse((cx - 170, 540, cx + 170, 880), fill=WHITE, outline=GOLD, width=9)
        d.ellipse((cx - 145, 565, cx + 145, 855), outline=HOT, width=3)
        tcenter(d, (cx, 640), label, F(JOSE, 22, 400), GOLD_D)
        fnt = F(JP, 40) if "分" in price else F(PLAY, 40, 700)
        tcenter(d, (cx, 740), price, fnt, HOT)
    d.rounded_rectangle((110, 940, W - 110, 1120), radius=16, fill=HOT, outline=GOLD_L, width=4)
    tcenter(d, (W // 2, 1000), "TAX 20%  ／  Set 50分", F(JP, 36), WHITE)
    tcenter(d, (W // 2, 1070), "初めてでも安心・明朗会計", F(JP, 28), GOLD_L)
    d.rounded_rectangle((110, 1160, W - 110, 1580), radius=18, fill=WHITE, outline=HOT, width=5)
    tcenter(d, (W // 2, 1240), "★ 飲み放題メニュー ★", F(JP, 38), HOT)
    tcenter(d, (W // 2, 1360), "甲類・ウイスキー・リキュール各種", F(JP, 32), INK)
    tcenter(d, (W // 2, 1460), "割りもの・お茶類・炭酸", F(JP, 32), INK)
    tcenter(d, (W // 2, 1540), "カウンター ¥3,000 ／ ボックス ¥4,000", F(JP, 28), GOLD_D)
    # bottom glam strip
    d.rectangle((90, 1650, W - 90, H - 170), fill=(255, 200, 220))
    for i, x in enumerate(range(260, W - 220, 180)):
        silhouette(d, x, 1900, 1.15, (255, 165 + i * 8, 195))
        rose(d, x, 1720, 28)
    champagne(d, 180, 1950, 1.0)
    champagne(d, W - 180, 1950, 1.0)
    footer_band(d)
    return apply_glitter(c, 20)


LAYOUTS = [
    ("01_pink_gold", "ピンクゴールド王道", L01),
    ("02_hero_price", "円形ヒーロー料金", L02),
    ("03_silhouette", "シルエット舞台", L03),
    ("04_split_bold", "左右分割インパクト", L04),
    ("05_radial_spark", "放射キラキラ", L05),
    ("06_gold_rich", "ゴールドリッチ枠", L06),
    ("07_two_column", "二席種カード", L07),
    ("08_ribbon_pop", "リボン連打", L08),
    ("09_diamond_luxe", "ダイヤメダル", L09),
    ("10_stage_arch", "ステージアーチ", L10),
    ("11_info_grid", "4マス華やか", L11),
    ("12_neon_pink", "ネオンピンク", L12),
    ("13_crown", "ティアラ王冠", L13),
    ("14_stripe_glam", "ストライプ華やか", L14),
    ("15_heart_cute", "ハートかわいい", L15),
    ("16_luxury_table", "高級感料金表", L16),
    ("17_badge_pop", "円形バッジ密集", L17),
    ("18_elegant_flash", "上品×派手", L18),
    ("19_big_type", "大文字インパクト", L19),
    ("20_full_glam", "全部盛り華やか", L20),
]


def contact_sheet(items):
    cols, rows = 5, 4
    tw, th = 340, int(340 * RATIO)
    pad, lh = 14, 36
    sw = cols * tw + (cols + 1) * pad
    sh = 70 + rows * (th + lh + pad) + pad
    sheet = Image.new("RGB", (sw, sh), (255, 230, 240))
    d = ImageDraw.Draw(sheet)
    d.text((pad, 16), "Four Seasons — ガールズバー/スナック華やか案20（写真なし・明るめ・密度高め）", font=F(JP, 22), fill=INK)
    small = F(JP, 13)
    for i, (path, title) in enumerate(items):
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = 58 + pad + r * (th + lh + pad)
        im = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(im, (x, y))
        d.text((x, y + th + 4), f"{i+1:02d} {title}", font=small, fill=SOFT)
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
<title>Four Seasons 華やか案内パネル20</title>
<style>
body{{margin:0;background:#1a0a12;color:#ffe4ef;font-family:system-ui,sans-serif}}
header{{padding:24px;max-width:1200px;margin:0 auto}}
a{{color:#ffb6c1}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px;padding:16px 20px 40px;max-width:1200px;margin:0 auto}}
figure{{margin:0;background:#2a1020;border:1px solid #d4af37}}
img{{width:100%;display:block;aspect-ratio:594/841;object-fit:cover}}
figcaption{{padding:8px 10px;font-size:.8rem;color:#ffb6c1}}
</style></head><body>
<header><h1>Four Seasons — ガールズバー／スナック華やか案</h1>
<p>参考: 看板のピンク×ゴールド・煌めき・料金大表示・面を埋める構成。写真なし／暗め背景NG。
<a href="全候補_1枚まとめ.jpg">1枚まとめ</a></p></header>
<div class="grid">{cards}</div></body></html>""",
        encoding="utf-8",
    )


def luminance(im: Image.Image) -> float:
    s = im.convert("RGB").resize((80, 110), Image.Resampling.BOX)
    px = list(s.getdata())
    return sum(0.299 * r + 0.587 * g + 0.114 * b for r, g, b in px) / len(px)


def main():
    print("Generating dense glamorous girls-bar panels…")
    for p in OUT.glob("*.jpg"):
        p.unlink()
    items = []
    for name, title, fn in LAYOUTS:
        im = fn()
        assert im.size == (W, H), (name, im.size)
        lum = luminance(im)
        print(f"    lum≈{lum:.0f}")
        assert lum > 140, (name, lum)  # keep bright
        items.append(save(im, f"{name}.jpg", title))
    contact_sheet(items)
    make_viewer()
    (ROOT / "README.md").write_text(
        """# Four Seasons — ガールズバー／スナック華やかA1案20

ネット上の看板事例（ピンク×ゴールド、煌めき、料金大、華やかフレーム、面を埋める構成）を参考。

- 写真なし
- 暗め背景NG（明るい華やかトーン）
- 余白を残しすぎない（装飾・情報で面埋め）

## 掲載
Set 50分 / カウンター席 ¥3,000 / ボックス席 ¥4,000 / TAX 20%  
飲み放題：甲類・ウイスキー・リキュール各種／割りもの・お茶類・炭酸
""",
        encoding="utf-8",
    )
    # LINE bundle
    line = ROOT / "LINE送信用"
    line.mkdir(exist_ok=True)
    import shutil

    for p in OUT.glob("*.jpg"):
        shutil.copy2(p, line / p.name)
    shutil.copy2(ROOT / "全候補_1枚まとめ.jpg", line / "00_全候補まとめ.jpg")
    (line / "00_見る.html").write_text(
        (ROOT / "見る.html").read_text(encoding="utf-8").replace('src="panels/', 'src="'),
        encoding="utf-8",
    )
    print("done")


if __name__ == "__main__":
    main()
