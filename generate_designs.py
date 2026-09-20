#!/usr/bin/env python3
"""Generate 21 Moët series design variants + review gallery."""
from pathlib import Path

ROOT = Path("/workspace")
DESIGNS = ROOT / "designs"
DESIGNS.mkdir(exist_ok=True)

ITEMS = [
    ("モエシロ", "モエ・エ・シャンドン ブリュット アンペリアル", "Brut Impérial", "¥20,000", "brut"),
    ("モエロゼ", "モエ・エ・シャンドン ロゼ アンペリアル", "Rosé Impérial", "¥25,000", "rose"),
    ("モエ黒", "モエ・エ・シャンドン ネクター アンペリアル", "Nectar Impérial", "¥30,000", "nectar"),
    ("モエアイス", "モエ・エ・シャンドン アイス アンペリアル", "Ice Impérial", "¥35,000", "ice"),
    ("モエピカ", "モエ・エ・シャンドン ネクター アンペリアル ロゼ ドライ", "N.I.R · Nectar Impérial Rosé Dry", "¥40,000", "pika"),
]

META = [
    (1, "winelist", "ワインリスト", "左にボトル、右に価格表のエディトリアル"),
    (2, "hero-nir", "ヒーローNIR", "ピカを全面に、下に価格オーバーレイ"),
    (3, "type-poster", "タイポポスター", "巨大文字が主役、ボトルは透かし"),
    (4, "art-deco", "アールデコ", "幾何学フレームと中央リスト"),
    (5, "spotlight", "スポットライト", "中央に1本、左右に価格"),
    (6, "filmstrip", "フィルムストリップ", "縦に5本を帯状、横にリスト"),
    (7, "cascade", "カスケード", "斜めに階段状のボトル配置"),
    (8, "gold-plate", "ゴールドプレート", "銘板メニュー風の中央パネル"),
    (9, "luminous", "ルミナス", "ネオン感のあるナイトライフ"),
    (10, "price-hero", "プライスヒーロー", "価格の数字を大きく見せる"),
    (11, "mirror", "ミラーフロア", "反射床の演出と立ちボトル"),
    (12, "glass-panel", "ガラスパネル", "半透明パネルにメニュー"),
    (13, "tate-gaki", "縦書きアクセント", "和の縦書きとボトル"),
    (14, "club-led", "クラブLED", "LEDバーとダーククラブ感"),
    (15, "silk", "シルク", "柔らかい光と浮动リスト"),
    (16, "brutal", "ブルータル", "極端なトリミングと大文字"),
    (17, "ornate-frame", "オーネイトフレーム", "金の二重枠と余白"),
    (18, "diptych", "ディプティク", "アイスとピカの二面、中央リスト"),
    (19, "ledger", "レジャー", "表形式の上品な料金表"),
    (20, "orbit", "オービット", "円弧にボトル、中央にタイトル"),
    (21, "manifesto", "マニフェスト", "宣言文ポスター＋透かしボトル"),
]

HEAD = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Design {num:02d} — {title} | Tachibana</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Shippori+Mincho:wght@400;600;700&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="shared.css"/>
<link rel="stylesheet" href="{slug}.css"/>
</head>
<body class="d{num:02d}">
<a class="back" href="../index.html">← ギャラリー</a>
<div class="badge">DESIGN {num:02d} · {title}</div>
"""

FOOT = """
<script src="nav.js"></script>
</body></html>
"""

SHARED_CSS = r"""
:root{
  --bg:#070504;--ink:#f6eee3;--muted:rgba(246,238,227,.68);--faint:rgba(246,238,227,.4);
  --gold:#c9a15d;--gold2:#edd6a4;--rose:#c47a7a;
  --serif:"Cormorant Garamond","Shippori Mincho",serif;
  --jp:"Shippori Mincho","Cormorant Garamond",serif;
  --sans:"Zen Kaku Gothic New",system-ui,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;height:100%;overflow:hidden;background:var(--bg);color:var(--ink);font-family:var(--jp);-webkit-font-smoothing:antialiased}
img{display:block;max-width:100%}
.back,.badge{position:fixed;z-index:100;font-family:var(--sans);font-size:11px;letter-spacing:.12em;text-decoration:none;color:rgba(246,238,227,.55);background:rgba(0,0,0,.45);backdrop-filter:blur(8px);border:1px solid rgba(201,161,93,.25);padding:.45rem .7rem}
.back{top:12px;left:12px}
.badge{top:12px;right:12px;color:var(--gold2)}
.back:hover{color:var(--gold2)}
@media (max-width:800px){
  html,body{overflow:auto;height:auto;min-height:100%}
}
"""

NAV_JS = r"""
(() => {
  const params = new URLSearchParams(location.search);
  const m = location.pathname.match(/(\d{2})-/);
  const n = m ? parseInt(m[1], 10) : 1;
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ') {
      e.preventDefault();
      const next = n >= 21 ? 1 : n + 1;
      location.href = location.pathname.replace(/\d{2}-[^/]+\.html/, String(next).padStart(2,'0') + '-' + (window.DESIGN_SLUGS||{})[next] + '.html');
    }
    if (e.key === 'ArrowLeft') {
      e.preventDefault();
      const prev = n <= 1 ? 21 : n - 1;
      location.href = location.pathname.replace(/\d{2}-[^/]+\.html/, String(prev).padStart(2,'0') + '-' + (window.DESIGN_SLUGS||{})[prev] + '.html');
    }
    if (e.key === 'Escape') location.href = '../index.html';
    if (e.key === 'g' || e.key === 'G') location.href = '../index.html';
  });
})();
"""

# Better nav with embedded slug map
def nav_js():
    slugs = {num: slug for num, slug, *_ in META}
    return f"window.DESIGN_SLUGS = {slugs};\n" + NAV_JS


def list_rows(feature_last=True, cls="row"):
    rows = []
    for i, (nick, formal, en, price, key) in enumerate(ITEMS):
        feat = " is-feature" if feature_last and i == 4 else ""
        rows.append(
            f'<div class="{cls}{feat}">'
            f'<div class="copy"><p class="nick">{nick}</p>'
            f'<p class="formal">{formal}</p><p class="en">{en}</p></div>'
            f'<span class="rule"></span><p class="price">{price}</p></div>'
        )
    return "\n".join(rows)


def bottle_imgs(keys, cls_prefix="b"):
    out = []
    for i, k in enumerate(keys):
        out.append(f'<img class="{cls_prefix} {cls_prefix}--{i+1}" src="../assets/moet/cut/{k}.png" alt=""/>')
    return "\n".join(out)


# —— Per-design HTML + CSS ——

def d01():
    html = HEAD.format(num=1, title="ワインリスト", slug="01-winelist") + f"""
<div class="stage">
  <img class="bg" src="../assets/moet/moet-bg.png" alt=""/>
  <div class="shade"></div>
  <div class="drama">{bottle_imgs(['rose','ice','pika'], 'bot')}</div>
  <div class="sheet">
    <p class="maison">MOËT &amp; CHANDON</p>
    <h1>モエシリーズ</h1>
    <p class="lead">今夜を祝う、5つの表情。</p>
    <div class="list">{list_rows()}</div>
  </div>
