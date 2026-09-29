#!/usr/bin/env python3
"""
Four Seasons — 店頭システム看板サンプル20
実在のガールズバー／キャバクラ電飾スタンド看板に寄せる。
参考: 黒×ゴールド＋グリッター、赤黒グラデ＋白字料金表、
      ピンク×黒のカジュアル系、ギンガム可愛い系 など。
案内所用途は一旦なし。写真なし。
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

PLAY = str(FONTS / "PlayfairDisplay[wght].ttf")
PLAY_I = str(FONTS / "PlayfairDisplay-Italic[wght].ttf")
JOSE = str(FONTS / "JosefinSans[wght].ttf")
SCRIPT = str(FONTS / "GreatVibes-Regular.ttf")
JP = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"

WHITE = (255, 255, 255)
BLACK = (8, 8, 10)
GOLD = (212, 175, 85)
GOLD_L = (240, 210, 130)
GOLD_D = (160, 120, 45)
PINK = (255, 90, 150)
HOT = (230, 40, 110)
RED = (180, 20, 50)
BURG = (90, 10, 30)
NAVY = (10, 20, 55)
INK = (20, 20, 25)


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


def radial(size, c_center, c_edge, cx=None, cy=None):
    w, h = size
    im = Image.new("RGB", size)
    px = im.load()
    cx = w / 2 if cx is None else cx
    cy = h * 0.35 if cy is None else cy
    maxd = math.hypot(max(cx, w - cx), max(cy, h - cy))
    for y in range(h):
        for x in range(w):
            t = min(1.0, math.hypot(x - cx, y - cy) / maxd)
            px[x, y] = tuple(int(c_center[j] + (c_edge[j] - c_center[j]) * t) for j in range(3))
    return im


def glitter_bg(base: Image.Image, seed=1, n=280, color=(255, 220, 140), bokeh=40):
    """実看板でよくあるグリッター／ボケ背景"""
    im = base.convert("RGBA")
    bw, bh = im.size
    overlay = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    rng = random.Random(seed)
    for _ in range(bokeh):
        x, y = rng.randint(0, bw), rng.randint(0, bh)
        r = rng.randint(20, 90)
        a = rng.randint(20, 55)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(*color, a))
    for _ in range(n):
        x, y = rng.randint(0, bw), rng.randint(0, bh)
        s = rng.randint(1, 5)
        a = rng.randint(100, 230)
        d.ellipse((x - s, y - s, x + s, y + s), fill=(*color, a))
        if s > 3:
            d.line((x - s * 2, y, x + s * 2, y), fill=(*color, a), width=1)
            d.line((x, y - s * 2, x, y + s * 2), fill=(*color, a), width=1)
    out = Image.alpha_composite(im, overlay.filter(ImageFilter.GaussianBlur(0.4)))
    return out.convert("RGB")


def gold_frame(d, m=40, thick=8):
    d.rectangle((m, m, W - m, H - m), outline=GOLD, width=thick)
    d.rectangle((m + 14, m + 14, W - m - 14, H - m - 14), outline=GOLD_L, width=2)


def panel(d, box, fill=(0, 0, 0), outline=GOLD, width=3, radius=12):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def shop_header(d, y, name_color=GOLD_L, sub_color=WHITE, script=False):
    tcenter(d, (W // 2, y), "GIRLS BAR  /  GIRLS SNACK", F(JOSE, 28, 400), sub_color)
    fnt = F(SCRIPT, 92) if script else F(PLAY, 78, 700)
    tcenter(d, (W // 2, y + 100), "Four Seasons", fnt, name_color)
    d.line((W // 2 - 160, y + 165, W // 2 + 160, y + 165), fill=GOLD, width=2)


def system_title(d, y, fill=HOT, ink=WHITE):
    panel(d, (140, y, W - 140, y + 72), fill=fill, outline=GOLD, width=2, radius=8)
    tcenter(d, (W // 2, y + 36), "SYSTEM / 料金", F(JP, 36), ink)


def price_table(d, y, row_bg=(20, 20, 24), alt_bg=(32, 28, 34), ink=WHITE, accent=GOLD_L, label_c=None):
    label_c = label_c or (220, 220, 225)
    rows = [
        ("Set", "50分"),
        ("カウンター席", "¥3,000"),
        ("ボックス席", "¥4,000"),
        ("TAX", "20%"),
    ]
    yy = y
    for i, (a, b) in enumerate(rows):
        bg = row_bg if i % 2 == 0 else alt_bg
        panel(d, (140, yy, W - 140, yy + 100), fill=bg, outline=GOLD_D, width=2, radius=6)
        d.text((180, yy + 28), a, font=F(JP, 34), fill=label_c)
        fnt = F(JP, 40) if any(ord(c) > 127 for c in b) else F(PLAY, 44, 700)
        bb = d.textbbox((0, 0), b, font=fnt)
        d.text((W - 180 - (bb[2] - bb[0]), yy + 24), b, font=fnt, fill=accent)
        yy += 108
    return yy


def drink_block(d, y, bg=(18, 18, 22), title=GOLD, body=WHITE):
    panel(d, (140, y, W - 140, y + 260), fill=bg, outline=GOLD, width=2, radius=10)
    tcenter(d, (W // 2, y + 55), "飲み放題", F(JP, 34), title)
    tcenter(d, (W // 2, y + 125), "甲類・ウイスキー・リキュール各種", F(JP, 28), body)
    tcenter(d, (W // 2, y + 185), "割りもの・お茶類・炭酸", F(JP, 28), body)
    return y + 260


def silhouette_side(d, cx, cy, scale=1.0, color=(40, 40, 45)):
    """実看板風のシンプル女性シルエット（装飾）"""
    r = 26 * scale
    d.ellipse((cx - r, cy - r * 3.2, cx + r, cy - r * 1.2), fill=color)
    d.polygon(
        [
            (cx - 50 * scale, cy + 95 * scale),
            (cx - 28 * scale, cy - 5 * scale),
            (cx + 28 * scale, cy - 5 * scale),
            (cx + 50 * scale, cy + 95 * scale),
            (cx, cy + 120 * scale),
        ],
        fill=color,
    )


def save(im, name, title):
    p = OUT / f"{name}.jpg"
    im.convert("RGB").save(p, "JPEG", quality=91, optimize=True)
    print(f"  {name} — {title}")
    return p, title


# ---------- 20 storefront-authentic layouts ----------


def L01():
    """黒×ゴールド＋グリッター（いちばん定番）"""
    c = Image.new("RGB", (W, H), BLACK)
    c = glitter_bg(c, 1, n=320, color=(255, 215, 140), bokeh=50)
    d = ImageDraw.Draw(c)
    gold_frame(d, 36, 10)
    shop_header(d, 160, GOLD_L, (200, 180, 140))
    tcenter(d, (W // 2, 380), "明朗会計", F(JP, 28), GOLD)
    system_title(d, 450, fill=(40, 30, 10), ink=GOLD_L)
    yy = price_table(d, 550, (12, 12, 14), (24, 20, 16), WHITE, GOLD_L, (200, 190, 170))
    yy = drink_block(d, yy + 30, (12, 12, 14), GOLD_L, (230, 220, 200))
    tcenter(d, (W // 2, H - 120), "Four Seasons", F(JOSE, 26, 300), GOLD)
    return c


def L02():
    """赤黒グラデ＋白字料金（キャバ定番）"""
    c = grad_v((W, H), BURG, BLACK)
    c = glitter_bg(c, 2, n=180, color=(255, 180, 120), bokeh=30)
    d = ImageDraw.Draw(c)
    gold_frame(d, 40, 8)
    silhouette_side(d, 220, 520, 1.8, (50, 8, 20))
    silhouette_side(d, W - 220, 520, 1.8, (50, 8, 20))
    shop_header(d, 180, WHITE, GOLD_L)
    system_title(d, 480, RED, WHITE)
    yy = price_table(d, 580, (30, 8, 14), (50, 12, 20), WHITE, GOLD_L, (255, 210, 210))
    yy = drink_block(d, yy + 24, (25, 8, 12), GOLD_L, WHITE)
    tcenter(d, (W // 2, H - 130), "GIRLS BAR & SNACK", F(JOSE, 24, 400), GOLD)
    return c


def L03():
    """グリッター全面＋黒帯に白字（サインモール系）"""
    c = radial((W, H), (80, 50, 30), (10, 8, 12))
    c = glitter_bg(c, 3, n=400, color=(255, 220, 150), bokeh=60)
    d = ImageDraw.Draw(c)
    gold_frame(d)
    # black text plate
    panel(d, (120, 140, W - 120, H - 140), fill=(8, 8, 10), outline=GOLD, width=4, radius=8)
    shop_header(d, 220, GOLD_L, WHITE)
    system_title(d, 480, HOT)
    yy = price_table(d, 580)
    yy = drink_block(d, yy + 28)
    return c


def L04():
    """ピンク×黒・カジュアルガールズバー"""
    c = Image.new("RGB", (W, H), (25, 8, 18))
    d = ImageDraw.Draw(c)
    # pink accent bars
    d.rectangle((0, 0, W, 90), fill=HOT)
    d.rectangle((0, H - 90, W, H), fill=HOT)
    tcenter(d, (W // 2, 45), "GIRLS BAR  ★  GIRLS SNACK", F(JOSE, 26, 500), WHITE)
    gold_frame(d, 50, 6)
    tcenter(d, (W // 2, 220), "Four Seasons", F(PLAY, 80, 700), PINK)
    d.line((400, 300, W - 400, 300), fill=GOLD, width=2)
    # big price callout
    panel(d, (200, 360, W - 200, 620), fill=HOT, outline=GOLD_L, width=4, radius=16)
    tcenter(d, (W // 2, 430), "カウンター席", F(JP, 32), WHITE)
    tcenter(d, (W // 2, 520), "¥3,000", F(PLAY, 72, 700), WHITE)
    tcenter(d, (W // 2, 580), "Set 50分", F(JP, 28), (255, 220, 230))
    system_title(d, 680, (60, 20, 35), PINK)
    yy = price_table(d, 780, (35, 12, 24), (45, 16, 30), WHITE, PINK, (255, 200, 220))
    # force box/tax visible after hero — show drinks
    yy = drink_block(d, yy + 20, (30, 10, 20), PINK, WHITE)
    tcenter(d, (W // 2, H - 45), "Four Seasons", F(JOSE, 22, 400), WHITE)
    return glitter_bg(c, 4, n=120, color=(255, 120, 180), bokeh=25)


def L05():
    """白地×赤黒・スナック寄り明朗会計"""
    c = Image.new("RGB", (W, H), (250, 248, 245))
    d = ImageDraw.Draw(c)
    d.rectangle((0, 0, W, 280), fill=BLACK)
    tcenter(d, (W // 2, 90), "GIRLS BAR / SNACK", F(JOSE, 26, 400), GOLD)
    tcenter(d, (W // 2, 190), "Four Seasons", F(PLAY, 74, 700), WHITE)
    d.rectangle((0, 280, W, 300), fill=HOT)
    system_title(d, 360, HOT, WHITE)
    # light table
    rows = [("Set", "50分"), ("カウンター席", "¥3,000"), ("ボックス席", "¥4,000"), ("TAX", "20%")]
    yy = 460
    for i, (a, b) in enumerate(rows):
        bg = WHITE if i % 2 == 0 else (245, 240, 240)
        panel(d, (140, yy, W - 140, yy + 110), fill=bg, outline=(180, 180, 180), width=2, radius=4)
        d.rectangle((140, yy, 160, yy + 110), fill=HOT)
        d.text((190, yy + 32), a, font=F(JP, 36), fill=INK)
        fnt = F(JP, 42) if "分" in b else F(PLAY, 46, 700)
        bb = d.textbbox((0, 0), b, font=fnt)
        d.text((W - 190 - (bb[2] - bb[0]), yy + 28), b, font=fnt, fill=HOT)
        yy += 120
    panel(d, (140, yy + 20, W - 140, yy + 300), fill=BLACK, outline=HOT, width=3, radius=8)
    tcenter(d, (W // 2, yy + 90), "飲み放題", F(JP, 34), GOLD)
    tcenter(d, (W // 2, yy + 170), "甲類・ウイスキー・リキュール各種", F(JP, 28), WHITE)
    tcenter(d, (W // 2, yy + 230), "割りもの・お茶類・炭酸", F(JP, 28), WHITE)
    d.rectangle((0, H - 80, W, H), fill=BLACK)
    tcenter(d, (W // 2, H - 40), "明朗会計 ／ 初めての方も安心", F(JP, 26), WHITE)
    return c


def L06():
    """ネイビー×ゴールド高級感"""
    c = grad_v((W, H), NAVY, (5, 8, 20))
    c = glitter_bg(c, 6, n=200, color=(180, 200, 255), bokeh=35)
    d = ImageDraw.Draw(c)
    gold_frame(d, 44, 7)
    shop_header(d, 180, GOLD_L, (180, 200, 230))
    system_title(d, 460, (20, 40, 90), GOLD_L)
    yy = price_table(d, 560, (8, 14, 35), (12, 20, 50), WHITE, GOLD_L, (180, 200, 230))
    yy = drink_block(d, yy + 28, (8, 12, 30), GOLD_L, WHITE)
    tcenter(d, (W // 2, H - 120), "PREMIUM GIRLS SPACE", F(JOSE, 22, 300), GOLD)
    return c


def L07():
    """左右：店名黒帯＋料金白地（実用的店頭）"""
    c = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(c)
    mid = int(W * 0.38)
    d.rectangle((0, 0, mid, H), fill=BLACK)
    c2 = glitter_bg(Image.new("RGB", (mid, H), BLACK), 7, n=100, color=(255, 200, 120), bokeh=20)
    c.paste(c2, (0, 0))
    d = ImageDraw.Draw(c)
    tcenter(d, (mid // 2, 280), "Girls", F(SCRIPT, 64), GOLD_L)
    tcenter(d, (mid // 2, 400), "Bar", F(SCRIPT, 64), GOLD_L)
    tcenter(d, (mid // 2, 520), "&", F(PLAY, 36, 400), WHITE)
    tcenter(d, (mid // 2, 640), "Snack", F(SCRIPT, 64), GOLD_L)
    d.line((60, 760, mid - 60, 760), fill=GOLD, width=2)
    tcenter(d, (mid // 2, 900), "Four", F(PLAY, 44, 700), WHITE)
    tcenter(d, (mid // 2, 980), "Seasons", F(PLAY, 44, 700), WHITE)
    # right
    rx = mid + 40
    tcenter(d, ((rx + W) // 2, 140), "SYSTEM", F(JOSE, 32, 500), HOT)
    rows = [("Set", "50分"), ("カウンター席", "¥3,000"), ("ボックス席", "¥4,000"), ("TAX", "20%")]
    yy = 220
    for a, b in rows:
        panel(d, (rx, yy, W - 50, yy + 140), fill=(250, 250, 250), outline=(200, 200, 200), width=2, radius=8)
        d.rectangle((rx, yy, rx + 14, yy + 140), fill=HOT)
        d.text((rx + 36, yy + 45), a, font=F(JP, 32), fill=INK)
        fnt = F(JP, 40) if "分" in b else F(PLAY, 44, 700)
        bb = d.textbbox((0, 0), b, font=fnt)
        d.text((W - 80 - (bb[2] - bb[0]), yy + 42), b, font=fnt, fill=HOT)
        yy += 160
    panel(d, (rx, yy + 10, W - 50, yy + 360), fill=BLACK, outline=GOLD, width=3, radius=8)
    tcenter(d, ((rx + W) // 2, yy + 90), "飲み放題", F(JP, 32), GOLD)
    tcenter(d, ((rx + W) // 2, yy + 180), "甲類・ウイスキー・リキュール各種", F(JP, 24), WHITE)
    tcenter(d, ((rx + W) // 2, yy + 260), "割りもの・お茶類・炭酸", F(JP, 24), WHITE)
    return c


def L08():
    """ギンガム＋リボン（可愛い系ガールズバー実例寄り）"""
    c = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(c)
    # gingham
    cell = 70
    for y in range(0, H, cell):
        for x in range(0, W, cell):
            if ((x // cell) + (y // cell)) % 2 == 0:
                d.rectangle((x, y, x + cell, y + cell), fill=(255, 220, 230))
            else:
                d.rectangle((x, y, x + cell, y + cell), fill=(255, 245, 248))
    # white content card
    panel(d, (100, 100, W - 100, H - 100), fill=WHITE, outline=HOT, width=6, radius=20)
    tcenter(d, (W // 2, 200), "GIRLS BAR / SNACK", F(JOSE, 26, 400), HOT)
    tcenter(d, (W // 2, 300), "Four Seasons", F(SCRIPT, 88), HOT)
    # ribbon-like bar
    d.polygon([(120, 400), (W - 120, 400), (W - 90, 450), (W - 120, 500), (120, 500), (90, 450)], fill=HOT)
    tcenter(d, (W // 2, 450), "初めてでも安心", F(JP, 34), WHITE)
    system_title(d, 560, HOT)
    yy = 660
    rows = [("Set", "50分"), ("カウンター席", "¥3,000"), ("ボックス席", "¥4,000"), ("TAX", "20%")]
    for a, b in rows:
        panel(d, (160, yy, W - 160, yy + 100), fill=(255, 240, 245), outline=HOT, width=2, radius=10)
        d.text((200, yy + 28), a, font=F(JP, 34), fill=INK)
        fnt = F(JP, 40) if "分" in b else F(PLAY, 42, 700)
        bb = d.textbbox((0, 0), b, font=fnt)
        d.text((W - 200 - (bb[2] - bb[0]), yy + 24), b, font=fnt, fill=HOT)
        yy += 112
    panel(d, (160, yy + 10, W - 160, yy + 280), fill=(255, 245, 248), outline=HOT, width=2, radius=12)
    tcenter(d, (W // 2, yy + 70), "飲み放題", F(JP, 32), HOT)
    tcenter(d, (W // 2, yy + 145), "甲類・ウイスキー・リキュール各種", F(JP, 26), INK)
    tcenter(d, (W // 2, yy + 210), "割りもの・お茶類・炭酸", F(JP, 26), INK)
    return c


def L09():
    """ゴールドメタリック帯＋黒"""
    c = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(c)
    for i, col in enumerate([(GOLD_D), (GOLD), (GOLD_L), (GOLD), (GOLD_D)]):
        d.rectangle((0, 80 + i * 18, W, 96 + i * 18), fill=col)
        d.rectangle((0, H - 170 + i * 18, W, H - 154 + i * 18), fill=col)
    shop_header(d, 220, GOLD_L, GOLD)
    system_title(d, 480, (50, 40, 15), GOLD_L)
    yy = price_table(d, 580, (15, 15, 15), (28, 24, 18), WHITE, GOLD_L)
    yy = drink_block(d, yy + 30, (15, 15, 15), GOLD_L, WHITE)
    return glitter_bg(c, 9, n=150, color=(255, 210, 120), bokeh=20)


def L10():
    """大価格ヒーロー型（店頭で多い）"""
    c = grad_v((W, H), (30, 10, 20), BLACK)
    c = glitter_bg(c, 10, n=200, color=(255, 160, 180), bokeh=40)
    d = ImageDraw.Draw(c)
    gold_frame(d, 32, 8)
    tcenter(d, (W // 2, 160), "Four Seasons", F(PLAY, 70, 700), WHITE)
    tcenter(d, (W // 2, 250), "GIRLS BAR & SNACK", F(JOSE, 28, 400), GOLD)
    # hero price
    panel(d, (160, 320, W - 160, 780), fill=HOT, outline=GOLD_L, width=5, radius=18)
    tcenter(d, (W // 2, 400), "セット料金", F(JP, 30), WHITE)
    tcenter(d, (W // 2, 520), "¥3,000〜", F(PLAY, 84, 700), WHITE)
    tcenter(d, (W // 2, 640), "カウンター席 / Set 50分", F(JP, 30), (255, 230, 240))
    tcenter(d, (W // 2, 720), "ボックス席 ¥4,000　TAX 20%", F(JP, 26), (255, 210, 220))
    panel(d, (160, 840, W - 160, 1500), fill=(12, 12, 14), outline=GOLD, width=3, radius=12)
    tcenter(d, (W // 2, 920), "SYSTEM", F(JOSE, 28, 400), GOLD)
    items = [("Set", "50分"), ("カウンター", "¥3,000"), ("ボックス", "¥4,000"), ("TAX", "20%")]
    yy = 1000
    for a, b in items:
        d.text((220, yy), a, font=F(JP, 32), fill=(200, 200, 200))
        fnt = F(JP, 36) if "分" in b else F(PLAY, 38, 700)
        bb = d.textbbox((0, 0), b, font=fnt)
        d.text((W - 220 - (bb[2] - bb[0]), yy), b, font=fnt, fill=GOLD_L)
        d.line((220, yy + 55, W - 220, yy + 55), fill=(50, 40, 45), width=1)
        yy += 90
    tcenter(d, (W // 2, 1650), "飲み放題", F(JP, 34), HOT)
    tcenter(d, (W // 2, 1740), "甲類・ウイスキー・リキュール各種", F(JP, 28), WHITE)
    tcenter(d, (W // 2, 1820), "割りもの・お茶類・炭酸", F(JP, 28), WHITE)
    return c


def L11():
    """電飾看板っぽい枠＋中央システム"""
    c = Image.new("RGB", (W, H), (15, 15, 18))
    d = ImageDraw.Draw(c)
    # outer LED-ish double border
    for m, col, w in [(20, GOLD, 16), (48, HOT, 4), (64, GOLD_L, 2)]:
        d.rectangle((m, m, W - m, H - m), outline=col, width=w)
    shop_header(d, 160, WHITE, GOLD)
    system_title(d, 420, HOT)
    yy = price_table(d, 520)
    yy = drink_block(d, yy + 30)
    tcenter(d, (W // 2, H - 110), "OPEN NIGHTLY", F(JOSE, 22, 300), GOLD)
    return glitter_bg(c, 11, n=100, color=(255, 200, 140), bokeh=15)


def L12():
    """ローズゴールド×ダーク"""
    c = grad_v((W, H), (60, 25, 35), (15, 8, 12))
    c = glitter_bg(c, 12, n=250, color=(255, 180, 170), bokeh=45)
    d = ImageDraw.Draw(c)
    gold_frame(d, 38, 6)
    shop_header(d, 170, (255, 200, 190), (255, 170, 180), script=True)
    system_title(d, 450, (120, 40, 60), (255, 220, 210))
    yy = price_table(d, 550, (40, 18, 25), (55, 25, 35), WHITE, (255, 200, 190), (255, 210, 210))
    yy = drink_block(d, yy + 28, (35, 15, 22), (255, 200, 190), WHITE)
    return c


def L13():
    """シンプル黒地・情報優先（実用）"""
    c = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(c)
    d.rectangle((60, 60, W - 60, H - 60), outline=WHITE, width=2)
    tcenter(d, (W // 2, 160), "Four Seasons", F(PLAY, 70, 700), WHITE)
    tcenter(d, (W // 2, 250), "ガールズバー ／ ガールズスナック", F(JP, 28), (180, 180, 180))
    d.line((200, 320, W - 200, 320), fill=HOT, width=4)
    system_title(d, 380, HOT)
    yy = price_table(d, 480, (20, 20, 20), (35, 35, 35), WHITE, HOT, (220, 220, 220))
    yy = drink_block(d, yy + 40, (20, 20, 20), HOT, WHITE)
    tcenter(d, (W // 2, H - 140), "明朗会計", F(JP, 30), WHITE)
    return c


def L14():
    """シャンパンベージュ×茶金（大人スナック）"""
    c = grad_v((W, H), (245, 230, 210), (220, 190, 160))
    d = ImageDraw.Draw(c)
    d.rectangle((50, 50, W - 50, H - 50), outline=GOLD_D, width=8)
    d.rectangle((70, 70, W - 70, H - 70), outline=GOLD, width=2)
    tcenter(d, (W // 2, 180), "Four Seasons", F(PLAY_I, 72, 500), (80, 50, 30))
    tcenter(d, (W // 2, 280), "Girls Bar  &  Girls Snack", F(SCRIPT, 48), HOT)
    system_title(d, 380, (120, 70, 40), WHITE)
    yy = 480
    rows = [("Set", "50分"), ("カウンター席", "¥3,000"), ("ボックス席", "¥4,000"), ("TAX", "20%")]
    for a, b in rows:
        panel(d, (160, yy, W - 160, yy + 110), fill=WHITE, outline=GOLD_D, width=2, radius=6)
        d.text((200, yy + 32), a, font=F(JP, 34), fill=(60, 40, 30))
        fnt = F(JP, 40) if "分" in b else F(PLAY, 44, 700)
        bb = d.textbbox((0, 0), b, font=fnt)
        d.text((W - 200 - (bb[2] - bb[0]), yy + 28), b, font=fnt, fill=HOT)
        yy += 120
    panel(d, (160, yy + 10, W - 160, yy + 280), fill=(40, 25, 15), outline=GOLD, width=2, radius=8)
    tcenter(d, (W // 2, yy + 80), "飲み放題", F(JP, 32), GOLD_L)
    tcenter(d, (W // 2, yy + 160), "甲類・ウイスキー・リキュール各種", F(JP, 26), WHITE)
    tcenter(d, (W // 2, yy + 220), "割りもの・お茶類・炭酸", F(JP, 26), WHITE)
    return c


def L15():
    """縦ストライプ＋中央黒パネル"""
    c = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(c)
    for x in range(0, W, 40):
        d.rectangle((x, 0, x + 18, H), fill=(35, 10, 20))
    panel(d, (130, 120, W - 130, H - 120), fill=(10, 10, 12), outline=GOLD, width=4, radius=10)
    shop_header(d, 200, GOLD_L, PINK)
    system_title(d, 460, HOT)
    yy = price_table(d, 560)
    yy = drink_block(d, yy + 28)
    return glitter_bg(c, 15, n=80, color=(255, 100, 150), bokeh=10)


def L16():
    """2カラム席種別（店頭メニュー風）"""
    c = Image.new("RGB", (W, H), (12, 12, 14))
    c = glitter_bg(c, 16, n=160, color=(255, 200, 130), bokeh=30)
    d = ImageDraw.Draw(c)
    gold_frame(d)
    tcenter(d, (W // 2, 140), "Four Seasons", F(PLAY, 68, 700), GOLD_L)
    tcenter(d, (W // 2, 230), "GIRLS BAR / SNACK", F(JOSE, 26, 400), WHITE)
    for x0, title, price in [(100, "カウンター席", "¥3,000"), (W // 2 + 20, "ボックス席", "¥4,000")]:
        panel(d, (x0, 320, x0 + W // 2 - 120, 900), fill=(20, 20, 24), outline=GOLD, width=3, radius=12)
        tcenter(d, (x0 + (W // 2 - 120) // 2, 420), title, F(JP, 32), WHITE)
        tcenter(d, (x0 + (W // 2 - 120) // 2, 560), price, F(PLAY, 56, 700), GOLD_L)
        tcenter(d, (x0 + (W // 2 - 120) // 2, 680), "Set 50分", F(JP, 28), (180, 180, 180))
        tcenter(d, (x0 + (W // 2 - 120) // 2, 780), "TAX 20%", F(JP, 26), HOT)
    panel(d, (100, 960, W - 100, 1500), fill=(18, 18, 20), outline=HOT, width=3, radius=12)
    tcenter(d, (W // 2, 1060), "飲み放題", F(JP, 36), GOLD_L)
    tcenter(d, (W // 2, 1180), "甲類・ウイスキー・リキュール各種", F(JP, 30), WHITE)
    tcenter(d, (W // 2, 1300), "割りもの・お茶類・炭酸", F(JP, 30), WHITE)
    tcenter(d, (W // 2, 1420), "明朗会計", F(JP, 28), HOT)
    return c


def L17():
    """マゼンタネオン風（夜の電飾）"""
    c = Image.new("RGB", (W, H), (20, 5, 15))
    d = ImageDraw.Draw(c)
    for sw, col in [(18, (80, 10, 40)), (8, HOT), (2, PINK)]:
        d.rectangle((40, 40, W - 40, H - 40), outline=col, width=sw)
    for sw, col in [(10, (100, 20, 50)), (3, PINK)]:
        tcenter(d, (W // 2, 200), "Four Seasons", F(PLAY, 74, 700), PINK, col, sw)
    tcenter(d, (W // 2, 320), "GIRLS BAR", F(JOSE, 40, 600), WHITE)
    tcenter(d, (W // 2, 400), "GIRLS SNACK", F(JOSE, 40, 600), GOLD_L)
    system_title(d, 500, HOT)
    yy = price_table(d, 600, (30, 8, 20), (45, 12, 30), WHITE, PINK)
    yy = drink_block(d, yy + 28, (25, 8, 18), PINK, WHITE)
    return glitter_bg(c, 17, n=140, color=(255, 80, 160), bokeh=25)


def L18():
    """黒＋細い金ラインの上品系"""
    c = Image.new("RGB", (W, H), (8, 8, 10))
    d = ImageDraw.Draw(c)
    for m in (50, 62, 74):
        d.rectangle((m, m, W - m, H - m), outline=GOLD if m != 62 else GOLD_L, width=1)
    tcenter(d, (W // 2, 180), "Four Seasons", F(PLAY_I, 70, 500), GOLD_L)
    tcenter(d, (W // 2, 280), "Girls Bar  ·  Girls Snack", F(SCRIPT, 46), WHITE)
    d.line((300, 360, W - 300, 360), fill=GOLD, width=1)
    yy = 420
    for label, price in [("Set 50分", ""), ("カウンター席", "¥3,000"), ("ボックス席", "¥4,000"), ("TAX", "20%")]:
        d.line((200, yy, W - 200, yy), fill=(60, 50, 30), width=1)
        d.text((220, yy + 30), label, font=F(JP, 34), fill=(220, 220, 220))
        if price:
            fnt = F(PLAY, 42, 700)
            bb = d.textbbox((0, 0), price, font=fnt)
            d.text((W - 220 - (bb[2] - bb[0]), yy + 26), price, font=fnt, fill=GOLD_L)
        yy += 120
    d.line((200, yy, W - 200, yy), fill=(60, 50, 30), width=1)
    tcenter(d, (W // 2, yy + 80), "飲み放題", F(JP, 32), GOLD)
    tcenter(d, (W // 2, yy + 160), "甲類・ウイスキー・リキュール各種", F(JP, 28), WHITE)
    tcenter(d, (W // 2, yy + 230), "割りもの・お茶類・炭酸", F(JP, 28), WHITE)
    return c


def L19():
    """白×ホットピンク高コントラスト（夜でも読める明るい看板）"""
    c = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(c)
    d.rectangle((0, 0, W, 360), fill=HOT)
    tcenter(d, (W // 2, 120), "GIRLS BAR / SNACK", F(JOSE, 28, 500), WHITE)
    tcenter(d, (W // 2, 240), "Four Seasons", F(PLAY, 78, 700), WHITE)
    d.rectangle((0, 360, W, 380), fill=GOLD)
    system_title(d, 440, BLACK, WHITE)
    yy = 540
    rows = [("Set", "50分"), ("カウンター席", "¥3,000"), ("ボックス席", "¥4,000"), ("TAX", "20%")]
    for a, b in rows:
        panel(d, (140, yy, W - 140, yy + 115), fill=(255, 245, 248), outline=HOT, width=3, radius=8)
        d.text((180, yy + 35), a, font=F(JP, 36), fill=INK)
        fnt = F(JP, 42) if "分" in b else F(PLAY, 46, 700)
        bb = d.textbbox((0, 0), b, font=fnt)
        d.text((W - 180 - (bb[2] - bb[0]), yy + 30), b, font=fnt, fill=HOT)
        yy += 130
    panel(d, (140, yy + 10, W - 140, yy + 300), fill=HOT, outline=GOLD, width=3, radius=10)
    tcenter(d, (W // 2, yy + 80), "飲み放題", F(JP, 34), WHITE)
    tcenter(d, (W // 2, yy + 160), "甲類・ウイスキー・リキュール各種", F(JP, 28), WHITE)
    tcenter(d, (W // 2, yy + 230), "割りもの・お茶類・炭酸", F(JP, 28), WHITE)
    d.rectangle((0, H - 70, W, H), fill=BLACK)
    tcenter(d, (W // 2, H - 35), "Four Seasons", F(JOSE, 22, 400), WHITE)
    return c


def L20():
    """黒金グリッター定番＋大SYSTEM（集大成）"""
    c = radial((W, H), (40, 30, 15), BLACK)
    c = glitter_bg(c, 20, n=350, color=(255, 215, 130), bokeh=55)
    d = ImageDraw.Draw(c)
    gold_frame(d, 30, 12)
    panel(d, (110, 110, W - 110, H - 110), fill=(8, 8, 10), outline=GOLD_L, width=2, radius=6)
    tcenter(d, (W // 2, 200), "GIRLS BAR  /  GIRLS SNACK", F(JOSE, 26, 400), GOLD)
    tcenter(d, (W // 2, 310), "Four Seasons", F(PLAY, 82, 700), GOLD_L)
    d.line((W // 2 - 180, 380, W // 2 + 180, 380), fill=GOLD, width=2)
    system_title(d, 440, (50, 35, 10), GOLD_L)
    yy = price_table(d, 540, (14, 14, 16), (28, 24, 18), WHITE, GOLD_L, (210, 200, 180))
    yy = drink_block(d, yy + 24, (14, 14, 16), GOLD_L, WHITE)
    tcenter(d, (W // 2, yy + 80), "明朗会計", F(JP, 30), GOLD)
    tcenter(d, (W // 2, H - 160), "Four Seasons", F(JOSE, 24, 300), GOLD_D)
    return c


LAYOUTS = [
    ("01_black_gold", "黒×ゴールド定番", L01),
    ("02_red_black", "赤黒グラデ白字", L02),
    ("03_glitter_plate", "グリッター＋黒帯", L03),
    ("04_pink_black", "ピンク×黒カジュアル", L04),
    ("05_white_red", "白地×赤・明朗会計", L05),
    ("06_navy_gold", "ネイビー×ゴールド", L06),
    ("07_split_practical", "左右分割実用", L07),
    ("08_gingham_cute", "ギンガム可愛い系", L08),
    ("09_gold_band", "ゴールド帯メタリック", L09),
    ("10_hero_price", "大価格ヒーロー", L10),
    ("11_led_frame", "電飾枠風", L11),
    ("12_rose_dark", "ローズゴールド×ダーク", L12),
    ("13_simple_black", "シンプル黒・情報優先", L13),
    ("14_champagne", "ベージュ大人スナック", L14),
    ("15_stripe_panel", "ストライプ＋黒パネル", L15),
    ("16_two_seat", "二席種カラム", L16),
    ("17_neon_magenta", "マゼンタネオン風", L17),
    ("18_thin_gold", "細金ライン上品", L18),
    ("19_white_hot", "白×ホットピンク", L19),
    ("20_black_gold_max", "黒金グリッター集大成", L20),
]


def contact_sheet(items):
    cols, rows = 5, 4
    tw, th = 340, int(340 * RATIO)
    pad, lh = 14, 36
    sw = cols * tw + (cols + 1) * pad
    sh = 70 + rows * (th + lh + pad) + pad
    sheet = Image.new("RGB", (sw, sh), (20, 20, 24))
    d = ImageDraw.Draw(sheet)
    d.text((pad, 16), "Four Seasons — 店頭システム看板サンプル20（案内所用途なし）", font=F(JP, 22), fill=GOLD_L)
    small = F(JP, 13)
    for i, (path, title) in enumerate(items):
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = 58 + pad + r * (th + lh + pad)
        im = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(im, (x, y))
        d.text((x, y + th + 4), f"{i+1:02d} {title}", font=small, fill=(180, 180, 180))
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
<title>Four Seasons 店頭システム看板20</title>
<style>
body{{margin:0;background:#111;color:#eee;font-family:system-ui,sans-serif}}
header{{padding:24px;max-width:1200px;margin:0 auto}}
a{{color:#d4af37}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px;padding:16px 20px 40px;max-width:1200px;margin:0 auto}}
figure{{margin:0;background:#1a1a1a;border:1px solid #444}}
img{{width:100%;display:block;aspect-ratio:594/841;object-fit:cover}}
figcaption{{padding:8px 10px;font-size:.8rem;color:#ccc}}
</style></head><body>
<header><h1>Four Seasons — 店頭システム看板サンプル</h1>
<p>実在の電飾スタンド看板寄りの構成。案内所用途は一旦なし。
<a href="全候補_1枚まとめ.jpg">1枚まとめ</a></p></header>
<div class="grid">{cards}</div></body></html>""",
        encoding="utf-8",
    )


