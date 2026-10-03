#!/usr/bin/env python3
"""Renderiza o carrossel de PORTFÓLIO (conceito fictício ALVA) em 1080x1350.
Uso: python3 src/render_portfolio.py
Saída: criativos/gerados/2026-10-07/qua-portfolio-alva/slide-01..06.png
Slides 2-4 = peças do projeto (cores da marca fictícia). Slide 1 = bastidor (monta as peças num monitor). Slides 5-6 = moldura SITH.IA."""
import base64, io
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "criativos/gerados/2026-10-07/qua-portfolio-alva"
LOGO = "data:image/png;base64," + base64.b64encode((ROOT / "marca/assets/logo.png").read_bytes()).decode()
SAND, BONE, INK, CLAY = "#E8DFD2", "#F6F2EB", "#2A2320", "#C06A4B"

BASE = """*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;overflow:hidden;position:relative;font-family:'Poppins','Inter',sans-serif}"""

def bottle(kind, x, y, s=1.0, body="#D9C7B2", cap="#2A2320", label="#F6F2EB"):
    """Frascos minimalistas em SVG. kind: serum | cleanser | jar. (x,y) = base central."""
    if kind == "serum":
        w,h=150,300
        g=f'''<rect x="{-w/2}" y="{-h}" width="{w}" height="{h-40}" rx="34" fill="url(#b)"/>
<rect x="{-w/2}" y="{-h+20}" width="{w}" height="{h-60}" rx="34" fill="url(#hl)" opacity=".55"/>
<rect x="{-34}" y="{-h-70}" width="68" height="74" rx="14" fill="{cap}"/>
<rect x="{-17}" y="{-h-150}" width="34" height="90" rx="17" fill="{cap}"/>
<rect x="{-48}" y="{-h+110}" width="96" height="86" rx="6" fill="{label}" opacity=".92"/>
<text x="0" y="{-h+160}" text-anchor="middle" font-size="22" letter-spacing="7" fill="{cap}" font-weight="500">ALVA</text>
<text x="0" y="{-h+182}" text-anchor="middle" font-size="9" letter-spacing="3" fill="{cap}">SERUM Nº1</text>'''
    elif kind == "cleanser":
        w,h=170,380
        g=f'''<rect x="{-w/2}" y="{-h}" width="{w}" height="{h-0}" rx="40" fill="url(#b)"/>
<rect x="{-w/2}" y="{-h+20}" width="{w}" height="{h-40}" rx="40" fill="url(#hl)" opacity=".55"/>
<rect x="{-46}" y="{-h-62}" width="92" height="66" rx="16" fill="{cap}"/>
<rect x="{-54}" y="{-h+170}" width="108" height="110" rx="6" fill="{label}" opacity=".92"/>
<text x="0" y="{-h+228}" text-anchor="middle" font-size="24" letter-spacing="8" fill="{cap}" font-weight="500">ALVA</text>
<text x="0" y="{-h+254}" text-anchor="middle" font-size="9.5" letter-spacing="3" fill="{cap}">LIMPEZA SUAVE</text>'''
    else:
        w,h=230,170
        g=f'''<rect x="{-w/2}" y="{-h}" width="{w}" height="{h}" rx="30" fill="url(#b)"/>
<rect x="{-w/2}" y="{-h+10}" width="{w}" height="{h-20}" rx="30" fill="url(#hl)" opacity=".5"/>
<rect x="{-w/2-6}" y="{-h-62}" width="{w+12}" height="68" rx="20" fill="{cap}"/>
<text x="0" y="{-h/2+10}" text-anchor="middle" font-size="26" letter-spacing="9" fill="{cap}" font-weight="500">ALVA</text>
<text x="0" y="{-h/2+36}" text-anchor="middle" font-size="10" letter-spacing="3.5" fill="{cap}">CREME Nº3</text>'''
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<ellipse cx="0" cy="8" rx="{w*0.62}" ry="14" fill="rgba(42,35,32,.18)"/>{g}</g>')

DEFS = '''<defs>
<linearGradient id="b" x1="0" x2="1"><stop offset="0" stop-color="#CDB89F"/><stop offset=".45" stop-color="#E6D6C2"/><stop offset="1" stop-color="#C2AB90"/></linearGradient>
<linearGradient id="hl" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".3" stop-color="#fff" stop-opacity=".55"/><stop offset=".42" stop-color="#fff" stop-opacity="0"/></linearGradient>
</defs>'''

