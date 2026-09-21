#!/usr/bin/env python3
"""20 variations based on velvet-billboard (Design 01)."""
from pathlib import Path

ROOT = Path("/workspace")
D = ROOT / "designs"
D.mkdir(exist_ok=True)

# Remove previous design html/css except shared/nav
for p in D.glob("*"):
    if p.name in ("shared.css", "nav.js"):
        continue
    if p.suffix in {".html", ".css"}:
        p.unlink()

ITEMS = [
    ("モエシロ", "ブリュット アンペリアル", "¥20,000"),
    ("モエロゼ", "ロゼ アンペリアル", "¥25,000"),
    ("モエ黒", "ネクター アンペリアル", "¥30,000"),
    ("モエアイス", "アイス アンペリアル", "¥35,000"),
    ("モエピカ", "N.I.R ロゼ ドライ", "¥40,000"),
]

META = [
    (1, "base", "ベース（現行01）"),
    (2, "pika-front", "ピカ最前・迫力アップ"),
    (3, "wide-menu", "メニュー広め・文字さらに大"),
    (4, "bottle-dominate", "ボトル強め・画面半分"),
    (5, "brut-stack", "シロ／黒／ピカの並び"),
    (6, "glass-panel", "ガラスパネル風メニュー"),
    (7, "gold-rule", "金ライン強調"),
    (8, "leader-dots", "ドットリーダー付き"),
    (9, "ice-lead", "アイス主導の重なり"),
    (10, "rose-lead", "ロゼ主導の重なり"),
    (11, "deep-noir", "より深いノワール"),
    (12, "warm-amber", "暖色アンバー寄り"),
    (13, "cool-night", "クールナイト寄り"),
    (14, "crop-impact", "ボトル寄りトリミング"),
    (15, "show-labels", "ラベルが見える高さ"),
    (16, "framed-panel", "右パネルに金枠"),
    (17, "glow-hot", "ピカ行を光らせる"),
    (18, "soft-fade", "ボトルからメニューへ柔らかい溶け"),
    (19, "five-ghost", "5本を薄く背後に"),
    (20, "bar-floor", "バーカウンター反射感"),
]

SHARED = Path("designs/shared.css").read_text(encoding="utf-8") if Path("designs/shared.css").exists() else ""
if "velvet" not in SHARED:
    SHARED = r"""
:root{
  --bg:#060403;--ink:#fff6ea;--muted:rgba(255,246,234,.78);--soft:rgba(255,246,234,.5);
  --gold:#e2b45c;--gold2:#ffe7b0;--rose:#e8a0a8;
  --serif:"Cormorant Garamond","Shippori Mincho",serif;
  --jp:"Shippori Mincho","Cormorant Garamond",serif;
  --sans:"Zen Kaku Gothic New",system-ui,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;height:100%;overflow:hidden;background:var(--bg);color:var(--ink);font-family:var(--jp);-webkit-font-smoothing:antialiased}
img{display:block;max-width:100%}
.back,.badge{position:fixed;z-index:50;font-family:var(--sans);font-size:11px;letter-spacing:.12em;text-decoration:none;color:rgba(255,246,234,.55);background:rgba(0,0,0,.45);border:1px solid rgba(226,180,92,.3);padding:.4rem .65rem}
.back{top:10px;left:10px}.badge{top:10px;right:10px;color:var(--gold2)}
body.shot .back,body.shot .badge,html.shot .back,html.shot .badge{display:none!important}
.maison{font-family:var(--serif);letter-spacing:.42em;color:var(--gold);font-size:clamp(1rem,1.5vw,1.3rem);font-weight:600}
.title{font-size:clamp(2.6rem,5.5vw,4.6rem);letter-spacing:.16em;font-weight:700;line-height:1.05}
.nick{font-size:clamp(2rem,4vw,3.5rem);font-weight:700;letter-spacing:.1em;line-height:1.05}
.formal{margin-top:.3rem;font-size:clamp(1.15rem,1.9vw,1.7rem);color:var(--muted);letter-spacing:.05em}
.price{font-family:var(--serif);font-size:clamp(2.1rem,4.2vw,3.7rem);font-weight:700;color:var(--gold);line-height:1;white-space:nowrap}
.is-hot .nick,.is-hot .price{color:var(--gold2)}
@media(max-width:800px){html,body{overflow:auto;height:auto;min-height:100%}}
"""

