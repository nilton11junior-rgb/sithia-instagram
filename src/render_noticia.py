#!/usr/bin/env python3
"""Renderiza o post de NOTÍCIA (coluna 3) em 1080x1350 a partir de um JSON de tipo "noticia".
Uso: python3 src/render_noticia.py conteudo/calendario/noticia-astra.json
Slides: capa (imagem gerada com IA), fato, ponte, cta. Visual SITH.IA (fundo escuro, azul-índigo).
Saída: criativos/gerados/noticia/<id>/slide-01..N.png"""
import base64, html, json, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "marca/fontes"
def b64(p): return base64.b64encode(Path(p).read_bytes()).decode()
LOGO = "data:image/png;base64," + b64(ROOT / "marca/assets/logo.png")
FONTS = "".join(
    f"@font-face{{font-family:'{n}';font-weight:{w};src:url(data:font/woff2;base64,{b64(F/f)}) format('woff2')}}"
    for n, w, f in [("Anton", 400, "anton-latin-400-normal.woff2"),
                    ("Mono", 400, "jetbrains-mono-latin-400-normal.woff2"), ("Mono", 700, "jetbrains-mono-latin-700-normal.woff2")])
def fmt(t, cor): return re.sub(r"\*(.+?)\*", rf'<em style="color:{cor};font-style:normal">\1</em>', html.escape(t))

def base(cor, extra=""):
    return (f"{FONTS}*{{margin:0;padding:0;box-sizing:border-box}}"
        f"body{{width:1080px;height:1350px;overflow:hidden;position:relative;background:#050507;color:#fff;font-family:'Inter','Helvetica',sans-serif}}"
        f".glow{{position:absolute;right:-200px;bottom:-200px;width:700px;height:700px;border-radius:50%;background:radial-gradient(circle,{cor}55 0,#0000 70%)}}"
        f".glow2{{position:absolute;left:-250px;top:-250px;width:600px;height:600px;border-radius:50%;background:radial-gradient(circle,{cor}2a 0,#0000 70%)}}"
        f".faixa{{position:absolute;top:56px;left:80px;right:80px;display:flex;justify-content:space-between;align-items:center;z-index:6;font-family:'Mono';font-size:20px;letter-spacing:.2em;color:#ffffffcc}}"
        f".faixa .b{{display:flex;align-items:center;gap:14px;font-weight:700;letter-spacing:.3em;color:#fff}}.faixa img{{height:44px}}"
        f".foot{{position:absolute;left:80px;right:80px;bottom:60px;display:flex;justify-content:space-between;font-family:'Mono';font-size:19px;letter-spacing:.15em;color:#ffffffaa;z-index:6}}"
        f".tit{{font-family:Anton;text-transform:uppercase;line-height:1.04}}{extra}")

def faixa(d, n, total):
    return (f'<div class="faixa"><div class="b"><img src="{LOGO}">SITH.IA</div><div>{html.escape(d["faixa"].split("·",1)[1].strip())}</div></div>'
            f'<div class="foot"><span>@SITH.IA.OFICIAL</span><span>{n}/{total}</span></div>')

def capa(d, s, n, total):
    cor = d["cor"]
    img = "data:image/jpeg;base64," + b64(ROOT / d["imagem_capa"])
    return (f'<html><head><meta charset="utf-8"><style>{base(cor, ".shade{position:absolute;inset:0;background:linear-gradient(180deg,#000b 0,#0000 24%,#0000 36%,#000f 80%)}")}'
        f'.bg{{position:absolute;left:0;top:0;width:1080px;height:1350px;object-fit:cover}}'
        f'.kick{{position:absolute;left:80px;top:716px;font-family:Mono;font-weight:700;font-size:24px;letter-spacing:.3em;color:#fff;text-shadow:0 2px 14px #000,0 0 30px #000}}'
        f'.tit{{position:absolute;left:80px;right:80px;top:790px;font-size:104px;text-shadow:0 6px 40px #000c}}'
        f'.sub{{position:absolute;left:80px;right:80px;top:1130px;font-family:Mono;font-size:28px;letter-spacing:.08em;color:#fff}}'
        f'.foot{{display:none}}</style></head><body><img class="bg" src="{img}"><div class="shade"></div>'
        f'{faixa(d, n, total)}<div class="kick">{html.escape(s["kicker"])}</div><div class="tit">{fmt(s["titulo"], cor)}</div>'
        f'<div class="sub">{html.escape(s["sub"])}</div>'
        f'<div class="foot" style="display:flex"><span>ARRASTE PRO LADO &rarr;</span><span>{n}/{total}</span></div></body></html>')