def peca1():
    return f'''<html><head><meta charset="utf-8"><style>{BASE}
body{{background:{BONE};color:{INK}}}
.sun{{position:absolute;left:150px;top:300px;width:780px;height:780px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#EFC9B3,#E9D2BF)}}
.top{{position:absolute;top:80px;left:90px;right:90px;display:flex;justify-content:space-between;font-size:26px;letter-spacing:.38em;font-weight:500}}
.top small{{font-size:20px;letter-spacing:.3em;color:#8a7d70;font-weight:400}}
h1{{position:absolute;left:90px;top:170px;font-size:108px;line-height:1.02;font-weight:300;letter-spacing:-.04em}}
h1 b{{font-weight:600}}
.pill{{position:absolute;left:90px;bottom:90px;border:2px solid {INK};border-radius:60px;padding:24px 54px;font-size:26px;letter-spacing:.28em;font-weight:500}}
.tag{{position:absolute;right:90px;bottom:108px;font-size:20px;letter-spacing:.3em;color:#8a7d70}}
svg{{position:absolute;left:0;top:0}}
</style></head><body>
<div class="sun"></div>
<svg width="1080" height="1350" viewBox="0 0 1080 1350">{DEFS}{bottle("cleanser",540,1130,1.55)}</svg>
<div class="top"><span>ALVA</span><small>SKINCARE</small></div>
<h1>Pele em<br><b>silêncio.</b></h1>
<div class="pill">CONHEÇA A LINHA &rarr;</div><div class="tag">NOVA COLEÇÃO 2026</div>
</body></html>'''.replace("#E9D2BF", "#E9D2BF")

def peca2():
    return f'''<html><head><meta charset="utf-8"><style>{BASE}
body{{background:{SAND};color:{INK}}}
.top{{position:absolute;top:80px;left:90px;right:90px;display:flex;justify-content:space-between;font-size:26px;letter-spacing:.38em;font-weight:500}}
.top small{{font-size:20px;letter-spacing:.3em;color:#8a7d70;font-weight:400}}
h2{{position:absolute;left:90px;top:170px;font-size:92px;line-height:1.05;font-weight:300;letter-spacing:-.035em}}
h2 b{{font-weight:600}}
.shelf{{position:absolute;left:0;right:0;top:1010px;height:340px;background:{BONE}}}
.cap{{position:absolute;top:1060px;width:300px;text-align:center;font-size:21px;letter-spacing:.28em;color:{INK}}}
.cap b{{display:block;font-size:40px;font-weight:300;letter-spacing:0;margin-bottom:8px;color:{CLAY}}}
svg{{position:absolute;left:0;top:0}}
</style></head><body>
<div class="shelf"></div>
<svg width="1080" height="1350" viewBox="0 0 1080 1350">{DEFS}
{bottle("cleanser",230,1010,1.2)}{bottle("serum",540,1010,1.22)}{bottle("jar",850,1010,1.15)}</svg>
<div class="top"><span>ALVA</span><small>ROTINA</small></div>
<h2>Três passos.<br><b>Só o essencial.</b></h2>
<div class="cap" style="left:80px"><b>01</b>LIMPA</div>
<div class="cap" style="left:390px"><b>02</b>TRATA</div>
<div class="cap" style="left:700px"><b>03</b>HIDRATA</div>
</body></html>'''