BASE_CSS = r"""
.stage{position:relative;width:100%;height:100%}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.32)}
.shade{position:absolute;inset:0;background:linear-gradient(105deg,rgba(6,4,3,.1),rgba(6,4,3,.7) 45%,rgba(6,4,3,.96) 66%);z-index:1}
.drama{position:absolute;left:0;top:0;bottom:0;width:52%;z-index:2;pointer-events:none}
.b{position:absolute;bottom:-6%;object-fit:contain;filter:drop-shadow(0 25px 50px rgba(0,0,0,.65))}
.b1{left:0;height:78%;opacity:.55;transform:rotate(-9deg)}
.b2{left:10%;height:88%;opacity:.8;transform:rotate(3deg)}
.b3{left:22%;height:105%;transform:rotate(-2deg)}
.panel{position:absolute;right:0;top:0;bottom:0;width:min(56vw,800px);z-index:3;padding:3.5vh 3.5vw;display:flex;flex-direction:column;justify-content:center}
.list{margin-top:2vh;display:flex;flex-direction:column;gap:1.2vh}
.row{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;border-bottom:2px solid rgba(226,180,92,.3);padding-bottom:1vh}
.ghost{position:absolute;opacity:.12;filter:grayscale(.2);bottom:0;height:55%;object-fit:contain;z-index:1}
.floor{display:none}
"""

