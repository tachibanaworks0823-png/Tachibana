#!/usr/bin/env python3
"""
Four Seasons — ガールズバー／スナック案内所パネル 華やか案20
参考: サインモール等の看板（ピンク×ゴールド、煌めき、料金大、華やかフレーム）
制約: 写真なし / 暗めNG（明るい華やかトーン）
"""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
FONTS = ROOT / "assets" / "fonts"
OUT = ROOT / "panels"
OUT.mkdir(exist_ok=True)

W, H = 1786, 2529
RATIO = H / W

# Bright glam palette (no dark bases)
PINK = (255, 182, 193)
HOT = (255, 105, 180)
ROSE = (255, 120, 160)
FUCHSIA = (255, 80, 160)
GOLD = (218, 175, 90)
GOLD_L = (255, 220, 140)
GOLD_D = (190, 145, 70)
CREAM = (255, 248, 240)
IVORY = (255, 252, 248)
PEACH = (255, 220, 200)
LILAC = (255, 210, 230)
WHITE = (255, 255, 255)
INK = (90, 40, 55)
SOFT = (140, 70, 90)

PLAY = str(FONTS / "PlayfairDisplay[wght].ttf")
PLAY_I = str(FONTS / "PlayfairDisplay-Italic[wght].ttf")
JOSE = str(FONTS / "JosefinSans[wght].ttf")
SCRIPT = str(FONTS / "GreatVibes-Regular.ttf")
CORM = str(FONTS / "CormorantGaramond[wght].ttf")
JP = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
JP2 = "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"


