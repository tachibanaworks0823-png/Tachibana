#!/usr/bin/env python3
"""High-impact Moët designs — large type for distance reading."""
from pathlib import Path

ROOT = Path("/workspace")
DESIGNS = ROOT / "designs"
DESIGNS.mkdir(exist_ok=True)

# Clean old design files
for p in DESIGNS.glob("*"):
    if p.name in ("shared.css", "nav.js"):
        continue
    p.unlink()

ITEMS = [
    ("モエシロ", "ブリュット アンペリアル", "Brut Impérial", "¥20,000", "brut"),
    ("モエロゼ", "ロゼ アンペリアル", "Rosé Impérial", "¥25,000", "rose"),
    ("モエ黒", "ネクター アンペリアル", "Nectar Impérial", "¥30,000", "nectar"),
    ("モエアイス", "アイス アンペリアル", "Ice Impérial", "¥35,000", "ice"),
    ("モエピカ", "N.I.R ロゼ ドライ", "Nectar Impérial Rosé Dry", "¥40,000", "pika"),
]

META = [
    (1, "billboard", "ビルボード", "巨大文字の縦リスト＋ボトル迫力"),
    (2, "scoreboard", "スコアボード", "通称と価格が超大きい電光掲示板風"),
    (3, "hero-punch", "ヒーローパンチ", "ピカ超大＋下部に大文字メニュー"),
    (4, "price-wall", "プライスウォール", "価格数字が主役の壁面"),
    (5, "split-blast", "スプリットブラスト", "左に大ボトル、右に巨大メニュー"),
    (6, "neon-club", "ネオンスクラブ", "ネオン強め・遠目でも刺さる"),
    (7, "band", "バンド", "太い横帯で1行ずつ大きく"),
    (8, "center-stage", "センターステージ", "中央揃えの特大メニュー"),
]

SHARED = r"""
:root{
  --bg:#050303;--ink:#fff8ef;--muted:rgba(255,248,239,.75);--faint:rgba(255,248,239,.45);
  --gold:#e0b45a;--gold2:#ffe6a8;--hot:#ff6b6b;
  --serif:"Cormorant Garamond","Shippori Mincho",serif;
  --jp:"Shippori Mincho","Cormorant Garamond",serif;
  --sans:"Zen Kaku Gothic New",system-ui,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;height:100%;overflow:hidden;background:var(--bg);color:var(--ink);font-family:var(--jp);-webkit-font-smoothing:antialiased}
img{display:block;max-width:100%}
.back,.badge{position:fixed;z-index:100;font-family:var(--sans);font-size:11px;letter-spacing:.12em;text-decoration:none;color:rgba(255,248,239,.55);background:rgba(0,0,0,.45);backdrop-filter:blur(8px);border:1px solid rgba(224,180,90,.3);padding:.45rem .7rem}
.back{top:12px;left:12px}.badge{top:12px;right:12px;color:var(--gold2)}
body.shot .back,body.shot .badge,html.shot .back,html.shot .badge{display:none!important}
@media(max-width:800px){html,body{overflow:auto;height:auto;min-height:100%}}
"""

NAV = """
if (new URLSearchParams(location.search).get("shot") === "1") {
  document.documentElement.classList.add("shot");
  document.addEventListener("DOMContentLoaded", () => document.body.classList.add("shot"));
}
window.DESIGN_FILES = {
  1: "01-billboard.html",
  2: "02-scoreboard.html",
  3: "03-hero-punch.html",
  4: "04-price-wall.html",
  5: "05-split-blast.html",
  6: "06-neon-club.html",
  7: "07-band.html",
  8: "08-center-stage.html",
};
(() => {
  const file = location.pathname.split("/").pop() || "";
  const m = file.match(/^(\\d{2})-/);
  const n = m ? parseInt(m[1], 10) : 1;
  const total = Object.keys(window.DESIGN_FILES).length;
  const go = (t) => { const name = window.DESIGN_FILES[t]; if (name) location.href = name; };
  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight" || e.key === " ") { e.preventDefault(); go(n >= total ? 1 : n + 1); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); go(n <= 1 ? total : n - 1); }
    else if (e.key === "Escape" || e.key === "g" || e.key === "G") location.href = "../index.html";
  });
})();
"""