</div>
""" + FOOT
    css = """
.stage{position:relative;width:100%;height:100%}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.55) saturate(.85)}
.shade{position:absolute;inset:0;background:linear-gradient(105deg,rgba(7,5,4,.15) 0%,rgba(7,5,4,.55) 40%,rgba(7,5,4,.92) 65%,#070504 100%)}
.drama{position:absolute;left:-2%;top:0;bottom:0;width:50vw;z-index:2}
.bot{position:absolute;object-fit:contain;bottom:0;filter:drop-shadow(0 30px 50px rgba(0,0,0,.7))}
.bot--1{width:32vw;max-width:300px;left:0;bottom:6%;opacity:.55;transform:rotate(-8deg)}
.bot--2{width:38vw;max-width:360px;left:10%;bottom:3%;opacity:.85;transform:rotate(4deg)}
.bot--3{width:46vw;max-width:460px;left:22%;bottom:-3%;transform:rotate(-2deg)}
.sheet{position:absolute;right:0;top:0;bottom:0;width:min(54vw,760px);z-index:3;display:flex;flex-direction:column;justify-content:center;padding:4vh 4vw 4vh 2vw}
.maison{font-family:var(--serif);letter-spacing:.5em;color:var(--gold);font-size:.85rem;margin-bottom:.6rem}
h1{font-size:clamp(2.4rem,5.5vw,4.2rem);letter-spacing:.22em;font-weight:600}
.lead{margin:.7rem 0 2rem;color:var(--faint);letter-spacing:.18em}
.list{display:flex;flex-direction:column;gap:1.1rem}
.row{display:grid;grid-template-columns:1fr minmax(2rem,1fr) auto;align-items:end;gap:.7rem}
.nick{font-size:clamp(1.1rem,2vw,1.55rem);letter-spacing:.14em;font-weight:600}
.formal{font-size:.78rem;color:var(--muted);margin-top:.15rem}
.en{font-family:var(--serif);font-style:italic;font-size:.82rem;color:var(--faint)}
.rule{border-bottom:1px dotted rgba(201,161,93,.35);transform:translateY(-.5em)}
.price{font-family:var(--serif);font-size:clamp(1.2rem,2.2vw,1.8rem);color:var(--gold);font-weight:600}
.is-feature .nick,.is-feature .price{color:var(--gold2)}
"""
    return "01-winelist", html, css


def d02():
    html = HEAD.format(num=2, title="ヒーローNIR", slug="02-hero-nir") + f"""
<div class="stage">
  <img class="hero" src="../assets/moet/cut/pika.png" alt=""/>
  <div class="veil"></div>
  <header>
    <p class="maison">MOËT &amp; CHANDON</p>
    <h1>モエシリーズ</h1>
  </header>
  <div class="bar">
    <div class="list">{list_rows(cls="row")}</div>
  </div>
</div>
""" + FOOT
    css = """
.stage{position:relative;width:100%;height:100%;background:#050303}
.hero{position:absolute;left:50%;bottom:-8%;transform:translateX(-50%);height:115%;width:auto;max-width:none;filter:drop-shadow(0 0 80px rgba(201,100,80,.35))}
.veil{position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,3,3,.55) 0%,transparent 35%,transparent 50%,rgba(5,3,3,.85) 78%,#050303 100%)}
header{position:absolute;top:8vh;left:0;right:0;text-align:center;z-index:2}
.maison{font-family:var(--serif);letter-spacing:.5em;color:var(--gold);font-size:.85rem}
h1{font-size:clamp(2.2rem,5vw,3.8rem);letter-spacing:.28em;margin-top:.5rem}
.bar{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:2vh 4vw 4vh;background:linear-gradient(180deg,transparent,rgba(5,3,3,.92))}
.list{display:grid;grid-template-columns:repeat(5,1fr);gap:1rem;max-width:1200px;margin:0 auto}
.row{text-align:center;display:flex;flex-direction:column;gap:.2rem}
.rule{display:none}
.nick{font-size:1rem;letter-spacing:.12em;color:var(--gold2)}
.formal{font-size:.65rem;color:var(--muted);line-height:1.4}
.en{font-family:var(--serif);font-style:italic;font-size:.7rem;color:var(--faint)}
.price{font-family:var(--serif);font-size:1.35rem;color:var(--gold);margin-top:.35rem}
.is-feature .price{color:#fff;text-shadow:0 0 20px rgba(255,120,100,.5)}
@media(max-width:800px){.list{grid-template-columns:1fr 1fr;}.row:last-child{grid-column:1/-1}}
"""
    return "02-hero-nir", html, css


def d03():
    html = HEAD.format(num=3, title="タイポポスター", slug="03-type-poster") + f"""
<div class="stage">
  <img class="wm" src="../assets/moet/cut/ice.png" alt=""/>
  <div class="content">
    <p class="maison">MOËT &amp; CHANDON</p>
    <h1>モエ<br/>シリーズ</h1>
    <div class="list">{list_rows()}</div>
  </div>
</div>
""" + FOOT
    css = """
.stage{position:relative;width:100%;height:100%;background:#0a0807}
.wm{position:absolute;right:-8%;bottom:-10%;height:120%;opacity:.18;filter:grayscale(.2)}
.content{position:relative;z-index:2;height:100%;display:flex;flex-direction:column;justify-content:center;padding:6vh 8vw;max-width:920px}
.maison{font-family:var(--serif);letter-spacing:.55em;color:var(--gold);font-size:.8rem}
h1{font-size:clamp(3.5rem,10vw,8rem);line-height:.95;letter-spacing:.12em;font-weight:700;margin:1rem 0 2.5rem}
.list{display:flex;flex-direction:column;gap:1rem;max-width:640px}
.row{display:flex;justify-content:space-between;align-items:baseline;gap:1.5rem;border-bottom:1px solid rgba(201,161,93,.2);padding-bottom:.75rem}
.rule{display:none}
.nick{font-size:1.35rem;letter-spacing:.16em}
.formal,.en{display:none}
.price{font-family:var(--serif);font-size:1.6rem;color:var(--gold)}
.is-feature .nick,.is-feature .price{color:var(--gold2)}
"""
    return "03-type-poster", html, css


def d04():
    html = HEAD.format(num=4, title="アールデコ", slug="04-art-deco") + f"""
<div class="stage">
  <div class="frame">
    <div class="inner">
      <p class="maison">MOËT &amp; CHANDON · ÉPERNAY</p>
      <div class="orn">◆</div>
      <h1>モエシリーズ</h1>
      <div class="orn">◆</div>
      <div class="list">{list_rows()}</div>
    </div>
  </div>
</div>
""" + FOOT
    css = """
.stage{width:100%;height:100%;display:grid;place-items:center;background:
  radial-gradient(ellipse at center, #1a120c 0%, #070504 70%),
  repeating-linear-gradient(90deg, transparent, transparent 80px, rgba(201,161,93,.03) 80px, rgba(201,161,93,.03) 81px)}
.frame{width:min(720px,88vw);border:1px solid var(--gold);padding:10px;box-shadow:0 0 0 1px rgba(201,161,93,.25) inset}
.inner{border:1px solid rgba(201,161,93,.45);padding:clamp(1.5rem,4vw,3rem);text-align:center}
.maison{font-family:var(--serif);letter-spacing:.4em;color:var(--gold);font-size:.75rem}
.orn{color:var(--gold);margin:.8rem 0;letter-spacing:.5em;opacity:.7}
h1{font-size:clamp(2rem,4.5vw,3.2rem);letter-spacing:.35em;font-weight:600}
.list{margin-top:1.5rem;text-align:left;display:flex;flex-direction:column;gap:.85rem}
.row{display:grid;grid-template-columns:1fr auto;gap:1rem;align-items:end;border-bottom:1px solid rgba(201,161,93,.2);padding-bottom:.6rem}
.rule{display:none}
.nick{font-size:1.15rem;letter-spacing:.14em}
.formal{font-size:.72rem;color:var(--muted)}
.en{font-family:var(--serif);font-style:italic;font-size:.75rem;color:var(--faint)}
.price{font-family:var(--serif);font-size:1.4rem;color:var(--gold)}
"""
    return "04-art-deco", html, css


def d05():
    prices_l = "".join(f'<div class="p"><span>{n}</span><b>{pr}</b></div>' for n,_,_,pr,_ in ITEMS[:2])
    prices_r = "".join(f'<div class="p"><span>{n}</span><b>{pr}</b></div>' for n,_,_,pr,_ in ITEMS[3:])
    mid = ITEMS[2]
    html = HEAD.format(num=5, title="スポットライト", slug="05-spotlight") + f"""
<div class="stage">
  <div class="spot"></div>
  <img class="center" src="../assets/moet/cut/nectar.png" alt=""/>
  <div class="side side--l">{prices_l}<div class="p is-mid"><span>{mid[0]}</span><b>{mid[3]}</b><small>{mid[2]}</small></div></div>
  <div class="side side--r">{prices_r}</div>
  <header><p class="maison">MOËT &amp; CHANDON</p><h1>モエシリーズ</h1></header>
</div>
""" + FOOT
    css = """
.stage{position:relative;width:100%;height:100%;background:#050303}
.spot{position:absolute;left:50%;top:40%;transform:translate(-50%,-50%);width:55vw;height:55vw;max-width:700px;max-height:700px;border-radius:50%;background:radial-gradient(circle,rgba(201,161,93,.28),transparent 65%);pointer-events:none}
.center{position:absolute;left:50%;bottom:0;transform:translateX(-50%);height:88%;z-index:2;filter:drop-shadow(0 20px 60px rgba(0,0,0,.8))}
header{position:absolute;top:5vh;left:0;right:0;text-align:center;z-index:3}
.maison{font-family:var(--serif);letter-spacing:.5em;color:var(--gold);font-size:.8rem}
h1{font-size:clamp(1.8rem,4vw,3rem);letter-spacing:.28em;margin-top:.4rem}
.side{position:absolute;top:50%;transform:translateY(-50%);z-index:3;display:flex;flex-direction:column;gap:1.75rem}
.side--l{left:5vw}.side--r{right:5vw;text-align:right}
.p span{display:block;letter-spacing:.14em;font-size:1.05rem;margin-bottom:.2rem}
.p b{font-family:var(--serif);font-size:1.5rem;color:var(--gold);font-weight:600}
.p small{display:block;font-family:var(--serif);font-style:italic;color:var(--faint);font-size:.75rem;margin-top:.15rem}
.is-mid{margin:1rem 0;padding:1rem 0;border-top:1px solid rgba(201,161,93,.3);border-bottom:1px solid rgba(201,161,93,.3)}
"""
    return "05-spotlight", html, css


def d06():
    strip = "".join(
        f'<div class="cell"><img src="../assets/moet/cut/{k}.png" alt=""/><p>{n}</p></div>'
        for n,_,_,_,k in ITEMS
    )
    html = HEAD.format(num=6, title="フィルムストリップ", slug="06-filmstrip") + f"""
<div class="stage">
  <div class="strip">{strip}</div>
  <div class="panel">
    <p class="maison">MOËT &amp; CHANDON</p>
    <h1>モエシリーズ</h1>
    <div class="list">{list_rows()}</div>
  </div>
</div>
""" + FOOT
    css = """
.stage{display:grid;grid-template-columns:140px 1fr;height:100%;background:#0b0908}
.strip{background:#111;border-right:1px solid rgba(201,161,93,.25);display:flex;flex-direction:column;justify-content:space-evenly;padding:.5rem 0;overflow:hidden}
.cell{text-align:center;padding:.35rem}
.cell img{height:14vh;margin:0 auto;filter:drop-shadow(0 8px 16px rgba(0,0,0,.5))}
.cell p{font-size:.65rem;letter-spacing:.1em;color:var(--gold);margin-top:.25rem}
.panel{padding:6vh 5vw;display:flex;flex-direction:column;justify-content:center;background:linear-gradient(90deg,#120e0c,#0b0908)}
.maison{font-family:var(--serif);letter-spacing:.5em;color:var(--gold);font-size:.8rem}
h1{font-size:clamp(2rem,4.5vw,3.5rem);letter-spacing:.22em;margin:.5rem 0 2rem}
.list{display:flex;flex-direction:column;gap:1rem;max-width:640px}
.row{display:grid;grid-template-columns:1fr auto;gap:1rem;align-items:end;border-bottom:1px solid rgba(255,255,255,.08);padding-bottom:.7rem}
.rule{display:none}
.nick{font-size:1.2rem;letter-spacing:.12em}
.formal{font-size:.72rem;color:var(--muted)}
.en{font-family:var(--serif);font-style:italic;font-size:.75rem;color:var(--faint)}
.price{font-family:var(--serif);font-size:1.45rem;color:var(--gold)}
@media(max-width:800px){.stage{grid-template-columns:1fr}.strip{flex-direction:row;border:none;border-bottom:1px solid rgba(201,161,93,.25)}.cell img{height:10vh}}
"""
    return "06-filmstrip", html, css


def d07():
    bots = bottle_imgs(['brut','rose','nectar','ice','pika'], 'c')
    html = HEAD.format(num=7, title="カスケード", slug="07-cascade") + f"""
<div class="stage">
  <img class="bg" src="../assets/moet/moet-bg.png" alt=""/>
  <div class="cascade">{bots}</div>
  <div class="rail">
    <p class="maison">MOËT &amp; CHANDON</p>
    <h1>モエシリーズ</h1>
    <div class="list">{list_rows()}</div>
  </div>
</div>
""" + FOOT
    css = """
.stage{position:relative;width:100%;height:100%}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.4)}
.cascade{position:absolute;left:0;right:40%;top:0;bottom:0;z-index:2}
.c{position:absolute;height:55vh;object-fit:contain;filter:drop-shadow(0 20px 40px rgba(0,0,0,.6))}
.c--1{left:2%;top:8%;transform:rotate(-12deg);opacity:.7}
.c--2{left:12%;top:18%;transform:rotate(-6deg);opacity:.8}
.c--3{left:22%;top:28%;transform:rotate(0)}
.c--4{left:32%;top:38%;transform:rotate(5deg)}
.c--5{left:42%;top:48%;transform:rotate(10deg);height:60vh}
.rail{position:absolute;right:0;top:0;bottom:0;width:min(42vw,560px);z-index:3;padding:5vh 3vw;display:flex;flex-direction:column;justify-content:center;background:rgba(7,5,4,.72);backdrop-filter:blur(6px)}
.maison{font-family:var(--serif);letter-spacing:.45em;color:var(--gold);font-size:.75rem}
h1{font-size:clamp(1.8rem,3.5vw,2.8rem);letter-spacing:.2em;margin:.5rem 0 1.5rem}
.list{display:flex;flex-direction:column;gap:.8rem}
.row{display:flex;justify-content:space-between;gap:1rem;align-items:baseline}
.rule,.formal,.en{display:none}
.nick{font-size:1rem;letter-spacing:.1em}
.price{font-family:var(--serif);color:var(--gold);font-size:1.2rem}
.is-feature .nick,.is-feature .price{color:var(--gold2)}
"""
    return "07-cascade", html, css


def d08():
    html = HEAD.format(num=8, title="ゴールドプレート", slug="08-gold-plate") + f"""
<div class="stage">
  <div class="plate">
    <p class="maison">CHAMPAGNE · MOËT &amp; CHANDON</p>
    <h1>モエシリーズ</h1>
    <div class="line"></div>
    <div class="list">{list_rows()}</div>
  </div>
</div>
""" + FOOT
    css = """
.stage{width:100%;height:100%;display:grid;place-items:center;background:#1a100a;
  background-image:radial-gradient(ellipse at 50% 0%, rgba(201,161,93,.15), transparent 50%)}
.plate{width:min(680px,90vw);background:linear-gradient(160deg,#2a1e14,#16100c 45%,#1c140e);
  border:1px solid rgba(201,161,93,.55);box-shadow:0 30px 80px rgba(0,0,0,.55), inset 0 1px 0 rgba(237,214,164,.2);
  padding:clamp(2rem,5vw,3.5rem);border-radius:2px}
.maison{font-family:var(--serif);text-align:center;letter-spacing:.35em;color:var(--gold);font-size:.72rem}
h1{text-align:center;font-size:clamp(2rem,4vw,3rem);letter-spacing:.28em;margin:.8rem 0}
.line{height:1px;background:linear-gradient(90deg,transparent,var(--gold),transparent);margin:0 auto 1.75rem;width:60%}
.list{display:flex;flex-direction:column;gap:1rem}
.row{display:grid;grid-template-columns:1fr auto;align-items:end;gap:1rem}
.rule{display:none}
.nick{font-size:1.15rem;letter-spacing:.12em}
.formal{font-size:.7rem;color:var(--muted)}
.en{font-family:var(--serif);font-style:italic;font-size:.72rem;color:var(--faint)}
.price{font-family:var(--serif);font-size:1.45rem;color:var(--gold2)}
"""
    return "08-gold-plate", html, css


def d09():
    html = HEAD.format(num=9, title="ルミナス", slug="09-luminous") + f"""
<div class="stage">
  <div class="glow"></div>
  <img class="hero" src="../assets/moet/cut/pika.png" alt=""/>
  <div class="panel">
    <p class="maison">NIGHT · LUMINOUS</p>
    <h1>モエシリーズ</h1>
    <div class="list">{list_rows()}</div>
  </div>
</div>
""" + FOOT
    css = """
.stage{position:relative;width:100%;height:100%;background:#030208;overflow:hidden}
.glow{position:absolute;right:10%;top:20%;width:50vw;height:50vw;background:radial-gradient(circle,rgba(255,80,120,.25),rgba(255,140,60,.12),transparent 70%);filter:blur(10px)}
.hero{position:absolute;right:-5%;bottom:-5%;height:100%;transform:rotate(8deg);filter:drop-shadow(0 0 40px rgba(255,100,80,.4))}
.panel{position:absolute;left:0;top:0;bottom:0;width:min(48vw,620px);padding:8vh 4vw;display:flex;flex-direction:column;justify-content:center;
  background:linear-gradient(90deg,rgba(3,2,8,.95) 60%,transparent)}
.maison{font-family:var(--sans);letter-spacing:.4em;color:#ff8a9a;font-size:.7rem}
h1{font-size:clamp(2rem,4.5vw,3.4rem);letter-spacing:.2em;margin:.6rem 0 2rem;text-shadow:0 0 30px rgba(255,100,120,.3)}
.list{display:flex;flex-direction:column;gap:.9rem}
.row{display:flex;justify-content:space-between;align-items:baseline;gap:1rem;border-bottom:1px solid rgba(255,120,140,.15);padding-bottom:.65rem}
.rule,.en{display:none}
.nick{font-size:1.1rem;letter-spacing:.12em}
.formal{font-size:.68rem;color:var(--muted)}
.price{font-family:var(--serif);font-size:1.35rem;color:#ffb4a0}
.is-feature .nick,.is-feature .price{color:#fff;text-shadow:0 0 16px rgba(255,120,100,.6)}
"""
    return "09-luminous", html, css


def d10():
    cards = "".join(
        f'<div class="card{" feat" if i==4 else ""}"><p class="big">{pr}</p><p class="n">{n}</p><p class="f">{fo}</p></div>'
        for i,(n,fo,_,pr,_) in enumerate(ITEMS)
    )
    html = HEAD.format(num=10, title="プライスヒーロー", slug="10-price-hero") + f"""
<div class="stage">
  <header><p class="maison">MOËT &amp; CHANDON</p><h1>モエシリーズ</h1></header>
  <div class="grid">{cards}</div>
</div>
""" + FOOT
    css = """
.stage{width:100%;height:100%;padding:5vh 4vw;display:flex;flex-direction:column;background:#080605;
  background-image:radial-gradient(ellipse at 50% 100%, rgba(201,161,93,.12), transparent 55%)}
header{text-align:center;margin-bottom:3vh}
.maison{font-family:var(--serif);letter-spacing:.5em;color:var(--gold);font-size:.8rem}
h1{font-size:clamp(2rem,4vw,3rem);letter-spacing:.25em;margin-top:.4rem}
.grid{flex:1;display:grid;grid-template-columns:repeat(5,1fr);gap:1rem;align-content:center}
.card{text-align:center;padding:2vh 1vw;border-top:1px solid rgba(201,161,93,.35)}
.big{font-family:var(--serif);font-size:clamp(1.6rem,3.5vw,2.8rem);color:var(--gold);font-weight:600;line-height:1}
.n{margin-top:1rem;letter-spacing:.14em;font-size:1.05rem}
.f{margin-top:.35rem;font-size:.68rem;color:var(--muted);line-height:1.4}
.feat{border-top-color:var(--gold2)}
.feat .big{color:var(--gold2);font-size:clamp(1.8rem,4vw,3.1rem)}
@media(max-width:800px){.grid{grid-template-columns:1fr 1fr}}
"""
    return "10-price-hero", html, css


def d11():
    html = HEAD.format(num=11, title="ミラーフロア", slug="11-mirror") + f"""
<div class="stage">
  <div class="floor"></div>
  <div class="bots">
    {bottle_imgs(['rose','ice','pika'], 'm')}
  </div>
  <div class="caption">
    <p class="maison">MOËT &amp; CHANDON</p>
    <h1>モエシリーズ</h1>
    <div class="list">{list_rows()}</div>
  </div>
</div>
""" + FOOT
    css = """
.stage{position:relative;width:100%;height:100%;background:linear-gradient(180deg,#12100e 0%,#080706 55%,#050403 100%)}
.floor{position:absolute;left:0;right:0;bottom:0;height:38%;background:linear-gradient(180deg,rgba(255,255,255,.04),rgba(0,0,0,.5));
  border-top:1px solid rgba(201,161,93,.2);transform:perspective(400px) rotateX(12deg);transform-origin:top}
.bots{position:absolute;left:0;right:0;bottom:22%;height:55%;display:flex;justify-content:center;align-items:flex-end;gap:1vw;z-index:2}
.m{height:100%;width:auto;object-fit:contain;filter:drop-shadow(0 20px 30px rgba(0,0,0,.5))}
.m--1{height:85%;opacity:.75;transform:translateY(4%)}
.m--2{height:92%;opacity:.9}
.m--3{height:100%}
.caption{position:absolute;top:4vh;left:0;right:0;z-index:3;text-align:center;padding:0 4vw}
.maison{font-family:var(--serif);letter-spacing:.5em;color:var(--gold);font-size:.75rem}
h1{font-size:clamp(1.8rem,4vw,3rem);letter-spacing:.25em;margin:.35rem 0 1rem}
.list{display:flex;justify-content:center;flex-wrap:wrap;gap:.75rem 1.5rem;max-width:1000px;margin:0 auto}
.row{display:flex;gap:.6rem;align-items:baseline}
.rule,.formal,.en{display:none}
.nick{font-size:.9rem;letter-spacing:.1em;color:var(--muted)}
.price{font-family:var(--serif);color:var(--gold);font-size:1.05rem}
.is-feature .nick,.is-feature .price{color:var(--gold2)}
"""
    return "11-mirror", html, css


def d12():
    html = HEAD.format(num=12, title="ガラスパネル", slug="12-glass-panel") + f"""
<div class="stage">
  <img class="bg" src="../assets/moet/moet-bg.png" alt=""/>
  <img class="sidebot" src="../assets/moet/cut/ice.png" alt=""/>
  <div class="glass">
    <p class="maison">MOËT &amp; CHANDON</p>
    <h1>モエシリーズ</h1>
    <p class="lead">Champagne Collection</p>
    <div class="list">{list_rows()}</div>
  </div>
</div>
""" + FOOT
    css = """
.stage{position:relative;width:100%;height:100%}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.45)}
.sidebot{position:absolute;left:5%;bottom:-5%;height:90%;opacity:.9;filter:drop-shadow(0 20px 40px rgba(0,0,0,.5));z-index:1}
.glass{position:absolute;right:5vw;top:50%;transform:translateY(-50%);width:min(520px,90vw);z-index:2;
  padding:2.5rem 2rem;background:rgba(20,16,14,.55);border:1px solid rgba(255,255,255,.12);
  backdrop-filter:blur(18px);box-shadow:0 30px 80px rgba(0,0,0,.4)}
.maison{font-family:var(--serif);letter-spacing:.45em;color:var(--gold);font-size:.75rem}
h1{font-size:clamp(1.8rem,3.5vw,2.6rem);letter-spacing:.2em;margin:.5rem 0 .3rem}
.lead{font-family:var(--serif);font-style:italic;color:var(--faint);margin-bottom:1.5rem}
.list{display:flex;flex-direction:column;gap:.85rem}
.row{display:grid;grid-template-columns:1fr auto;gap:.8rem;align-items:end}
.rule{display:none}
.nick{font-size:1.05rem;letter-spacing:.12em}
.formal{font-size:.68rem;color:var(--muted)}
.en{display:none}
.price{font-family:var(--serif);font-size:1.3rem;color:var(--gold)}
"""
    return "12-glass-panel", html, css


def d13():
    html = HEAD.format(num=13, title="縦書きアクセント", slug="13-tate-gaki") + f"""
<div class="stage">
  <p class="tate">橘 · Tachibana</p>
  <div class="main">
    <p class="maison">MOËT &amp; CHANDON</p>
    <h1>モエシリーズ</h1>
    <div class="split">
      <div class="list">{list_rows()}</div>
      <img class="pic" src="../assets/moet/cut/rose.png" alt=""/>
    </div>
  </div>
</div>
""" + FOOT
    css = """
.stage{display:grid;grid-template-columns:auto 1fr;height:100%;background:#0c0a08}
.tate{writing-mode:vertical-rl;padding:3vh 1.2vw;letter-spacing:.45em;color:var(--gold);font-size:.95rem;
  border-right:1px solid rgba(201,161,93,.3);font-family:var(--jp)}
.main{padding:6vh 4vw;display:flex;flex-direction:column;justify-content:center}
.maison{font-family:var(--serif);letter-spacing:.45em;color:var(--gold);font-size:.8rem}
h1{font-size:clamp(2.2rem,5vw,3.6rem);letter-spacing:.22em;margin:.5rem 0 2rem}
.split{display:grid;grid-template-columns:1fr minmax(180px,28%);gap:2vw;align-items:end}
.list{display:flex;flex-direction:column;gap:1rem}
.row{display:grid;grid-template-columns:1fr auto;gap:1rem;border-bottom:1px solid rgba(201,161,93,.18);padding-bottom:.7rem}
.rule,.en{display:none}
.nick{font-size:1.15rem;letter-spacing:.14em}
.formal{font-size:.72rem;color:var(--muted)}
.price{font-family:var(--serif);font-size:1.4rem;color:var(--gold)}
.pic{height:55vh;margin:0 auto;filter:drop-shadow(0 20px 40px rgba(0,0,0,.45))}
@media(max-width:800px){.stage{grid-template-columns:1fr}.tate{writing-mode:horizontal-tb;border:none;padding:1rem}.split{grid-template-columns:1fr}}
"""
    return "13-tate-gaki", html, css


def d14():
    html = HEAD.format(num=14, title="クラブLED", slug="14-club-led") + f"""
<div class="stage">
  <div class="leds" aria-hidden="true"></div>
  <header>
    <p class="maison">CLUB MONITOR · MOËT</p>
    <h1>モエシリーズ</h1>
  </header>
  <div class="row5">
    {"".join(f'<div class="item"><img src="../assets/moet/cut/{k}.png" alt=""/><p class="n">{n}</p><p class="p">{pr}</p></div>' for n,_,_,pr,k in ITEMS)}
  </div>
</div>
""" + FOOT
    css = """
.stage{width:100%;height:100%;background:#05050a;padding:4vh 3vw;display:flex;flex-direction:column;
  background-image:linear-gradient(180deg,rgba(80,40,120,.15),transparent 40%)}
.leds{position:absolute;left:0;right:0;top:0;height:6px;background:linear-gradient(90deg,#ff2d55,#ffcc00,#00e5ff,#ff2d55);background-size:200% 100%;animation:led 4s linear infinite}
@keyframes led{to{background-position:200% 0}}
header{text-align:center;margin:2vh 0 3vh;position:relative;z-index:1}
.maison{font-family:var(--sans);letter-spacing:.4em;color:#00e5ff;font-size:.7rem}
h1{font-size:clamp(2rem,4.5vw,3.2rem);letter-spacing:.2em;margin-top:.4rem}
.row5{flex:1;display:grid;grid-template-columns:repeat(5,1fr);gap:1vw;align-items:end;position:relative;z-index:1}
.item{text-align:center;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);padding:2vh 1vw 2.5vh;border-radius:4px}
.item img{height:38vh;margin:0 auto 1rem;filter:drop-shadow(0 0 20px rgba(0,229,255,.15))}
.n{letter-spacing:.12em;font-size:.95rem}
.p{font-family:var(--serif);color:#ffcc66;font-size:1.25rem;margin-top:.35rem}
.item:last-child{border-color:rgba(255,45,85,.45);box-shadow:0 0 30px rgba(255,45,85,.15)}
.item:last-child .p{color:#ff8aa0}
@media(max-width:800px){.row5{grid-template-columns:1fr 1fr}.item img{height:22vh}}
"""
    return "14-club-led", html, css


def d15():
    html = HEAD.format(num=15, title="シルク", slug="15-silk") + f"""
<div class="stage">
  <div class="silk"></div>
  <img class="soft" src="../assets/moet/cut/brut.png" alt=""/>
  <div class="float">
    <p class="maison">MOËT &amp; CHANDON</p>
    <h1>モエシリーズ</h1>
    <div class="list">{list_rows()}</div>
  </div>
</div>
""" + FOOT
    css = """
.stage{position:relative;width:100%;height:100%;background:#140f0c;overflow:hidden}
.silk{position:absolute;inset:-20%;background:
  radial-gradient(ellipse at 20% 30%, rgba(201,161,93,.2), transparent 40%),
  radial-gradient(ellipse at 80% 70%, rgba(160,90,90,.18), transparent 45%),
  radial-gradient(ellipse at 50% 50%, rgba(255,240,220,.05), transparent 60%);
  filter:blur(40px)}
.soft{position:absolute;left:5%;bottom:-8%;height:95%;opacity:.35;filter:blur(1px) saturate(.8)}
.float{position:absolute;right:6vw;top:50%;transform:translateY(-50%);width:min(500px,88vw);z-index:2}
.maison{font-family:var(--serif);letter-spacing:.45em;color:var(--gold);font-size:.78rem}
h1{font-size:clamp(2rem,4vw,3rem);letter-spacing:.22em;margin:.5rem 0 1.75rem;font-weight:600}
.list{display:flex;flex-direction:column;gap:1rem}
.row{display:flex;justify-content:space-between;align-items:baseline;gap:1rem}
.rule,.en{display:none}
.nick{font-size:1.1rem;letter-spacing:.12em}
.formal{font-size:.7rem;color:var(--muted)}
.price{font-family:var(--serif);font-size:1.35rem;color:var(--gold2)}
"""
    return "15-silk", html, css


def d16():
    html = HEAD.format(num=16, title="ブルータル", slug="16-brutal") + f"""
<div class="stage">
  <img class="crop" src="../assets/moet/cut/pika.png" alt=""/>
  <div class="type">
    <p class="maison">MOËT</p>
    <h1>モエ<br/>シリーズ</h1>
    <ul>
      {"".join(f'<li><b>{n}</b> <span>{pr}</span></li>' for n,_,_,pr,_ in ITEMS)}
    </ul>
  </div>
</div>
""" + FOOT
    css = """
.stage{position:relative;width:100%;height:100%;background:#000;overflow:hidden}
.crop{position:absolute;left:-20%;top:-10%;height:140%;width:auto;max-width:none;object-fit:cover;filter:contrast(1.1) brightness(.85)}
.type{position:absolute;right:0;top:0;bottom:0;width:min(55vw,700px);padding:6vh 4vw;display:flex;flex-direction:column;justify-content:center;
  background:linear-gradient(90deg,transparent,rgba(0,0,0,.75) 18%,#000 45%)}
.maison{font-family:var(--sans);font-weight:700;letter-spacing:.4em;font-size:.75rem;color:var(--gold)}
h1{font-size:clamp(3rem,8vw,6.5rem);line-height:.9;letter-spacing:.04em;font-weight:700;margin:1rem 0 2rem}
ul{list-style:none;display:flex;flex-direction:column;gap:.9rem}
li{display:flex;justify-content:space-between;font-size:clamp(1.1rem,2vw,1.5rem);letter-spacing:.1em;border-bottom:2px solid #222;padding-bottom:.6rem}
li span{font-family:var(--serif);color:var(--gold)}
li:last-child{border-color:var(--gold)}
li:last-child b,li:last-child span{color:var(--gold2)}
"""
    return "16-brutal", html, css


def d17():
    html = HEAD.format(num=17, title="オーネイトフレーム", slug="17-ornate-frame") + f"""
<div class="stage">
  <div class="outer">
    <div class="inner">
      <img class="tl" src="../assets/moet/cut/brut.png" alt=""/>
      <img class="br" src="../assets/moet/cut/pika.png" alt=""/>
      <p class="maison">MOËT &amp; CHANDON</p>
      <h1>モエシリーズ</h1>
      <div class="list">{list_rows()}</div>
    </div>
  </div>
</div>
""" + FOOT
    css = """
.stage{width:100%;height:100%;display:grid;place-items:center;padding:4vh 3vw;background:#0a0806}
.outer{width:min(900px,94vw);height:min(92vh,900px);border:1px solid var(--gold);padding:8px}
.inner{position:relative;height:100%;border:1px solid rgba(201,161,93,.4);padding:clamp(2rem,5vh,3.5rem) clamp(2rem,5vw,4rem);
  display:flex;flex-direction:column;justify-content:center;overflow:hidden}
.tl{position:absolute;left:-2%;top:8%;height:42%;opacity:.22;transform:rotate(-15deg)}
.br{position:absolute;right:-4%;bottom:-4%;height:50%;opacity:.28;transform:rotate(8deg)}
.maison{position:relative;z-index:1;font-family:var(--serif);letter-spacing:.5em;color:var(--gold);font-size:.8rem;text-align:center}
h1{position:relative;z-index:1;text-align:center;font-size:clamp(2rem,4.5vw,3.2rem);letter-spacing:.28em;margin:.6rem 0 2rem}
.list{position:relative;z-index:1;display:flex;flex-direction:column;gap:1rem;max-width:560px;margin:0 auto;width:100%}
.row{display:grid;grid-template-columns:1fr minmax(1rem,1fr) auto;align-items:end;gap:.5rem}
.nick{font-size:1.15rem;letter-spacing:.12em}
.formal{font-size:.7rem;color:var(--muted)}
.en{font-family:var(--serif);font-style:italic;font-size:.72rem;color:var(--faint)}
.rule{border-bottom:1px dotted rgba(201,161,93,.4);transform:translateY(-.45em)}
.price{font-family:var(--serif);font-size:1.4rem;color:var(--gold)}
"""
    return "17-ornate-frame", html, css


def d18():
    html = HEAD.format(num=18, title="ディプティク", slug="18-diptych") + f"""
<div class="stage">
  <div class="half half--l"><img src="../assets/moet/cut/ice.png" alt=""/><p>ICE</p></div>
  <div class="half half--r"><img src="../assets/moet/cut/pika.png" alt=""/><p>N.I.R</p></div>
  <div class="center">
    <p class="maison">MOËT &amp; CHANDON</p>
    <h1>モエシリーズ</h1>
    <div class="list">{list_rows()}</div>
  </div>
</div>
""" + FOOT
    css = """
.stage{position:relative;width:100%;height:100%;display:grid;grid-template-columns:1fr 1fr;background:#050303}
.half{position:relative;overflow:hidden;display:flex;align-items:flex-end;justify-content:center}
.half--l{background:#0e0c0a}.half--r{background:#12080a}
.half img{height:85%;object-fit:contain;filter:drop-shadow(0 20px 40px rgba(0,0,0,.5))}
.half p{position:absolute;top:4vh;font-family:var(--serif);letter-spacing:.4em;color:rgba(255,255,255,.25);font-size:.85rem}
.center{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:min(420px,86vw);z-index:3;
  background:rgba(8,6,5,.88);border:1px solid rgba(201,161,93,.4);padding:2rem 1.5rem;backdrop-filter:blur(10px)}
.maison{font-family:var(--serif);letter-spacing:.4em;color:var(--gold);font-size:.7rem;text-align:center}
h1{text-align:center;font-size:1.8rem;letter-spacing:.2em;margin:.4rem 0 1.2rem}
.list{display:flex;flex-direction:column;gap:.65rem}
.row{display:flex;justify-content:space-between;align-items:baseline;gap:.8rem}
.rule,.formal,.en{display:none}
.nick{font-size:.95rem;letter-spacing:.1em}
.price{font-family:var(--serif);font-size:1.1rem;color:var(--gold)}
.is-feature .price{color:var(--gold2)}
"""
    return "18-diptych", html, css


def d19():
    rows = "".join(
        f'<tr class="{"feat" if i==4 else ""}"><td class="nick">{n}</td><td class="fo">{fo}</td><td class="en">{en}</td><td class="pr">{pr}</td></tr>'
        for i,(n,fo,en,pr,_) in enumerate(ITEMS)
    )
    html = HEAD.format(num=19, title="レジャー", slug="19-ledger") + f"""
<div class="stage">
  <div class="banner"><img src="../assets/moet/moet-bg.png" alt=""/><div class="bt"><p class="maison">MOËT &amp; CHANDON</p><h1>モエシリーズ</h1></div></div>
  <div class="table-wrap">
    <table>
      <thead><tr><th>通称</th><th>正式名称</th><th>Appellation</th><th>Price</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
</div>
""" + FOOT
    css = """
.stage{width:100%;height:100%;display:flex;flex-direction:column;background:#0b0908}
.banner{position:relative;height:32vh;overflow:hidden;flex-shrink:0}
.banner img{width:100%;height:100%;object-fit:cover;filter:brightness(.45)}
.bt{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.maison{font-family:var(--serif);letter-spacing:.5em;color:var(--gold);font-size:.8rem}
h1{font-size:clamp(2rem,4.5vw,3.2rem);letter-spacing:.25em;margin-top:.4rem}
.table-wrap{flex:1;display:flex;align-items:center;padding:3vh 4vw}
table{width:100%;max-width:1100px;margin:0 auto;border-collapse:collapse}
th{font-family:var(--serif);font-weight:400;letter-spacing:.2em;color:var(--gold);font-size:.75rem;text-align:left;
  border-bottom:1px solid rgba(201,161,93,.4);padding:0 1rem 1rem}
td{padding:1.1rem 1rem;border-bottom:1px solid rgba(255,255,255,.06);vertical-align:middle}
.nick{font-size:1.15rem;letter-spacing:.12em}
.fo{font-size:.85rem;color:var(--muted)}
.en{font-family:var(--serif);font-style:italic;color:var(--faint);font-size:.9rem}
.pr{font-family:var(--serif);font-size:1.4rem;color:var(--gold);text-align:right;white-space:nowrap}
.feat td{background:rgba(201,161,93,.06)}
.feat .pr{color:var(--gold2)}
@media(max-width:800px){th:nth-child(3),td.en{display:none}}
"""
    return "19-ledger", html, css


def d20():
    bots = "".join(
        f'<img class="o o--{i+1}" src="../assets/moet/cut/{k}.png" alt=""/>'
        for i,(*_,k) in enumerate(ITEMS)
    )
    prices = "".join(f'<p><span>{n}</span><b>{pr}</b></p>' for n,_,_,pr,_ in ITEMS)
    html = HEAD.format(num=20, title="オービット", slug="20-orbit") + f"""
<div class="stage">
  <div class="orbit">{bots}</div>
  <div class="core">
    <p class="maison">MOËT &amp; CHANDON</p>
    <h1>モエ<br/>シリーズ</h1>
    <div class="prices">{prices}</div>
  </div>
</div>
""" + FOOT
    css = """
.stage{position:relative;width:100%;height:100%;background:#080604;overflow:hidden}
.orbit{position:absolute;inset:0}
.o{position:absolute;height:42vh;object-fit:contain;filter:drop-shadow(0 16px 30px rgba(0,0,0,.55))}
.o--1{left:4%;top:8%;transform:rotate(-18deg);height:36vh;opacity:.75}
.o--2{right:6%;top:6%;transform:rotate(14deg);height:36vh;opacity:.8}
.o--3{left:8%;bottom:4%;transform:rotate(-8deg);height:38vh;opacity:.85}
.o--4{right:8%;bottom:6%;transform:rotate(10deg);height:40vh}
.o--5{left:50%;top:50%;transform:translate(-50%,-42%);height:48vh;z-index:2}
.core{position:absolute;left:50%;top:58%;transform:translate(-50%,0);z-index:3;text-align:center;
  background:rgba(8,6,4,.75);padding:1.5rem 2rem;border:1px solid rgba(201,161,93,.3);min-width:min(360px,86vw)}
.maison{font-family:var(--serif);letter-spacing:.45em;color:var(--gold);font-size:.7rem}
h1{font-size:clamp(1.6rem,3.5vw,2.4rem);letter-spacing:.18em;line-height:1.15;margin:.4rem 0 1rem}
.prices{display:flex;flex-direction:column;gap:.4rem}
.prices p{display:flex;justify-content:space-between;gap:1.5rem;font-size:.9rem;letter-spacing:.08em}
.prices b{font-family:var(--serif);color:var(--gold);font-weight:600}
.prices p:last-child b{color:var(--gold2)}
"""
    return "20-orbit", html, css


def d21():
    html = HEAD.format(num=21, title="マニフェスト", slug="21-manifesto") + f"""
<div class="stage">
  <img class="wm" src="../assets/moet/cut/nectar.png" alt=""/>
  <div class="wrap">
    <p class="eyebrow">A NIGHT WITH</p>
    <h1>MOËT</h1>
    <h2>モエシリーズ</h2>
    <p class="manifest">ボトルが開くたび、夜の温度が変わる。<br/>5つの表情から、今夜の1本を。</p>
    <div class="list">{list_rows()}</div>
  </div>
</div>
""" + FOOT
    css = """
.stage{position:relative;width:100%;height:100%;background:#0a0706}
.wm{position:absolute;right:-10%;top:50%;transform:translateY(-50%);height:110%;opacity:.12;filter:grayscale(.3)}
.wrap{position:relative;z-index:1;height:100%;max-width:820px;padding:8vh 6vw;display:flex;flex-direction:column;justify-content:center}
.eyebrow{font-family:var(--sans);letter-spacing:.45em;font-size:.7rem;color:var(--gold)}
h1{font-family:var(--serif);font-size:clamp(4rem,12vw,9rem);line-height:.85;letter-spacing:.06em;margin:.3rem 0}
h2{font-size:clamp(1.4rem,3vw,2rem);letter-spacing:.28em;color:var(--gold2);margin-bottom:1.25rem}
.manifest{font-size:clamp(.95rem,1.6vw,1.15rem);letter-spacing:.12em;line-height:1.9;color:var(--muted);margin-bottom:2.5rem}
.list{display:flex;flex-direction:column;gap:.85rem;max-width:560px}
.row{display:grid;grid-template-columns:1fr auto;gap:1rem;align-items:baseline;border-top:1px solid rgba(201,161,93,.2);padding-top:.7rem}
.rule,.en{display:none}
.nick{font-size:1.15rem;letter-spacing:.14em}
.formal{font-size:.7rem;color:var(--faint)}
.price{font-family:var(--serif);font-size:1.35rem;color:var(--gold)}
.is-feature{border-top-color:var(--gold)}
.is-feature .nick,.is-feature .price{color:var(--gold2)}
"""
    return "21-manifesto", html, css


GENERATORS = [d01,d02,d03,d04,d05,d06,d07,d08,d09,d10,d11,d12,d13,d14,d15,d16,d17,d18,d19,d20,d21]


def write_gallery():
    cards = []
    for num, slug, title, desc in META:
        cards.append(f"""
        <a class="card" href="designs/{num:02d}-{slug}.html">
          <span class="num">DESIGN {num:02d}</span>
          <strong>{title}</strong>
          <span class="desc">{desc}</span>
          <span class="open">開く →</span>
        </a>""")
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Tachibana — モエシリーズ デザイン案（21種）</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Shippori+Mincho:wght@500;700&family=Zen+Kaku+Gothic+New:wght@400;500&display=swap" rel="stylesheet"/>
<style>
:root{{--bg:#0a0806;--ink:#f6eee3;--gold:#c9a15d;--muted:rgba(246,238,227,.6)}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--ink);font-family:"Zen Kaku Gothic New",system-ui,sans-serif;padding:3rem 4vw 4rem}}
header{{max-width:1100px;margin:0 auto 2.5rem}}
.eyebrow{{font-family:"Cormorant Garamond",serif;letter-spacing:.4em;color:var(--gold);font-size:.85rem}}
h1{{font-family:"Shippori Mincho",serif;font-size:clamp(1.8rem,4vw,2.8rem);letter-spacing:.18em;margin:.6rem 0}}
.sub{{color:var(--muted);line-height:1.7;max-width:40rem}}
.hint{{margin-top:1rem;font-size:.85rem;color:rgba(246,238,227,.45)}}
.grid{{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:1rem}}
.card{{display:flex;flex-direction:column;gap:.45rem;padding:1.25rem 1.15rem;border:1px solid rgba(201,161,93,.25);
  text-decoration:none;color:inherit;background:rgba(255,255,255,.02);transition:border-color .2s,transform .2s}}
.card:hover{{border-color:var(--gold);transform:translateY(-2px)}}
.num{{font-size:.7rem;letter-spacing:.2em;color:var(--gold)}}
strong{{font-family:"Shippori Mincho",serif;font-size:1.15rem;letter-spacing:.08em;font-weight:600}}
.desc{{font-size:.8rem;color:var(--muted);line-height:1.5;flex:1}}
.open{{font-size:.75rem;color:var(--gold);margin-top:.5rem}}
.card:first-child{{border-color:rgba(237,214,164,.55);background:rgba(201,161,93,.06)}}
</style>
</head>
<body>
<header>
  <p class="eyebrow">TACHIBANA · REVIEW</p>
  <h1>モエシリーズ デザイン案</h1>
  <p class="sub">デザイン1（ワインリスト）をベースに、全21案を用意しました。カードをクリックして各案を全画面で確認できます。各デザイン内では ← → で前後の案へ移動、Esc / G でギャラリーに戻ります。</p>
  <p class="hint">採用したい番号を教えてください。</p>
</header>
<nav class="grid">{''.join(cards)}</nav>
</body>
</html>"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")


def main():
    (DESIGNS / "shared.css").write_text(SHARED_CSS, encoding="utf-8")
    (DESIGNS / "nav.js").write_text(nav_js(), encoding="utf-8")
    for gen in GENERATORS:
        slug, html, css = gen()
        (DESIGNS / f"{slug}.html").write_text(html, encoding="utf-8")
        (DESIGNS / f"{slug}.css").write_text(css, encoding="utf-8")
        print("wrote", slug)
    write_gallery()
    # README
    (ROOT / "README.md").write_text(
        """# Tachibana — モエシリーズ デザイン案

店舗モニター向けスライドのデザイン検討用です。

## 確認方法

1. `index.html` を開く（ギャラリー）
2. 各カードからデザイン案を全画面表示
3. デザイン内で `←` `→` で前後移動、`Esc` / `G` でギャラリーへ

## デザイン一覧（21案）

| # | 名前 | 概要 |
|---|------|------|
| 01 | ワインリスト | 左ボトル／右価格表（現行案） |
| 02 | ヒーローNIR | ピカ全面＋下部価格 |
| 03 | タイポポスター | 巨大文字主役 |
| 04 | アールデコ | 幾何学フレーム |
| 05 | スポットライト | 中央1本＋左右価格 |
| 06 | フィルムストリップ | 縦帯5本＋リスト |
| 07 | カスケード | 斜め階段配置 |
| 08 | ゴールドプレート | 銘板メニュー |
| 09 | ルミナス | ネオンナイト |
| 10 | プライスヒーロー | 価格数字が大きく |
| 11 | ミラーフロア | 反射床演出 |
| 12 | ガラスパネル | 半透明パネル |
| 13 | 縦書きアクセント | 和の縦書き |
| 14 | クラブLED | LEDバー＋5カラム |
| 15 | シルク | 柔らかい光 |
| 16 | ブルータル | 大トリミング＋大文字 |
| 17 | オーネイトフレーム | 金の二重枠 |
| 18 | ディプティク | アイス／ピカ二面 |
| 19 | レジャー | 表形式料金表 |
| 20 | オービット | 円弧配置 |
| 21 | マニフェスト | 宣言ポスター |

料金・正式名称は全案共通です。
""",
        encoding="utf-8",
    )
    print("gallery ready")


if __name__ == "__main__":
    main()
