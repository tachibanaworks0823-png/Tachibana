#!/usr/bin/env python3
"""20 variants based on Design 07 (gold rule + dynamic left bottles).
Right menu panel stays identical; left photo drama varies.
"""
from pathlib import Path

ROOT = Path("/workspace")
D = ROOT / "designs"
D.mkdir(exist_ok=True)

for p in D.glob("*"):
    if p.name in ("shared.css", "nav.js"):
        continue
    if p.suffix in {".html", ".css"}:
        p.unlink()

META = [
    (1, "base", "ベース（現行07）"),
    (2, "pika-hero", "ピカ特大ヒーロー"),
    (3, "ice-surge", "アイスが金ラインへ"),
    (4, "rose-fan", "ロゼ主導の扇状"),
    (5, "five-wall", "5本で壁のように埋める"),
    (6, "diagonal-rise", "左下から右上へ斜め上昇"),
    (7, "tight-crop", "寄りトリミング・迫力"),
    (8, "stagger-depth", "遠近を強くした奥行き"),
    (9, "duo-front", "ピカ＋アイスの二枚看板"),
    (10, "cascade", "左から階段状カスケード"),
    (11, "spill-right", "文字側へ大きくはみ出し"),
    (12, "low-angle", "ローアングル・足元強調"),
    (13, "label-line", "ラベルが読める高さ"),
    (14, "noir-glow", "深ノワール＋ピカ発光"),
    (15, "warm-haze", "暖色ヘイズ"),
    (16, "cool-steel", "クールスチール"),
    (17, "cross-tilt", "交差する強い傾き"),
    (18, "ghost-echo", "半透明エコー重ね"),
    (19, "trio-focus", "3本フォーカス＋2影"),
    (20, "bar-reflect", "バー反射感"),
]

# Bottle order per design: (src, class) list — classes b1..b5
ORDERS = {
    1: ["brut", "rose", "nectar", "pika", "ice"],
    2: ["brut", "nectar", "rose", "ice", "pika"],  # pika as b5→remap via CSS hero
    3: ["rose", "brut", "nectar", "pika", "ice"],
    4: ["brut", "nectar", "ice", "pika", "rose"],
    5: ["brut", "rose", "nectar", "ice", "pika"],
    6: ["brut", "rose", "nectar", "ice", "pika"],
    7: ["brut", "rose", "nectar", "pika", "ice"],
    8: ["brut", "rose", "nectar", "pika", "ice"],
    9: ["brut", "rose", "nectar", "pika", "ice"],
    10: ["brut", "rose", "nectar", "pika", "ice"],
    11: ["brut", "rose", "nectar", "pika", "ice"],
    12: ["brut", "rose", "nectar", "pika", "ice"],
    13: ["brut", "rose", "nectar", "pika", "ice"],
    14: ["brut", "rose", "nectar", "pika", "ice"],
    15: ["brut", "rose", "nectar", "pika", "ice"],
    16: ["brut", "rose", "nectar", "pika", "ice"],
    17: ["brut", "rose", "nectar", "pika", "ice"],
    18: ["brut", "rose", "nectar", "pika", "ice"],
    19: ["brut", "rose", "nectar", "pika", "ice"],
    20: ["brut", "rose", "nectar", "pika", "ice"],
}

# Special: for 2 pika-hero put pika as b4 (hero slot); for 3 ice as b5; for 4 rose as b5
ORDERS[2] = ["brut", "nectar", "rose", "pika", "ice"]
ORDERS[3] = ["brut", "rose", "nectar", "pika", "ice"]
ORDERS[4] = ["brut", "nectar", "ice", "pika", "rose"]
ORDERS[9] = ["brut", "rose", "nectar", "pika", "ice"]