HEAD = """<!DOCTYPE html>
<html lang="ja"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Design {num:02d} — {title} | Tachibana</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,400&family=Shippori+Mincho:wght@600;700&family=Zen+Kaku+Gothic+New:wght@500;700&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="shared.css"/><link rel="stylesheet" href="{slug}.css"/>
</head><body class="d{num:02d}">
<a class="back" href="../index.html">← 一覧</a>
<div class="badge">DESIGN {num:02d} · {title}</div>
"""

FOOT = """
<script>if(new URLSearchParams(location.search).get("shot")==="1"){document.documentElement.classList.add("shot");document.addEventListener("DOMContentLoaded",()=>document.body.classList.add("shot"));}</script>
<script src="nav.js"></script>
</body></html>
"""


def rows_html(extra_class=""):
    parts = []
    for i, (nick, formal, en, price, key) in enumerate(ITEMS):
        feat = " is-hot" if i == 4 else ""
        parts.append(
            f'<div class="row{feat} {extra_class}">'
            f'<div class="left"><p class="nick">{nick}</p>'
            f'<p class="formal">モエ・エ・シャンドン {formal}</p></div>'
            f'<p class="price">{price}</p></div>'
        )
    return "\n".join(parts)


def write(num, slug, title, html_body, css):
    name = f"{num:02d}-{slug}"
    html = HEAD.format(num=num, title=title, slug=name) + html_body + FOOT
    (DESIGNS / f"{name}.html").write_text(html, encoding="utf-8")
    (DESIGNS / f"{name}.css").write_text(css, encoding="utf-8")
    print("wrote", name)


# 1 Billboard
write(1, "billboard", "ビルボード", f"""
<div class="stage">
  <img class="bg" src="../assets/moet/moet-bg.png" alt=""/>
  <div class="shade"></div>
  <img class="bot" src="../assets/moet/cut/pika.png" alt=""/>
  <div class="panel">
    <p class="maison">MOËT &amp; CHANDON</p>
    <h1>モエシリーズ</h1>
    <div class="list">{rows_html()}</div>
  </div>
</div>
""", """
.stage{position:relative;width:100%;height:100%}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.35) saturate(.9)}
.shade{position:absolute;inset:0;background:linear-gradient(100deg,rgba(5,3,3,.15),rgba(5,3,3,.75) 48%,rgba(5,3,3,.96) 68%)}
.bot{position:absolute;left:-2%;bottom:-8%;height:115%;z-index:1;filter:drop-shadow(0 0 60px rgba(255,100,60,.35))}
.panel{position:absolute;right:0;top:0;bottom:0;width:min(58vw,820px);z-index:2;padding:4vh 4vw 4vh 2vw;display:flex;flex-direction:column;justify-content:center}
.maison{font-family:var(--serif);letter-spacing:.45em;color:var(--gold);font-size:clamp(1rem,1.6vw,1.35rem);font-weight:600}
h1{font-size:clamp(3rem,6.5vw,5.5rem);letter-spacing:.18em;font-weight:700;line-height:1;margin:.4rem 0 3vh;text-shadow:0 10px 40px rgba(0,0,0,.5)}
.list{display:flex;flex-direction:column;gap:clamp(1rem,2.2vh,1.75rem)}
.row{display:flex;justify-content:space-between;align-items:flex-end;gap:1.5rem;border-bottom:2px solid rgba(224,180,90,.28);padding-bottom:clamp(.7rem,1.4vh,1.1rem)}
.nick{font-size:clamp(2rem,4.2vw,3.6rem);font-weight:700;letter-spacing:.12em;line-height:1.05}
.formal{margin-top:.35rem;font-size:clamp(1rem,1.6vw,1.35rem);color:var(--muted);letter-spacing:.06em}
.price{font-family:var(--serif);font-size:clamp(2.2rem,4.5vw,3.8rem);font-weight:700;color:var(--gold);white-space:nowrap;line-height:1}
.is-hot .nick,.is-hot .price{color:var(--gold2);text-shadow:0 0 24px rgba(255,180,80,.35)}
.is-hot{border-bottom-color:var(--gold2)}
""")