def peca3():
    return f'''<html><head><meta charset="utf-8"><style>{BASE}
body{{background:{CLAY};color:{BONE}}}
.top{{position:absolute;top:80px;left:90px;right:90px;display:flex;justify-content:space-between;font-size:26px;letter-spacing:.38em;font-weight:500}}
.top small{{font-size:20px;letter-spacing:.3em;opacity:.75;font-weight:400}}
.card{{position:absolute;left:90px;right:90px;top:210px;height:610px;border-radius:56px;background:{BONE};color:{INK};padding:70px}}
.card .k{{font-size:22px;letter-spacing:.34em;color:#8a7d70}}
.card h2{{font-size:76px;font-weight:300;letter-spacing:-.035em;margin-top:18px;line-height:1.02}}
.card h2 b{{font-weight:600}}
.price{{position:absolute;left:70px;bottom:62px;font-size:26px;color:#8a7d70}}
.price strong{{display:block;font-size:150px;font-weight:300;letter-spacing:-.05em;color:{CLAY};line-height:1}}
.price strong span{{font-size:50px;vertical-align:top;margin-right:8px;position:relative;top:22px}}
.pill{{position:absolute;left:90px;bottom:100px;background:{INK};color:{BONE};border-radius:60px;padding:26px 60px;font-size:26px;letter-spacing:.28em;font-weight:500}}
.seal{{position:absolute;right:140px;top:470px;width:230px;height:230px}}
svg.p{{position:absolute;left:0;top:0}}
</style></head><body>
<svg class="p" width="1080" height="1350" viewBox="0 0 1080 1350">{DEFS}
<ellipse cx="540" cy="1275" rx="520" ry="26" fill="rgba(0,0,0,.14)"/>
{bottle("jar",270,1270,1.4)}{bottle("serum",800,1270,0.9)}{bottle("cleanser",560,1270,0.85)}</svg>
<div class="top"><span>ALVA</span><small>KIT ESSENCIAL</small></div>
<div class="card"><div class="k">OFERTA DE LANÇAMENTO</div><h2>Rotina<br>completa<br><b>em um kit.</b></h2>
<div class="price">a partir de<strong><span>R$</span>189</strong></div></div>
<svg class="seal" viewBox="0 0 250 250"><circle cx="125" cy="125" r="122" fill="{INK}"/>
<defs><path id="c" d="M125,125 m-92,0 a92,92 0 1,1 184,0 a92,92 0 1,1 -184,0"/></defs>
<text font-size="19" letter-spacing="5" fill="{BONE}" font-family="Poppins"><textPath href="#c">FRETE GRÁTIS · PELE EM SILÊNCIO · </textPath></text>
<path d="M95 125h60M135 105l20 20-20 20" stroke="{BONE}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
<div class="pill" style="display:none"></div>
</body></html>'''

SIT_CSS = """body{background:#050507;color:#fff}
.glow{position:absolute;right:-260px;bottom:-260px;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,rgba(79,91,255,.5),rgba(79,91,255,0) 65%)}
.glow2{position:absolute;left:-300px;top:-300px;width:700px;height:700px;border-radius:50%;background:radial-gradient(circle,rgba(79,91,255,.22),rgba(79,91,255,0) 65%)}
.brand{position:absolute;top:70px;left:80px;display:flex;align-items:center;gap:26px}
.brand img{height:84px}.brand span{font-size:30px;letter-spacing:.32em;font-weight:600}
.pager{position:absolute;top:96px;right:80px;font-size:22px;letter-spacing:.3em;color:#8d92b8}
.foot{position:absolute;left:80px;bottom:70px;font-size:22px;letter-spacing:.3em;color:#6b7094}
em{font-style:normal;background:linear-gradient(90deg,#4f5bff,#7a86ff);-webkit-background-clip:text;color:transparent}
.kicker{font-size:24px;letter-spacing:.35em;color:#8d92b8;display:flex;align-items:center;gap:20px}
.kicker:before{content:"";width:48px;height:2px;background:#4f5bff}"""

def frame(i, body, extra=""):
    return (f'<html><head><meta charset="utf-8"><style>{BASE}{SIT_CSS}{extra}</style></head><body>'
            f'<div class="glow2"></div><div class="glow"></div>'
            f'<div class="brand"><img src="{LOGO}"><span>SITH.IA</span></div>'
            f'<div class="pager">{i:02d} / 06</div>{body}'
            f'<div class="foot">CRIATIVIDADE · TECNOLOGIA · RESULTADOS</div></body></html>')

