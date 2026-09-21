#!/usr/bin/env python3
"""20 luxury lounge Moët designs — always with bottle photos + large type."""
from pathlib import Path

ROOT = Path("/workspace")
D = ROOT / "designs"
D.mkdir(exist_ok=True)

for p in D.glob("*"):
    if p.suffix in {".html", ".css"} and p.name not in ("shared.css",):
        p.unlink()

ITEMS = [
    ("モエシロ", "ブリュット アンペリアル", "¥20,000", "brut"),
    ("モエロゼ", "ロゼ アンペリアル", "¥25,000", "rose"),
    ("モエ黒", "ネクター アンペリアル", "¥30,000", "nectar"),
    ("モエアイス", "アイス アンペリアル", "¥35,000", "ice"),
    ("モエピカ", "N.I.R ロゼ ドライ", "¥40,000", "pika"),
]

META = [
    (1, "velvet-billboard", "ベルベットビルボード"),
    (2, "vip-hero", "VIPヒーロー"),
    (3, "gold-salon", "ゴールドサロン"),
    (4, "rose-night", "ローズナイト"),
    (5, "ice-lounge", "アイスラウンジ"),
    (6, "pika-glow", "ピカグロウ"),
    (7, "triple-vip", "トリプルVIP"),
    (8, "mahogany-bar", "マホガニーバー"),
    (9, "champagne-mist", "シャンパンミスト"),
    (10, "spotlight-nectar", "スポットネクター"),
    (11, "cascade-luxe", "カスケードリュクス"),
    (12, "mirror-suite", "ミラースイート"),
    (13, "framed-collection", "フレームコレクション"),
    (14, "runway-bottles", "ランウェイ"),
    (15, "overlay-panel", "オーバーレイパネル"),
    (16, "duo-stage", "デュオステージ"),
    (17, "noir-glamour", "ノワールグラマー"),
    (18, "amber-lounge", "アンバーラウンジ"),
    (19, "vertical-gallery", "バーチカルギャラリー"),
    (20, "grand-arrival", "グランドアライバル"),
]

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

def rows():
    out=[]
    for i,(n,f,p,_) in enumerate(ITEMS):
        hot=" is-hot" if i==4 else ""
        out.append(f'<div class="row{hot}"><div><p class="nick">{n}</p><p class="formal">モエ・エ・シャンドン {f}</p></div><p class="price">{p}</p></div>')
    return "\n".join(out)

def head(num,slug,title):
    return f"""<!DOCTYPE html><html lang="ja"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Design {num:02d} — {title}</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Shippori+Mincho:wght@600;700&family=Zen+Kaku+Gothic+New:wght@500;700&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="shared.css"/><link rel="stylesheet" href="{num:02d}-{slug}.css"/>
</head><body>
<a class="back" href="../index.html">← 一覧</a>
<div class="badge">DESIGN {num:02d} · {title}</div>
"""

FOOT="""
<script>if(new URLSearchParams(location.search).get('shot')==='1'){document.documentElement.classList.add('shot');document.addEventListener('DOMContentLoaded',()=>document.body.classList.add('shot'));}</script>
<script src="nav.js"></script></body></html>
"""

def save(num,slug,title,body,css):
    (D/f"{num:02d}-{slug}.html").write_text(head(num,slug,title)+body+FOOT,encoding="utf-8")
    (D/f"{num:02d}-{slug}.css").write_text(css,encoding="utf-8")
    print("ok", f"{num:02d}-{slug}")

R=rows()

# 1 velvet billboard
save(1,"velvet-billboard","ベルベットビルボード",f"""
<div class="stage">
<img class="bg" src="../assets/moet/moet-bg.png" alt=""/>
<div class="shade"></div>
<img class="b b1" src="../assets/moet/cut/rose.png" alt=""/>
<img class="b b2" src="../assets/moet/cut/ice.png" alt=""/>
<img class="b b3" src="../assets/moet/cut/pika.png" alt=""/>
<div class="panel"><p class="maison">MOËT &amp; CHANDON</p><h1 class="title">モエシリーズ</h1><div class="list">{R}</div></div>
</div>""","""
.stage{position:relative;width:100%;height:100%}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.32)}
.shade{position:absolute;inset:0;background:linear-gradient(105deg,rgba(6,4,3,.1),rgba(6,4,3,.7) 45%,rgba(6,4,3,.96) 66%)}
.b{position:absolute;bottom:-6%;object-fit:contain;filter:drop-shadow(0 25px 50px rgba(0,0,0,.65));z-index:1}
.b1{left:0;height:78%;opacity:.55;transform:rotate(-9deg)}
.b2{left:10%;height:88%;opacity:.8;transform:rotate(3deg)}
.b3{left:22%;height:105%;transform:rotate(-2deg)}
.panel{position:absolute;right:0;top:0;bottom:0;width:min(56vw,800px);z-index:2;padding:3.5vh 3.5vw;display:flex;flex-direction:column;justify-content:center}
.list{margin-top:2vh;display:flex;flex-direction:column;gap:1.2vh}
.row{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;border-bottom:2px solid rgba(226,180,92,.3);padding-bottom:1vh}
""")