PANEL_CSS = """
.panel{position:absolute;right:0;top:0;bottom:0;width:min(56vw,800px);z-index:3;padding:3.5vh 3.5vw;display:flex;flex-direction:column;justify-content:center;padding-left:4.2vw}
.list{margin-top:2vh;display:flex;flex-direction:column;gap:1.2vh}
.row{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;border-bottom:3px solid rgba(226,180,92,.45);padding-bottom:1vh}
.is-hot{border-bottom-color:var(--gold2)}
.panel::before{content:"";position:absolute;left:0;top:12%;bottom:12%;width:2px;background:linear-gradient(180deg,transparent,var(--gold),transparent)}
.ghost{display:none}.floor{display:none}
"""

DRIFT = """
@keyframes driftA{0%,100%{transform:rotate(var(--r1,-12deg)) translate3d(0,0,0)}50%{transform:rotate(calc(var(--r1,-12deg) + 2deg)) translate3d(1.4%,-1.5%,0)}}
@keyframes driftB{0%,100%{transform:rotate(var(--r2,5deg)) translate3d(0,0,0)}50%{transform:rotate(calc(var(--r2,5deg) - 1.5deg)) translate3d(-.9%,-2%,0)}}
@keyframes driftC{0%,100%{transform:rotate(var(--r3,-3deg)) translate3d(0,0,0)}50%{transform:rotate(calc(var(--r3,-3deg) + 1.5deg)) translate3d(1%,-2.2%,0)}}
@keyframes driftD{0%,100%{transform:rotate(var(--r4,2deg)) translate3d(0,0,0) scale(1)}50%{transform:rotate(calc(var(--r4,2deg) - 1deg)) translate3d(-.7%,-2.6%,0) scale(1.025)}}
@keyframes driftE{0%,100%{transform:rotate(var(--r5,-7deg)) translate3d(0,0,0)}50%{transform:rotate(calc(var(--r5,-7deg) + 2deg)) translate3d(1.5%,-1.6%,0)}}
@media (prefers-reduced-motion:reduce){.b1,.b2,.b3,.b4,.b5{animation:none!important}}
"""

BASE_STAGE = """
.stage{position:relative;width:100%;height:100%}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.32)}
.shade{position:absolute;inset:0;z-index:1}
.drama{position:absolute;left:0;top:0;bottom:0;width:78%;z-index:2;pointer-events:none;overflow:visible}
.b{position:absolute;object-fit:contain;filter:drop-shadow(0 30px 60px rgba(0,0,0,.75));will-change:transform}
.b1{z-index:1;animation:driftA 7.5s ease-in-out infinite}
.b2{z-index:2;animation:driftB 8.5s ease-in-out infinite}
.b3{z-index:3;animation:driftC 6.8s ease-in-out infinite}
.b4{z-index:5;animation:driftD 7.2s ease-in-out infinite}
.b5{z-index:4;animation:driftE 9s ease-in-out infinite}
"""

# Default positions = current 07
DEFAULT_POS = """
.shade{background:linear-gradient(100deg,rgba(6,4,3,.02) 0%,rgba(6,4,3,.28) 34%,rgba(6,4,3,.78) 58%,rgba(6,4,3,.96) 72%)}
.b1{left:-14%;bottom:-18%;height:108%;opacity:.38;--r1:-14deg;transform:rotate(-14deg)}
.b2{left:2%;bottom:-14%;height:118%;opacity:.58;--r2:6deg;transform:rotate(6deg)}
.b3{left:16%;bottom:-10%;height:128%;opacity:.82;--r3:-4deg;transform:rotate(-4deg)}
.b4{left:34%;bottom:-6%;height:138%;opacity:1;--r4:2deg;transform:rotate(2deg)}
.b5{left:52%;bottom:-12%;height:122%;opacity:.78;--r5:-8deg;transform:rotate(-8deg)}
"""