VARIANTS = {
    1: "",  # base
    2: """
.b1{left:2%;height:70%;opacity:.4;transform:rotate(-12deg)}
.b2{left:8%;height:82%;opacity:.65;transform:rotate(2deg)}
.b3{left:18%;height:118%;transform:rotate(-1deg);filter:drop-shadow(0 0 55px rgba(255,90,60,.4))}
""",
    3: """
.drama{width:42%}
.panel{width:min(64vw,920px)}
.nick{font-size:clamp(2.3rem,4.6vw,4rem)}
.formal{font-size:clamp(1.25rem,2.1vw,1.9rem)}
.price{font-size:clamp(2.4rem,4.8vw,4.2rem)}
.title{font-size:clamp(2.8rem,6vw,5rem)}
""",
    4: """
.drama{width:58%}
.panel{width:min(46vw,680px)}
.b1{left:-2%;height:85%;opacity:.5}
.b2{left:12%;height:95%;opacity:.75}
.b3{left:26%;height:112%}
.shade{background:linear-gradient(105deg,rgba(6,4,3,.05),rgba(6,4,3,.55) 50%,rgba(6,4,3,.96) 72%)}
""",
    5: "",  # bottle swap in html
    6: """
.panel{right:3vw;top:50%;bottom:auto;transform:translateY(-50%);height:auto;max-height:90vh;width:min(52vw,720px);
  background:rgba(12,9,7,.55);border:1px solid rgba(255,255,255,.12);backdrop-filter:blur(14px);padding:3.2vh 2.8vw;box-shadow:0 30px 80px rgba(0,0,0,.35)}
""",
    7: """
.row{border-bottom-width:3px;border-bottom-color:rgba(226,180,92,.45)}
.is-hot{border-bottom-color:var(--gold2)}
.panel::before{content:"";position:absolute;left:0;top:12%;bottom:12%;width:2px;background:linear-gradient(180deg,transparent,var(--gold),transparent)}
.panel{padding-left:4.2vw}
""",
    8: """
.row{display:grid;grid-template-columns:auto 1fr auto;align-items:end;gap:.8rem}
.row .rule{border-bottom:2px dotted rgba(226,180,92,.4);transform:translateY(-.55em);min-width:1.5rem}
""",
    9: "",  # bottle swap
    10: "",  # bottle swap
    11: """
.bg{filter:brightness(.22) contrast(1.15)}
.shade{background:linear-gradient(105deg,rgba(0,0,0,.25),rgba(0,0,0,.8) 48%,rgba(0,0,0,.97) 68%)}
.b1,.b2{opacity:.45}
""",
    12: """
.bg{filter:brightness(.34) sepia(.25) saturate(1.15)}
.shade{background:linear-gradient(105deg,rgba(40,18,8,.15),rgba(20,10,6,.7) 45%,rgba(8,5,3,.96) 68%)}
.maison,.price{color:#f0c27a}
""",
    13: """
.bg{filter:brightness(.3) hue-rotate(18deg) saturate(.9)}
.shade{background:linear-gradient(105deg,rgba(8,12,20,.2),rgba(6,8,14,.75) 48%,rgba(4,5,10,.97) 68%)}
.maison{color:#b8cce0}
.price{color:#d4dff0}
.is-hot .nick,.is-hot .price{color:#fff}
""",
    14: """
.b1{left:-6%;height:90%;bottom:-12%;opacity:.5}
.b2{left:4%;height:100%;bottom:-14%;opacity:.75}
.b3{left:16%;height:125%;bottom:-16%}
.drama{width:50%}
""",
    15: """
.b1{bottom:2%;height:70%;opacity:.55}
.b2{bottom:2%;height:78%;opacity:.8}
.b3{bottom:0;height:88%}
""",
    16: """
.panel{right:3vw;top:5vh;bottom:5vh;width:min(52vw,740px);border:1px solid rgba(226,180,92,.5);padding:3.5vh 3vw;
  background:rgba(8,6,5,.35);box-shadow:inset 0 0 0 1px rgba(226,180,92,.15)}
""",
    17: """
.is-hot{background:linear-gradient(90deg,rgba(226,180,92,.12),transparent);padding:.6vh .8vw;margin:0 -.8vw;border-bottom-color:var(--gold2)}
.is-hot .nick,.is-hot .price{text-shadow:0 0 22px rgba(255,180,80,.45)}
.b3{filter:drop-shadow(0 0 50px rgba(255,90,60,.45)) drop-shadow(0 25px 50px rgba(0,0,0,.65))}
""",
    18: """
.shade{background:linear-gradient(100deg,rgba(6,4,3,.05),rgba(6,4,3,.45) 38%,rgba(6,4,3,.88) 58%,rgba(6,4,3,.98) 72%)}
.drama{width:54%}
.panel{width:min(58vw,820px);background:linear-gradient(90deg,transparent,rgba(6,4,3,.55) 12%,rgba(6,4,3,.0))}
""",
    19: """
.ghost.g1{left:2%;height:50%;bottom:0;opacity:.14}
.ghost.g2{left:12%;height:52%;bottom:0;opacity:.12}
.ghost.g3{left:22%;height:54%;bottom:0;opacity:.1}
.b1{left:4%;height:76%;opacity:.5}
.b2{left:14%;height:86%;opacity:.75}
.b3{left:26%;height:105%}
""",
    20: """
.floor{display:block;position:absolute;left:0;width:52%;bottom:0;height:28%;z-index:2;
  background:linear-gradient(180deg,rgba(255,255,255,.04),rgba(0,0,0,.35));
  border-top:1px solid rgba(226,180,92,.18);transform:perspective(500px) rotateX(8deg);transform-origin:top;pointer-events:none}
.b1,.b2,.b3{bottom:8%}
.drama{width:52%}
""",
}