# 2 vip hero
save(2,"vip-hero","VIPヒーロー",f"""
<div class="stage">
<img class="hero" src="../assets/moet/cut/pika.png" alt=""/>
<img class="side" src="../assets/moet/cut/ice.png" alt=""/>
<div class="veil"></div>
<header><p class="maison">MOËT &amp; CHANDON</p><h1 class="title">モエシリーズ</h1></header>
<div class="dock">{R}</div>
</div>""","""
.stage{position:relative;width:100%;height:100%;background:#050203}
.hero{position:absolute;left:48%;top:38%;transform:translate(-50%,-50%);height:92%;z-index:2;filter:drop-shadow(0 0 70px rgba(255,90,60,.4))}
.side{position:absolute;left:8%;bottom:-5%;height:70%;opacity:.45;transform:rotate(-12deg);z-index:1}
.veil{position:absolute;inset:0;z-index:3;background:linear-gradient(180deg,rgba(5,2,3,.75),transparent 30%,transparent 50%,rgba(5,2,3,.9) 75%,#050203)}
header{position:absolute;top:3vh;left:0;right:0;text-align:center;z-index:4}
.dock{position:absolute;left:0;right:0;bottom:0;z-index:4;padding:1.5vh 3vw 3vh;display:grid;grid-template-columns:repeat(5,1fr);gap:1vw;background:linear-gradient(180deg,transparent,rgba(5,2,3,.96))}
.row{text-align:center}
.row .nick{font-size:clamp(1.5rem,2.8vw,2.4rem)}
.row .formal{font-size:clamp(1rem,1.4vw,1.25rem)}
.row .price{margin-top:.45rem;font-size:clamp(1.7rem,3vw,2.7rem)}
""")

# 3 gold salon
save(3,"gold-salon","ゴールドサロン",f"""
<div class="stage">
<img class="bg" src="../assets/moet/moet-bg.png" alt=""/>
<div class="shade"></div>
<div class="frame">
<img class="pic" src="../assets/moet/cut/brut.png" alt=""/>
<div class="copy"><p class="maison">MOËT &amp; CHANDON</p><h1 class="title">モエシリーズ</h1><div class="list">{R}</div></div>
</div></div>""","""
.stage{position:relative;width:100%;height:100%}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.28) sepia(.15)}
.shade{position:absolute;inset:0;background:rgba(6,4,3,.55)}
.frame{position:absolute;inset:4vh 4vw;border:1px solid rgba(226,180,92,.55);display:grid;grid-template-columns:38% 1fr;overflow:hidden;background:rgba(10,7,5,.55);backdrop-filter:blur(6px)}
.pic{height:100%;width:100%;object-fit:contain;object-position:center bottom;padding:3vh 1vw 0;filter:drop-shadow(0 20px 40px rgba(0,0,0,.5))}
.copy{padding:4vh 3vw;display:flex;flex-direction:column;justify-content:center}
.list{margin-top:2vh;display:flex;flex-direction:column;gap:1.1vh}
.row{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;border-bottom:1px solid rgba(226,180,92,.28);padding-bottom:.9vh}
""")

# 4 rose night
save(4,"rose-night","ローズナイト",f"""
<div class="stage">
<div class="glow"></div>
<img class="hero" src="../assets/moet/cut/rose.png" alt=""/>
<img class="accent" src="../assets/moet/cut/pika.png" alt=""/>
<div class="panel"><p class="maison">ROSÉ &amp; NIGHT</p><h1 class="title">モエシリーズ</h1><div class="list">{R}</div></div>
</div>""","""
.stage{position:relative;width:100%;height:100%;background:#10080c;overflow:hidden}
.glow{position:absolute;left:20%;top:10%;width:50vw;height:50vw;background:radial-gradient(circle,rgba(232,120,140,.28),transparent 70%)}
.hero{position:absolute;left:5%;bottom:-8%;height:105%;z-index:1;filter:drop-shadow(0 20px 40px rgba(0,0,0,.5))}
.accent{position:absolute;left:28%;bottom:-10%;height:80%;opacity:.35;transform:rotate(8deg);z-index:0}
.panel{position:absolute;right:0;top:0;bottom:0;width:min(54vw,760px);z-index:2;padding:4vh 3.5vw;display:flex;flex-direction:column;justify-content:center;background:linear-gradient(90deg,transparent,rgba(16,8,12,.88) 18%,rgba(16,8,12,.96))}
.maison{color:var(--rose)}
.list{margin-top:2vh;display:flex;flex-direction:column;gap:1.15vh}
.row{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;border-bottom:2px solid rgba(232,160,168,.28);padding-bottom:1vh}
.is-hot .nick,.is-hot .price{color:#ffd0d6}
""")

# 5 ice lounge
save(5,"ice-lounge","アイスラウンジ",f"""
<div class="stage">
<img class="bg" src="../assets/moet/moet-bg.png" alt=""/>
<div class="shade"></div>
<img class="hero" src="../assets/moet/cut/ice.png" alt=""/>
<img class="sub" src="../assets/moet/cut/brut.png" alt=""/>
<div class="panel"><p class="maison">ON THE ROCKS</p><h1 class="title">モエシリーズ</h1><div class="list">{R}</div></div>
</div>""","""
.stage{position:relative;width:100%;height:100%}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.3) hue-rotate(10deg)}
.shade{position:absolute;inset:0;background:linear-gradient(110deg,rgba(8,12,16,.2),rgba(6,4,3,.85) 55%)}
.hero{position:absolute;left:8%;bottom:-6%;height:100%;z-index:2;filter:drop-shadow(0 0 40px rgba(180,220,255,.2))}
.sub{position:absolute;left:-2%;bottom:0;height:70%;opacity:.35;transform:rotate(-8deg);z-index:1}
.panel{position:absolute;right:0;top:0;bottom:0;width:min(52vw,740px);z-index:3;padding:4vh 3.5vw;display:flex;flex-direction:column;justify-content:center}
.maison{color:#b8d4e8}
.list{margin-top:2vh;display:flex;flex-direction:column;gap:1.15vh}
.row{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;border-bottom:2px solid rgba(180,210,230,.25);padding-bottom:1vh}
""")

