#!/usr/bin/env python3
"""飲食店トイレ注意フライヤーを A4 PDF として生成する"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import Color, white, HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
pdfmetrics.registerFont(TTFont("JP", FONT_PATH, subfontIndex=0))

OUTPUT = "/workspace/トイレ注意フライヤー.pdf"

# 配色（飲食店掲示向け・警戒赤×紺）
BG = HexColor("#F4F6F8")
INK = HexColor("#15202B")
ACCENT = HexColor("#B91C1C")
NAVY = HexColor("#1E2A38")
RULE = HexColor("#7A8490")
ICON = HexColor("#2F4A63")


def draw_toilet_icon(c: canvas.Canvas, cx: float, cy: float, scale: float = 1.0) -> None:
    """シンプルなトイレ線画アイコン"""
    c.saveState()
    c.setStrokeColor(ICON)
    c.setFillColor(Color(0, 0, 0, alpha=0))
    c.setLineWidth(2.2 * scale)
    c.setLineCap(1)
    c.setLineJoin(1)

    # タンク
    tw, th = 38 * scale, 22 * scale
    c.roundRect(cx - tw / 2, cy + 18 * scale, tw, th, 3 * scale, stroke=1, fill=0)
    # 便座（楕円）
    seat_w, seat_h = 48 * scale, 28 * scale
    c.ellipse(
        cx - seat_w / 2,
        cy - 8 * scale,
        cx + seat_w / 2,
        cy - 8 * scale + seat_h,
        stroke=1,
        fill=0,
    )
    # ベース
    bw, bh = 28 * scale, 20 * scale
    c.roundRect(cx - bw / 2, cy - 28 * scale, bw, bh, 2 * scale, stroke=1, fill=0)
    # 取っ手
    c.circle(cx + tw / 2 - 8 * scale, cy + 29 * scale, 2.5 * scale, stroke=1, fill=0)

    c.restoreState()


def create_flyer() -> None:
    width, height = A4
    c = canvas.Canvas(OUTPUT, pagesize=A4)

    # 背景
    c.setFillColor(BG)
    c.rect(0, 0, width, height, stroke=0, fill=1)

    # 外枠
    margin = 10 * mm
    c.setStrokeColor(NAVY)
    c.setLineWidth(2.5)
    c.rect(margin, margin, width - 2 * margin, height - 2 * margin, stroke=1, fill=0)
    c.setLineWidth(0.6)
    c.rect(
        margin + 3 * mm,
        margin + 3 * mm,
        width - 2 * margin - 6 * mm,
        height - 2 * margin - 6 * mm,
        stroke=1,
        fill=0,
    )

    # 上部アクセント帯
    band_top = height - margin - 3 * mm
    band_h = 32 * mm
    c.setFillColor(ACCENT)
    c.rect(
        margin + 3 * mm,
        band_top - band_h,
        width - 2 * margin - 6 * mm,
        band_h,
        stroke=0,
        fill=1,
    )

    # 帯テキスト
    c.setFillColor(white)
    c.setFont("JP", 32)
    title = "ご注意ください"
    c.drawCentredString(width / 2, band_top - band_h / 2 - 9, title)

    # アイコン（ページ中央寄りに配置）
    icon_y = height * 0.62
    draw_toilet_icon(c, width / 2, icon_y, scale=1.35)

    # メイン文言
    c.setFillColor(INK)
    c.setFont("JP", 36)
    line1 = "トイレを汚したり"
    line2 = "破損させた場合"
    y = icon_y - 48 * mm
    c.drawCentredString(width / 2, y, line1)
    c.drawCentredString(width / 2, y - 16 * mm, line2)

    # 区切り線
    rule_y = y - 30 * mm
    c.setStrokeColor(RULE)
    c.setLineWidth(1.2)
    c.line(width / 2 - 50 * mm, rule_y, width / 2 + 50 * mm, rule_y)

    # 請求文言
    c.setFillColor(ACCENT)
    c.setFont("JP", 34)
    charge1 = "清掃費・修理費を"
    charge2 = "請求いたします"
    cy = rule_y - 20 * mm
    c.drawCentredString(width / 2, cy, charge1)
    c.drawCentredString(width / 2, cy - 16 * mm, charge2)

    # 下部協力依頼
    coop_y = margin + 28 * mm
    c.setStrokeColor(RULE)
    c.setLineWidth(0.8)
    c.line(width / 2 - 55 * mm, coop_y + 16 * mm, width / 2 + 55 * mm, coop_y + 16 * mm)

    c.setFillColor(NAVY)
    c.setFont("JP", 18)
    c.drawCentredString(width / 2, coop_y + 5 * mm, "ご協力をお願いいたします")

    c.setFont("JP", 14)
    c.setFillColor(RULE)
    c.drawCentredString(width / 2, coop_y - 8 * mm, "—  当店  —")
    c.save()
    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    create_flyer()