# 2 Scoreboard
write(2, "scoreboard", "スコアボード", f"""
<div class="stage">
  <header>
    <p class="maison">MOËT &amp; CHANDON</p>
    <h1>モエシリーズ</h1>
  </header>
  <div class="board">{rows_html()}</div>
</div>
""", """
.stage{width:100%;height:100%;padding:3vh 4vw;display:flex;flex-direction:column;background:#030201;
  background-image:radial-gradient(ellipse at 50% 0%,rgba(224,180,90,.18),transparent 55%)}
header{text-align:center;margin-bottom:2vh}
.maison{font-family:var(--serif);letter-spacing:.5em;color:var(--gold);font-size:clamp(1rem,1.5vw,1.3rem)}
h1{font-size:clamp(2.8rem,6vw,5rem);letter-spacing:.2em;font-weight:700;margin-top:.3rem}
.board{flex:1;display:flex;flex-direction:column;justify-content:center;gap:clamp(.6rem,1.5vh,1.2rem);max-width:1400px;margin:0 auto;width:100%}
.row{display:grid;grid-template-columns:1fr auto;align-items:center;gap:2rem;background:rgba(255,255,255,.03);
  border:1px solid rgba(224,180,90,.22);padding:clamp(1rem,2.2vh,1.8rem) clamp(1.2rem,3vw,2.5rem)}
.nick{font-size:clamp(2.4rem,5vw,4.2rem);font-weight:700;letter-spacing:.14em;line-height:1}
.formal{margin-top:.4rem;font-size:clamp(1.05rem,1.7vw,1.45rem);color:var(--muted)}
.price{font-family:var(--serif);font-size:clamp(2.6rem,5.5vw,4.6rem);font-weight:700;color:var(--gold);line-height:1}
.is-hot{background:rgba(224,180,90,.1);border-color:var(--gold2)}
.is-hot .nick,.is-hot .price{color:var(--gold2)}
""")

# 3 Hero punch
write(3, "hero-punch", "ヒーローパンチ", f"""
<div class="stage">
  <img class="hero" src="../assets/moet/cut/pika.png" alt=""/>
  <div class="veil"></div>
  <header>
    <p class="maison">MOËT &amp; CHANDON</p>
    <h1>モエシリーズ</h1>
  </header>
  <div class="dock">{rows_html()}</div>
</div>
""", """
.stage{position:relative;width:100%;height:100%;background:#050203}
.hero{position:absolute;left:50%;top:42%;transform:translate(-50%,-50%);height:95%;filter:drop-shadow(0 0 80px rgba(255,90,60,.45))}
.veil{position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,2,3,.7) 0%,transparent 28%,transparent 48%,rgba(5,2,3,.88) 72%,#050203 100%)}
header{position:absolute;top:3.5vh;left:0;right:0;text-align:center;z-index:2}
.maison{font-family:var(--serif);letter-spacing:.5em;color:var(--gold);font-size:clamp(1rem,1.5vw,1.25rem)}
h1{font-size:clamp(2.8rem,6vw,4.8rem);letter-spacing:.22em;font-weight:700;margin-top:.25rem;text-shadow:0 8px 30px rgba(0,0,0,.6)}
.dock{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:2vh 3vw 3.5vh;background:linear-gradient(180deg,transparent,rgba(5,2,3,.95))}
.list,.dock{display:grid;grid-template-columns:repeat(5,1fr);gap:1vw}
.row{text-align:center;padding:1vh .4vw}
.nick{font-size:clamp(1.5rem,2.8vw,2.5rem);font-weight:700;letter-spacing:.08em}
.formal{margin-top:.3rem;font-size:clamp(.85rem,1.2vw,1.1rem);color:var(--muted);line-height:1.35}
.price{margin-top:.55rem;font-family:var(--serif);font-size:clamp(1.8rem,3.2vw,2.9rem);font-weight:700;color:var(--gold)}
.is-hot .nick,.is-hot .price{color:#fff;text-shadow:0 0 20px rgba(255,120,80,.7)}
@media(max-width:900px){.dock{grid-template-columns:1fr 1fr}}
""")