BOTTLE_SETS = {
    1: ("rose", "ice", "pika"),
    2: ("rose", "ice", "pika"),
    3: ("rose", "ice", "pika"),
    4: ("rose", "ice", "pika"),
    5: ("brut", "nectar", "pika"),
    6: ("rose", "ice", "pika"),
    7: ("rose", "ice", "pika"),
    8: ("rose", "ice", "pika"),
    9: ("brut", "pika", "ice"),
    10: ("ice", "pika", "rose"),
    11: ("rose", "ice", "pika"),
    12: ("rose", "ice", "pika"),
    13: ("rose", "ice", "pika"),
    14: ("rose", "ice", "pika"),
    15: ("rose", "ice", "pika"),
    16: ("rose", "ice", "pika"),
    17: ("rose", "ice", "pika"),
    18: ("rose", "ice", "pika"),
    19: ("rose", "ice", "pika"),
    20: ("rose", "ice", "pika"),
}


def list_html(with_rules=False):
    rows = []
    for i, (nick, formal, price) in enumerate(ITEMS):
        hot = " is-hot" if i == 4 else ""
        rule = '<span class="rule" aria-hidden="true"></span>' if with_rules else ""
        rows.append(
            f'<div class="row{hot}"><div><p class="nick">{nick}</p>'
            f'<p class="formal">モエ・エ・シャンドン {formal}</p></div>'
            f'{rule}<p class="price">{price}</p></div>'
        )
    return "\n".join(rows)


def ghosts_html():
    return """
<img class="ghost g1" src="../assets/moet/cut/brut.png" alt=""/>
<img class="ghost g2" src="../assets/moet/cut/nectar.png" alt=""/>
<img class="ghost g3" src="../assets/moet/cut/rose.png" alt=""/>
"""


def write_one(num, slug, title):
    b1, b2, b3 = BOTTLE_SETS[num]
    rules = num == 8
    ghost = ghosts_html() if num == 19 else ""
    floor = '<div class="floor"></div>' if num == 20 else ""
    body = f"""
<div class="stage">
<img class="bg" src="../assets/moet/moet-bg.png" alt=""/>
<div class="shade"></div>
{floor}
<div class="drama">
{ghost}
<img class="b b1" src="../assets/moet/cut/{b1}.png" alt=""/>
<img class="b b2" src="../assets/moet/cut/{b2}.png" alt=""/>
<img class="b b3" src="../assets/moet/cut/{b3}.png" alt=""/>
</div>
<div class="panel">
<p class="maison">MOËT &amp; CHANDON</p>
<h1 class="title">モエシリーズ</h1>
<div class="list">{list_html(rules)}</div>
</div>
</div>
"""
    html = f"""<!DOCTYPE html><html lang="ja"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Design {num:02d} — {title}</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Shippori+Mincho:wght@600;700&family=Zen+Kaku+Gothic+New:wght@500;700&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="shared.css"/><link rel="stylesheet" href="{num:02d}-{slug}.css"/>
</head><body>
<a class="back" href="../index.html">← 一覧</a>
<div class="badge">DESIGN {num:02d} · {title}</div>
{body}
<script>if(new URLSearchParams(location.search).get('shot')==='1'){{document.documentElement.classList.add('shot');document.addEventListener('DOMContentLoaded',()=>document.body.classList.add('shot'));}}</script>
<script src="nav.js"></script></body></html>"""
    css = BASE_CSS + "\n" + VARIANTS.get(num, "")
    (D / f"{num:02d}-{slug}.html").write_text(html, encoding="utf-8")
    (D / f"{num:02d}-{slug}.css").write_text(css, encoding="utf-8")
    print("ok", num, slug)


for num, slug, title in META:
    write_one(num, slug, title)

