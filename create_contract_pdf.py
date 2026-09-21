#!/usr/bin/env python3
"""広告掲示契約書を A4 PDF として生成する"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# 22px ≈ 16.5pt (96dpi基準)
FONT_SIZE = 16.5
# WenQuanYi Micro Hei（TrueType・数字/英字対応）
FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"

pdfmetrics.registerFont(TTFont("JP", FONT_PATH, subfontIndex=0))

OUTPUT = "/workspace/広告掲示契約書.pdf"

# 余白をやや広めに（契約書らしい見た目）
MARGIN = 18 * mm

styles = {
    "title": ParagraphStyle(
        "title",
        fontName="JP",
        fontSize=FONT_SIZE + 4,
        leading=(FONT_SIZE + 4) * 1.6,
        alignment=TA_CENTER,
        spaceAfter=8 * mm,
    ),
    "body": ParagraphStyle(
        "body",
        fontName="JP",
        fontSize=FONT_SIZE,
        leading=FONT_SIZE * 1.75,
        alignment=TA_JUSTIFY,
        firstLineIndent=0,
        spaceAfter=3 * mm,
    ),
    "article": ParagraphStyle(
        "article",
        fontName="JP",
        fontSize=FONT_SIZE,
        leading=FONT_SIZE * 1.75,
        alignment=TA_LEFT,
        spaceBefore=5 * mm,
        spaceAfter=2 * mm,
    ),
    "indent": ParagraphStyle(
        "indent",
        fontName="JP",
        fontSize=FONT_SIZE,
        leading=FONT_SIZE * 1.75,
        alignment=TA_LEFT,
        leftIndent=8 * mm,
        spaceAfter=1.5 * mm,
    ),
    "center": ParagraphStyle(
        "center",
        fontName="JP",
        fontSize=FONT_SIZE,
        leading=FONT_SIZE * 1.75,
        alignment=TA_CENTER,
        spaceBefore=4 * mm,
        spaceAfter=4 * mm,
    ),
    "sig": ParagraphStyle(
        "sig",
        fontName="JP",
        fontSize=FONT_SIZE,
        leading=FONT_SIZE * 1.85,
        alignment=TA_LEFT,
        spaceAfter=1.5 * mm,
    ),
}


def P(text, style="body"):
    return Paragraph(text.replace("\n", "<br/>"), styles[style])


def build():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="広告掲示契約書",
        author="",
    )

    story = []

    story.append(P("広告掲示契約書", "title"))

    story.append(
        P(
            "広告主（以下「甲」という。）と、広告掲示場所の所有者または管理者（以下「乙」という。）は、"
            "乙が管理する店舗等に甲の広告物を掲示することについて、以下のとおり契約を締結する。"
        )
    )

    # 第1条
    story.append(P("第1条（広告掲示場所）", "article"))
    story.append(P("乙は、甲に対し、下記の場所に甲の広告物を掲示することを承諾する。"))
    story.append(P("掲示場所", "indent"))
    story.append(P("住所：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿", "indent"))
    story.append(P("店舗名：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿", "indent"))
    story.append(P("掲示箇所：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿", "indent"))
    story.append(P("広告物の種類：看板・広告板・その他（＿＿＿＿＿＿）", "indent"))
    story.append(P("広告物のサイズ：縦＿＿＿＿cm × 横＿＿＿＿cm", "indent"))

    # 第2条
    story.append(P("第2条（掲示期間）", "article"))
    story.append(
        P("掲示期間は、令和＿＿年＿＿月＿＿日から令和＿＿年＿＿月＿＿日までとする。")
    )
    story.append(
        P("契約期間満了後も掲示を継続する場合は、甲乙協議のうえ更新するものとする。")
    )

    # 第3条
    story.append(P("第3条（広告掲示料）", "article"))
    story.append(P("甲は乙に対し、広告掲示料として以下の金額を支払う。"))
    story.append(P("月額：＿＿＿＿＿＿円（税込）", "indent"))
    story.append(P("支払方法：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿", "indent"))
    story.append(P("支払期日：毎月＿＿日まで", "indent"))

    # 第4条
    story.append(P("第4条（広告物の設置・管理）", "article"))
    story.append(
        P(
            "広告物の製作、設置、修理、交換、撤去その他これらに付随する費用は、"
            "原則として甲の負担とする。"
        )
    )
    story.append(
        P(
            "甲は、広告物が落下、破損その他の事故を起こさないよう、適切に管理するものとする。"
        )
    )

    # 第5条
    story.append(P("第5条（広告内容）", "article"))
    story.append(
        P(
            "甲は、広告内容について法令、公序良俗その他関係規定に違反しないことを保証する。"
        )
    )
    story.append(
        P(
            "広告内容について第三者から苦情、請求その他の問題が生じた場合、"
            "原則として甲の責任と費用において対応するものとする。"
        )
    )

    # 第6条
    story.append(P("第6条（広告内容の変更）", "article"))
    story.append(
        P(
            "甲が広告内容、デザイン、サイズまたは掲示方法を変更する場合は、"
            "事前に乙の承諾を得るものとする。"
        )
    )

    # 第7条
    story.append(P("第7条（損害賠償）", "article"))
    story.append(
        P(
            "広告物の設置または管理に起因して、乙または第三者に損害が発生した場合、"
            "甲はその損害を賠償するものとする。"
        )
    )
    story.append(
        P("ただし、乙の故意または過失によって生じた損害については、この限りではない。")
    )

    # 第8条
    story.append(P("第8条（撤去・原状回復）", "article"))
    story.append(
        P(
            "契約終了時、甲は自己の費用と責任において広告物を撤去し、"
            "掲示場所を原状に回復するものとする。"
        )
    )
    story.append(
        P(
            "撤去に伴って建物等に損傷が生じた場合、その修復費用は甲が負担するものとする。"
        )
    )

    # 第9条
    story.append(P("第9条（契約解除）", "article"))
    story.append(
        P(
            "甲または乙が本契約に違反し、相当期間を定めて是正を求めたにもかかわらず"
            "改善されない場合、相手方は本契約を解除することができる。"
        )
    )
    story.append(
        P(
            "また、広告内容が法令等に違反することが判明した場合、"
            "乙は甲に対して広告物の撤去または契約の解除を求めることができる。"
        )
    )

    # 第10条
    story.append(P("第10条（途中解約）", "article"))
    story.append(
        P(
            "甲または乙が契約期間中に本契約を終了させる場合は、"
            "原則として＿＿か月前までに相手方へ書面またはその他合意した方法により通知するものとする。"
        )
    )
    story.append(P("途中解約に伴う費用等については、甲乙協議のうえ決定する。"))

    # 第11条
    story.append(P("第11条（協議事項）", "article"))
    story.append(
        P(
            "本契約に定めのない事項、または本契約の解釈について疑義が生じた場合は、"
            "甲乙誠意をもって協議し、解決するものとする。"
        )
    )

    story.append(Spacer(1, 4 * mm))
    story.append(
        P(
            "以上、本契約の成立を証するため、本書2通を作成し、甲乙それぞれ1通を保管する。"
        )
    )

    story.append(P("令和＿＿年＿＿月＿＿日", "center"))

    story.append(HRFlowable(width="100%", thickness=0.5, spaceBefore=2 * mm, spaceAfter=4 * mm, color="#333333"))

    story.append(P("【甲：広告主】", "sig"))
    story.append(P("住所：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿", "sig"))
    story.append(P("会社名・氏名：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿", "sig"))
    story.append(P("代表者：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿", "sig"))
    story.append(P("電話番号：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿", "sig"))
    story.append(P("印：＿＿＿＿＿＿", "sig"))

    story.append(Spacer(1, 6 * mm))

    story.append(P("【乙：広告掲示場所提供者】", "sig"))
    story.append(P("住所：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿", "sig"))
    story.append(P("会社名・氏名：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿", "sig"))
    story.append(P("代表者：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿", "sig"))
    story.append(P("電話番号：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿", "sig"))
    story.append(P("印：＿＿＿＿＿＿", "sig"))

    page_count = {"n": 0}

    def count_pages(canvas, doc):
        page_count["n"] = doc.page

    doc.build(story, onFirstPage=count_pages, onLaterPages=count_pages)
    return page_count["n"]


if __name__ == "__main__":
    pages = build()
    print(f"PDF created: {OUTPUT}")
    print(f"Page count: {pages}")