# 4 Price wall
cards = "".join(
    f'<div class="card{" is-hot" if i==4 else ""}"><p class="price">{pr}</p><p class="nick">{n}</p><p class="formal">モエ・エ・シャンドン {fo}</p></div>'
    for i, (n, fo, _, pr, _) in enumerate(ITEMS)
)
write(4, "price-wall", "プライスウォール", f"""
<div class="stage">
  <header>
    <p class="maison">MOËT &amp; CHANDON</p>
    <h1>モエシリーズ</h1>
  </header>
  <div class="wall">{cards}</div>
</div>
""", """
.stage{width:100%;height:100%;padding:3.5vh 3vw;display:flex;flex-direction:column;background:#060403;
  background-image:radial-gradient(ellipse at 50% 120%,rgba(224,180,90,.2),transparent 50%)}
header{text-align:center;margin-bottom:2.5vh}
.maison{font-family:var(--serif);letter-spacing:.5em;color:var(--gold);font-size:clamp(1rem,1.5vw,1.3rem)}
h1{font-size:clamp(2.8rem,5.5vw,4.5rem);letter-spacing:.2em;font-weight:700;margin-top:.3rem}
.wall{flex:1;display:grid;grid-template-columns:repeat(5,1fr);gap:1.2vw;align-content:center}
.card{text-align:center;padding:3vh 1vw;border-top:3px solid rgba(224,180,90,.45)}
.price{font-family:var(--serif);font-size:clamp(2.2rem,4.8vw,4.2rem);font-weight:700;color:var(--gold);line-height:1}
.nick{margin-top:1.4rem;font-size:clamp(1.6rem,3vw,2.6rem);font-weight:700;letter-spacing:.12em}
.formal{margin-top:.55rem;font-size:clamp(.95rem,1.4vw,1.25rem);color:var(--muted);line-height:1.4;padding:0 .3vw}
.is-hot{border-top-color:var(--gold2);background:rgba(224,180,90,.08)}
.is-hot .price,.is-hot .nick{color:var(--gold2)}
@media(max-width:900px){.wall{grid-template-columns:1fr 1fr}}
""")

# 5 Split blast
write(5, "split-blast", "スプリットブラスト", f"""
<div class="stage">
  <div class="visual">
    <img class="b1" src="../assets/moet/cut/ice.png" alt=""/>
    <img class="b2" src="../assets/moet/cut/pika.png" alt=""/>
  </div>
  <div class="menu">
    <p class="maison">MOËT &amp; CHANDON</p>
    <h1>モエ<br/>シリーズ</h1>
    <div class="list">{rows_html()}</div>
  </div>
</div>
""", """
.stage{display:grid;grid-template-columns:1.05fr 1fr;height:100%;background:#070403}
.visual{position:relative;overflow:hidden;background:radial-gradient(ellipse at 40% 60%,rgba(224,180,90,.2),transparent 55%),#0c0806}
.b1{position:absolute;left:2%;bottom:-5%;height:85%;opacity:.55;transform:rotate(-10deg);filter:brightness(.7)}
.b2{position:absolute;left:18%;bottom:-8%;height:105%;filter:drop-shadow(0 20px 50px rgba(0,0,0,.6))}
.menu{padding:4vh 3.5vw;display:flex;flex-direction:column;justify-content:center;background:linear-gradient(90deg,#120c09,#070403)}
.maison{font-family:var(--serif);letter-spacing:.45em;color:var(--gold);font-size:clamp(1rem,1.4vw,1.25rem)}
h1{font-size:clamp(3rem,6vw,5.2rem);letter-spacing:.14em;font-weight:700;line-height:.95;margin:.5rem 0 3vh}
.list{display:flex;flex-direction:column;gap:clamp(.9rem,2vh,1.5rem)}
.row{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;border-bottom:2px solid rgba(224,180,90,.25);padding-bottom:.75rem}
.nick{font-size:clamp(1.9rem,3.6vw,3.1rem);font-weight:700;letter-spacing:.1em}
.formal{margin-top:.3rem;font-size:clamp(1rem,1.5vw,1.3rem);color:var(--muted)}
.price{font-family:var(--serif);font-size:clamp(2rem,3.8vw,3.3rem);font-weight:700;color:var(--gold)}
.is-hot .nick,.is-hot .price{color:var(--gold2)}
@media(max-width:900px){.stage{grid-template-columns:1fr}.visual{min-height:40vh}}
""")