# 6 pika glow
save(6,"pika-glow","ピカグロウ",f"""
<div class="stage">
<div class="glow"></div>
<img class="hero" src="../assets/moet/cut/pika.png" alt=""/>
<img class="l" src="../assets/moet/cut/nectar.png" alt=""/>
<div class="panel"><p class="maison">N.I.R · LUMINOUS</p><h1 class="title">モエシリーズ</h1><div class="list">{R}</div></div>
</div>""","""
.stage{position:relative;width:100%;height:100%;background:#060208;overflow:hidden}
.glow{position:absolute;right:10%;top:15%;width:55vw;height:55vw;background:radial-gradient(circle,rgba(255,70,90,.32),rgba(255,140,50,.12),transparent 70%)}
.hero{position:absolute;right:-5%;bottom:-8%;height:112%;z-index:1;transform:rotate(5deg);filter:drop-shadow(0 0 55px rgba(255,80,90,.45))}
.l{position:absolute;right:28%;bottom:0;height:65%;opacity:.3;z-index:0}
.panel{position:absolute;left:0;top:0;bottom:0;width:min(55vw,760px);z-index:2;padding:4vh 3.5vw;display:flex;flex-direction:column;justify-content:center;background:linear-gradient(90deg,rgba(6,2,8,.97) 72%,transparent)}
.maison{color:#ff8fa3}
.list{margin-top:2vh;display:flex;flex-direction:column;gap:1.1vh}
.row{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;border-bottom:2px solid rgba(255,120,140,.25);padding-bottom:1vh}
.price{color:#ffc3a8}
.is-hot .nick,.is-hot .price{color:#fff;text-shadow:0 0 18px rgba(255,100,110,.6)}
""")

# 7 triple vip
save(7,"triple-vip","トリプルVIP",f"""
<div class="stage">
<img class="bg" src="../assets/moet/moet-bg.png" alt=""/>
<div class="shade"></div>
<div class="bots">
<img src="../assets/moet/cut/rose.png" alt=""/><img src="../assets/moet/cut/ice.png" alt=""/><img src="../assets/moet/cut/pika.png" alt=""/>
</div>
<div class="sheet"><p class="maison">MOËT &amp; CHANDON</p><h1 class="title">モエシリーズ</h1><div class="list">{R}</div></div>
</div>""","""
.stage{position:relative;width:100%;height:100%}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.28)}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,4,3,.55),rgba(6,4,3,.2) 35%,rgba(6,4,3,.92))}
.bots{position:absolute;left:0;right:0;top:6%;height:48%;display:flex;justify-content:center;align-items:flex-end;gap:2vw;z-index:1}
.bots img{height:100%;object-fit:contain;filter:drop-shadow(0 20px 35px rgba(0,0,0,.55))}
.bots img:nth-child(1),.bots img:nth-child(3){height:88%;opacity:.85}
.sheet{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:1vh 5vw 3.5vh;background:linear-gradient(180deg,transparent,rgba(6,4,3,.95) 28%)}
.sheet .maison,.sheet .title{text-align:center}
.list{margin-top:1.5vh;display:grid;grid-template-columns:repeat(5,1fr);gap:1vw}
.row{text-align:center;border:none;padding:0}
.row .nick{font-size:clamp(1.4rem,2.6vw,2.3rem)}
.row .formal{font-size:clamp(.95rem,1.35vw,1.2rem)}
.row .price{margin-top:.4rem;font-size:clamp(1.6rem,2.9vw,2.6rem)}
""")

# 8 mahogany bar
save(8,"mahogany-bar","マホガニーバー",f"""
<div class="stage">
<img class="bg" src="../assets/moet/moet-bg.png" alt=""/>
<div class="shade"></div>
<img class="b1" src="../assets/moet/cut/nectar.png" alt=""/>
<img class="b2" src="../assets/moet/cut/brut.png" alt=""/>
<div class="panel"><p class="maison">LOUNGE COLLECTION</p><h1 class="title">モエシリーズ</h1><div class="list">{R}</div></div>
</div>""","""
.stage{position:relative;width:100%;height:100%}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.3) saturate(1.1)}
.shade{position:absolute;inset:0;background:linear-gradient(115deg,rgba(20,10,6,.25),rgba(6,4,3,.88) 58%)}
.b1{position:absolute;left:6%;bottom:-5%;height:95%;z-index:1;filter:drop-shadow(0 20px 40px rgba(0,0,0,.55))}
.b2{position:absolute;left:24%;bottom:-2%;height:72%;opacity:.4;transform:rotate(7deg);z-index:0}
.panel{position:absolute;right:0;top:0;bottom:0;width:min(54vw,760px);z-index:2;padding:4vh 3.5vw;display:flex;flex-direction:column;justify-content:center}
.list{margin-top:2vh;display:flex;flex-direction:column;gap:1.15vh}
.row{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;border-bottom:2px solid rgba(226,180,92,.28);padding-bottom:1vh}
""")