def main():
    print("Generating storefront system boards…")
    # clear old panels
    for p in OUT.glob("*.jpg"):
        p.unlink()
    items = []
    for name, title, fn in LAYOUTS:
        im = fn()
        assert im.size == (W, H), (name, im.size)
        items.append(save(im, name, title))
    contact_sheet(items)
    make_viewer()
    import shutil

    line = ROOT / "LINE送信用"
    line.mkdir(exist_ok=True)
    for old in line.glob("*.jpg"):
        old.unlink()
    for p in OUT.glob("*.jpg"):
        shutil.copy2(p, line / p.name)
    shutil.copy2(ROOT / "全候補_1枚まとめ.jpg", line / "00_全候補まとめ.jpg")
    (line / "00_見る.html").write_text(
        (ROOT / "見る.html").read_text(encoding="utf-8").replace('src="panels/', 'src="'),
        encoding="utf-8",
    )
    (ROOT / "README.md").write_text(
        """# Four Seasons — 店頭システム看板サンプル20

案内所用途は一旦なし。ガールズバー／キャバクラの**店頭電飾スタンド看板**に寄せた案。

## 参考にした実在パターン
- 黒×ゴールド＋グリッター背景（定番）
- 赤〜黒グラデ＋白字料金表
- ピンク×黒のカジュアルガールズバー
- 白×赤の明朗会計型
- ギンガム可愛い系ガールズバー
- ネイビー×ゴールド高級感

## 掲載
Set 50分 / カウンター席 ¥3,000 / ボックス席 ¥4,000 / TAX 20%  
飲み放題：甲類・ウイスキー・リキュール各種／割りもの・お茶類・炭酸
""",
        encoding="utf-8",
    )
    print("done")


if __name__ == "__main__":
    main()