# 6 Neon club
write(6, "neon-club", "ネオンスクラブ", f"""
<div class="stage">
  <div class="glow"></div>
  <img class="hero" src="../assets/moet/cut/pika.png" alt=""/>
  <div class="panel">
    <p class="maison">NIGHT IMPACT</p>
    <h1>モエシリーズ</h1>
    <div class="list">{rows_html()}</div>
  </div>
</div>
""", """
.stage{position:relative;width:100%;height:100%;background:#02010a;overflow:hidden}
.glow{position:absolute;right:5%;top:10%;width:55vw;height:55vw;background:radial-gradient(circle,rgba(255,60,100,.35),rgba(255,120,40,.12),transparent 70%);filter:blur(8px)}
.hero{position:absolute;right:-8%;bottom:-10%;height:115%;transform:rotate(6deg);filter:drop-shadow(0 0 50px rgba(255,80,100,.5))}
.panel{position:absolute;left:0;top:0;bottom:0;width:min(56vw,780px);padding:5vh 3.5vw;display:flex;flex-direction:column;justify-content:center;
  background:linear-gradient(90deg,rgba(2,1,10,.97) 70%,transparent)}
.maison{font-family:var(--sans);letter-spacing:.4em;color:#ff7a9a;font-size:clamp(1rem,1.4vw,1.2rem);font-weight:700}
h1{font-size:clamp(3rem,6vw,5rem);letter-spacing:.16em;font-weight:700;margin:.4rem 0 3vh;text-shadow:0 0 40px rgba(255,80,120,.35)}
.list{display:flex;flex-direction:column;gap:clamp(.85rem,1.8vh,1.4rem)}
.row{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;border-bottom:2px solid rgba(255,100,130,.25);padding-bottom:.7rem}
.nick{font-size:clamp(1.9rem,3.5vw,3rem);font-weight:700;letter-spacing:.1em}
.formal{margin-top:.3rem;font-size:clamp(1rem,1.45vw,1.25rem);color:var(--muted)}
.price{font-family:var(--serif);font-size:clamp(2rem,3.8vw,3.2rem);font-weight:700;color:#ffc4a8}
.is-hot .nick,.is-hot .price{color:#fff;text-shadow:0 0 18px rgba(255,100,120,.75)}
.is-hot{border-bottom-color:#ff6b8a}
""")

