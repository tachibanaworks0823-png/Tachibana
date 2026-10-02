#!/usr/bin/env python3
"""飲食店トイレ注意フライヤー（白背景・大文字）を A4 PDF / PNG として生成する"""

from __future__ import annotations

import io
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
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

# 配色（白系・シンプル）
BG = (252, 252, 251)
INK = (28, 28, 30)
INK_SOFT = (70, 70, 74)
LINE = (40, 40, 44)
ACCENT = (180, 28, 28)
ACCENT_DEEP = (140, 20, 20)
MUTED = (110, 110, 116)
WHITE = (255, 255, 255)
BOX_BG = (247, 247, 246)
BOX_LINE = (180, 180, 184)


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(SERIF.format(weight), size=size, index=0)


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


def draw_corner(draw: ImageDraw.ImageDraw, x: int, y: int, dx: int, dy: int, length: int, width: int = 3) -> None:
    draw.line([(x, y), (x + dx * length, y)], fill=LINE, width=width)
    draw.line([(x, y), (x, y + dy * length)], fill=LINE, width=width)


def draw_frame(draw: ImageDraw.ImageDraw) -> None:
    m_o = int(10 / 25.4 * DPI)
    m_i = int(12.5 / 25.4 * DPI)
    draw.rectangle([m_o, m_o, W - m_o, H - m_o], outline=LINE, width=3)
    draw.rectangle([m_i, m_i, W - m_i, H - m_i], outline=BOX_LINE, width=1)

    cl = int(12 / 25.4 * DPI)
    draw_corner(draw, m_o, m_o, 1, 1, cl)
    draw_corner(draw, W - m_o, m_o, -1, 1, cl)
    draw_corner(draw, m_o, H - m_o, 1, -1, cl)
    draw_corner(draw, W - m_o, H - m_o, -1, -1, cl)


def render() -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_frame(draw)
    cx = W // 2

    f_title = font("Black", 76)
    f_body = font("Regular", 50)
    f_box_h = font("Medium", 62)
    f_item = font("Regular", 66)
    f_num = font("Bold", 66)
    f_fee = font("Bold", 68)
    f_note = font("Regular", 46)
    f_close = font("Medium", 48)

    # ページ中央寄りに配置（削除後の余白を活かす）
    y = int(38 / 25.4 * DPI)
    draw_centered(draw, "トイレのご利用について", cx, y, f_title, INK)

    y = int(56 / 25.4 * DPI)
    half = int(36 / 25.4 * DPI)
    draw.line([(cx - half, y), (cx + half, y)], fill=LINE, width=3)
    s = int(2.2 / 25.4 * DPI)
    draw.polygon([(cx, y - s), (cx + s, y), (cx, y + s), (cx - s, y)], fill=ACCENT)

    y = int(74 / 25.4 * DPI)
    draw_centered(draw, "いつも綺麗にご利用いただき、ありがとうございます。", cx, y, f_body, INK_SOFT)
    y = int(92 / 25.4 * DPI)
    draw_centered(draw, "当店のトイレを汚損または破損された場合、", cx, y, f_body, INK_SOFT)
    y = int(108 / 25.4 * DPI)
    draw_centered(draw, "下記のとおり費用をご請求いたします。", cx, y, f_body, INK_SOFT)

    # 請求内容ボックス（広め・中の文字大きめ）
    box_w = int(182 / 25.4 * DPI)
    box_h = int(118 / 25.4 * DPI)
    box_x0 = cx - box_w // 2
    box_y0 = int(122 / 25.4 * DPI)
    box_x1 = box_x0 + box_w
    box_y1 = box_y0 + box_h

    draw.rounded_rectangle(
        [box_x0, box_y0, box_x1, box_y1],
        radius=4,
        fill=BOX_BG,
        outline=BOX_LINE,
        width=2,
    )

    hy = box_y0 + int(22 / 25.4 * DPI)
    sq = int(5.5 / 25.4 * DPI)
    draw.rectangle(
        [box_x0 + int(14 / 25.4 * DPI), hy - sq // 2, box_x0 + int(14 / 25.4 * DPI) + sq, hy + sq // 2],
        fill=ACCENT,
    )
    draw.text(
        (box_x0 + int(24 / 25.4 * DPI), hy),
        "請求内容",
        font=f_box_h,
        fill=INK,
        anchor="lm",
    )

    rows = [
        ("1.", "汚損による清掃費", "金50,000円"),
        ("2.", "破損による修繕費", "実費（全額）"),
    ]
    iy = box_y0 + int(44 / 25.4 * DPI)
    label_x = box_x0 + int(14 / 25.4 * DPI)
    # 金額は左揃えで縦位置を揃える
    fee_x = box_x0 + int(112 / 25.4 * DPI)
    for num, label, fee in rows:
        draw.text((label_x, iy), num, font=f_num, fill=ACCENT, anchor="lt")
        draw.text(
            (label_x + int(16 / 25.4 * DPI), iy),
            label,
            font=f_item,
            fill=INK,
            anchor="lt",
        )
        draw.text((fee_x, iy), fee, font=f_fee, fill=ACCENT, anchor="lt")
        guide_y = iy + int(14 / 25.4 * DPI)
        gx0 = label_x + int(16 / 25.4 * DPI) + text_size(draw, label, f_item)[0] + int(4 / 25.4 * DPI)
        gx1 = fee_x - int(4 / 25.4 * DPI)
        if gx1 > gx0 + 8:
            x = gx0
            while x < gx1:
                draw.ellipse([x, guide_y, x + 3, guide_y + 3], fill=BOX_LINE)
                x += 10
        iy += int(28 / 25.4 * DPI)

    draw_centered(
        draw,
        "※修繕費は、修理・交換に要した費用をそのままご請求します。",
        cx,
        box_y1 - int(15 / 25.4 * DPI),
        f_note,
        MUTED,
    )

    # 結び
    close_y = box_y1 + int(28 / 25.4 * DPI)
    draw_centered(
        draw,
        "何卒ご理解とご協力のほど、お願い申し上げます。",
        cx,
        close_y,
        f_close,
        INK,
    )

    return img


def save_pdf(img: Image.Image) -> None:
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
    img.convert("RGB").save(JPG_OUT, "JPEG", quality=92, dpi=(DPI, DPI))
    save_pdf(img)
    print(f"Created: {PDF_OUT}")
    print(f"Created: {PNG_OUT}")
    print(f"Created: {JPG_OUT}")


if __name__ == "__main__":
    main()