VARIANT_CSS = {
    1: DEFAULT_POS,
    2: """
.shade{background:linear-gradient(100deg,rgba(6,4,3,.02) 0%,rgba(6,4,3,.22) 30%,rgba(6,4,3,.78) 56%,rgba(6,4,3,.96) 72%)}
.b1{left:-18%;bottom:-22%;height:100%;opacity:.28;--r1:-16deg;transform:rotate(-16deg)}
.b2{left:-2%;bottom:-16%;height:112%;opacity:.48;--r2:8deg;transform:rotate(8deg)}
.b3{left:12%;bottom:-12%;height:120%;opacity:.7;--r3:-5deg;transform:rotate(-5deg)}
.b4{left:28%;bottom:-4%;height:148%;opacity:1;--r4:1deg;transform:rotate(1deg);filter:drop-shadow(0 0 70px rgba(255,80,40,.45)) drop-shadow(0 30px 60px rgba(0,0,0,.75))}
.b5{left:50%;bottom:-14%;height:118%;opacity:.65;--r5:-9deg;transform:rotate(-9deg)}
""",
    3: """
.shade{background:linear-gradient(100deg,rgba(6,4,3,.02) 0%,rgba(6,4,3,.28) 34%,rgba(6,4,3,.78) 58%,rgba(6,4,3,.96) 72%)}
.b1{left:-12%;bottom:-16%;height:102%;opacity:.32;--r1:-11deg;transform:rotate(-11deg)}
.b2{left:4%;bottom:-12%;height:114%;opacity:.55;--r2:5deg;transform:rotate(5deg)}
.b3{left:18%;bottom:-10%;height:122%;opacity:.72;--r3:-3deg;transform:rotate(-3deg)}
.b4{left:30%;bottom:-8%;height:130%;opacity:.88;--r4:2deg;transform:rotate(2deg)}
.b5{left:46%;bottom:-6%;height:140%;opacity:1;--r5:-4deg;transform:rotate(-4deg);z-index:6;filter:drop-shadow(0 0 40px rgba(180,210,255,.25)) drop-shadow(0 30px 60px rgba(0,0,0,.75))}
""",
    4: """
.shade{background:linear-gradient(105deg,rgba(40,10,18,.15),rgba(6,4,3,.55) 45%,rgba(6,4,3,.96) 70%)}
.b1{left:-16%;bottom:-20%;height:104%;opacity:.3;--r1:-13deg;transform:rotate(-13deg)}
.b2{left:0%;bottom:-14%;height:116%;opacity:.5;--r2:7deg;transform:rotate(7deg)}
.b3{left:14%;bottom:-10%;height:124%;opacity:.68;--r3:-2deg;transform:rotate(-2deg)}
.b4{left:28%;bottom:-8%;height:132%;opacity:.85;--r4:3deg;transform:rotate(3deg)}
.b5{left:44%;bottom:-5%;height:142%;opacity:1;--r5:-6deg;transform:rotate(-6deg);z-index:6;filter:drop-shadow(0 0 50px rgba(232,160,168,.35)) drop-shadow(0 30px 60px rgba(0,0,0,.75))}
""",
    5: """
.shade{background:linear-gradient(100deg,rgba(6,4,3,.0) 0%,rgba(6,4,3,.2) 28%,rgba(6,4,3,.75) 55%,rgba(6,4,3,.96) 70%)}
.drama{width:82%}
.b1{left:-8%;bottom:-14%;height:118%;opacity:.55;--r1:-6deg;transform:rotate(-6deg)}
.b2{left:8%;bottom:-12%;height:122%;opacity:.7;--r2:4deg;transform:rotate(4deg)}
.b3{left:22%;bottom:-10%;height:126%;opacity:.85;--r3:-2deg;transform:rotate(-2deg)}
.b4{left:36%;bottom:-8%;height:130%;opacity:.95;--r4:2deg;transform:rotate(2deg)}
.b5{left:50%;bottom:-10%;height:124%;opacity:.9;--r5:-5deg;transform:rotate(-5deg)}
""",
    6: """
.shade{background:linear-gradient(115deg,rgba(6,4,3,.05),rgba(6,4,3,.5) 40%,rgba(6,4,3,.96) 68%)}
.b1{left:-10%;bottom:-28%;height:95%;opacity:.4;--r1:-18deg;transform:rotate(-18deg)}
.b2{left:6%;bottom:-18%;height:110%;opacity:.6;--r2:8deg;transform:rotate(8deg)}
.b3{left:20%;bottom:-8%;height:122%;opacity:.8;--r3:-6deg;transform:rotate(-6deg)}
.b4{left:36%;bottom:0%;height:132%;opacity:1;--r4:4deg;transform:rotate(4deg)}
.b5{left:52%;bottom:6%;height:118%;opacity:.75;--r5:-10deg;transform:rotate(-10deg)}
""",
    7: """
.shade{background:linear-gradient(100deg,rgba(6,4,3,.0) 0%,rgba(6,4,3,.25) 32%,rgba(6,4,3,.8) 58%,rgba(6,4,3,.98) 72%)}
.b1{left:-20%;bottom:-28%;height:120%;opacity:.35;--r1:-12deg;transform:rotate(-12deg)}
.b2{left:-4%;bottom:-24%;height:132%;opacity:.55;--r2:5deg;transform:rotate(5deg)}
.b3{left:12%;bottom:-20%;height:142%;opacity:.8;--r3:-3deg;transform:rotate(-3deg)}
.b4{left:30%;bottom:-16%;height:155%;opacity:1;--r4:1deg;transform:rotate(1deg)}
.b5{left:50%;bottom:-22%;height:138%;opacity:.78;--r5:-7deg;transform:rotate(-7deg)}
""",
    8: """
.shade{background:linear-gradient(100deg,rgba(6,4,3,.08) 0%,rgba(6,4,3,.35) 36%,rgba(6,4,3,.85) 60%,rgba(6,4,3,.97) 74%)}
.b1{left:-18%;bottom:-10%;height:88%;opacity:.22;--r1:-8deg;transform:rotate(-8deg) scale(.92)}
.b2{left:0%;bottom:-12%;height:102%;opacity:.4;--r2:6deg;transform:rotate(6deg)}
.b3{left:16%;bottom:-10%;height:118%;opacity:.65;--r3:-3deg;transform:rotate(-3deg)}
.b4{left:34%;bottom:-6%;height:142%;opacity:1;--r4:2deg;transform:rotate(2deg)}
.b5{left:54%;bottom:-14%;height:110%;opacity:.55;--r5:-9deg;transform:rotate(-9deg)}
""",
    9: """
.shade{background:linear-gradient(100deg,rgba(6,4,3,.02) 0%,rgba(6,4,3,.28) 34%,rgba(6,4,3,.78) 58%,rgba(6,4,3,.96) 72%)}
.b1{left:-16%;bottom:-20%;height:96%;opacity:.25;--r1:-14deg;transform:rotate(-14deg)}
.b2{left:-2%;bottom:-16%;height:108%;opacity:.4;--r2:7deg;transform:rotate(7deg)}
.b3{left:12%;bottom:-12%;height:115%;opacity:.55;--r3:-4deg;transform:rotate(-4deg)}
.b4{left:26%;bottom:-4%;height:145%;opacity:1;--r4:3deg;transform:rotate(3deg);filter:drop-shadow(0 0 55px rgba(255,70,35,.4)) drop-shadow(0 30px 60px rgba(0,0,0,.75))}
.b5{left:46%;bottom:-6%;height:140%;opacity:.95;--r5:-5deg;transform:rotate(-5deg);z-index:6}
""",
    10: """
.shade{background:linear-gradient(100deg,rgba(6,4,3,.02) 0%,rgba(6,4,3,.3) 35%,rgba(6,4,3,.8) 58%,rgba(6,4,3,.96) 72%)}
.b1{left:-6%;bottom:-22%;height:100%;opacity:.45;--r1:-5deg;transform:rotate(-5deg)}
.b2{left:8%;bottom:-16%;height:112%;opacity:.6;--r2:3deg;transform:rotate(3deg)}
.b3{left:22%;bottom:-10%;height:124%;opacity:.78;--r3:-2deg;transform:rotate(-2deg)}
.b4{left:36%;bottom:-4%;height:136%;opacity:1;--r4:1deg;transform:rotate(1deg)}
.b5{left:50%;bottom:2%;height:120%;opacity:.82;--r5:-4deg;transform:rotate(-4deg)}
""",
    11: """
.shade{background:linear-gradient(95deg,rgba(6,4,3,.0) 0%,rgba(6,4,3,.18) 30%,rgba(6,4,3,.7) 52%,rgba(6,4,3,.95) 68%)}
.drama{width:88%}
.b1{left:-10%;bottom:-16%;height:110%;opacity:.35;--r1:-12deg;transform:rotate(-12deg)}
.b2{left:6%;bottom:-12%;height:120%;opacity:.55;--r2:5deg;transform:rotate(5deg)}
.b3{left:22%;bottom:-8%;height:130%;opacity:.78;--r3:-3deg;transform:rotate(-3deg)}
.b4{left:40%;bottom:-4%;height:142%;opacity:1;--r4:2deg;transform:rotate(2deg)}
.b5{left:58%;bottom:-10%;height:128%;opacity:.85;--r5:-7deg;transform:rotate(-7deg)}
""",
    12: """
.shade{background:linear-gradient(100deg,rgba(6,4,3,.05) 0%,rgba(6,4,3,.35) 38%,rgba(6,4,3,.88) 62%,rgba(6,4,3,.98) 76%)}
.b1{left:-14%;bottom:-32%;height:115%;opacity:.4;--r1:-10deg;transform:rotate(-10deg)}
.b2{left:2%;bottom:-28%;height:125%;opacity:.6;--r2:6deg;transform:rotate(6deg)}
.b3{left:18%;bottom:-24%;height:135%;opacity:.82;--r3:-3deg;transform:rotate(-3deg)}
.b4{left:36%;bottom:-20%;height:148%;opacity:1;--r4:2deg;transform:rotate(2deg)}
.b5{left:54%;bottom:-26%;height:132%;opacity:.75;--r5:-8deg;transform:rotate(-8deg)}
""",
    13: """
.shade{background:linear-gradient(100deg,rgba(6,4,3,.02) 0%,rgba(6,4,3,.28) 34%,rgba(6,4,3,.78) 58%,rgba(6,4,3,.96) 72%)}
.b1{left:-12%;bottom:2%;height:92%;opacity:.4;--r1:-10deg;transform:rotate(-10deg)}
.b2{left:4%;bottom:4%;height:98%;opacity:.58;--r2:5deg;transform:rotate(5deg)}
.b3{left:18%;bottom:6%;height:104%;opacity:.8;--r3:-3deg;transform:rotate(-3deg)}
.b4{left:34%;bottom:4%;height:112%;opacity:1;--r4:2deg;transform:rotate(2deg)}
.b5{left:50%;bottom:2%;height:100%;opacity:.78;--r5:-6deg;transform:rotate(-6deg)}
""",
    14: """
.bg{filter:brightness(.22)}
.shade{background:linear-gradient(100deg,rgba(0,0,0,.15) 0%,rgba(0,0,0,.45) 40%,rgba(0,0,0,.92) 65%,rgba(0,0,0,.98) 78%)}
.b1{left:-14%;bottom:-18%;height:108%;opacity:.28;--r1:-14deg;transform:rotate(-14deg)}
.b2{left:2%;bottom:-14%;height:118%;opacity:.42;--r2:6deg;transform:rotate(6deg)}
.b3{left:16%;bottom:-10%;height:128%;opacity:.62;--r3:-4deg;transform:rotate(-4deg)}
.b4{left:34%;bottom:-6%;height:142%;opacity:1;--r4:2deg;transform:rotate(2deg);filter:drop-shadow(0 0 80px rgba(255,60,30,.55)) drop-shadow(0 30px 60px rgba(0,0,0,.85))}
.b5{left:52%;bottom:-12%;height:122%;opacity:.55;--r5:-8deg;transform:rotate(-8deg)}
""",
    15: """
.bg{filter:brightness(.36) sepia(.25) saturate(1.15)}
.shade{background:linear-gradient(100deg,rgba(50,22,8,.12) 0%,rgba(30,14,6,.4) 38%,rgba(10,6,4,.88) 62%,rgba(6,4,3,.97) 76%)}
.b1{left:-14%;bottom:-18%;height:108%;opacity:.4;--r1:-14deg;transform:rotate(-14deg)}
.b2{left:2%;bottom:-14%;height:118%;opacity:.6;--r2:6deg;transform:rotate(6deg)}
.b3{left:16%;bottom:-10%;height:128%;opacity:.84;--r3:-4deg;transform:rotate(-4deg)}
.b4{left:34%;bottom:-6%;height:138%;opacity:1;--r4:2deg;transform:rotate(2deg)}
.b5{left:52%;bottom:-12%;height:122%;opacity:.8;--r5:-8deg;transform:rotate(-8deg)}
""",
    16: """
.bg{filter:brightness(.3) hue-rotate(12deg) saturate(.85)}
.shade{background:linear-gradient(100deg,rgba(8,12,22,.1) 0%,rgba(6,8,16,.4) 38%,rgba(4,5,10,.88) 62%,rgba(3,3,6,.98) 76%)}
.b1{left:-14%;bottom:-18%;height:108%;opacity:.36;--r1:-14deg;transform:rotate(-14deg)}
.b2{left:2%;bottom:-14%;height:118%;opacity:.55;--r2:6deg;transform:rotate(6deg)}
.b3{left:16%;bottom:-10%;height:128%;opacity:.8;--r3:-4deg;transform:rotate(-4deg)}
.b4{left:34%;bottom:-6%;height:138%;opacity:1;--r4:2deg;transform:rotate(2deg)}
.b5{left:52%;bottom:-12%;height:122%;opacity:.82;--r5:-8deg;transform:rotate(-8deg);filter:drop-shadow(0 0 35px rgba(140,180,255,.2)) drop-shadow(0 30px 60px rgba(0,0,0,.75))}
""",
    17: """
.shade{background:linear-gradient(100deg,rgba(6,4,3,.02) 0%,rgba(6,4,3,.28) 34%,rgba(6,4,3,.78) 58%,rgba(6,4,3,.96) 72%)}
.b1{left:-16%;bottom:-18%;height:112%;opacity:.4;--r1:-22deg;transform:rotate(-22deg)}
.b2{left:2%;bottom:-14%;height:120%;opacity:.58;--r2:16deg;transform:rotate(16deg)}
.b3{left:18%;bottom:-10%;height:128%;opacity:.8;--r3:-14deg;transform:rotate(-14deg)}
.b4{left:34%;bottom:-6%;height:140%;opacity:1;--r4:10deg;transform:rotate(10deg)}
.b5{left:52%;bottom:-12%;height:124%;opacity:.78;--r5:-18deg;transform:rotate(-18deg)}
""",
    18: """
.shade{background:linear-gradient(100deg,rgba(6,4,3,.02) 0%,rgba(6,4,3,.28) 34%,rgba(6,4,3,.78) 58%,rgba(6,4,3,.96) 72%)}
.b1{left:-8%;bottom:-10%;height:125%;opacity:.18;--r1:-8deg;transform:rotate(-8deg) scale(1.05);filter:blur(1px) drop-shadow(0 30px 60px rgba(0,0,0,.4))}
.b2{left:10%;bottom:-8%;height:130%;opacity:.22;--r2:5deg;transform:rotate(5deg) scale(1.04);filter:blur(.8px) drop-shadow(0 30px 60px rgba(0,0,0,.4))}
.b3{left:14%;bottom:-12%;height:122%;opacity:.75;--r3:-4deg;transform:rotate(-4deg)}
.b4{left:32%;bottom:-6%;height:138%;opacity:1;--r4:2deg;transform:rotate(2deg)}
.b5{left:50%;bottom:-12%;height:120%;opacity:.8;--r5:-7deg;transform:rotate(-7deg)}
""",
    19: """
.shade{background:linear-gradient(100deg,rgba(6,4,3,.04) 0%,rgba(6,4,3,.3) 34%,rgba(6,4,3,.8) 58%,rgba(6,4,3,.96) 72%)}
.b1{left:-12%;bottom:-16%;height:105%;opacity:.2;--r1:-12deg;transform:rotate(-12deg)}
.b2{left:4%;bottom:-12%;height:128%;opacity:.9;--r2:5deg;transform:rotate(5deg);z-index:4}
.b3{left:22%;bottom:-8%;height:136%;opacity:1;--r3:-2deg;transform:rotate(-2deg);z-index:5}
.b4{left:40%;bottom:-6%;height:142%;opacity:1;--r4:2deg;transform:rotate(2deg);z-index:6;filter:drop-shadow(0 0 50px rgba(255,80,40,.35)) drop-shadow(0 30px 60px rgba(0,0,0,.75))}
.b5{left:58%;bottom:-14%;height:108%;opacity:.22;--r5:-8deg;transform:rotate(-8deg);z-index:2}
""",
    20: """
.shade{background:linear-gradient(100deg,rgba(6,4,3,.02) 0%,rgba(6,4,3,.28) 34%,rgba(6,4,3,.78) 58%,rgba(6,4,3,.96) 72%)}
.b1{left:-14%;bottom:-18%;height:108%;opacity:.38;--r1:-14deg;transform:rotate(-14deg)}
.b2{left:2%;bottom:-14%;height:118%;opacity:.58;--r2:6deg;transform:rotate(6deg)}
.b3{left:16%;bottom:-10%;height:128%;opacity:.82;--r3:-4deg;transform:rotate(-4deg)}
.b4{left:34%;bottom:-6%;height:138%;opacity:1;--r4:2deg;transform:rotate(2deg)}
.b5{left:52%;bottom:-12%;height:122%;opacity:.78;--r5:-8deg;transform:rotate(-8deg)}
.floor{display:block;position:absolute;left:0;right:42%;bottom:0;height:18%;z-index:2;pointer-events:none;
  background:linear-gradient(180deg,transparent,rgba(226,180,92,.06));
  -webkit-mask-image:linear-gradient(180deg,transparent,black);
  mask-image:linear-gradient(180deg,transparent,black);
  transform:scaleY(-1);opacity:.55;mix-blend-mode:screen}
.drama::after{content:"";position:absolute;left:5%;right:20%;bottom:0;height:14%;
  background:linear-gradient(180deg,rgba(255,246,234,.08),transparent);filter:blur(8px);opacity:.5}
""",
}