# 7 Band
bands = "".join(
    f'<div class="band{" is-hot" if i==4 else ""}"><p class="nick">{n}</p><p class="formal">モエ・エ・シャンドン {fo}</p><p class="price">{pr}</p></div>'
    for i, (n, fo, _, pr, _) in enumerate(ITEMS)
)
write(7, "band", "バンド", f"""
<div class="stage">
  <header>
    <p class="maison">MOËT &amp; CHANDON</p>
    <h1>モエシリーズ</h1>
  </header>
  <div class="bands">{bands}</div>
</div>
""", """
.stage{width:100%;height:100%;display:flex;flex-direction:column;background:#040303}
header{padding:2.5vh 4vw 1.5vh;text-align:center;flex-shrink:0}
.maison{font-family:var(--serif);letter-spacing:.5em;color:var(--gold);font-size:clamp(1rem,1.4vw,1.2rem)}
h1{font-size:clamp(2.4rem,5vw,4rem);letter-spacing:.2em;font-weight:700;margin-top:.2rem}
.bands{flex:1;display:flex;flex-direction:column}
.band{flex:1;display:grid;grid-template-columns:1.1fr 1.4fr auto;align-items:center;gap:2vw;
  padding:0 4vw;border-top:1px solid rgba(224,180,90,.2);
  background:linear-gradient(90deg,rgba(224,180,90,.04),transparent 40%)}
.band:nth-child(even){background:linear-gradient(90deg,rgba(255,255,255,.03),transparent 45%)}
.nick{font-size:clamp(2.2rem,4.5vw,3.8rem);font-weight:700;letter-spacing:.12em}
.formal{font-size:clamp(1.1rem,1.8vw,1.55rem);color:var(--muted);letter-spacing:.06em}
.price{font-family:var(--serif);font-size:clamp(2.4rem,5vw,4.2rem);font-weight:700;color:var(--gold);justify-self:end}
.is-hot{background:linear-gradient(90deg,rgba(224,180,90,.16),rgba(224,180,90,.04))!important;border-top-color:var(--gold2)}
.is-hot .nick,.is-hot .price{color:var(--gold2)}
@media(max-width:900px){.band{grid-template-columns:1fr;padding:1rem 1.2rem;gap:.2rem}}
""")

# 8 Center stage
write(8, "center-stage", "センターステージ", f"""
<div class="stage">
  <img class="wm" src="../assets/moet/cut/nectar.png" alt=""/>
  <div class="wrap">
    <p class="maison">MOËT &amp; CHANDON</p>
    <h1>モエシリーズ</h1>
    <p class="lead">今夜を祝う、5つの表情。</p>
    <div class="list">{rows_html()}</div>
  </div>
</div>
""", """
.stage{position:relative;width:100%;height:100%;background:#080504}
.wm{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);height:120%;opacity:.12;filter:grayscale(.2)}
.wrap{position:relative;z-index:1;height:100%;max-width:1100px;margin:0 auto;padding:4vh 4vw;display:flex;flex-direction:column;justify-content:center;text-align:center}
.maison{font-family:var(--serif);letter-spacing:.5em;color:var(--gold);font-size:clamp(1rem,1.5vw,1.3rem)}
h1{font-size:clamp(3.2rem,7vw,5.8rem);letter-spacing:.2em;font-weight:700;margin:.35rem 0 .5rem}
.lead{font-size:clamp(1.1rem,1.8vw,1.5rem);letter-spacing:.2em;color:var(--muted);margin-bottom:3.5vh}
.list{display:flex;flex-direction:column;gap:clamp(1rem,2vh,1.6rem)}
.row{display:grid;grid-template-columns:1fr auto;align-items:end;gap:2rem;text-align:left;
  border-bottom:2px solid rgba(224,180,90,.28);padding-bottom:.85rem}
.nick{font-size:clamp(2.2rem,4.2vw,3.5rem);font-weight:700;letter-spacing:.14em}
.formal{margin-top:.35rem;font-size:clamp(1.05rem,1.6vw,1.4rem);color:var(--muted)}
.price{font-family:var(--serif);font-size:clamp(2.4rem,4.6vw,3.9rem);font-weight:700;color:var(--gold)}
.is-hot .nick,.is-hot .price{color:var(--gold2)}
.is-hot{border-bottom-color:var(--gold2)}
""")


# Gallery index
cards = []
for num, slug, title, desc in META:
    cards.append(
        f'<a class="card" href="#d{num:02d}"><span class="num">{num:02d}</span><strong>{title}</strong><span class="desc">{desc}</span></a>'
    )

