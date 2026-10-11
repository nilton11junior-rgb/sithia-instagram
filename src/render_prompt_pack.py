#!/usr/bin/env python3
"""Post de PROMPT no formato "pack de estilos" (referência: pasta PROMPTS do Pinterest, 11/10/2026).
Slides: 1 capa (foto com a palavra gerada na própria imagem) · 2..N um estilo por slide, com painel
"PROMPT:" translúcido para copiar · último: CTA.
Uso: python3 src/render_prompt_pack.py conteudo/calendario/<post>.json
JSON: id, pasta_imagens, capa{imagem, rotulo, sub}, estilos[{imagem, nome, cor, prompt}], cta{titulo, sub, botao}"""
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
def uri(p): return "data:image/jpeg;base64," + b64(p)

def base(cor):
    return (f"{FONTS}*{{margin:0;padding:0;box-sizing:border-box}}"
        f"body{{width:1080px;height:1350px;overflow:hidden;position:relative;background:#050505;color:#fff;font-family:'Mono',monospace}}"
        f".bg{{position:absolute;inset:0;width:1080px;height:1350px;object-fit:cover}}"
        f".cn{{position:absolute;width:70px;height:70px;border:0 solid {cor};z-index:6;opacity:.9}}"
        f".top{{position:absolute;top:56px;left:70px;right:70px;display:flex;justify-content:space-between;align-items:center;z-index:7;font-size:21px;letter-spacing:.25em;text-shadow:0 2px 12px #000}}"
        f".top .b{{display:flex;gap:12px;align-items:center;font-weight:700}}.top img{{height:40px}}"
        f".bot{{position:absolute;bottom:52px;left:70px;right:70px;display:flex;justify-content:space-between;z-index:7;font-size:19px;letter-spacing:.2em;color:#ffffffd0;text-shadow:0 2px 12px #000}}")

def cantos():
    return "".join(f'<div class="cn" style="{p};border-width:{w}"></div>' for p, w in [
        ("left:40px;top:40px", "4px 0 0 4px"), ("right:40px;top:40px", "4px 4px 0 0"),
        ("left:40px;bottom:40px", "0 0 4px 4px"), ("right:40px;bottom:40px", "0 4px 4px 0")])

def topo(dir_):
    return f'<div class="top"><span class="b"><img src="{LOGO}">SITH.IA</span><span>{dir_}</span></div>'

def capa(d, pasta, total):
    c = d["capa"]; cor = d.get("cor", "#B06BFF")
    return (f'<html><head><meta charset="utf-8"><style>{base(cor)}'
        f".sh{{position:absolute;inset:0;background:linear-gradient(180deg,#0007 0,#0000 18%,#0000 70%,#000c 100%)}}"
        f".rot{{position:absolute;left:70px;bottom:150px;z-index:7;font-family:Anton;font-size:64px;line-height:1.05;text-transform:uppercase;text-shadow:0 6px 30px #000}}"
        f".sub{{position:absolute;left:70px;bottom:112px;z-index:7;font-size:22px;letter-spacing:.12em;color:#ffffffd8;text-shadow:0 2px 12px #000}}"
        f'</style></head><body><img class="bg" src="{uri(pasta / c["imagem"])}"><div class="sh"></div>{cantos()}{topo(f"01 / {total:02d}")}'
        f'<div class="rot">{fmt(c["rotulo"], cor)}</div><div class="sub">{html.escape(c["sub"])}</div>'
        f'<div class="bot"><span>DESLIZE PARA VER &rarr;</span><span>@SITH.IA.OFICIAL</span></div></body></html>')

def estilo(d, pasta, e, n, total):
    cor = e["cor"]
    return (f'<html><head><meta charset="utf-8"><style>{base(cor)}'
        f".sh{{position:absolute;inset:0;background:linear-gradient(180deg,#0006 0,#0000 15%,#0000 55%,#000b 100%)}}"
        f".pan{{position:absolute;left:60px;bottom:110px;width:560px;z-index:7;background:#000000b8;border:1px solid {cor}88;border-radius:14px;padding:24px 26px;backdrop-filter:blur(6px)}}"
        f".pan .h{{font-family:Anton;font-size:40px;letter-spacing:.02em;margin-bottom:10px;color:{cor}}}"
        f".pan .t{{font-size:16px;line-height:1.5;color:#f2f2f2}}"
        f".nome{{position:absolute;right:70px;bottom:118px;z-index:7;text-align:right;font-size:20px;letter-spacing:.25em;color:{cor};text-shadow:0 2px 12px #000}}"
        f'</style></head><body><img class="bg" src="{uri(pasta / e["imagem"])}"><div class="sh"></div>{cantos()}{topo(f"{n:02d} / {total:02d}")}'
        f'<div class="pan"><div class="h">PROMPT:</div><div class="t">{html.escape(e["prompt"])}</div></div>'
        f'<div class="nome">ESTILO {n-1:02d}<br>{html.escape(e["nome"].upper())}</div>'
        f'<div class="bot"><span>COPIE E COLE</span><span>ANEXE SUA FOTO &rarr;</span></div></body></html>')

def cta(d, pasta, total):
    c = d["cta"]; cor = d.get("cor", "#B06BFF")
    return (f'<html><head><meta charset="utf-8"><style>{base(cor)}'
        f".bg{{filter:blur(16px) brightness(.35);transform:scale(1.08)}}"
        f".w{{position:absolute;left:70px;right:70px;top:400px;z-index:7}}"
        f"h1{{font-family:Anton;font-weight:400;font-size:132px;line-height:1;text-transform:uppercase}}"
        f".s{{font-size:30px;line-height:1.45;margin-top:34px;color:#eee}}"
        f".btn{{display:inline-block;margin-top:46px;background:{cor};color:#000;font-weight:700;font-size:28px;letter-spacing:.18em;padding:24px 54px;border-radius:60px}}"
        f'</style></head><body><img class="bg" src="{uri(pasta / d["capa"]["imagem"])}">{cantos()}{topo(f"{total:02d} / {total:02d}")}'
        f'<div class="w"><h1>{fmt(c["titulo"], cor)}</h1><div class="s">{html.escape(c["sub"])}</div><span class="btn">{html.escape(c["botao"])}</span></div>'
        f'<div class="bot"><span>SALVE PARA USAR DEPOIS</span><span>@SITH.IA.OFICIAL</span></div></body></html>')

def main(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    pasta = ROOT / d["pasta_imagens"]
    out = ROOT / "criativos/gerados" / Path(d["pasta_imagens"]).name / d["id"]; out.mkdir(parents=True, exist_ok=True)
    total = len(d["estilos"]) + 2
    htmls = [capa(d, pasta, total)] + [estilo(d, pasta, e, i + 2, total) for i, e in enumerate(d["estilos"])] + [cta(d, pasta, total)]
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, h in enumerate(htmls, 1):
            pg.set_content(h); pg.wait_for_timeout(300); pg.screenshot(path=str(out / f"slide-{i:02d}.png"))
        b.close()
    print("ok", out)

if __name__ == "__main__":
    main(sys.argv[1])
