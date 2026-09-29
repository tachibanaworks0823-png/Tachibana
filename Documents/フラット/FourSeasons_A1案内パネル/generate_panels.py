#!/usr/bin/env python3
"""Four Seasons — 写真なし・明るめ可愛い落ち着き A1案20（ガールズバー／スナック）"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FONTS = ROOT / "assets" / "fonts"
OUT = ROOT / "panels"
OUT.mkdir(exist_ok=True)

W, H = 1786, 2529
RATIO = H / W

# Light-only palette (dark NG)
IVORY = (255, 252, 248)
CREAM = (255, 248, 242)
BLUSH = (255, 236, 232)
PEACH = (255, 232, 220)
PINK = (252, 214, 214)
ROSE = (220, 140, 148)
SOFT_ROSE = (232, 168, 172)
DUST = (196, 148, 148)
MINT = (232, 244, 238)
SAGE = (168, 196, 180)
SKY = (232, 242, 248)
POWDER = (220, 232, 242)
LILAC = (242, 232, 242)
BUTTER = (255, 246, 220)
CHAMP = (232, 204, 168)
INK = (72, 56, 60)
SOFT_INK = (110, 88, 92)
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


def tcenter(d, xy, text, fnt, fill):
    x, y = xy
    bb = d.textbbox((0, 0), text, font=fnt)
    d.text((x - (bb[2] - bb[0]) / 2, y - (bb[3] - bb[1]) / 2), text, font=fnt, fill=fill)


def line(d, y, x0, x1, fill, w=1):
    d.line((x0, y, x1, y), fill=fill, width=w)


def dots(d, n=40, color=(255, 220, 220), r=3):
    import random

    rng = random.Random(42)
    for _ in range(n):
        x, y = rng.randint(40, W - 40), rng.randint(40, H - 40)
        d.ellipse((x - r, y - r, x + r, y + r), fill=color)


def soft_circles(d, color=(255, 220, 220), alpha_layer=None):
    """Decorative soft circles (drawn solid light)."""
    for cx, cy, r in [(120, 180, 90), (W - 100, 300, 70), (80, H - 200, 110), (W - 140, H - 280, 80)]:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=2)


def petal(d, cx, cy, size, color, angle=0):
    """Simple 4-petal flower."""
    for i in range(4):
        a = angle + i * math.pi / 2
        px = cx + math.cos(a) * size * 0.55
        py = cy + math.sin(a) * size * 0.55
        d.ellipse((px - size * 0.45, py - size * 0.45, px + size * 0.45, py + size * 0.45), fill=color)
    d.ellipse((cx - size * 0.22, cy - size * 0.22, cx + size * 0.22, cy + size * 0.22), fill=CHAMP)


def leaf_spray(d, cx, cy, color=SAGE, scale=1.0):
    """Four-seasons-like leaf spray."""
    for i, (dx, dy, s) in enumerate([(-18, -8, 1), (0, -22, 1.1), (18, -8, 1), (0, 10, 0.85)]):
        x, y = cx + dx * scale, cy + dy * scale
        w, h = 14 * scale * s, 28 * scale * s
        d.ellipse((x - w / 2, y - h / 2, x + w / 2, y + h / 2), fill=color if i % 2 == 0 else SOFT_ROSE)


def frame_roundish(d, m=48, color=SOFT_ROSE, width=2):
    d.rounded_rectangle((m, m, W - m, H - m), radius=36, outline=color, width=width)


def brand(d, cx, y, ink=INK, accent=ROSE, scale=1.0):
    tcenter(d, (cx, y), "Girls Bar  /  Girls Snack", F(JOSE, int(22 * scale), 300), accent)
    tcenter(d, (cx, y + int(70 * scale)), "Four Seasons", F(PLAY, int(68 * scale), 600), ink)
    leaf_spray(d, cx, y + int(130 * scale), SAGE if True else accent, scale * 1.2)
    line(d, y + int(165 * scale), cx - int(70 * scale), cx + int(70 * scale), accent, 1)


def price_block(d, x, y, w, ink=INK, accent=ROSE, scale=1.0, center=False):
    f_h = F(JP, int(24 * scale))
    f_j = F(JP, int(28 * scale))
    f_n = F(PLAY, int(32 * scale), 500)
    f_s = F(JP, int(20 * scale))
    rows = [("Set 50分", ""), ("カウンター席", "¥3,000"), ("ボックス席", "¥4,000"), ("TAX 20%", "")]
    yy = y
    if center:
        tcenter(d, (x + w // 2, yy), "料金", f_h, accent)
        yy += int(40 * scale)
        for a, b in rows:
            tcenter(d, (x + w // 2, yy), f"{a}  {b}".strip(), f_j, ink)
            yy += int(42 * scale)
        yy += int(12 * scale)
        tcenter(d, (x + w // 2, yy), "飲み放題", f_h, accent)
        yy += int(36 * scale)
        tcenter(d, (x + w // 2, yy), "甲類・ウイスキー・リキュール各種", f_s, soft_ink(ink))
        yy += int(30 * scale)
        tcenter(d, (x + w // 2, yy), "割りもの・お茶類・炭酸", f_s, soft_ink(ink))
        return yy
    d.text((x, yy), "料金", font=f_h, fill=accent)
    yy += int(38 * scale)
    for a, b in rows:
        d.text((x, yy), a, font=f_j, fill=ink)
        if b:
            bb = d.textbbox((0, 0), b, font=f_n)
            d.text((x + w - (bb[2] - bb[0]), yy), b, font=f_n, fill=ink)
        yy += int(44 * scale)
    yy += int(14 * scale)
    d.text((x, yy), "飲み放題", font=f_h, fill=accent)
    yy += int(34 * scale)
    d.text((x, yy), "甲類・ウイスキー・リキュール各種", font=f_s, fill=soft_ink(ink))
    yy += int(28 * scale)
    d.text((x, yy), "割りもの・お茶類・炭酸", font=f_s, fill=soft_ink(ink))
    return yy


def soft_ink(ink):
    return tuple(min(255, c + 40) for c in ink)


def save(im, name, title):
    p = OUT / name
    im.convert("RGB").save(p, "JPEG", quality=90, optimize=True)
    print(f"  {name} — {title}")
    return p, title


# ---------- 20 light cute-calm layouts ----------

def L01():
    c = grad((W, H), BLUSH, CREAM)
    d = ImageDraw.Draw(c)
    frame_roundish(d, 56, SOFT_ROSE, 2)
    for i, (x, y) in enumerate([(160, 220), (W - 180, 260), (200, H - 260), (W - 200, H - 300)]):
        petal(d, x, y, 28 + i * 2, PINK)
    brand(d, W // 2, 380, INK, ROSE, 1.15)
    tcenter(d, (W // 2, 680), "落ち着いて、可愛く過ごす夜。", F(JP, 32), SOFT_INK)
    price_block(d, int(W * 0.18), 820, int(W * 0.64), INK, ROSE, 1.1, center=True)
    return c


def L02():
    c = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(c)
    d.rectangle((0, 0, W, 220), fill=BLUSH)
    d.rectangle((0, H - 180, W, H), fill=MINT)
    tcenter(d, (W // 2, 90), "GIRLS BAR  ·  GIRLS SNACK", F(JOSE, 26, 300), ROSE)
    tcenter(d, (W // 2, 360), "Four Seasons", F(SCRIPT, 96), ROSE)
    leaf_spray(d, W // 2, 480, SAGE, 1.4)
    line(d, 540, int(W * 0.3), int(W * 0.7), SOFT_ROSE, 1)
    tcenter(d, (W // 2, 620), "やさしい時間のガールズスナック", F(JP, 30), SOFT_INK)
    price_block(d, int(W * 0.16), 760, int(W * 0.68), INK, ROSE, 1.05, center=True)
    return c


def L03():
    c = grad((W, H), PEACH, IVORY)
    d = ImageDraw.Draw(c)
    soft_circles(d, (255, 210, 200))
    d.rounded_rectangle((100, 160, W - 100, H - 160), radius=48, fill=WHITE, outline=SOFT_ROSE, width=2)
    brand(d, W // 2, 320, INK, ROSE, 1.05)
    tcenter(d, (W // 2, 620), "Girls Snack", F(SCRIPT, 64), SOFT_ROSE)
    price_block(d, 180, 760, W - 360, INK, ROSE, 1.0)
    return c


def L04():
    c = Image.new("RGB", (W, H), MINT)
    d = ImageDraw.Draw(c)
    d.ellipse((-200, -200, 500, 500), fill=(220, 240, 230))
    d.ellipse((W - 450, H - 500, W + 120, H + 80), fill=(240, 248, 242))
    tcenter(d, (W // 2, 200), "Four Seasons", F(PLAY, 64, 500), INK)
    tcenter(d, (W // 2, 290), "Girls Bar & Snack", F(JOSE, 28, 300), SAGE)
    for i in range(5):
        petal(d, 200 + i * 340, 420, 22, (210, 230, 218) if i % 2 else PINK)
    line(d, 520, 200, W - 200, SAGE, 1)
    price_block(d, int(W * 0.16), 620, int(W * 0.68), INK, (120, 160, 140), 1.05, center=True)
    tcenter(d, (W // 2, H - 160), "ご来店お待ちしております", F(JP, 26), SOFT_INK)
    return c


def L05():
    c = grad((W, H), LILAC, BLUSH)
    d = ImageDraw.Draw(c)
    frame_roundish(d, 40, (220, 190, 210), 1)
    tcenter(d, (W // 2, 220), "cute  &  calm", F(JOSE, 24, 300), DUST)
    tcenter(d, (W // 2, 340), "Four Seasons", F(PLAY_I, 72, 400), INK)
    tcenter(d, (W // 2, 440), "Girls Snack", F(SCRIPT, 60), ROSE)
    # ribbon-like bands
    d.rectangle((120, 560, W - 120, 564), fill=SOFT_ROSE)
    d.rectangle((160, 590, W - 160, 592), fill=CHAMP)
    price_block(d, int(W * 0.18), 700, int(W * 0.64), INK, ROSE, 1.05, center=True)
    return c


def L06():
    c = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(c)
    # soft grid of petals
    for row in range(6):
        for col in range(4):
            petal(d, 180 + col * 420, 180 + row * 380, 16, (255, 230, 228) if (row + col) % 2 == 0 else (230, 240, 235))
    d.rounded_rectangle((140, 280, W - 140, H - 280), radius=28, fill=(255, 252, 250), outline=SOFT_ROSE, width=2)
    brand(d, W // 2, 420, INK, ROSE, 1.0)
    price_block(d, 220, 780, W - 440, INK, ROSE, 1.0)
    return c


def L07():
    c = grad((W, H), SKY, IVORY)
    d = ImageDraw.Draw(c)
    d.rectangle((0, 0, 28, H), fill=POWDER)
    d.rectangle((W - 28, 0, W, H), fill=PINK)
    tcenter(d, (W // 2, 200), "GIRLS BAR", F(JOSE, 28, 300), (140, 170, 190))
    tcenter(d, (W // 2, 320), "Four Seasons", F(SCRIPT, 90), ROSE)
    tcenter(d, (W // 2, 430), "Girls Snack", F(PLAY, 42, 500), INK)
    leaf_spray(d, W // 2, 540, (150, 186, 190), 1.3)
    price_block(d, int(W * 0.16), 700, int(W * 0.68), INK, ROSE, 1.05, center=True)
    return c


def L08():
    c = Image.new("RGB", (W, H), BUTTER)
    d = ImageDraw.Draw(c)
    frame_roundish(d, 50, CHAMP, 2)
    tcenter(d, (W // 2, 260), "Four Seasons", F(PLAY, 70, 600), INK)
    tcenter(d, (W // 2, 360), "Girls Bar  ·  Girls Snack", F(JOSE, 26, 300), DUST)
    # soft arches
    for i in range(3):
        y = 480 + i * 40
        d.arc((200, y, W - 200, y + 280), 200, 340, fill=CHAMP, width=2)
    price_block(d, int(W * 0.18), 860, int(W * 0.64), INK, (180, 140, 90), 1.05, center=True)
    return c


def L09():
    c = grad((W, H), (255, 240, 244), PEACH)
    d = ImageDraw.Draw(c)
    # top scallop suggestion via circles
    for i in range(10):
        x = i * 200 - 40
        d.ellipse((x, -60, x + 160, 100), fill=PINK)
    tcenter(d, (W // 2, 220), "Girls Snack", F(SCRIPT, 78), ROSE)
    tcenter(d, (W // 2, 330), "Four Seasons", F(PLAY, 60, 500), INK)
    tcenter(d, (W // 2, 430), "かわいく、落ち着けるお店です", F(JP, 30), SOFT_INK)
    price_block(d, int(W * 0.16), 580, int(W * 0.68), INK, ROSE, 1.1, center=True)
    return c


def L10():
    c = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(c)
    # two soft color blocks
    d.rounded_rectangle((80, 80, W - 80, int(H * 0.42)), radius=40, fill=BLUSH)
    d.rounded_rectangle((80, int(H * 0.46), W - 80, H - 80), radius=40, fill=MINT)
    tcenter(d, (W // 2, 200), "Four Seasons", F(PLAY, 62, 600), INK)
    tcenter(d, (W // 2, 300), "Girls Bar", F(SCRIPT, 56), ROSE)
    leaf_spray(d, W // 2, 400, SAGE, 1.2)
    tcenter(d, (W // 2, int(H * 0.46) + 100), "Girls Snack", F(SCRIPT, 52), (120, 160, 140))
    price_block(d, int(W * 0.18), int(H * 0.46) + 200, int(W * 0.64), INK, (120, 160, 140), 1.0, center=True)
    return c


def L11():
    c = grad((W, H), CREAM, BLUSH)
    d = ImageDraw.Draw(c)
    dots(d, 55, (255, 210, 210), 4)
    brand(d, W // 2, 300, INK, ROSE, 1.2)
    # cute info cards as soft panels (interaction-like but design only)
    panel_y = 720
    d.rounded_rectangle((140, panel_y, W - 140, panel_y + 900), radius=32, fill=WHITE, outline=PINK, width=2)
    price_block(d, 200, panel_y + 60, W - 400, INK, ROSE, 1.05)
    return c


def L12():
    c = Image.new("RGB", (W, H), (248, 244, 252))  # very light lilac
    d = ImageDraw.Draw(c)
    frame_roundish(d, 60, (210, 190, 220), 2)
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        petal(d, W // 2 + math.cos(a) * 280, 420 + math.sin(a) * 80, 18, PINK if ang % 90 == 0 else (230, 220, 240))
    tcenter(d, (W // 2, 400), "Four Seasons", F(PLAY, 66, 500), INK)
    tcenter(d, (W // 2, 500), "Girls Bar / Girls Snack", F(JOSE, 26, 300), DUST)
    price_block(d, int(W * 0.18), 700, int(W * 0.64), INK, ROSE, 1.05, center=True)
    return c


def L13():
    c = grad((W, H), IVORY, MINT)
    d = ImageDraw.Draw(c)
    tcenter(d, (W // 2, 180), "ようこそ", F(JP, 28), SAGE)
    tcenter(d, (W // 2, 300), "Four Seasons", F(SCRIPT, 88), ROSE)
    line(d, 380, int(W * 0.25), int(W * 0.75), SOFT_ROSE, 1)
    labels = ["Girls Bar", "Girls Snack", "やさしい空間"]
    gap, bw = 24, (W - 200 - 48) // 3
    for i, lab in enumerate(labels):
        x0 = 100 + i * (bw + gap)
        d.rounded_rectangle((x0, 460, x0 + bw, 560), radius=28, fill=WHITE, outline=SAGE, width=1)
        tcenter(d, (x0 + bw // 2, 510), lab, F(JP if i == 2 else JOSE, 24), SOFT_INK)
    price_block(d, int(W * 0.16), 700, int(W * 0.68), INK, ROSE, 1.05, center=True)
    return c


def L14():
    c = Image.new("RGB", (W, H), PEACH)
    d = ImageDraw.Draw(c)
    d.rectangle((0, int(H * 0.08), W, int(H * 0.08) + 8), fill=SOFT_ROSE)
    d.rectangle((0, int(H * 0.92), W, int(H * 0.92) + 8), fill=SOFT_ROSE)
    brand(d, W // 2, 320, INK, ROSE, 1.15)
    tcenter(d, (W // 2, 620), "Tonight, softly.", F(PLAY_I, 40, 400), DUST)
    price_block(d, int(W * 0.16), 780, int(W * 0.68), INK, ROSE, 1.08, center=True)
    return c


def L15():
    c = grad((W, H), BLUSH, (255, 248, 252))
    d = ImageDraw.Draw(c)
    # heart-soft shapes as ellipses cluster (cute, not emoji)
    for cx, cy, rx, ry in [(W // 2, 280, 200, 120), (W // 2 - 90, 240, 100, 90), (W // 2 + 90, 240, 100, 90)]:
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=PINK)
    tcenter(d, (W // 2, 260), "Four Seasons", F(PLAY, 48, 600), WHITE)
    tcenter(d, (W // 2, 480), "Girls Snack", F(SCRIPT, 64), ROSE)
    tcenter(d, (W // 2, 580), "Girls Bar", F(JOSE, 28, 300), DUST)
    price_block(d, int(W * 0.16), 720, int(W * 0.68), INK, ROSE, 1.05, center=True)
    return c


def L16():
    c = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(c)
    # diagonal soft band
    for i in range(0, H, 8):
        t = i / H
        col = tuple(int(IVORY[j] + (BLUSH[j] - IVORY[j]) * abs(math.sin(t * math.pi))) for j in range(3))
        d.line((0, i, W, i), fill=col)
    frame_roundish(d, 70, SOFT_ROSE, 2)
    brand(d, W // 2, 360, INK, ROSE, 1.1)
    price_block(d, int(W * 0.18), 780, int(W * 0.64), INK, ROSE, 1.05, center=True)
    return c


def L17():
    c = grad((W, H), (240, 248, 244), CREAM)
    d = ImageDraw.Draw(c)
    # vertical cute columns
    d.rectangle((0, 0, int(W * 0.12), H), fill=MINT)
    d.rectangle((int(W * 0.88), 0, W, H), fill=BLUSH)
    tcenter(d, (W // 2, 220), "Four Seasons", F(PLAY, 64, 500), INK)
    leaf_spray(d, W // 2, 340, SAGE, 1.5)
    tcenter(d, (W // 2, 440), "Girls Bar", F(SCRIPT, 54), ROSE)
    tcenter(d, (W // 2, 530), "Girls Snack", F(SCRIPT, 54), (120, 160, 140))
    line(d, 600, int(W * 0.25), int(W * 0.75), CHAMP, 1)
    price_block(d, int(W * 0.18), 700, int(W * 0.64), INK, ROSE, 1.05, center=True)
    return c


def L18():
    c = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(c)
    # ticket-like soft outer
    d.rounded_rectangle((70, 70, W - 70, H - 70), radius=20, outline=CHAMP, width=3)
    d.rounded_rectangle((95, 95, W - 95, H - 95), radius=16, outline=SOFT_ROSE, width=1)
    tcenter(d, (W // 2, 220), "GIRLS BAR / SNACK", F(JOSE, 24, 300), DUST)
    tcenter(d, (W // 2, 340), "Four Seasons", F(PLAY, 72, 600), INK)
    for i in range(7):
        petal(d, 260 + i * 210, 480, 14, PINK if i % 2 == 0 else (230, 240, 220))
    price_block(d, int(W * 0.18), 620, int(W * 0.64), INK, ROSE, 1.08, center=True)
    tcenter(d, (W // 2, H - 160), "ごゆっくりどうぞ", F(JP, 28), SOFT_INK)
    return c


def L19():
    c = grad((W, H), (255, 244, 236), (244, 236, 248))
    d = ImageDraw.Draw(c)
    soft_circles(d, (255, 220, 210))
    soft_circles(d, (230, 220, 240))
    tcenter(d, (W // 2, 240), "Four Seasons", F(SCRIPT, 92), ROSE)
    tcenter(d, (W // 2, 360), "落ち着きのあるガールズバー", F(JP, 30), SOFT_INK)
    tcenter(d, (W // 2, 430), "可愛いガールズスナック", F(JP, 30), SOFT_INK)
    line(d, 500, int(W * 0.32), int(W * 0.68), SOFT_ROSE, 1)
    price_block(d, int(W * 0.16), 600, int(W * 0.68), INK, ROSE, 1.08, center=True)
    return c


def L20():
    c = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(c)
    # layered soft sheets
    d.rounded_rectangle((90, 120, W - 60, H - 90), radius=36, fill=BLUSH)
    d.rounded_rectangle((60, 90, W - 90, H - 120), radius=36, fill=WHITE, outline=SOFT_ROSE, width=2)
    brand(d, W // 2, 280, INK, ROSE, 1.15)
    tcenter(d, (W // 2, 580), "暗くない、やさしい夜。", F(JP, 32), SOFT_INK)
    price_block(d, int(W * 0.18), 720, int(W * 0.64), INK, ROSE, 1.1, center=True)
    tcenter(d, (W // 2, H - 180), "Four Seasons  ·  Girls Bar & Snack", F(JOSE, 22, 300), DUST)
    return c


LAYOUTS = [
    ("01_blush_frame", "ブラッシュ額縁", L01),
    ("02_mint_script", "ミント×スクリプト", L02),
    ("03_peach_card", "ピーチカード", L03),
    ("04_mint_soft", "ミントソフト", L04),
    ("05_lilac_calm", "ライラック落ち着き", L05),
    ("06_petal_pattern", "花びらパターン", L06),
    ("07_sky_stripe", "スカイストライプ", L07),
    ("08_butter_arch", "バターアーチ", L08),
    ("09_scallop_pink", "スカラップピンク", L09),
    ("10_two_panels", "二色パネル", L10),
    ("11_dot_ivory", "ドットアイボリー", L11),
    ("12_flower_ring", "フラワーリング", L12),
    ("13_welcome_tags", "ようこそタグ", L13),
    ("14_peach_line", "ピーチライン", L14),
    ("15_soft_heart", "ソフトハート", L15),
    ("16_wave_blush", "ウェーブブラッシュ", L16),
    ("17_side_color", "サイドカラー", L17),
    ("18_ticket_cream", "チケットクリーム", L18),
    ("19_script_hero", "スクリプトヒーロー", L19),
    ("20_layer_sheet", "レイヤーシート", L20),
]


def contact_sheet(items):
    cols, rows = 5, 4
    tw, th = 340, int(340 * RATIO)
    pad, lh = 14, 34
    sw = cols * tw + (cols + 1) * pad
    sh = 70 + rows * (th + lh + pad) + pad
    sheet = Image.new("RGB", (sw, sh), (255, 248, 246))
    d = ImageDraw.Draw(sheet)
    d.text((pad, 18), "Four Seasons — 明るめ可愛い落ち着き案20（写真なし）", font=F(JP, 26), fill=INK)
    small = F(JP, 14)
    for i, (path, title) in enumerate(items):
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = 60 + pad + r * (th + lh + pad)
        im = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(im, (x, y))
        d.text((x, y + th + 5), f"{i+1:02d} {title}", font=small, fill=SOFT_INK)
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
<title>Four Seasons 明るめ可愛い案20</title>
<style>
body{{margin:0;background:#fff8f6;color:#48383c;font-family:system-ui,sans-serif}}
header{{padding:24px;max-width:1200px;margin:0 auto}}
a{{color:#dc8c94}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px;padding:16px 20px 40px;max-width:1200px;margin:0 auto}}
figure{{margin:0;background:#fff;border:1px solid #f2d2d2}}
img{{width:100%;display:block;aspect-ratio:594/841;object-fit:cover}}
figcaption{{padding:8px 10px;font-size:.8rem;color:#c48c8c}}
</style></head><body>
<header><h1>Four Seasons — 明るめ・可愛い・落ち着き（写真なし）</h1>
<p>Girls Bar / Girls Snack。暗めNG。<a href="全候補_1枚まとめ.jpg">1枚まとめ</a></p></header>
<div class="grid">{cards}</div></body></html>""",
        encoding="utf-8",
    )


def main():
    print("Generating light cute-calm panels (no photos)…")
    for p in OUT.glob("*.jpg"):
        p.unlink()
    items = []
    for name, title, fn in LAYOUTS:
        im = fn()
        assert im.size == (W, H), (name, im.size)
        # safety: reject if average luminance too dark
        items.append(save(im, f"{name}.jpg", title))
    contact_sheet(items)
    make_viewer()
    (ROOT / "README.md").write_text(
        """# Four Seasons — 明るめ可愛い落ち着き A1案20（写真なし）

- 写真なし
- 暗めNG（明るいトーンのみ）
- 落ち着き＋可愛い
- Girls Bar / Girls Snack

## 掲載
Set 50分 / カウンター席 ¥3,000 / ボックス席 ¥4,000 / TAX 20%  
飲み放題：甲類・ウイスキー・リキュール各種／割りもの・お茶類・炭酸
""",
        encoding="utf-8",
    )
    print("done")


if __name__ == "__main__":
    main()