FORMAL = {
    "モエシロ": "モエ・エ・シャンドン ブリュット アンペリアル",
    "モエロゼ": "モエ・エ・シャンドン ロゼ アンペリアル",
    "モエ黒": "モエ・エ・シャンドン ネクター アンペリアル",
    "モエアイス": "モエ・エ・シャンドン アイス アンペリアル",
    "モエピカ": "モエ・エ・シャンドン N.I.R ロゼ ドライ",
}
ROWS = [
    ("モエシロ", "¥20,000", False),
    ("モエロゼ", "¥25,000", False),
    ("モエ黒", "¥30,000", False),
    ("モエアイス", "¥35,000", False),
    ("モエピカ", "¥40,000", True),
]

PANEL_HTML = "".join(
    f'<div class="row{" is-hot" if hot else ""}"><div><p class="nick">{nick}</p>'
    f'<p class="formal">{FORMAL[nick]}</p></div><p class="price">{price}</p></div>'
    for nick, price, hot in ROWS
)


def html_for(n, slug, title, bottles):
    imgs = "\n".join(
        f'<img class="b b{i}" src="../assets/moet/cut/{name}.png" alt=""/>'
        for i, name in enumerate(bottles, 1)
    )
    floor = '<div class="floor"></div>' if n == 20 else ""
    return f"""<!DOCTYPE html><html lang="ja"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Design {n:02d} — {title}</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Shippori+Mincho:wght@600;700&family=Zen+Kaku+Gothic+New:wght@500;700&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="shared.css"/><link rel="stylesheet" href="{n:02d}-{slug}.css"/>
</head><body>
<a class="back" href="../index.html">← 一覧</a>
<div class="badge">DESIGN {n:02d} · {title}</div>

<div class="stage">
<img class="bg" src="../assets/moet/moet-bg.png" alt=""/>
<div class="shade"></div>
{floor}
<div class="drama">
{imgs}
</div>
<div class="panel">
<p class="maison">MOËT &amp; CHANDON</p>
<h1 class="title">モエシリーズ</h1>
<div class="list">{PANEL_HTML}</div>
</div>
</div>

<script>if(new URLSearchParams(location.search).get('shot')==='1'){{document.documentElement.classList.add('shot');document.addEventListener('DOMContentLoaded',()=>document.body.classList.add('shot'));}}</script>
<script src="nav.js"></script></body></html>
"""