# 9 champagne mist
save(9,"champagne-mist","シャンパンミスト",f"""
<div class="stage">
<img class="bg" src="../assets/moet/moet-bg.png" alt=""/>
<div class="mist"></div>
<img class="b1" src="../assets/moet/cut/pika.png" alt=""/>
<img class="b2" src="../assets/moet/cut/rose.png" alt=""/>
<div class="panel"><p class="maison">MOËT &amp; CHANDON</p><h1 class="title">モエシリーズ</h1><div class="list">{R}</div></div>
</div>""","""
.stage{position:relative;width:100%;height:100%}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.35)}
.mist{position:absolute;inset:0;background:radial-gradient(ellipse at 30% 70%,rgba(226,180,92,.22),transparent 50%),linear-gradient(100deg,transparent 30%,rgba(6,4,3,.9) 70%)}
.b1{position:absolute;left:2%;bottom:-10%;height:110%;z-index:1;opacity:.95;filter:drop-shadow(0 0 40px rgba(255,100,70,.25))}
.b2{position:absolute;left:20%;bottom:0;height:75%;opacity:.4;transform:rotate(-8deg);z-index:0}
.panel{position:absolute;right:3vw;top:50%;transform:translateY(-50%);width:min(50vw,700px);z-index:2;padding:3vh 2.5vw;background:rgba(8,6,5,.55);border:1px solid rgba(226,180,92,.28);backdrop-filter:blur(12px)}
.list{margin-top:1.8vh;display:flex;flex-direction:column;gap:1vh}
.row{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;border-bottom:1px solid rgba(226,180,92,.25);padding-bottom:.85vh}
.row .nick{font-size:clamp(1.7rem,3.3vw,2.9rem)}
.row .price{font-size:clamp(1.8rem,3.5vw,3.1rem)}
""")

# 10 spotlight nectar
save(10,"spotlight-nectar","スポットネクター",f"""
<div class="stage">
<div class="spot"></div>
<img class="hero" src="../assets/moet/cut/nectar.png" alt=""/>
<img class="l" src="../assets/moet/cut/rose.png" alt=""/>
<img class="r" src="../assets/moet/cut/ice.png" alt=""/>
<header><p class="maison">MOËT &amp; CHANDON</p><h1 class="title">モエシリーズ</h1></header>
<div class="menu">{R}</div>
</div>""","""
.stage{position:relative;width:100%;height:100%;background:#050303}
.spot{position:absolute;left:50%;top:42%;transform:translate(-50%,-50%);width:50vw;height:50vw;border-radius:50%;background:radial-gradient(circle,rgba(226,180,92,.3),transparent 65%)}
.hero{position:absolute;left:50%;bottom:18%;transform:translateX(-50%);height:70%;z-index:2;filter:drop-shadow(0 25px 50px rgba(0,0,0,.65))}
.l{position:absolute;left:6%;bottom:22%;height:48%;opacity:.45;transform:rotate(-14deg);z-index:1}
.r{position:absolute;right:6%;bottom:22%;height:48%;opacity:.45;transform:rotate(12deg);z-index:1}
header{position:absolute;top:3vh;left:0;right:0;text-align:center;z-index:3}
.menu{position:absolute;left:4vw;right:4vw;bottom:2.5vh;z-index:3;display:grid;grid-template-columns:repeat(5,1fr);gap:1vw}
.row{text-align:center;background:rgba(0,0,0,.35);border:1px solid rgba(226,180,92,.25);padding:1.2vh .5vw}
.row .nick{font-size:clamp(1.35rem,2.5vw,2.2rem)}
.row .formal{font-size:clamp(.95rem,1.3vw,1.15rem)}
.row .price{margin-top:.35rem;font-size:clamp(1.5rem,2.8vw,2.5rem)}
""")

# 11 cascade luxe
save(11,"cascade-luxe","カスケードリュクス",f"""
<div class="stage">
<img class="bg" src="../assets/moet/moet-bg.png" alt=""/>
<div class="shade"></div>
<img class="c c1" src="../assets/moet/cut/brut.png" alt=""/>
<img class="c c2" src="../assets/moet/cut/rose.png" alt=""/>
<img class="c c3" src="../assets/moet/cut/nectar.png" alt=""/>
<img class="c c4" src="../assets/moet/cut/ice.png" alt=""/>
<img class="c c5" src="../assets/moet/cut/pika.png" alt=""/>
<div class="rail"><p class="maison">MOËT &amp; CHANDON</p><h1 class="title">モエシリーズ</h1><div class="list">{R}</div></div>
</div>""","""
.stage{position:relative;width:100%;height:100%}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.28)}
.shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(6,4,3,.2),rgba(6,4,3,.88) 62%)}
.c{position:absolute;height:52vh;object-fit:contain;filter:drop-shadow(0 18px 30px rgba(0,0,0,.5));z-index:1}
.c1{left:1%;top:6%;transform:rotate(-12deg);opacity:.7}
.c2{left:10%;top:16%;transform:rotate(-6deg);opacity:.8}
.c3{left:19%;top:26%}
.c4{left:28%;top:36%;transform:rotate(4deg)}
.c5{left:37%;top:42%;height:58vh;transform:rotate(8deg)}
.rail{position:absolute;right:0;top:0;bottom:0;width:min(46vw,680px);z-index:2;padding:4vh 3vw;display:flex;flex-direction:column;justify-content:center;background:rgba(6,4,3,.72);backdrop-filter:blur(8px)}
.list{margin-top:2vh;display:flex;flex-direction:column;gap:1.1vh}
.row{display:flex;justify-content:space-between;align-items:flex-end;gap:.8rem;border-bottom:2px solid rgba(226,180,92,.25);padding-bottom:.9vh}
.row .nick{font-size:clamp(1.7rem,3.2vw,2.8rem)}
.row .price{font-size:clamp(1.8rem,3.4vw,3rem)}
""")

