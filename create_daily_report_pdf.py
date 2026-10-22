#!/usr/bin/env python3
"""wonderland 営業日報を A4 縦 PDF として生成する"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
pdfmetrics.registerFont(TTFont("JP", FONT_PATH, subfontIndex=0))

OUTPUT = "/workspace/営業日報_wonderland.pdf"
PAGE_W, PAGE_H = A4

MARGIN_L = 12 * mm
MARGIN_R = 12 * mm
MARGIN_T = 12 * mm
MARGIN_B = 12 * mm

CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R
ROWS = 15


def draw_hline(c, x1, x2, y, stroke=0.6):
    c.setStrokeColorRGB(0.15, 0.15, 0.15)
    c.setLineWidth(stroke)
    c.line(x1, y, x2, y)


def draw_vline(c, x, y1, y2, stroke=0.6):
    c.setStrokeColorRGB(0.15, 0.15, 0.15)
    c.setLineWidth(stroke)
    c.line(x, y1, x, y2)


def draw_rect(c, x, y, w, h, stroke=0.8, fill=0):
    c.setStrokeColorRGB(0.15, 0.15, 0.15)
    c.setLineWidth(stroke)
    c.rect(x, y, w, h, stroke=1, fill=fill)


def centered_text(c, text, x, y, font="JP", size=10):
    c.setFont(font, size)
    c.drawCentredString(x, y, text)


def left_text(c, text, x, y, font="JP", size=10):
    c.setFont(font, size)
    c.drawString(x, y, text)


def draw_name_place_grid(
    c, x0, y, title, label_w, content_w, cells=5, top_label="名前", bottom_label="配置場所"
):
    """左ラベル＋上段/下段の5マス表。戻り値は次の y（上端）。"""
    top_h = 8.5 * mm
    bottom_h = 8.5 * mm
    total_h = top_h + bottom_h
    grid_w = content_w - label_w
    cell_w = grid_w / cells

    draw_rect(c, x0, y - total_h, content_w, total_h, stroke=0.9)

    # 左ラベル
    c.setFillColorRGB(0.94, 0.94, 0.94)
    c.rect(x0, y - total_h, label_w, total_h, stroke=0, fill=1)
    c.setFillColorRGB(0, 0, 0)
    draw_vline(c, x0 + label_w, y - total_h, y, stroke=0.6)
    centered_text(c, title, x0 + label_w / 2, y - total_h / 2 - 1.5 * mm, size=9)

    # 上段 / 下段の区切り
    draw_hline(c, x0 + label_w, x0 + content_w, y - top_h, stroke=0.55)

    # 縦マス区切り＋小ラベル
    for i in range(cells):
        cx = x0 + label_w + i * cell_w
        if i > 0:
            draw_vline(c, cx, y - total_h, y, stroke=0.5)
        left_text(c, top_label, cx + 1.2 * mm, y - 3.2 * mm, size=6)
        left_text(c, bottom_label, cx + 1.2 * mm, y - top_h - 3.2 * mm, size=6)

    return y - total_h


def build():
    c = canvas.Canvas(OUTPUT, pagesize=A4)
    c.setTitle("営業日報 - wonderland")
    c.setAuthor("wonderland")

    x0 = MARGIN_L
    y = PAGE_H - MARGIN_T

    # ---- ヘッダー ----
    title_h = 12 * mm
    draw_rect(c, x0, y - title_h, CONTENT_W, title_h, stroke=1.2)
    centered_text(c, "wonderland", x0 + CONTENT_W / 2, y - 5.2 * mm, size=15)
    centered_text(c, "営 業 日 報", x0 + CONTENT_W / 2, y - 10.2 * mm, size=10)
    y -= title_h + 2.5 * mm

    # ---- 日付・記載者 ----
    meta_h = 10 * mm
    label_w = 18 * mm
    col_w = CONTENT_W / 2
    draw_rect(c, x0, y - meta_h, CONTENT_W, meta_h, stroke=0.9)
    draw_vline(c, x0 + col_w, y - meta_h, y, stroke=0.7)

    # 左：日付（ラベル列＋記入）
    c.setFillColorRGB(0.94, 0.94, 0.94)
    c.rect(x0, y - meta_h, label_w, meta_h, stroke=0, fill=1)
    c.setFillColorRGB(0, 0, 0)
    draw_vline(c, x0 + label_w, y - meta_h, y, stroke=0.6)
    centered_text(c, "日付", x0 + label_w / 2, y - meta_h / 2 - 1.5 * mm, size=9)
    left_text(
        c,
        "　　　年　　　月　　　日（　　）",
        x0 + label_w + 3 * mm,
        y - meta_h / 2 - 1.5 * mm,
        size=10,
    )

    # 右：記載者（記入線なし・空白のみ）
    c.setFillColorRGB(0.94, 0.94, 0.94)
    c.rect(x0 + col_w, y - meta_h, label_w, meta_h, stroke=0, fill=1)
    c.setFillColorRGB(0, 0, 0)
    draw_vline(c, x0 + col_w + label_w, y - meta_h, y, stroke=0.6)
    centered_text(c, "記載者", x0 + col_w + label_w / 2, y - meta_h / 2 - 1.5 * mm, size=9)
    y -= meta_h + 2 * mm

    # ---- 出勤者（出勤時間×5 / 名前×5） ----
    y = draw_name_place_grid(
        c,
        x0,
        y,
        "出勤者",
        label_w,
        CONTENT_W,
        cells=5,
        top_label="出勤時間",
        bottom_label="名前",
    )
    y -= 2 * mm

    # ---- 配置（名前×5 / 配置場所×5） ----
    y = draw_name_place_grid(
        c,
        x0,
        y,
        "配置",
        label_w,
        CONTENT_W,
        cells=5,
        top_label="名前",
        bottom_label="配置場所",
    )
    y -= 2 * mm

    # ---- 特筆事項（均一5マス） ----
    note_lines = 5
    label_h = 4.5 * mm
    row_h = 8.5 * mm  # 書きやすい高さ・均一
    note_h = label_h + note_lines * row_h
    draw_rect(c, x0, y - note_h, CONTENT_W, note_h, stroke=0.9)
    c.setFillColorRGB(0.94, 0.94, 0.94)
    c.rect(x0, y - label_h, CONTENT_W, label_h, stroke=0, fill=1)
    c.setFillColorRGB(0, 0, 0)
    draw_hline(c, x0, x0 + CONTENT_W, y - label_h, stroke=0.6)
    left_text(c, "特筆事項", x0 + 2.5 * mm, y - 3.3 * mm, size=9)
    for i in range(1, note_lines):
        ly = y - label_h - i * row_h
        draw_hline(c, x0, x0 + CONTENT_W, ly, stroke=0.45)
    y -= note_h + 2 * mm

    # ---- 案内組数・客数合計 ----
    total_h = 9 * mm
    total_label_w = 38 * mm
    half = CONTENT_W / 2
    draw_rect(c, x0, y - total_h, CONTENT_W, total_h, stroke=0.9)
    draw_vline(c, x0 + half, y - total_h, y, stroke=0.7)

    # 案内組数
    c.setFillColorRGB(0.94, 0.94, 0.94)
    c.rect(x0, y - total_h, total_label_w, total_h, stroke=0, fill=1)
    c.setFillColorRGB(0, 0, 0)
    draw_vline(c, x0 + total_label_w, y - total_h, y, stroke=0.6)
    centered_text(
        c, "案内組数（合計）", x0 + total_label_w / 2, y - total_h / 2 - 1.5 * mm, size=8
    )
    draw_hline(
        c, x0 + total_label_w + 4 * mm, x0 + half - 12 * mm, y - total_h / 2 - 1 * mm, stroke=0.5
    )
    left_text(c, "組", x0 + half - 9 * mm, y - total_h / 2 - 1.5 * mm, size=10)

    # 客数
    c.setFillColorRGB(0.94, 0.94, 0.94)
    c.rect(x0 + half, y - total_h, total_label_w, total_h, stroke=0, fill=1)
    c.setFillColorRGB(0, 0, 0)
    draw_vline(c, x0 + half + total_label_w, y - total_h, y, stroke=0.6)
    centered_text(
        c,
        "客数（合計）",
        x0 + half + total_label_w / 2,
        y - total_h / 2 - 1.5 * mm,
        size=8,
    )
    draw_hline(
        c,
        x0 + half + total_label_w + 4 * mm,
        x0 + CONTENT_W - 12 * mm,
        y - total_h / 2 - 1 * mm,
        stroke=0.5,
    )
    left_text(c, "名", x0 + CONTENT_W - 9 * mm, y - total_h / 2 - 1.5 * mm, size=10)
    y -= total_h + 2 * mm

    # ---- 案内記録テーブル（15行） ----
    # カラム: No. | 時間 | 案内場所 | 対応者 | 対応場所
    headers = ["No.", "時間", "案内場所", "対応者", "対応場所"]
    # 幅比率
    ratios = [0.07, 0.16, 0.29, 0.19, 0.29]
    col_widths = [CONTENT_W * r for r in ratios]

    header_h = 7 * mm
    # 残り高さに合わせて行高を計算
    avail = y - MARGIN_B - 2 * mm
    row_h = min(7.2 * mm, avail / (ROWS + 1))
    table_h = header_h + ROWS * row_h

    table_bottom = y - table_h
    draw_rect(c, x0, table_bottom, CONTENT_W, table_h, stroke=1.0)

    # ヘッダー背景（薄いグレー）
    c.setFillColorRGB(0.92, 0.92, 0.92)
    c.rect(x0, y - header_h, CONTENT_W, header_h, stroke=0, fill=1)
    c.setFillColorRGB(0, 0, 0)
    draw_hline(c, x0, x0 + CONTENT_W, y - header_h, stroke=0.8)

    # 縦線・ヘッダー文字
    cx = x0
    for i, (w, htext) in enumerate(zip(col_widths, headers)):
        if i > 0:
            draw_vline(c, cx, table_bottom, y, stroke=0.6)
        centered_text(c, htext, cx + w / 2, y - header_h + 2.2 * mm, size=9)
        cx += w

    # データ行
    for r in range(ROWS):
        ry = y - header_h - (r + 1) * row_h
        draw_hline(c, x0, x0 + CONTENT_W, ry, stroke=0.45)
        # 行番号
        centered_text(
            c,
            str(r + 1),
            x0 + col_widths[0] / 2,
            ry + row_h / 2 - 1.2 * mm,
            size=8,
        )

    # フッター注記
    left_text(
        c,
        "※ 時間・案内場所・対応者・対応場所を記入してください",
        x0,
        table_bottom - 4.5 * mm,
        size=7,
    )

    c.save()
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