blocks = []
for num, slug, title, desc in META:
    blocks.append(
        f'<section class="block" id="d{num:02d}"><h2>{num:02d} · {title}</h2>'
        f'<p class="desc">{desc}</p>'
        f'<img src="previews/phone/{num:02d}-{slug}.jpg" alt="Design {num:02d}"/>'
        f'<p class="open"><a href="designs/{num:02d}-{slug}.html">全画面で見る</a></p></section>'
    )

index = f"""<!DOCTYPE html>
<html lang="ja"><head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>モエシリーズ 新デザイン案（インパクト版）</title>
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@600;700&family=Zen+Kaku+Gothic+New:wght@400;500&display=swap" rel="stylesheet"/>
<style>
:root{{--bg:#0a0806;--ink:#fff8ef;--gold:#e0b45a;--muted:rgba(255,248,239,.65)}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--ink);font-family:"Zen Kaku Gothic New",system-ui,sans-serif}}
header{{padding:1.2rem 1rem;position:sticky;top:0;z-index:10;background:rgba(10,8,6,.94);backdrop-filter:blur(10px);border-bottom:1px solid rgba(224,180,90,.3)}}
.eyebrow{{font-size:.7rem;letter-spacing:.28em;color:var(--gold)}}
h1{{font-family:"Shippori Mincho",serif;font-size:1.35rem;letter-spacing:.1em;margin:.35rem 0}}
.sub{{font-size:.85rem;color:var(--muted);line-height:1.65}}
.jump{{display:flex;gap:.4rem;overflow-x:auto;padding:.7rem 1rem;border-bottom:1px solid rgba(255,255,255,.06)}}
.jump a{{flex:0 0 auto;padding:.35rem .7rem;border:1px solid rgba(224,180,90,.4);color:var(--gold);text-decoration:none;border-radius:999px;font-size:.8rem}}
.block{{scroll-margin-top:6.5rem;padding:1.1rem 1rem 0}}
.block h2{{font-family:"Shippori Mincho",serif;font-size:1.1rem;letter-spacing:.08em;color:var(--gold)}}
.block .desc{{font-size:.8rem;color:var(--muted);margin:.35rem 0 .7rem}}
.block img{{width:100%;height:auto;border:1px solid rgba(224,180,90,.25);display:block;background:#111}}
.open{{margin:.55rem 0 0;font-size:.8rem}}
.open a{{color:var(--gold)}}
.note{{padding:1.2rem 1rem 2.5rem;font-size:.85rem;color:var(--muted);line-height:1.7}}
</style></head><body>
<header>
  <p class="eyebrow">REDESIGN · HIGH IMPACT</p>
  <h1>モエシリーズ 新デザイン案</h1>
  <p class="sub">遠目でも読める大文字＋インパクト重視で作り直しました（全8案）。下にスクロールして確認し、番号を送ってください。</p>
</header>
<nav class="jump">
  <a href="#d01">01</a><a href="#d02">02</a><a href="#d03">03</a><a href="#d04">04</a>
  <a href="#d05">05</a><a href="#d06">06</a><a href="#d07">07</a><a href="#d08">08</a>
</nav>
<main>
{''.join(blocks)}
<p class="note">気に入った番号を送ってください。決まったら本番用PNGスライドショーにします。</p>
</main>
</body></html>
"""
(ROOT / "index.html").write_text(index, encoding="utf-8")
(DESIGNS / "shared.css").write_text(SHARED, encoding="utf-8")
(DESIGNS / "nav.js").write_text(NAV, encoding="utf-8")
(ROOT / "README.md").write_text(
    """# Tachibana — モエシリーズ（インパクト版）

遠目でも読める大文字・高インパクトのデザイン案（8種）。

## 確認
`index.html` を開き、下にスクロール（スマホ向け画像一覧）。

## 案
01 ビルボード / 02 スコアボード / 03 ヒーローパンチ / 04 プライスウォール
05 スプリットブラスト / 06 ネオンスクラブ / 07 バンド / 08 センターステージ
""",
    encoding="utf-8",
)
print("done", len(META), "designs")