# 12 mirror suite
save(12,"mirror-suite","ミラースイート",f"""
<div class="stage">
<div class="floor"></div>
<div class="bots"><img src="../assets/moet/cut/rose.png" alt=""/><img src="../assets/moet/cut/ice.png" alt=""/><img src="../assets/moet/cut/pika.png" alt=""/></div>
<div class="top"><p class="maison">MOËT &amp; CHANDON</p><h1 class="title">モエシリーズ</h1></div>
<div class="menu">{R}</div>
</div>""","""
.stage{position:relative;width:100%;height:100%;background:linear-gradient(180deg,#14100e,#070504 60%)}
.floor{position:absolute;left:0;right:0;bottom:0;height:34%;background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(0,0,0,.45));border-top:1px solid rgba(226,180,92,.25)}
.bots{position:absolute;left:0;right:0;bottom:26%;height:52%;display:flex;justify-content:center;align-items:flex-end;gap:1.5vw;z-index:2}
.bots img{height:100%;object-fit:contain;filter:drop-shadow(0 18px 28px rgba(0,0,0,.5))}
.bots img:first-child,.bots img:last-child{height:88%;opacity:.85}
.top{position:absolute;top:3vh;left:0;right:0;text-align:center;z-index:3}
.menu{position:absolute;left:4vw;right:4vw;bottom:3vh;z-index:3;display:grid;grid-template-columns:repeat(5,1fr);gap:1vw}
.row{text-align:center}
.row .nick{font-size:clamp(1.4rem,2.6vw,2.25rem)}
.row .formal{font-size:clamp(.95rem,1.3vw,1.15rem)}
.row .price{margin-top:.35rem;font-size:clamp(1.55rem,2.8vw,2.5rem)}
""")

# 13 framed collection
save(13,"framed-collection","フレームコレクション",f"""
<div class="stage">
<img class="bg" src="../assets/moet/moet-bg.png" alt=""/>
<div class="shade"></div>
<div class="frame">
<img class="corner tl" src="../assets/moet/cut/brut.png" alt=""/>
<img class="corner br" src="../assets/moet/cut/pika.png" alt=""/>
<p class="maison">MOËT &amp; CHANDON</p><h1 class="title">モエシリーズ</h1>
<div class="mid"><img src="../assets/moet/cut/ice.png" alt=""/><div class="list">{R}</div></div>
</div></div>""","""
.stage{position:relative;width:100%;height:100%}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.25)}
.shade{position:absolute;inset:0;background:rgba(6,4,3,.6)}
.frame{position:absolute;inset:3.5vh 3.5vw;border:1px solid var(--gold);padding:3vh 3vw;display:flex;flex-direction:column;justify-content:center;overflow:hidden}
.corner{position:absolute;height:42%;opacity:.22;object-fit:contain}
.tl{left:-1%;top:4%;transform:rotate(-12deg)}
.br{right:-2%;bottom:-4%;height:48%;transform:rotate(8deg)}
.maison,.title{position:relative;z-index:1;text-align:center}
.mid{position:relative;z-index:1;margin-top:2vh;display:grid;grid-template-columns:28% 1fr;gap:2vw;align-items:center}
.mid>img{height:55vh;margin:0 auto;filter:drop-shadow(0 20px 35px rgba(0,0,0,.45))}
.list{display:flex;flex-direction:column;gap:1vh}
.row{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;border-bottom:1px solid rgba(226,180,92,.28);padding-bottom:.85vh}
.row .nick{font-size:clamp(1.7rem,3.2vw,2.8rem)}
.row .price{font-size:clamp(1.8rem,3.4vw,3rem)}
""")

