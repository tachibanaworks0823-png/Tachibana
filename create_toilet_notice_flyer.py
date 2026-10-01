#!/usr/bin/env python3
"""飲食店トイレ注意フライヤー（謹告スタイル）を A4 PDF / PNG として生成する"""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas as pdf_canvas

ROOT = Path("/workspace")
PDF_OUT = ROOT / "トイレ注意フライヤー.pdf"
PNG_OUT = ROOT / "トイレ注意フライヤー_preview.png"
JPG_OUT = ROOT / "トイレ注意フライヤー.jpg"

# A4 @ 300dpi
DPI = 300
W = int(210 / 25.4 * DPI)  # 2480
H = int(297 / 25.4 * DPI)  # 3508

SERIF = "/usr/share/fonts/opentype/noto/NotoSerifCJK-{}.ttc"
SANS = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

# 配色
GOLD = (201, 162, 39)
GOLD_DIM = (168, 137, 58)
CREAM = (245, 240, 230)
WHITE = (255, 255, 255)
RED = (155, 27, 27)
RED_DEEP = (110, 18, 18)
MUTED = (208, 200, 184)


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    path = SERIF.format(weight)
    return ImageFont.truetype(path, size=size, index=0)


def font_sans(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(SANS, size=size, index=0)


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_centered(
    draw: ImageDraw.ImageDraw,
    text: str,
    cx: int,
    y: int,
    fnt: ImageFont.FreeTypeFont,
    fill: tuple[int, ...],
    anchor: str = "ma",
) -> None:
    draw.text((cx, y), text, font=fnt, fill=fill, anchor=anchor)


def draw_spaced(
    draw: ImageDraw.ImageDraw,
    text: str,
    cx: int,
    y: int,
    fnt: ImageFont.FreeTypeFont,
    fill: tuple[int, ...],
    tracking: float,
) -> None:
    widths = [text_size(draw, ch, fnt)[0] for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill, anchor="la")
        x += w + tracking


def make_background() -> Image.Image:
    """黒〜暗赤のビネット＋微細テクスチャ"""
    img = Image.new("RGB", (W, H), (12, 7, 8))
    px = img.load()
    cx, cy = W / 2, H / 2
    max_r = math.hypot(cx, cy)

    rng = random.Random(42)
    for y in range(H):
        for x in range(0, W, 2):  # 速度のため2px飛ばし後にぼかす
            dx = (x - cx) / max_r
            dy = (y - cy) / max_r
            r = math.sqrt(dx * dx + dy * dy)
            # 外側ほど暗赤
            edge = max(0.0, min(1.0, (r - 0.25) / 0.85))
            noise = rng.uniform(-6, 6)
            rr = int(18 + edge * 42 + noise)
            gg = int(8 + edge * 8 + noise * 0.4)
            bb = int(10 + edge * 12 + noise * 0.3)
            px[x, y] = (max(0, min(255, rr)), max(0, min(255, gg)), max(0, min(255, bb)))
            if x + 1 < W:
                px[x + 1, y] = px[x, y]

    img = img.filter(ImageFilter.GaussianBlur(radius=1.2))

    # ごく薄い斜め筋テクスチャ
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for x in range(-H, W + H, 18):
        od.line([(x, 0), (x - int(H * 0.4), H)], fill=(120, 80, 40, 10), width=1)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return ImageEnhance.Contrast(img).enhance(1.05)


def draw_corner(draw: ImageDraw.ImageDraw, x: int, y: int, dx: int, dy: int, length: int, width: int = 3) -> None:
    draw.line([(x, y), (x + dx * length, y)], fill=GOLD, width=width)
    draw.line([(x, y), (x, y + dy * length)], fill=GOLD, width=width)


def draw_frame(draw: ImageDraw.ImageDraw) -> None:
    m_o = int(9 / 25.4 * DPI)
    m_i = int(11.5 / 25.4 * DPI)
    # 外枠
    draw.rectangle([m_o, m_o, W - m_o, H - m_o], outline=GOLD, width=3)
    # 内枠
    draw.rectangle([m_i, m_i, W - m_i, H - m_i], outline=GOLD_DIM, width=1)

    cl = int(14 / 25.4 * DPI)
    draw_corner(draw, m_o, m_o, 1, 1, cl)
    draw_corner(draw, W - m_o, m_o, -1, 1, cl)
    draw_corner(draw, m_o, H - m_o, 1, -1, cl)
    draw_corner(draw, W - m_o, H - m_o, -1, -1, cl)


def render() -> Image.Image:
    img = make_background()
    draw = ImageDraw.Draw(img)
    draw_frame(draw)
    cx = W // 2

    # fonts
    f_en = font_sans(28)
    f_title = font("Black", 168)
    f_sub = font("Medium", 48)
    f_body = font("Regular", 40)
    f_box_h = font("Medium", 38)
    f_item = font("Regular", 40)
    f_num = font("Bold", 40)
    f_bar = font("Bold", 44)
    f_note = font("Regular", 32)
    f_close = font("Medium", 40)

    y = int(32 / 25.4 * DPI)
    draw_spaced(draw, "OFFICIAL NOTICE", cx, y, f_en, GOLD, tracking=12)

    y = int(56 / 25.4 * DPI)
    draw_centered(draw, "謹告", cx, y, f_title, WHITE)

    # 金ライン＋菱形
    y = int(88 / 25.4 * DPI)
    half = int(32 / 25.4 * DPI)
    draw.line([(cx - half, y), (cx + half, y)], fill=GOLD, width=2)
    s = int(2.0 / 25.4 * DPI)
    draw.polygon([(cx, y - s), (cx + s, y), (cx, y + s), (cx - s, y)], fill=GOLD)

    y = int(102 / 25.4 * DPI)
    draw_centered(draw, "トイレのご利用について", cx, y, f_sub, GOLD)

    y = int(124 / 25.4 * DPI)
    draw_centered(draw, "当店のトイレを汚損または破損された場合、", cx, y, f_body, CREAM)
    y = int(136 / 25.4 * DPI)
    draw_centered(draw, "下記のとおり費用をご請求いたします。", cx, y, f_body, CREAM)

    # 請求内容ボックス
    box_w = int(158 / 25.4 * DPI)
    box_h = int(70 / 25.4 * DPI)
    box_x0 = cx - box_w // 2
    box_y0 = int(148 / 25.4 * DPI)
    box_x1 = box_x0 + box_w
    box_y1 = box_y0 + box_h

    # 半透明ボックス
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle(
        [box_x0, box_y0, box_x1, box_y1],
        radius=6,
        fill=(20, 8, 10, 140),
        outline=GOLD_DIM + (255,),
        width=2,
    )
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 見出し
    hy = box_y0 + int(13 / 25.4 * DPI)
    sq = int(3.8 / 25.4 * DPI)
    draw.rectangle(
        [box_x0 + int(14 / 25.4 * DPI), hy - sq // 2, box_x0 + int(14 / 25.4 * DPI) + sq, hy + sq // 2],
        fill=RED,
    )
    draw.text(
        (box_x0 + int(21 / 25.4 * DPI), hy),
        "請求内容",
        font=f_box_h,
        fill=GOLD,
        anchor="lm",
    )

    # 左：項目 / 右：金額（料金表風）
    f_fee = font("Bold", 42)
    rows = [
        ("1.", "汚損による清掃費", "金50,000円"),
        ("2.", "破損による修繕費", "実費（全額）"),
    ]
    iy = box_y0 + int(26 / 25.4 * DPI)
    label_x = box_x0 + int(16 / 25.4 * DPI)
    fee_x = box_x1 - int(14 / 25.4 * DPI)
    for num, label, fee in rows:
        draw.text((label_x, iy), num, font=f_num, fill=RED, anchor="lt")
        draw.text(
            (label_x + int(12 / 25.4 * DPI), iy),
            label,
            font=f_item,
            fill=CREAM,
            anchor="lt",
        )
        draw.text((fee_x, iy), fee, font=f_fee, fill=GOLD, anchor="rt")
        # 点線ガイド
        guide_y = iy + int(9 / 25.4 * DPI)
        gx0 = label_x + int(12 / 25.4 * DPI) + text_size(draw, label, f_item)[0] + int(4 / 25.4 * DPI)
        gx1 = fee_x - text_size(draw, fee, f_fee)[0] - int(4 / 25.4 * DPI)
        if gx1 > gx0 + 8:
            x = gx0
            while x < gx1:
                draw.ellipse([x, guide_y, x + 3, guide_y + 3], fill=GOLD_DIM)
                x += 10
        iy += int(16 / 25.4 * DPI)

    # 注記（ボックス内）
    draw_centered(
        draw,
        "※修繕費は、修理・交換に要した費用をそのままご請求します。",
        cx,
        box_y1 - int(9 / 25.4 * DPI),
        f_note,
        MUTED,
    )

    # 強調帯
    f_bar_sm = font("Bold", 38)
    bar_w = int(168 / 25.4 * DPI)
    bar_h = int(15 / 25.4 * DPI)
    bar_x0 = cx - bar_w // 2
    bar_y0 = box_y1 + int(12 / 25.4 * DPI)
    accent_w = int(4 / 25.4 * DPI)
    draw.rectangle([bar_x0, bar_y0, bar_x0 + accent_w, bar_y0 + bar_h], fill=RED)
    draw.rectangle([bar_x0 + accent_w, bar_y0, bar_x0 + bar_w, bar_y0 + bar_h], fill=RED_DEEP)
    draw.line([(bar_x0, bar_y0), (bar_x0 + bar_w, bar_y0)], fill=GOLD, width=2)
    draw.line([(bar_x0, bar_y0 + bar_h), (bar_x0 + bar_w, bar_y0 + bar_h)], fill=GOLD, width=2)
    draw_centered(
        draw,
        "清掃費5万円／修繕費は実費を請求いたします",
        cx + accent_w // 2,
        bar_y0 + bar_h // 2,
        f_bar_sm,
        WHITE,
        anchor="mm",
    )

    # 補足
    note_y = bar_y0 + bar_h + int(12 / 25.4 * DPI)
    draw_centered(
        draw,
        "悪質な場合は、警察へ通報のうえ然るべき措置を講じます。",
        cx,
        note_y,
        f_note,
        MUTED,
    )

    # 結び
    close_top = note_y + int(16 / 25.4 * DPI)
    half2 = int(48 / 25.4 * DPI)
    draw.line([(cx - half2, close_top), (cx + half2, close_top)], fill=GOLD_DIM, width=1)
    draw_centered(draw, "何卒ご理解とご協力のほど、", cx, close_top + int(12 / 25.4 * DPI), f_close, WHITE)
    draw_centered(draw, "お願い申し上げます。", cx, close_top + int(23 / 25.4 * DPI), f_close, WHITE)

    return img


def save_pdf(img: Image.Image) -> None:
    # JPEG埋め込みで印刷品質を保ちつつファイルサイズを抑える
    import io

    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=94, dpi=(DPI, DPI))
    buf.seek(0)
    c = pdf_canvas.Canvas(str(PDF_OUT), pagesize=A4)
    c.drawImage(ImageReader(buf), 0, 0, width=A4[0], height=A4[1], preserveAspectRatio=False)
    c.save()


def main() -> None:
    print(f"Rendering {W}x{H} @ {DPI}dpi …")
    img = render()
    img.save(PNG_OUT, "PNG", dpi=(DPI, DPI))
    # 掲示用JPG（やや圧縮）
    img.convert("RGB").save(JPG_OUT, "JPEG", quality=92, dpi=(DPI, DPI))
    save_pdf(img)
    print(f"Created: {PDF_OUT}")
    print(f"Created: {PNG_OUT}")
    print(f"Created: {JPG_OUT}")


if __name__ == "__main__":
    main()