files = {n: f"{n:02d}-{s}.html" for n, s, _ in META}
(D / "shared.css").write_text(SHARED, encoding="utf-8")
(D / "nav.js").write_text(
    f"""
window.DESIGN_FILES = {files};
if (new URLSearchParams(location.search).get('shot') === '1') {{
  document.documentElement.classList.add('shot');
  document.addEventListener('DOMContentLoaded', () => document.body.classList.add('shot'));
}}
(() => {{
  const m = (location.pathname.split('/').pop() || '').match(/^(\\d{{2}})-/);
  const n = m ? parseInt(m[1], 10) : 1;
  const total = Object.keys(DESIGN_FILES).length;
  const go = (t) => {{ const name = DESIGN_FILES[t]; if (name) location.href = name; }};
  document.addEventListener('keydown', (e) => {{
    if (e.key === 'ArrowRight' || e.key === ' ') {{ e.preventDefault(); go(n >= total ? 1 : n + 1); }}
    else if (e.key === 'ArrowLeft') {{ e.preventDefault(); go(n <= 1 ? total : n - 1); }}
    else if (e.key === 'Escape' || e.key === 'g' || e.key === 'G') location.href = '../index.html';
  }});
}})();
""",
    encoding="utf-8",
)

blocks = [
    f'<section class="block" id="d{n:02d}"><h2>{n:02d} · {t}</h2>'
    f'<img src="previews/phone/{n:02d}-{s}.jpg" alt="{t}"/></section>'
    for n, s, t in META
]
(ROOT / "index.html").write_text(
    f"""<!DOCTYPE html><html lang="ja"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"/>
<title>ベルベットビルボード派生 20案</title>
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@600;700&family=Zen+Kaku+Gothic+New:wght@400;500&display=swap" rel="stylesheet"/>
<style>
:root{{--bg:#0a0806;--ink:#fff6ea;--gold:#e2b45c;--muted:rgba(255,246,234,.65)}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--ink);font-family:"Zen Kaku Gothic New",system-ui,sans-serif}}
header{{padding:1.1rem 1rem;position:sticky;top:0;z-index:10;background:rgba(10,8,6,.94);backdrop-filter:blur(10px);border-bottom:1px solid rgba(226,180,92,.3)}}
.eyebrow{{font-size:.7rem;letter-spacing:.28em;color:var(--gold)}}
h1{{font-family:"Shippori Mincho",serif;font-size:1.25rem;letter-spacing:.08em;margin:.35rem 0}}
.sub{{font-size:.84rem;color:var(--muted);line-height:1.65}}
.jump{{display:flex;gap:.35rem;overflow-x:auto;padding:.65rem 1rem;border-bottom:1px solid rgba(255,255,255,.06)}}
.jump a{{flex:0 0 auto;padding:.3rem .6rem;border:1px solid rgba(226,180,92,.4);color:var(--gold);text-decoration:none;border-radius:999px;font-size:.78rem}}
.block{{scroll-margin-top:6.2rem;padding:1rem 1rem 0}}
.block h2{{font-family:"Shippori Mincho",serif;font-size:1.05rem;color:var(--gold);margin-bottom:.55rem}}
.block img{{width:100%;height:auto;display:block;border:1px solid rgba(226,180,92,.25);background:#111}}
.note{{padding:1.1rem 1rem 2.5rem;font-size:.84rem;color:var(--muted);line-height:1.7}}
</style></head><body>
<header>
<p class="eyebrow">BASED ON 01 · VELVET BILLBOARD</p>
<h1>01ベースの派生案 20種</h1>
<p class="sub">左ボトル／右大メニューの構成はそのままに、迫力・色味・余白・ボトル順などを変えています。番号を送ってください。</p>
</header>
<nav class="jump">{''.join(f'<a href="#d{n:02d}">{n:02d}</a>' for n,_,__ in META)}</nav>
<main>{''.join(blocks)}<p class="note">近い案の番号（複数可）を送ってください。</p></main>
</body></html>""",
    encoding="utf-8",
)

(ROOT / "README.md").write_text(
    "# ベルベットビルボード派生20案\n\nDesign 01 をベースにしたバリエーション。`index.html` で確認。\n",
    encoding="utf-8",
)
print("DONE", len(META))