# 14 runway
save(14,"runway-bottles","ランウェイ",f"""
<div class="stage">
<img class="bg" src="../assets/moet/moet-bg.png" alt=""/>
<div class="shade"></div>
<div class="run">
<img src="../assets/moet/cut/brut.png" alt=""/><img src="../assets/moet/cut/rose.png" alt=""/><img src="../assets/moet/cut/nectar.png" alt=""/><img src="../assets/moet/cut/ice.png" alt=""/><img src="../assets/moet/cut/pika.png" alt=""/>
</div>
<div class="overlay"><p class="maison">MOËT &amp; CHANDON</p><h1 class="title">モエシリーズ</h1><div class="list">{R}</div></div>
</div>""","""
.stage{position:relative;width:100%;height:100%}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.28)}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,4,3,.75),rgba(6,4,3,.25) 40%,rgba(6,4,3,.92))}
.run{position:absolute;left:0;right:0;bottom:8%;height:58%;display:flex;justify-content:center;align-items:flex-end;gap:.8vw;z-index:1;perspective:800px}
.run img{height:85%;object-fit:contain;filter:drop-shadow(0 18px 30px rgba(0,0,0,.5));transform:translateY(0)}
.run img:nth-child(1){height:70%;opacity:.7;transform:translateY(8%) rotateY(18deg)}
.run img:nth-child(2){height:78%;opacity:.85;transform:translateY(4%) rotateY(8deg)}
.run img:nth-child(3){height:88%}
.run img:nth-child(4){height:78%;opacity:.85;transform:translateY(4%) rotateY(-8deg)}
.run img:nth-child(5){height:70%;opacity:.7;transform:translateY(8%) rotateY(-18deg)}
.overlay{position:absolute;left:0;right:0;top:0;z-index:2;padding:3vh 5vw 0;text-align:center}
.list{margin:1.5vh auto 0;max-width:1200px;display:grid;grid-template-columns:repeat(5,1fr);gap:1vw;text-align:center}
.row .nick{font-size:clamp(1.35rem,2.5vw,2.15rem)}
.row .formal{font-size:clamp(.95rem,1.3vw,1.15rem)}
.row .price{margin-top:.35rem;font-size:clamp(1.5rem,2.8vw,2.45rem)}
""")

# 15 overlay panel
save(15,"overlay-panel","オーバーレイパネル",f"""
<div class="stage">
<img class="bg" src="../assets/moet/moet-bg.png" alt=""/>
<img class="hero" src="../assets/moet/cut/pika.png" alt=""/>
<img class="side" src="../assets/moet/cut/ice.png" alt=""/>
<div class="glass"><p class="maison">MOËT &amp; CHANDON</p><h1 class="title">モエシリーズ</h1><div class="list">{R}</div></div>
</div>""","""
.stage{position:relative;width:100%;height:100%}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.35)}
.hero{position:absolute;left:8%;bottom:-8%;height:108%;z-index:1;filter:drop-shadow(0 0 45px rgba(255,90,60,.28))}
.side{position:absolute;left:32%;bottom:-2%;height:70%;opacity:.35;transform:rotate(8deg);z-index:0}
.glass{position:absolute;right:4vw;top:50%;transform:translateY(-50%);width:min(50vw,700px);z-index:2;padding:3vh 2.5vw;background:rgba(12,9,7,.58);border:1px solid rgba(255,255,255,.12);backdrop-filter:blur(16px);box-shadow:0 30px 80px rgba(0,0,0,.4)}
.list{margin-top:1.8vh;display:flex;flex-direction:column;gap:1vh}
.row{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;border-bottom:1px solid rgba(226,180,92,.25);padding-bottom:.85vh}
.row .nick{font-size:clamp(1.7rem,3.3vw,2.9rem)}
.row .price{font-size:clamp(1.8rem,3.5vw,3.1rem)}
""")

# 16 duo stage
save(16,"duo-stage","デュオステージ",f"""
<div class="stage">
<div class="half l"><img src="../assets/moet/cut/ice.png" alt=""/><span>ICE</span></div>
<div class="half r"><img src="../assets/moet/cut/pika.png" alt=""/><span>N.I.R</span></div>
<div class="center"><p class="maison">MOËT &amp; CHANDON</p><h1 class="title">モエシリーズ</h1><div class="list">{R}</div></div>
</div>""","""
.stage{position:relative;width:100%;height:100%;display:grid;grid-template-columns:1fr 1fr;background:#050303}
.half{position:relative;overflow:hidden;display:flex;align-items:flex-end;justify-content:center}
.l{background:linear-gradient(180deg,#12161a,#0a0c0e)}.r{background:linear-gradient(180deg,#1a0c10,#0a0507)}
.half img{height:88%;object-fit:contain;filter:drop-shadow(0 20px 40px rgba(0,0,0,.5))}
.half span{position:absolute;top:4vh;font-family:var(--serif);letter-spacing:.4em;color:rgba(255,255,255,.22);font-size:1rem}
.center{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:min(460px,86vw);z-index:3;background:rgba(8,6,5,.9);border:1px solid rgba(226,180,92,.45);padding:2.2rem 1.6rem;backdrop-filter:blur(10px)}
.maison,.title{text-align:center}
.title{font-size:clamp(1.8rem,3.5vw,2.6rem);margin:.35rem 0 1.2rem}
.list{display:flex;flex-direction:column;gap:.7vh}
.row{display:flex;justify-content:space-between;align-items:baseline;gap:.8rem}
.row .nick{font-size:clamp(1.2rem,2.2vw,1.7rem)}
.row .formal{display:none}
.row .price{font-size:clamp(1.25rem,2.3vw,1.85rem)}
""")