def fato(d, s, n, total):
    cor = d["cor"]
    fonte = f'<div class="fonte">{html.escape(s["fonte"])}</div>' if s.get("fonte") else ""
    return (f'<html><head><meta charset="utf-8"><style>{base(cor)}'
        f'.num{{position:absolute;left:80px;top:190px;font-family:Anton;font-size:150px;color:{cor};line-height:1}}'
        f'.tit{{position:absolute;left:80px;right:80px;top:350px;font-size:96px}}'
        f'.lin{{position:absolute;left:80px;top:620px;width:120px;height:6px;background:{cor}}}'
        f'.t1{{position:absolute;left:80px;right:80px;top:664px;font-size:44px;line-height:1.3;font-weight:600}}'
        f'.t2{{position:absolute;left:80px;right:80px;top:810px;font-size:35px;line-height:1.4;color:#c7c9de}}'
        f'.fonte{{position:absolute;left:80px;right:80px;bottom:130px;font-family:Mono;font-size:21px;letter-spacing:.08em;color:#8d92b8}}'
        f'</style></head><body><div class="glow"></div><div class="glow2"></div>{faixa(d, n, total)}'
        f'<div class="num">{s["num"]}</div><div class="tit">{fmt(s["titulo"], cor)}</div><div class="lin"></div>'
        f'<div class="t1">{html.escape(s["texto"])}</div><div class="t2">{html.escape(s["texto2"])}</div>{fonte}</body></html>')

def ponte(d, s, n, total):
    cor = d["cor"]
    itens = "".join(f'<div class="it"><span>{i+1}</span><p>{html.escape(t)}</p></div>' for i, t in enumerate(s["itens"]))
    return (f'<html><head><meta charset="utf-8"><style>{base(cor)}'
        f'.num{{position:absolute;left:80px;top:190px;font-family:Anton;font-size:150px;color:{cor};line-height:1}}'
        f'.tit{{position:absolute;left:80px;right:80px;top:350px;font-size:88px}}'
        f'.lista{{position:absolute;left:80px;right:80px;top:640px;display:flex;flex-direction:column;gap:26px}}'
        f'.it{{display:flex;gap:28px;align-items:center;border:2px solid {cor}55;border-radius:28px;padding:30px 34px;background:#ffffff0d}}'
        f'.it span{{font-family:Anton;font-size:60px;color:{cor};min-width:50px}}.it p{{font-size:31px;line-height:1.35;color:#fff}}'
        f'.nota{{position:absolute;left:80px;bottom:130px;font-family:Mono;font-size:21px;letter-spacing:.2em;color:#8d92b8}}'
        f'</style></head><body><div class="glow"></div><div class="glow2"></div>{faixa(d, n, total)}'
        f'<div class="num">{s["num"]}</div><div class="tit">{fmt(s["titulo"], cor)}</div><div class="lista">{itens}</div>'
        f'<div class="nota">{html.escape(s["nota"].upper())}</div></body></html>')

def cta(d, s, n, total):
    cor = d["cor"]
    return (f'<html><head><meta charset="utf-8"><style>{base(cor)}'
        f'.tit{{position:absolute;left:80px;right:80px;top:380px;font-size:130px}}'
        f'.sub{{position:absolute;left:80px;right:80px;top:820px;font-size:38px;line-height:1.35;color:#c7c9de}}'
        f'.btn{{position:absolute;left:80px;top:990px;border:3px solid {cor};border-radius:70px;padding:26px 60px;font-family:Mono;font-weight:700;font-size:30px;letter-spacing:.2em;background:{cor}22}}'
        f'</style></head><body><div class="glow"></div><div class="glow2"></div>{faixa(d, n, total)}'
        f'<div class="tit">{fmt(s["titulo"], cor)}</div><div class="sub">{html.escape(s["sub"])}</div>'
        f'<div class="btn">{html.escape(s["botao"])} &rarr;</div></body></html>')

TIPOS = {"capa": capa, "fato": fato, "ponte": ponte, "cta": cta}

def main(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    out = ROOT / "criativos/gerados/noticia" / d["id"]; out.mkdir(parents=True, exist_ok=True)
    total = len(d["slides"])
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={"width": 1080, "height": 1350})
        for i, s in enumerate(d["slides"], 1):
            pg.set_content(TIPOS[s["tipo"]](d, s, i, total)); pg.wait_for_timeout(400)
            pg.screenshot(path=str(out / f"slide-{i:02d}.png"))
        br.close()
    print("ok", out)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "conteudo/calendario/noticia-astra.json"))