def F(path: str, size: int, weight: int | None = None) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(path, size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f


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


def radial(size, c_center, c_edge):
    w, h = size
    im = Image.new("RGB", size)
    px = im.load()
    cx, cy = w / 2, h / 2
    maxd = math.hypot(cx, cy)
    for y in range(h):
        for x in range(w):
            t = min(1.0, math.hypot(x - cx, y - cy) / maxd)
            px[x, y] = tuple(int(c_center[j] + (c_edge[j] - c_center[j]) * t) for j in range(3))
    return im


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


def sparkles(d, n=80, color=GOLD_L, seed=1):
    rng = random.Random(seed)
    for _ in range(n):
        x, y = rng.randint(30, W - 30), rng.randint(30, H - 30)
        s = rng.randint(2, 7)
        # 4-point star
        d.line((x - s, y, x + s, y), fill=color, width=1)
        d.line((x, y - s, x, y + s), fill=color, width=1)
        if s > 4:
            d.line((x - s // 2, y - s // 2, x + s // 2, y + s // 2), fill=color, width=1)


def diamond(d, cx, cy, s, fill=GOLD_L, outline=GOLD):
    pts = [(cx, cy - s), (cx + s * 0.7, cy), (cx, cy + s), (cx - s * 0.7, cy)]
    d.polygon(pts, fill=fill, outline=outline)


def ornate_frame(d, m=36, outer=GOLD, inner=HOT, mid=GOLD_L):
    """三重の華やかフレーム"""
    d.rectangle((m, m, W - m, H - m), outline=outer, width=8)
    d.rectangle((m + 14, m + 14, W - m - 14, H - m - 14), outline=mid, width=3)
    d.rectangle((m + 26, m + 26, W - m - 26, H - m - 26), outline=inner, width=2)
    # corner ornaments
    for cx, cy in [(m + 50, m + 50), (W - m - 50, m + 50), (m + 50, H - m - 50), (W - m - 50, H - m - 50)]:
        diamond(d, cx, cy, 18, GOLD_L, GOLD)
        for a in range(0, 360, 45):
            rad = math.radians(a)
            d.line(
                (cx + math.cos(rad) * 10, cy + math.sin(rad) * 10, cx + math.cos(rad) * 28, cy + math.sin(rad) * 28),
                fill=GOLD,
                width=2,
            )


def flourish(d, cx, cy, scale=1.0, color=GOLD):
    """装飾曲線（簡易アラベスク）"""
    for sign in (-1, 1):
        pts = []
        for i in range(20):
            t = i / 19
            x = cx + sign * (40 + t * 90) * scale
            y = cy + math.sin(t * math.pi * 1.5) * 35 * scale * (1 if sign > 0 else -1)
            pts.append((x, y))
        if len(pts) > 1:
            d.line(pts, fill=color, width=3)


def ribbon(d, y, text, fill=HOT, ink=WHITE):
    """横断リボン帯"""
    d.polygon(
        [
            (80, y),
            (W - 80, y),
            (W - 50, y + 55),
            (W - 80, y + 110),
            (80, y + 110),
            (50, y + 55),
        ],
        fill=fill,
    )
    d.polygon([(80, y), (50, y + 55), (80, y + 40)], fill=GOLD_D)
    d.polygon([(W - 80, y), (W - 50, y + 55), (W - 80, y + 40)], fill=GOLD_D)
    tcenter(d, (W // 2, y + 55), text, F(JP, 36), ink)


def price_glam(d, y, ink=INK, accent=HOT, gold=GOLD):
    """派手な料金ブロック — 案内所向けに大きく"""
    # banner
    d.rounded_rectangle((120, y, W - 120, y + 70), radius=12, fill=accent)
    tcenter(d, (W // 2, y + 35), "★  SYSTEM / 料金  ★", F(JP, 34), WHITE)

    rows = [
        ("Set 50分", ""),
        ("カウンター席", "¥3,000"),
        ("ボックス席", "¥4,000"),
        ("TAX", "20%"),
    ]
    yy = y + 100
    for label, price in rows:
        d.rounded_rectangle((140, yy, W - 140, yy + 78), radius=10, outline=gold, width=3, fill=WHITE)
        d.text((170, yy + 18), label, font=F(JP, 34), fill=ink)
        if price:
            bb = d.textbbox((0, 0), price, font=F(PLAY, 40, 700))
            d.text((W - 170 - (bb[2] - bb[0]), yy + 14), price, font=F(PLAY, 40, 700), fill=accent)
        else:
            # emphasize set time
            tcenter(d, (W // 2 + 120, yy + 39), "50min", F(PLAY, 36, 600), gold)
        yy += 90

    # drink box
    d.rounded_rectangle((140, yy + 10, W - 140, yy + 200), radius=14, fill=(255, 240, 245), outline=accent, width=3)
    tcenter(d, (W // 2, yy + 50), "★ 飲み放題メニュー ★", F(JP, 32), accent)
    tcenter(d, (W // 2, yy + 105), "甲類・ウイスキー・リキュール各種", F(JP, 26), ink)
    tcenter(d, (W // 2, yy + 150), "割りもの・お茶類・炭酸", F(JP, 26), ink)
    return yy + 220


def brand_glam(d, y, ink=INK, accent=HOT):
    tcenter(d, (W // 2, y), "GIRLS BAR  /  GIRLS SNACK", F(JOSE, 28, 400), accent)
    flourish(d, W // 2 - 40, y + 55, 1.0, GOLD)
    flourish(d, W // 2 + 40, y + 55, 1.0, GOLD)
    tcenter(d, (W // 2, y + 120), "Four Seasons", F(PLAY, 78, 700), ink, stroke=GOLD_L, sw=1)
    # underline diamonds
    for dx in (-80, -40, 0, 40, 80):
        diamond(d, W // 2 + dx, y + 185, 10, GOLD_L, GOLD)


def silhouette(d, cx, cy, scale=1.0, color=(255, 200, 210)):
    """上品な女性シルエット（装飾用・顔なし）"""
    # head
    r = 28 * scale
    d.ellipse((cx - r, cy - r * 3.2, cx + r, cy - r * 1.2), fill=color)
    # hair suggestion
    d.ellipse((cx - r * 1.3, cy - r * 3.4, cx + r * 0.9, cy - r * 1.5), outline=HOT, width=3)
    # shoulders/dress
    d.polygon(
        [
            (cx - 55 * scale, cy + 90 * scale),
            (cx - 30 * scale, cy - 10 * scale),
            (cx + 30 * scale, cy - 10 * scale),
            (cx + 55 * scale, cy + 90 * scale),
            (cx, cy + 120 * scale),
        ],
        fill=color,
    )
    d.ellipse((cx - 35 * scale, cy - 20 * scale, cx + 35 * scale, cy + 40 * scale), fill=color)


def save(im, name, title):
    p = OUT / name
    im.convert("RGB").save(p, "JPEG", quality=90, optimize=True)
    print(f"  {name} — {title}")
    return p, title


# ---------- 20 glamorous layouts ----------

def L01():
    """ピンクゴールド王道"""
    c = radial((W, H), (255, 230, 240), (255, 180, 200))
    d = ImageDraw.Draw(c)
    ornate_frame(d)
    sparkles(d, 100, GOLD_L, 1)
    brand_glam(d, 180)
    ribbon(d, 480, "初めてでも安心 ◎ 明朗会計")
    price_glam(d, 640)
    tcenter(d, (W // 2, H - 90), "Four Seasons  ガールズバー＆スナック", F(JP, 26), SOFT)
    return c


def L02():
    """シャンパン×ホットピンク"""
    c = grad((W, H), CREAM, PEACH)
    d = ImageDraw.Draw(c)
    ornate_frame(d, 40, GOLD, FUCHSIA, GOLD_L)
    sparkles(d, 70, GOLD, 2)
    for i in range(6):
        diamond(d, 120 + i * 280, 140, 16)
    tcenter(d, (W // 2, 220), "Four Seasons", F(SCRIPT, 100), HOT)
    tcenter(d, (W // 2, 340), "GIRLS BAR  ★  GIRLS SNACK", F(JOSE, 30, 500), GOLD_D)
    # big price hero
    d.ellipse((W // 2 - 220, 420, W // 2 + 220, 860), fill=HOT, outline=GOLD, width=8)
    tcenter(d, (W // 2, 520), "カウンター", F(JP, 32), WHITE)
    tcenter(d, (W // 2, 620), "¥3,000", F(PLAY, 72, 700), GOLD_L)
    tcenter(d, (W // 2, 720), "Set 50分", F(JP, 30), WHITE)
    tcenter(d, (W // 2, 790), "TAX 20%", F(JOSE, 22, 400), GOLD_L)
    d.rounded_rectangle((160, 920, W - 160, 1280), radius=20, fill=WHITE, outline=GOLD, width=4)
    tcenter(d, (W // 2, 980), "ボックス席  ¥4,000", F(JP, 40), INK)
    tcenter(d, (W // 2, 1080), "飲み放題つき", F(JP, 36), HOT)
    tcenter(d, (W // 2, 1160), "甲類・ウイスキー・リキュール各種", F(JP, 26), SOFT)
    tcenter(d, (W // 2, 1220), "割りもの・お茶類・炭酸", F(JP, 26), SOFT)
    return c


def L03():
    """シルエット入り可愛い系（サインモール系）"""
    c = grad((W, H), (255, 240, 248), (255, 200, 220))
    d = ImageDraw.Draw(c)
    ornate_frame(d, 32, GOLD, HOT, GOLD_L)
    sparkles(d, 90, WHITE, 3)
    brand_glam(d, 160)
    # silhouettes row
    for i, x in enumerate([280, 560, 840, 1120, 1400]):
        silhouette(d, x, 620, 1.0 + (i % 2) * 0.15, (255, 190 + i * 8, 210))
    ribbon(d, 860, "かわいい女の子がお出迎え")
    price_glam(d, 1020, accent=HOT)
    return c


def L04():
    """縦分割・左ブランド右料金"""
    c = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(c)
    d.rectangle((0, 0, int(W * 0.48), H), fill=(255, 160, 190))
    sparkles(d, 50, GOLD_L, 4)
    # left
    tcenter(d, (int(W * 0.24), 280), "Girls", F(SCRIPT, 70), WHITE)
    tcenter(d, (int(W * 0.24), 380), "Bar", F(SCRIPT, 70), WHITE)
    tcenter(d, (int(W * 0.24), 520), "&", F(PLAY, 48, 400), GOLD_L)
    tcenter(d, (int(W * 0.24), 640), "Snack", F(SCRIPT, 70), WHITE)
    tcenter(d, (int(W * 0.24), 820), "Four", F(PLAY, 56, 700), GOLD_L)
    tcenter(d, (int(W * 0.24), 900), "Seasons", F(PLAY, 56, 700), GOLD_L)
    for i in range(8):
        diamond(d, int(W * 0.24), 1050 + i * 50, 8)
    # right
    rx = int(W * 0.52)
    tcenter(d, ((rx + W) // 2, 160), "料金 SYSTEM", F(JP, 36), HOT)
    rows = [("Set", "50分"), ("カウンター席", "¥3,000"), ("ボックス席", "¥4,000"), ("TAX", "20%")]
    yy = 240
    for a, b in rows:
        d.rounded_rectangle((rx + 30, yy, W - 50, yy + 120), radius=16, outline=GOLD, width=4, fill=WHITE)
        d.text((rx + 60, yy + 35), a, font=F(JP, 32), fill=INK)
        bb = d.textbbox((0, 0), b, font=F(PLAY, 44, 700))
        d.text((W - 80 - (bb[2] - bb[0]), yy + 30), b, font=F(PLAY, 44, 700), fill=HOT)
        yy += 140
    d.rounded_rectangle((rx + 30, yy + 20, W - 50, yy + 280), radius=16, fill=(255, 230, 240), outline=HOT, width=3)
    tcenter(d, ((rx + W) // 2, yy + 80), "飲み放題", F(JP, 34), HOT)
    tcenter(d, ((rx + W) // 2, yy + 150), "甲類・ウイスキー・リキュール", F(JP, 24), INK)
    tcenter(d, ((rx + W) // 2, yy + 210), "お茶・炭酸・割りもの", F(JP, 24), INK)
    return c


def L05():
    """放射キラキラ・中央店名"""
    c = radial((W, H), WHITE, (255, 170, 200))
    d = ImageDraw.Draw(c)
    # rays
    cx, cy = W // 2, int(H * 0.35)
    for a in range(0, 360, 8):
        rad = math.radians(a)
        d.line((cx, cy, cx + math.cos(rad) * 900, cy + math.sin(rad) * 900), fill=(255, 210, 220), width=3)
    ornate_frame(d, 28, GOLD, FUCHSIA, GOLD_L)
    sparkles(d, 120, GOLD_L, 5)
    brand_glam(d, 200)
    # price chips
    chips = [("Set 50分", 700), ("カウンター ¥3,000", 860), ("ボックス ¥4,000", 1020), ("TAX 20%", 1180)]
    for text, y in chips:
        d.rounded_rectangle((200, y, W - 200, y + 110), radius=55, fill=HOT, outline=GOLD, width=5)
        tcenter(d, (W // 2, y + 55), text, F(JP, 40), WHITE)
    tcenter(d, (W // 2, 1400), "飲み放題  甲類・ウイスキー・リキュール / お茶・炭酸", F(JP, 24), INK)
    return c


def L06():
    """ゴールド枠リッチ・白地"""
    c = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(c)
    # thick gold border bands
    for i, w in enumerate([40, 20, 8]):
        col = [GOLD_D, GOLD, GOLD_L][i]
        d.rectangle((30 + i * 18, 30 + i * 18, W - 30 - i * 18, H - 30 - i * 18), outline=col, width=w)
    sparkles(d, 60, GOLD, 6)
    tcenter(d, (W // 2, 200), "PREMIUM GIRLS SPACE", F(JOSE, 26, 400), GOLD_D)
    tcenter(d, (W // 2, 320), "Four Seasons", F(PLAY, 82, 700), INK)
    flourish(d, W // 2, 400, 1.3, GOLD)
    tcenter(d, (W // 2, 480), "Girls Bar  &  Girls Snack", F(SCRIPT, 52), HOT)
    ribbon(d, 580, "飲み放題付きセットあり")
    price_glam(d, 740, accent=FUCHSIA)
    return c


def L07():
    """二段組料金＋上部華やかヘッダー"""
    c = grad((W, H), (255, 220, 230), CREAM)
    d = ImageDraw.Draw(c)
    ornate_frame(d, 30, GOLD, HOT, GOLD_L)
    d.rectangle((60, 60, W - 60, 420), fill=HOT)
    sparkles(d, 40, GOLD_L, 7)
    tcenter(d, (W // 2, 140), "Four Seasons", F(SCRIPT, 86), GOLD_L)
    tcenter(d, (W // 2, 260), "GIRLS BAR / SNACK", F(JOSE, 32, 500), WHITE)
    tcenter(d, (W // 2, 340), "大人女子の楽しい夜を", F(JP, 28), WHITE)
    # two columns
    left, right = 80, W // 2 + 20
    for x0, title, lines in [
        (left, "カウンター席", [("Set 50分", ""), ("料金", "¥3,000"), ("TAX", "20%")]),
        (right, "ボックス席", [("Set 50分", ""), ("料金", "¥4,000"), ("TAX", "20%")]),
    ]:
        d.rounded_rectangle((x0, 480, x0 + W // 2 - 100, 1200), radius=24, fill=WHITE, outline=GOLD, width=5)
        tcenter(d, (x0 + (W // 2 - 100) // 2, 560), title, F(JP, 36), HOT)
        yy = 660
        for a, b in lines:
            tcenter(d, (x0 + (W // 2 - 100) // 2, yy), a if not b else f"{a}  {b}", F(JP, 32), INK)
            yy += 100
    d.rounded_rectangle((80, 1280, W - 80, 1680), radius=20, fill=(255, 235, 245), outline=HOT, width=4)
    tcenter(d, (W // 2, 1380), "★ 飲み放題メニュー ★", F(JP, 34), HOT)
    tcenter(d, (W // 2, 1500), "甲類・ウイスキー・リキュール各種", F(JP, 28), INK)
    tcenter(d, (W // 2, 1580), "割りもの・お茶類・炭酸", F(JP, 28), INK)
    return c


def L08():
    """リボン多めポップ華やか"""
    c = Image.new("RGB", (W, H), (255, 245, 250))
    d = ImageDraw.Draw(c)
    ornate_frame(d, 24, FUCHSIA, GOLD, GOLD_L)
    sparkles(d, 100, HOT, 8)
    brand_glam(d, 160, accent=FUCHSIA)
    for i, (txt, col) in enumerate(
        [("NEW OPEN 歓迎", HOT), ("女性スタッフ在籍", FUCHSIA), ("飲み放題あり", GOLD_D)]
    ):
        ribbon(d, 500 + i * 140, txt, col)
    price_glam(d, 980, accent=FUCHSIA)
    return c


def L09():
    """ダイヤ散りばめラグジュアリー（明るい）"""
    c = grad((W, H), (255, 236, 220), (255, 200, 210))
    d = ImageDraw.Draw(c)
    ornate_frame(d, 36, GOLD_D, HOT, GOLD)
    for _ in range(40):
        diamond(d, random.Random(9 + _).randint(80, W - 80), random.Random(20 + _).randint(80, H - 80), random.Random(30 + _).randint(6, 14))
    tcenter(d, (W // 2, 200), "Four Seasons", F(PLAY, 76, 700), INK, GOLD_L, 2)
    tcenter(d, (W // 2, 310), "Girls Bar  ★  Girls Snack", F(JOSE, 28, 400), HOT)
    # medal price
    d.ellipse((W // 2 - 260, 400, W // 2 + 260, 920), outline=GOLD, width=10)
    d.ellipse((W // 2 - 230, 430, W // 2 + 230, 890), outline=HOT, width=4)
    tcenter(d, (W // 2, 540), "いちばん人気", F(JP, 28), HOT)
    tcenter(d, (W // 2, 640), "¥3,000〜", F(PLAY, 70, 700), INK)
    tcenter(d, (W // 2, 740), "カウンター Set 50分", F(JP, 28), SOFT)
    tcenter(d, (W // 2, 820), "ボックス ¥4,000 / TAX20%", F(JP, 26), SOFT)
    d.rounded_rectangle((140, 1000, W - 140, 1400), radius=18, fill=WHITE, outline=GOLD, width=4)
    tcenter(d, (W // 2, 1080), "飲み放題", F(JP, 36), HOT)
    tcenter(d, (W // 2, 1180), "甲類・ウイスキー・リキュール各種", F(JP, 28), INK)
    tcenter(d, (W // 2, 1280), "割りもの・お茶類・炭酸", F(JP, 28), INK)
    return c


def L10():
    """ステージ風アーチ"""
    c = radial((W, H), (255, 250, 245), (255, 170, 190))
    d = ImageDraw.Draw(c)
    ornate_frame(d)
    # arch
    d.arc((200, 120, W - 200, 700), 200, 340, fill=GOLD, width=12)
    d.arc((240, 160, W - 240, 660), 200, 340, fill=HOT, width=5)
    brand_glam(d, 280)
    silhouette(d, W // 2 - 180, 780, 1.3, (255, 190, 205))
    silhouette(d, W // 2 + 180, 780, 1.3, (255, 200, 215))
    silhouette(d, W // 2, 750, 1.5, (255, 170, 195))
    price_glam(d, 1100)
    return c


def L11():
    """雑誌風だけど情報量多め・飾り枠"""
    c = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(c)
    for i in range(5):
        d.rectangle((20 + i * 10, 20 + i * 10, W - 20 - i * 10, H - 20 - i * 10), outline=[HOT, GOLD, FUCHSIA, GOLD_L, PINK][i], width=3)
    sparkles(d, 50, GOLD, 11)
    tcenter(d, (W // 2, 160), "TONIGHT", F(JOSE, 24, 300), GOLD_D)
    tcenter(d, (W // 2, 260), "Four Seasons", F(SCRIPT, 96), HOT)
    tcenter(d, (W // 2, 380), "ガールズバー ＆ ガールズスナック", F(JP, 32), INK)
    # info grid
    items = [
        ("Set", "50分"),
        ("Counter", "¥3,000"),
        ("Box", "¥4,000"),
        ("TAX", "20%"),
    ]
    positions = [(120, 500), (W // 2 + 20, 500), (120, 900), (W // 2 + 20, 900)]
    for (x, y), (a, b) in zip(positions, items):
        d.rounded_rectangle((x, y, x + W // 2 - 140, y + 320), radius=20, fill=(255, 235, 245), outline=GOLD, width=4)
        tcenter(d, (x + (W // 2 - 140) // 2, y + 100), a, F(JOSE, 28, 400), GOLD_D)
        tcenter(d, (x + (W // 2 - 140) // 2, y + 200), b, F(PLAY, 52, 700), HOT)
    d.rounded_rectangle((120, 1300, W - 120, 1700), radius=20, fill=HOT)
    tcenter(d, (W // 2, 1400), "飲み放題メニュー", F(JP, 36), WHITE)
    tcenter(d, (W // 2, 1520), "甲類・ウイスキー・リキュール各種", F(JP, 28), GOLD_L)
    tcenter(d, (W // 2, 1600), "割りもの・お茶類・炭酸", F(JP, 28), GOLD_L)
    return c


def L12():
    """ネオン風だけど明るいピンク地"""
    c = Image.new("RGB", (W, H), (255, 230, 240))
    d = ImageDraw.Draw(c)
    ornate_frame(d, 30, FUCHSIA, GOLD, HOT)
    # faux neon text glow via multiple strokes
    for sw, col in [(10, (255, 200, 220)), (4, HOT)]:
        tcenter(d, (W // 2, 220), "Four Seasons", F(PLAY, 74, 700), HOT, col, sw)
    tcenter(d, (W // 2, 340), "GIRLS BAR", F(JOSE, 40, 500), FUCHSIA)
    tcenter(d, (W // 2, 420), "GIRLS SNACK", F(JOSE, 40, 500), GOLD_D)
    sparkles(d, 90, WHITE, 12)
    price_glam(d, 520, accent=FUCHSIA)
    return c


def L13():
    """王冠・ティアラ装飾"""
    c = grad((W, H), CREAM, LILAC)
    d = ImageDraw.Draw(c)
    ornate_frame(d)
    # crown
    cx, cy = W // 2, 200
    d.polygon(
        [
            (cx - 120, cy + 40),
            (cx - 100, cy - 40),
            (cx - 50, cy + 10),
            (cx, cy - 70),
            (cx + 50, cy + 10),
            (cx + 100, cy - 40),
            (cx + 120, cy + 40),
        ],
        fill=GOLD_L,
        outline=GOLD,
    )
    for dx in (-100, 0, 100):
        diamond(d, cx + dx, cy - 20, 12, HOT, GOLD)
    tcenter(d, (W // 2, 320), "Four Seasons", F(PLAY, 72, 700), INK)
    tcenter(d, (W // 2, 420), "Girls Bar  /  Girls Snack", F(SCRIPT, 48), HOT)
    ribbon(d, 520, "特別な一夜を、ここで。")
    price_glam(d, 700)
    return c


def L14():
    """横帯ストライプ華やか"""
    c = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(c)
    colors = [HOT, GOLD_L, FUCHSIA, PEACH, PINK, GOLD]
    for i, col in enumerate(colors):
        d.rectangle((0, i * 40, W, i * 40 + 28), fill=col)
        d.rectangle((0, H - (i + 1) * 40, W, H - i * 40 - 12), fill=col)
    ornate_frame(d, 50, GOLD, HOT, GOLD_L)
    brand_glam(d, 320)
    price_glam(d, 700, accent=HOT)
    return c


def L15():
    """ハート装飾かわいい系強め"""
    c = radial((W, H), WHITE, (255, 190, 210))
    d = ImageDraw.Draw(c)
    ornate_frame(d, 28, HOT, GOLD, FUCHSIA)
    sparkles(d, 80, GOLD_L, 15)

    def heart(cx, cy, s, fill):
        d.ellipse((cx - s, cy - s // 2, cx, cy + s // 2), fill=fill)
        d.ellipse((cx, cy - s // 2, cx + s, cy + s // 2), fill=fill)
        d.polygon([(cx - s, cy), (cx + s, cy), (cx, cy + s * 1.2)], fill=fill)

    for cx, cy, s in [(200, 200, 40), (W - 200, 220, 36), (180, H - 220, 44), (W - 180, H - 240, 38)]:
        heart(cx, cy, s, PINK)
    brand_glam(d, 280, accent=HOT)
    price_glam(d, 650)
    return c


def L16():
    """高級感ゴールド多め・明るいベージュ"""
    c = grad((W, H), (255, 245, 230), (255, 220, 200))
    d = ImageDraw.Draw(c)
    for i in range(4):
        d.rectangle((25 + i * 12, 25 + i * 12, W - 25 - i * 12, H - 25 - i * 12), outline=GOLD if i % 2 == 0 else GOLD_L, width=4)
    sparkles(d, 70, GOLD, 16)
    tcenter(d, (W // 2, 180), "LUXURY NIGHT", F(JOSE, 24, 300), GOLD_D)
    tcenter(d, (W // 2, 300), "Four Seasons", F(PLAY, 80, 700), INK)
    flourish(d, W // 2, 380, 1.4, GOLD)
    tcenter(d, (W // 2, 460), "Girls Bar & Snack", F(SCRIPT, 50), HOT)
    # big system table
    d.rounded_rectangle((100, 560, W - 100, 1500), radius=16, fill=WHITE, outline=GOLD, width=6)
    headers = ["内容", "料金"]
    tcenter(d, (W // 4 + 50, 640), "内容", F(JP, 30), GOLD_D)
    tcenter(d, (3 * W // 4 - 50, 640), "料金", F(JP, 30), GOLD_D)
    d.line((140, 700, W - 140, 700), fill=GOLD, width=2)
    data = [("Set 時間", "50分"), ("カウンター席", "¥3,000"), ("ボックス席", "¥4,000"), ("TAX", "20%"), ("飲み放題", "あり")]
    yy = 760
    for a, b in data:
        d.text((180, yy), a, font=F(JP, 34), fill=INK)
        bb = d.textbbox((0, 0), b, font=F(PLAY, 38, 700))
        d.text((W - 180 - (bb[2] - bb[0]), yy), b, font=F(PLAY, 38, 700), fill=HOT)
        yy += 100
        d.line((160, yy - 30, W - 160, yy - 30), fill=(255, 220, 180), width=1)
    tcenter(d, (W // 2, 1600), "甲類・ウイスキー・リキュール / お茶・炭酸", F(JP, 24), SOFT)
    return c


def L17():
    """ポップ円形バッジ多数"""
    c = Image.new("RGB", (W, H), (255, 240, 245))
    d = ImageDraw.Draw(c)
    ornate_frame(d, 26, HOT, GOLD, FUCHSIA)
    brand_glam(d, 140)
    badges = [
        (300, 550, "Set\n50分", HOT),
        (900, 550, "Counter\n¥3,000", FUCHSIA),
        (1500, 550, "Box\n¥4,000", GOLD_D),
        (600, 950, "TAX\n20%", HOT),
        (1200, 950, "飲み\n放題", FUCHSIA),
    ]
    for cx, cy, text, col in badges:
        d.ellipse((cx - 160, cy - 160, cx + 160, cy + 160), fill=col, outline=GOLD_L, width=6)
        lines = text.split("\n")
        for i, line in enumerate(lines):
            tcenter(d, (cx, cy - 30 + i * 50), line, F(JP if any(ord(ch) > 127 for ch in line) else PLAY, 32), WHITE)
    d.rounded_rectangle((120, 1250, W - 120, 1650), radius=20, fill=WHITE, outline=GOLD, width=4)
    tcenter(d, (W // 2, 1350), "飲み放題メニュー", F(JP, 34), HOT)
    tcenter(d, (W // 2, 1470), "甲類・ウイスキー・リキュール各種", F(JP, 28), INK)
    tcenter(d, (W // 2, 1560), "割りもの・お茶類・炭酸", F(JP, 28), INK)
    return c


def L18():
    """エレガント＋派手の両立（参考: 派手だけど上品）"""
    c = grad((W, H), (255, 248, 252), (255, 210, 225))
    d = ImageDraw.Draw(c)
    ornate_frame(d, 40, GOLD, HOT, GOLD_L)
    sparkles(d, 110, GOLD_L, 18)
    flourish(d, W // 2, 160, 1.6, GOLD)
    tcenter(d, (W // 2, 240), "Four Seasons", F(PLAY_I, 70, 500), INK)
    tcenter(d, (W // 2, 340), "Girls Bar  ·  Girls Snack", F(SCRIPT, 48), HOT)
    # elegant price list with gold rules
    yy = 450
    for label, price in [("Set 50分", ""), ("カウンター席", "¥3,000"), ("ボックス席", "¥4,000"), ("TAX 20%", "")]:
        d.line((200, yy, W - 200, yy), fill=GOLD, width=2)
        d.text((220, yy + 25), label, font=F(JP, 36), fill=INK)
        if price:
            bb = d.textbbox((0, 0), price, font=F(PLAY, 44, 700))
            d.text((W - 220 - (bb[2] - bb[0]), yy + 20), price, font=F(PLAY, 44, 700), fill=HOT)
        yy += 110
    d.line((200, yy, W - 200, yy), fill=GOLD, width=2)
    ribbon(d, yy + 40, "飲み放題  甲類・ウイスキー・リキュール / お茶・炭酸")
    silhouette(d, 220, H - 280, 1.1, (255, 200, 215))
    silhouette(d, W - 220, H - 280, 1.1, (255, 200, 215))
    return c


def L19():
    """インパクト大文字＋下部システム"""
    c = Image.new("RGB", (W, H), HOT)
    d = ImageDraw.Draw(c)
    d.rectangle((40, 40, W - 40, H - 40), outline=GOLD_L, width=10)
    d.rectangle((60, 60, W - 60, H - 60), outline=WHITE, width=3)
    sparkles(d, 80, GOLD_L, 19)
    tcenter(d, (W // 2, 200), "GIRLS", F(JOSE, 70, 600), WHITE)
    tcenter(d, (W // 2, 320), "BAR", F(JOSE, 70, 600), GOLD_L)
    tcenter(d, (W // 2, 440), "& SNACK", F(JOSE, 48, 500), WHITE)
    tcenter(d, (W // 2, 580), "Four Seasons", F(SCRIPT, 80), GOLD_L)
    d.rounded_rectangle((100, 720, W - 100, H - 120), radius=24, fill=WHITE)
    price_glam(d, 780, accent=HOT)
    return c


def L20():
    """集大成・全部盛り華やか"""
    c = radial((W, H), (255, 245, 250), (255, 160, 190))
    d = ImageDraw.Draw(c)
    ornate_frame(d, 22, GOLD, FUCHSIA, GOLD_L)
    sparkles(d, 130, GOLD_L, 20)
    for i in range(12):
        diamond(d, 100 + i * 140, 100, 12)
        diamond(d, 100 + i * 140, H - 100, 12)
    brand_glam(d, 180)
    ribbon(d, 480, "★ ガールズバー＆スナック ★")
    # triple price medals
    medals = [("50分", "SET", 380), ("¥3,000", "COUNTER", 900), ("¥4,000", "BOX", 1420)]
    for price, label, cx in medals:
        d.ellipse((cx - 150, 640, cx + 150, 940), fill=WHITE, outline=GOLD, width=8)
        tcenter(d, (cx, 740), label, F(JOSE, 20, 400), GOLD_D)
        tcenter(d, (cx, 820), price, F(PLAY, 36, 700), HOT)
    d.rounded_rectangle((120, 1040, W - 120, 1550), radius=18, fill=WHITE, outline=HOT, width=5)
    tcenter(d, (W // 2, 1120), "TAX 20%", F(JP, 34), INK)
    tcenter(d, (W // 2, 1220), "飲み放題メニュー", F(JP, 36), HOT)
    tcenter(d, (W // 2, 1340), "甲類・ウイスキー・リキュール各種", F(JP, 28), INK)
    tcenter(d, (W // 2, 1440), "割りもの・お茶類・炭酸", F(JP, 28), INK)
    tcenter(d, (W // 2, H - 120), "Four Seasons へようこそ", F(JP, 30), WHITE)
    return c


LAYOUTS = [
    ("01_pink_gold", "ピンクゴールド王道", L01),
    ("02_hero_price", "円形ヒーロー料金", L02),
    ("03_silhouette", "シルエット可愛い系", L03),
    ("04_split_bold", "左右分割インパクト", L04),
    ("05_radial_spark", "放射キラキラ", L05),
    ("06_gold_rich", "ゴールドリッチ枠", L06),
    ("07_two_column", "二席種カラム", L07),
    ("08_ribbon_pop", "リボンポップ", L08),
    ("09_diamond_luxe", "ダイヤラグジュアリー", L09),
    ("10_stage_arch", "ステージアーチ", L10),
    ("11_info_grid", "情報グリッド華やか", L11),
    ("12_neon_pink", "ネオンピンク", L12),
    ("13_crown", "ティアラ王冠", L13),
    ("14_stripe_glam", "ストライプ華やか", L14),
    ("15_heart_cute", "ハートかわいい", L15),
    ("16_luxury_table", "高級感料金表", L16),
    ("17_badge_pop", "円形バッジ", L17),
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
    sheet = Image.new("RGB", (sw, sh), (255, 240, 245))
    d = ImageDraw.Draw(sheet)
    d.text((pad, 16), "Four Seasons — ガールズバー/スナック華やか案20（写真なし・明るめ）", font=F(JP, 24), fill=INK)
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
<p>参考: 看板のピンク×ゴールド・煌めき・料金大表示。写真なし／暗め背景NG。
<a href="全候補_1枚まとめ.jpg">1枚まとめ</a></p></header>
<div class="grid">{cards}</div></body></html>""",
        encoding="utf-8",
    )


def main():
    print("Generating glamorous girls-bar panels…")
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
        """# Four Seasons — ガールズバー／スナック華やかA1案20

ネット上の看板事例（ピンク×ゴールド、煌めき、料金を大きく、華やかフレーム）を参考。

- 写真なし
- 暗め背景NG（明るい華やかトーン）
- シンプル過ぎない装飾多め

## 掲載
Set 50分 / カウンター席 ¥3,000 / ボックス席 ¥4,000 / TAX 20%  
飲み放題：甲類・ウイスキー・リキュール各種／割りもの・お茶類・炭酸
""",
        encoding="utf-8",
    )
    print("done")


if __name__ == "__main__":
    main()