# 17 noir glamour
save(17,"noir-glamour","ノワールグラマー",f"""
<div class="stage">
<img class="bg" src="../assets/moet/moet-bg.png" alt=""/>
<div class="shade"></div>
<img class="hero" src="../assets/moet/cut/nectar.png" alt=""/>
<img class="glowbot" src="../assets/moet/cut/pika.png" alt=""/>
<div class="panel"><p class="maison">AFTER DARK</p><h1 class="title">モエシリーズ</h1><div class="list">{R}</div></div>
</div>""","""
.stage{position:relative;width:100%;height:100%}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.22) contrast(1.1)}
.shade{position:absolute;inset:0;background:linear-gradient(120deg,rgba(0,0,0,.2),rgba(0,0,0,.85) 60%)}
.hero{position:absolute;left:4%;bottom:-4%;height:98%;z-index:1;filter:drop-shadow(0 20px 40px rgba(0,0,0,.7))}
.glowbot{position:absolute;left:26%;bottom:-6%;height:70%;opacity:.28;z-index:0}
.panel{position:absolute;right:0;top:0;bottom:0;width:min(55vw,760px);z-index:2;padding:4vh 3.5vw;display:flex;flex-direction:column;justify-content:center}
.maison{color:#c9a;letter-spacing:.4em}
.list{margin-top:2vh;display:flex;flex-direction:column;gap:1.15vh}
.row{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;border-bottom:2px solid rgba(226,180,92,.22);padding-bottom:1vh}
""")

# 18 amber lounge
save(18,"amber-lounge","アンバーラウンジ",f"""
<div class="stage">
<img class="bg" src="../assets/moet/moet-bg.png" alt=""/>
<div class="amber"></div>
<img class="b1" src="../assets/moet/cut/brut.png" alt=""/>
<img class="b2" src="../assets/moet/cut/ice.png" alt=""/>
<img class="b3" src="../assets/moet/cut/pika.png" alt=""/>
<div class="panel"><p class="maison">MOËT &amp; CHANDON</p><h1 class="title">モエシリーズ</h1><div class="list">{R}</div></div>
</div>""","""
.stage{position:relative;width:100%;height:100%}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.3)}
.amber{position:absolute;inset:0;background:radial-gradient(ellipse at 25% 60%,rgba(226,140,60,.25),transparent 55%),linear-gradient(105deg,transparent 35%,rgba(6,4,3,.92) 68%)}
.b1{position:absolute;left:-2%;bottom:0;height:75%;opacity:.45;transform:rotate(-10deg);z-index:0}
.b2{position:absolute;left:8%;bottom:-3%;height:88%;opacity:.7;z-index:1}
.b3{position:absolute;left:20%;bottom:-8%;height:108%;z-index:2;filter:drop-shadow(0 0 40px rgba(255,120,60,.25))}
.panel{position:absolute;right:0;top:0;bottom:0;width:min(54vw,760px);z-index:3;padding:4vh 3.5vw;display:flex;flex-direction:column;justify-content:center}
.list{margin-top:2vh;display:flex;flex-direction:column;gap:1.15vh}
.row{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;border-bottom:2px solid rgba(226,180,92,.3);padding-bottom:1vh}
""")

# 19 vertical gallery
save(19,"vertical-gallery","バーチカルギャラリー",f"""
<div class="stage">
<div class="strip">
<img src="../assets/moet/cut/brut.png" alt=""/><img src="../assets/moet/cut/rose.png" alt=""/><img src="../assets/moet/cut/nectar.png" alt=""/><img src="../assets/moet/cut/ice.png" alt=""/><img src="../assets/moet/cut/pika.png" alt=""/>
</div>
<div class="main"><p class="maison">MOËT &amp; CHANDON</p><h1 class="title">モエシリーズ</h1><div class="list">{R}</div></div>
</div>""","""
.stage{display:grid;grid-template-columns:160px 1fr;height:100%;background:#0a0706}
.strip{background:linear-gradient(180deg,#16120f,#0c0a08);border-right:1px solid rgba(226,180,92,.3);display:flex;flex-direction:column;justify-content:space-evenly;padding:.6rem 0;overflow:hidden}
.strip img{height:16vh;margin:0 auto;filter:drop-shadow(0 8px 16px rgba(0,0,0,.45))}
.main{padding:4vh 4vw;display:flex;flex-direction:column;justify-content:center;background:radial-gradient(ellipse at 80% 20%,rgba(226,180,92,.12),transparent 45%)}
.list{margin-top:2.2vh;display:flex;flex-direction:column;gap:1.2vh;max-width:780px}
.row{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;border-bottom:2px solid rgba(226,180,92,.28);padding-bottom:1vh}
@media(max-width:800px){.stage{grid-template-columns:1fr}.strip{flex-direction:row;border:none;border-bottom:1px solid rgba(226,180,92,.3)}.strip img{height:10vh}}
""")