# Ensure shared.css exists with gold-rule friendly styles
(D / "shared.css").write_text(
    """
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
""".lstrip(),
    encoding="utf-8",
)

for n, slug, title in META:
    css = BASE_STAGE + PANEL_CSS + DRIFT + VARIANT_CSS[n]
    (D / f"{n:02d}-{slug}.css").write_text(css.strip() + "\n", encoding="utf-8")
    (D / f"{n:02d}-{slug}.html").write_text(
        html_for(n, slug, title, ORDERS[n]), encoding="utf-8"
    )

blocks = []
jumps = []
for n, slug, title in META:
    jumps.append(f'<a href="#d{n:02d}">{n:02d}</a>')
    blocks.append(
        f'<section class="block" id="d{n:02d}"><h2>{n:02d} · {title}</h2>'
        f'<img src="previews/phone/{n:02d}-{slug}.jpg" alt="{title}"/>'
        f'<p class="open"><a href="designs/{n:02d}-{slug}.html">フル画面で見る</a></p></section>'
    )

(ROOT / "index.html").write_text(
    f"""<!DOCTYPE html><html lang="ja"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"/>
<title>07金ライン強調ベース 20案</title>
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
.open{{margin:.45rem 0 0;font-size:.8rem}}
.open a{{color:var(--gold);text-decoration:none}}
.note{{padding:1.1rem 1rem 2.5rem;font-size:.84rem;color:var(--muted);line-height:1.7}}
</style></head><body>
<header>
<p class="eyebrow">BASED ON 07 · GOLD RULE DYNAMIC</p>
<h1>07ベースの派生案 20種</h1>
<p class="sub">右メニュー（金ライン・文字）は固定。左ボトルの構図・色味・迫力だけ変えています。番号を送ってください。</p>
</header>
<nav class="jump">{"".join(jumps)}</nav>
<main>{"".join(blocks)}<p class="note">近い案の番号（複数可）を送ってください。</p></main>
</body></html>
""",
    encoding="utf-8",
)

(ROOT / "README.md").write_text(
    "# 07 金ライン強調ベース派生20案\n\n"
    "採用した Design 07 をベースに、右側メニューは固定・左側ボトル構図を変えたバリエーション。"
    "`index.html` で確認。\n",
    encoding="utf-8",
)

print("generated", len(META), "designs")
for n, slug, title in META:
    print(f"  {n:02d} {slug} — {title}")
