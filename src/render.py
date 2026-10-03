#!/usr/bin/env python3
"""Renderiza carrosséis da SITH.IA (1080x1350) a partir de content/*.json.
Uso (a partir da raiz do projeto): python3 src/render.py conteudo/calendario/semana-2026-10-05.json
Saída: criativos/gerados/<semana>/<id-do-post>/slide-01.png ..."""
import base64, html, json, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
LOGO = "data:image/png;base64," + base64.b64encode((ROOT / "marca/assets/logo.png").read_bytes()).decode()

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#050507;color:#fff;font-family:'Poppins','Inter',sans-serif;
 position:relative;overflow:hidden}
.glow{position:absolute;right:-260px;bottom:-260px;width:900px;height:900px;border-radius:50%;
 background:radial-gradient(circle,rgba(79,91,255,.55),rgba(79,91,255,0) 65%)}
.glow2{position:absolute;left:-300px;top:-300px;width:700px;height:700px;border-radius:50%;
 background:radial-gradient(circle,rgba(79,91,255,.22),rgba(79,91,255,0) 65%)}
.line{position:absolute;left:-100px;right:-100px;bottom:230px;height:2px;
 background:linear-gradient(90deg,transparent,rgba(110,120,255,.7),transparent);transform:rotate(-14deg)}
.brand{position:absolute;top:70px;left:80px;display:flex;align-items:center;gap:26px}
.brand img{height:84px}
.brand span{font-size:30px;letter-spacing:.32em;font-weight:600}
.pager{position:absolute;top:96px;right:80px;font-size:22px;letter-spacing:.3em;color:#8d92b8}
.wrap{position:absolute;left:80px;right:80px;top:300px;bottom:200px;display:flex;flex-direction:column;justify-content:center}
.kicker{font-size:24px;letter-spacing:.35em;color:#8d92b8;margin-bottom:34px;display:flex;align-items:center;gap:20px}
.kicker:before{content:"";width:48px;height:2px;background:#4f5bff}
h1{font-size:104px;line-height:1.04;font-weight:700;letter-spacing:-.03em}
h2{font-size:84px;line-height:1.08;font-weight:700;letter-spacing:-.025em}
em{font-style:normal;background:linear-gradient(90deg,#4f5bff,#7a86ff);-webkit-background-clip:text;color:transparent}
.sub{font-size:38px;color:#c7c9de;margin-top:44px;line-height:1.35}
.num{font-size:200px;font-weight:700;line-height:1;color:transparent;-webkit-text-stroke:3px #4f5bff;margin-bottom:10px}
.card{border:2px solid rgba(110,120,255,.45);border-radius:36px;padding:56px;
 background:linear-gradient(145deg,rgba(79,91,255,.14),rgba(255,255,255,.02))}
.texto{font-size:42px;color:#d3d5ea;line-height:1.38;margin-top:36px}
.btn{display:inline-block;margin-top:60px;border:2px solid #4f5bff;border-radius:60px;padding:28px 64px;
 font-size:30px;letter-spacing:.3em;font-weight:600}
.foot{position:absolute;left:80px;bottom:70px;font-size:22px;letter-spacing:.3em;color:#6b7094}
.swipe{position:absolute;right:80px;bottom:70px;font-size:22px;letter-spacing:.3em;color:#8d92b8}
"""

def fmt(t):
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", html.escape(t))

def slide_html(s, i, n):
    t = s["tipo"]
    if t == "capa":
        body = f'<div class="kicker">{fmt(s["kicker"])}</div><h1>{fmt(s["titulo"])}</h1><div class="sub">{fmt(s.get("sub",""))}</div>'
    elif t == "item":
        body = f'<div class="card"><div class="num">{s["num"]}</div><h2>{fmt(s["titulo"])}</h2><div class="texto">{fmt(s["texto"])}</div></div>'
    else:
        body = f'<h1>{fmt(s["titulo"])}</h1><div class="sub">{fmt(s["sub"])}</div><div><span class="btn">{fmt(s["botao"])} &rarr;</span></div>'
    swipe = '<div class="swipe">ARRASTE &rarr;</div>' if i < n - 1 else ""
    return (f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            f'<div class="glow2"></div><div class="glow"></div><div class="line"></div>'
            f'<div class="brand"><img src="{LOGO}"><span>SITH.IA</span></div>'
            f'<div class="pager">{i+1:02d} / {n:02d}</div>'
            f'<div class="wrap">{body}</div>'
            f'<div class="foot">CRIATIVIDADE · TECNOLOGIA · RESULTADOS</div>{swipe}</body></html>')

def main(path):
    data = json.loads(Path(path).read_text())
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for post in data["posts"]:
            d = ROOT / "criativos" / "gerados" / data["semana"] / post["id"]
            d.mkdir(parents=True, exist_ok=True)
            n = len(post["slides"])
            for i, s in enumerate(post["slides"]):
                pg.set_content(slide_html(s, i, n))
                pg.screenshot(path=str(d / f"slide-{i+1:02d}.png"))
            print(f"ok {post['id']}: {n} slides")
        b.close()

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "conteudo/calendario/semana-2026-10-05.json")