# 20 grand arrival
save(20,"grand-arrival","グランドアライバル",f"""
<div class="stage">
<img class="bg" src="../assets/moet/moet-bg.png" alt=""/>
<div class="shade"></div>
<img class="hero" src="../assets/moet/cut/pika.png" alt=""/>
<img class="a" src="../assets/moet/cut/rose.png" alt=""/>
<img class="b" src="../assets/moet/cut/ice.png" alt=""/>
<div class="content">
<p class="maison">WELCOME TO THE NIGHT</p>
<h1 class="title">モエシリーズ</h1>
<p class="lead">ボトルが開くたび、夜が華やぐ。</p>
<div class="list">{R}</div>
</div></div>""","""
.stage{position:relative;width:100%;height:100%}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.3)}
.shade{position:absolute;inset:0;background:linear-gradient(115deg,rgba(6,4,3,.15) 0%,rgba(6,4,3,.75) 48%,rgba(6,4,3,.96) 70%)}
.hero{position:absolute;left:12%;bottom:-10%;height:115%;z-index:2;filter:drop-shadow(0 0 55px rgba(255,100,70,.3))}
.a{position:absolute;left:-2%;bottom:0;height:78%;opacity:.4;transform:rotate(-12deg);z-index:1}
.b{position:absolute;left:30%;bottom:-2%;height:70%;opacity:.35;transform:rotate(10deg);z-index:1}
.content{position:absolute;right:0;top:0;bottom:0;width:min(54vw,760px);z-index:3;padding:4vh 3.5vw;display:flex;flex-direction:column;justify-content:center}
.lead{margin:.6rem 0 2vh;font-size:clamp(1.15rem,1.8vw,1.5rem);letter-spacing:.16em;color:var(--muted)}
.list{display:flex;flex-direction:column;gap:1.15vh}
.row{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;border-bottom:2px solid rgba(226,180,92,.3);padding-bottom:1vh}
""")

# nav + index
files={i:f"{i:02d}-{s}.html" for i,s,_ in META}
(D/"shared.css").write_text(SHARED,encoding="utf-8")
(D/"nav.js").write_text(f"""
window.DESIGN_FILES={files};
if(new URLSearchParams(location.search).get('shot')==='1'){{document.documentElement.classList.add('shot');document.addEventListener('DOMContentLoaded',()=>document.body.classList.add('shot'));}}
(()=>{{
  const m=(location.pathname.split('/').pop()||'').match(/^(\\d{{2}})-/);
  const n=m?parseInt(m[1],10):1; const total=Object.keys(DESIGN_FILES).length;
  const go=t=>{{const name=DESIGN_FILES[t]; if(name) location.href=name;}};
  document.addEventListener('keydown',e=>{{
    if(e.key==='ArrowRight'||e.key===' '){{e.preventDefault();go(n>=total?1:n+1);}}
    else if(e.key==='ArrowLeft'){{e.preventDefault();go(n<=1?total:n-1);}}
    else if(e.key==='Escape'||e.key==='g'||e.key==='G') location.href='../index.html';
  }});
}})();
""",encoding="utf-8")

blocks=[]
for num,slug,title in META:
    blocks.append(f'<section class="block" id="d{num:02d}"><h2>{num:02d} · {title}</h2><img src="previews/phone/{num:02d}-{slug}.jpg" alt="{title}"/></section>')

(ROOT/"index.html").write_text(f"""<!DOCTYPE html><html lang="ja"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"/>
<title>モエシリーズ デザイン案20（高級ラウンジ）</title>
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@600;700&family=Zen+Kaku+Gothic+New:wght@400;500&display=swap" rel="stylesheet"/>
<style>
:root{{--bg:#0a0806;--ink:#fff6ea;--gold:#e2b45c;--muted:rgba(255,246,234,.65)}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--ink);font-family:"Zen Kaku Gothic New",system-ui,sans-serif}}
header{{padding:1.1rem 1rem;position:sticky;top:0;z-index:10;background:rgba(10,8,6,.94);backdrop-filter:blur(10px);border-bottom:1px solid rgba(226,180,92,.3)}}
.eyebrow{{font-size:.7rem;letter-spacing:.28em;color:var(--gold)}}
h1{{font-family:"Shippori Mincho",serif;font-size:1.3rem;letter-spacing:.1em;margin:.35rem 0}}
.sub{{font-size:.84rem;color:var(--muted);line-height:1.65}}
.jump{{display:flex;gap:.35rem;overflow-x:auto;padding:.65rem 1rem;border-bottom:1px solid rgba(255,255,255,.06)}}
.jump a{{flex:0 0 auto;padding:.3rem .6rem;border:1px solid rgba(226,180,92,.4);color:var(--gold);text-decoration:none;border-radius:999px;font-size:.78rem}}
.block{{scroll-margin-top:6.2rem;padding:1rem 1rem 0}}
.block h2{{font-family:"Shippori Mincho",serif;font-size:1.05rem;letter-spacing:.08em;color:var(--gold);margin-bottom:.55rem}}
.block img{{width:100%;height:auto;display:block;border:1px solid rgba(226,180,92,.25);background:#111}}
.note{{padding:1.1rem 1rem 2.5rem;font-size:.84rem;color:var(--muted);line-height:1.7}}
</style></head><body>
<header>
<p class="eyebrow">CABARET / LOUNGE · LUXURY</p>
<h1>モエシリーズ デザイン案 20種</h1>
<p class="sub">文字だけはなし。ボトル写真あり・高級感・遠目でも読める大文字。下にスクロールして番号を送ってください。</p>
</header>
<nav class="jump">{''.join(f'<a href="#d{n:02d}">{n:02d}</a>' for n,_,__ in META)}</nav>
<main>{''.join(blocks)}<p class="note">採用したい番号（複数可）を送ってください。</p></main>
</body></html>""",encoding="utf-8")

(ROOT/"README.md").write_text("# Tachibana Moët — 高級ラウンジ向けデザイン案20\n\nボトル写真必須・大文字・高級感。`index.html` でスマホ確認。\n",encoding="utf-8")
print("DONE 20")