def bastidor(imgs):
    ims = "".join(f'<img src="{u}">' for u in imgs)
    extra = """
.bar{position:absolute;left:150px;right:150px;top:330px;height:10px;border-radius:10px;background:linear-gradient(90deg,#8a93ff,#fff,#8a93ff);box-shadow:0 0 60px 30px rgba(110,120,255,.55),0 0 160px 90px rgba(79,91,255,.35)}
.beam{position:absolute;left:100px;right:100px;top:340px;height:220px;background:linear-gradient(180deg,rgba(110,120,255,.28),rgba(110,120,255,0));clip-path:polygon(8% 0,92% 0,100% 100%,0 100%)}
.mon{position:absolute;left:50px;right:50px;top:560px;height:424px;border-radius:26px;background:#0b0b10;border:3px solid #1c1d2b;padding:20px;display:flex;gap:18px;box-shadow:0 0 120px rgba(79,91,255,.3)}
.mon img{flex:1;min-width:0;height:100%;object-fit:cover;object-position:center;border-radius:10px}
.stand{position:absolute;left:470px;width:140px;top:984px;height:70px;background:linear-gradient(180deg,#1b1c28,#0b0b10)}
.base{position:absolute;left:360px;width:360px;top:1050px;height:14px;border-radius:14px;background:#1d1e2c}
.desk{position:absolute;left:0;right:0;top:1064px;height:2px;background:linear-gradient(90deg,transparent,rgba(110,120,255,.6),transparent)}
.cap{position:absolute;left:80px;right:80px;top:1110px}
.cap b{font-size:40px;font-weight:600;letter-spacing:-.01em}
.cap small{display:block;margin-top:8px;font-size:22px;letter-spacing:.3em;color:#8d92b8}
.tagc{position:absolute;top:250px;left:0;right:0;text-align:center}
"""
    body = ('<div class="bar"></div><div class="beam"></div>'
            f'<div class="mon">{ims}</div><div class="stand"></div><div class="base"></div><div class="desk"></div>'
            '<div class="cap"><b>ALVA · Social media | Skincare</b><small>PORTFÓLIO · CONCEITO · MARCA FICTÍCIA</small></div>')
    return frame(1, body, extra)

def processo():
    extra = """.wrap{position:absolute;left:80px;right:80px;top:300px}
h2{font-size:84px;line-height:1.06;font-weight:700;letter-spacing:-.03em;margin-top:34px}
.it{display:flex;gap:36px;align-items:flex-start;border:2px solid rgba(110,120,255,.4);border-radius:30px;padding:34px 40px;margin-top:26px;background:linear-gradient(145deg,rgba(79,91,255,.14),rgba(255,255,255,.02))}
.it .n{font-size:64px;font-weight:700;color:transparent;-webkit-text-stroke:2px #4f5bff;line-height:1}
.it p{font-size:36px;line-height:1.3;color:#d3d5ea}.it p b{color:#fff;font-weight:600}"""
    body = ('<div class="wrap"><div class="kicker">COMO FIZEMOS</div><h2>Do briefing ao post <em>com IA.</em></h2>'
            '<div class="it"><div class="n">01</div><p><b>Conceito de marca</b> criado a partir de um briefing curto: nome, paleta e tom de voz.</p></div>'
            '<div class="it"><div class="n">02</div><p><b>Direção de arte</b> e peças geradas e refinadas com IA, no mesmo estilo.</p></div>'
            '<div class="it"><div class="n">03</div><p><b>Revisão humana</b> e entrega nos formatos de feed e story.</p></div></div>')
    return frame(5, body, extra)

def cta():
    extra = """.wrap{position:absolute;left:80px;right:80px;top:400px}
h1{font-size:104px;line-height:1.04;font-weight:700;letter-spacing:-.03em}
.sub{font-size:38px;color:#c7c9de;margin-top:44px;line-height:1.35}
.btn{display:inline-block;margin-top:60px;border:2px solid #4f5bff;border-radius:60px;padding:28px 64px;font-size:30px;letter-spacing:.3em;font-weight:600}"""
    body = ('<div class="wrap"><h1>Quer um projeto <em>assim</em> para a sua marca?</h1>'
            '<div class="sub">Campanhas, vídeos, sites e influencers virtuais, criados com IA.</div>'
            '<div><span class="btn">CHAME NA DM &rarr;</span></div></div>')
    return frame(6, body, extra)

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1350})
        def shot(html, name):
            pg.set_content(html); pg.wait_for_timeout(150)
            path = OUT / name; pg.screenshot(path=str(path)); return path
        a = shot(peca1(), "slide-02.png"); bb = shot(peca2(), "slide-03.png"); c = shot(peca3(), "slide-04.png")
        uris = ["data:image/png;base64," + base64.b64encode(x.read_bytes()).decode() for x in (a, bb, c)]
        shot(bastidor(uris), "slide-01.png"); shot(processo(), "slide-05.png"); shot(cta(), "slide-06.png")
        b.close()
    print("ok", OUT)

if __name__ == "__main__":
    main()
