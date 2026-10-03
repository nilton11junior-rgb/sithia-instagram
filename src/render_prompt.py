#!/usr/bin/env python3
"""Renderiza o post de PROMPT (coluna 1) em 1080x1350 a partir de um JSON de tipo "prompt".
Uso: python3 src/render_prompt.py conteudo/calendario/prompt-teste.json
Imagens: criativos/fontes/prompt-teste/antes.png e depois.png (geradas no Gemini). Se faltarem, usa um espaço reservado.
Saída: criativos/gerados/prompt-teste/<id>/slide-01..05.png"""
import base64, html, json, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "marca/fontes"
def b64(p): return base64.b64encode(Path(p).read_bytes()).decode()
LOGO = "data:image/png;base64," + b64(ROOT / "marca/assets/logo.png")
FONTS = "".join(
    f"@font-face{{font-family:'{n}';font-weight:{w};src:url(data:font/woff2;base64,{b64(F/f)}) format('woff2')}}"
    for n, w, f in [("Anton", 400, "anton-latin-400-normal.woff2"), ("Script", 400, "great-vibes-latin-400-normal.woff2"),
                    ("Mono", 400, "jetbrains-mono-latin-400-normal.woff2"), ("Mono", 700, "jetbrains-mono-latin-700-normal.woff2")])

def fmt(t, cor): return re.sub(r"\*(.+?)\*", rf'<em style="color:{cor};font-style:normal">\1</em>', html.escape(t))

def img_uri(pasta, nome):
    p = pasta / nome
    if p.exists():
        return "data:image/png;base64," + b64(p)
    return None

BASE = lambda cor: f"""{FONTS}*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;overflow:hidden;position:relative;background:#06161a;color:#fff;font-family:'Inter',sans-serif}}
.top{{position:absolute;top:60px;left:70px;right:70px;display:flex;justify-content:space-between;align-items:center;z-index:5}}
.brand{{display:flex;align-items:center;gap:16px;font-size:22px;letter-spacing:.3em;font-weight:600}}.brand img{{height:48px}}
.tag{{font-family:'Mono';font-size:20px;letter-spacing:.2em;border:2px solid #fff6;border-radius:40px;padding:10px 22px;background:#0006}}
.foot{{position:absolute;left:70px;right:70px;bottom:56px;display:flex;justify-content:space-between;font-family:'Mono';font-size:20px;letter-spacing:.15em;color:#ffffffcc;z-index:5}}
.pill{{border:2px solid #fff8;border-radius:60px;padding:16px 34px;background:#0007;font-family:'Mono';font-size:22px;letter-spacing:.1em}}
.acc{{color:{cor}}}"""

def ph(label):
    return f'<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 40%,#244 0,#06161a 70%);display:flex;align-items:center;justify-content:center;font-family:Mono;color:#ffffff55;font-size:26px;letter-spacing:.2em">[{label}]</div>'

def capa(d, pasta, n):
    c, cor = d["capa"], d["cor"]
    depois = img_uri(pasta, d["imagens"]["depois"])
    bg = f'<img src="{depois}" style="position:absolute;left:0;top:0;width:1080px;height:1350px;object-fit:cover">' if depois else ph("IMAGEM DEPOIS")
    return (f'<html><head><meta charset="utf-8"><style>{BASE(cor)}'
        f'.shade{{position:absolute;inset:0;background:linear-gradient(180deg,#000a 0,#0000 28%,#0000 55%,#000e 100%)}}'
        f'.chamada{{position:absolute;top:150px;left:0;right:0;text-align:center;font-family:Mono;font-size:26px;letter-spacing:.25em;text-transform:uppercase}}'
        f'.script{{position:absolute;top:196px;left:0;right:0;text-align:center;font-family:Script;font-size:150px;color:{cor};line-height:1;text-shadow:0 4px 30px #000a}}'
        f'.gig{{position:absolute;left:0;right:0;top:690px;text-align:center;font-family:Anton;font-size:330px;line-height:1;letter-spacing:.01em;text-shadow:0 10px 60px #000b}}'
        f'.sub{{position:absolute;left:0;right:0;top:1010px;text-align:center;font-family:Mono;font-size:30px;letter-spacing:.3em}}'
        f'.pillw{{position:absolute;left:0;right:0;top:1100px;text-align:center}}</style></head><body>{bg}<div class="shade"></div>'
        f'<div class="top"><div class="brand"><img src="{LOGO}">SITH.IA</div><div class="tag">PROMPT · 01</div></div>'
        f'<div class="chamada">{html.escape(c["chamada"])}</div><div class="script">{html.escape(c["script"])}</div>'
        f'<div class="gig">{html.escape(c["palavra"])}</div><div class="sub">{html.escape(c["sub"].upper())}</div>'
        f'<div class="pillw"><span class="pill">ARRASTE PRO LADO &rarr;</span></div>'
        f'<div class="foot"><span>SALVE PRA NÃO PERDER</span><span>@SITH.IA.OFICIAL</span></div></body></html>')

def antes_depois(d, pasta, n):
    cor = d["cor"]
    a = img_uri(pasta, d["imagens"]["antes"]); b = img_uri(pasta, d["imagens"]["depois"])
    ia = f'<img src="{a}" style="width:100%;height:100%;object-fit:cover">' if a else ph("ANTES")
    ib = f'<img src="{b}" style="width:100%;height:100%;object-fit:cover">' if b else ph("DEPOIS")
    return (f'<html><head><meta charset="utf-8"><style>{BASE(cor)}'
        f'.t{{position:absolute;top:150px;left:70px;font-family:Anton;font-size:120px;line-height:1}}'
        f'.card{{position:absolute;border-radius:28px;overflow:hidden;border:3px solid #fff3}}'
        f'.lab{{position:absolute;left:18px;top:18px;font-family:Mono;font-size:22px;letter-spacing:.2em;background:#000a;padding:8px 16px;border-radius:30px;z-index:3}}'
        f'.arrow{{position:absolute;left:300px;top:760px;font-family:Mono;font-size:70px;color:{cor}}}</style></head><body>'
        f'<div class="top"><div class="brand"><img src="{LOGO}">SITH.IA</div><div class="tag">02 / 05</div></div>'
        f'<div class="t">{d.get("titulo_antes_depois", "DA FOTO <span class=\"acc\">SIMPLES</span><br>AO <span class=\"acc\">CINEMA</span>")}</div>'
        f'<div class="card" style="left:70px;top:520px;width:330px;height:440px"><div class="lab">ANTES</div>{ia}</div>'
        f'<div class="arrow" style="left:410px;top:700px">&rarr;</div>'
        f'<div class="card" style="left:500px;top:430px;width:510px;height:680px;border-color:{cor}"><div class="lab" style="background:{cor};color:#000">DEPOIS</div>{ib}</div>'
        f'<div class="foot"><span>MESMA FOTO, UM PROMPT</span><span>PRÓXIMO &rarr;</span></div></body></html>')

def prompt_slide(d, n):
    cor = d["cor"]
    return (f'<html><head><meta charset="utf-8"><style>{BASE(cor)}'
        f'body{{background:radial-gradient(circle at 80% 90%,{cor}22,#06161a 60%)}}'
        f'.t{{position:absolute;top:150px;left:70px;font-family:Anton;font-size:130px;line-height:1}}'
        f'.box{{position:absolute;left:70px;right:70px;top:420px;border:2px solid {cor}88;border-radius:26px;padding:48px;background:#00000066;font-family:Mono;font-size:31px;line-height:1.55;color:#e9f3f4}}'
        f'.hint{{position:absolute;left:70px;top:1130px;font-family:Mono;font-size:24px;letter-spacing:.12em;color:{cor}}}</style></head><body>'
        f'<div class="top"><div class="brand"><img src="{LOGO}">SITH.IA</div><div class="tag">03 / 05</div></div>'
        f'<div class="t">COPIE E <span class="acc">COLE</span></div>'
        f'<div class="box">{html.escape(d["prompt_pt"])}</div>'
        f'<div class="hint">&#9656; USE NO GEMINI COM A SUA FOTO ANEXADA</div>'
        f'<div class="foot"><span>TESTADO NO {html.escape(d["ferramenta"].upper())}</span><span>PRÓXIMO &rarr;</span></div></body></html>')

def ajustes(d, n):
    cor = d["cor"]
    itens = "".join(f'<div class="it"><div class="k">{html.escape(k)}</div><div class="v">{html.escape(v)}</div></div>' for k, v in d["ajustes"])
    return (f'<html><head><meta charset="utf-8"><style>{BASE(cor)}'
        f'body{{background:radial-gradient(circle at 20% 15%,{cor}30,#06161a 55%)}}'
        f'.t{{position:absolute;top:150px;left:70px;font-family:Anton;font-size:120px;line-height:1.02}}'
        f'.l{{position:absolute;left:70px;right:70px;top:430px}}'
        f'.it{{border:2px solid #fff3;border-radius:26px;padding:26px 40px;margin-bottom:22px;background:#ffffff0d}}'
        f'.k{{font-family:Anton;font-size:56px;color:{cor};letter-spacing:.03em}}.v{{font-size:32px;line-height:1.3;color:#e9f3f4;margin-top:6px}}</style></head><body>'
        f'<div class="top"><div class="brand"><img src="{LOGO}">SITH.IA</div><div class="tag">04 / 05</div></div>'
        f'<div class="t">MUDE <span class="acc">3 COISAS</span><br>E TENHA OUTRA CENA</div><div class="l">{itens}</div>'
        f'<div class="foot"><span>TESTE E COMENTE O RESULTADO</span><span>PRÓXIMO &rarr;</span></div></body></html>')

def cta(d, n):
    cor, c = d["cor"], d["cta"]
    return (f'<html><head><meta charset="utf-8"><style>{BASE(cor)}'
        f'body{{background:radial-gradient(circle at 50% 100%,{cor}22,#06161a 60%)}}'
        f'.w{{position:absolute;left:70px;right:70px;top:420px}}'
        f'h1{{font-family:Anton;font-size:150px;line-height:1.02;font-weight:400}}'
        f'.s{{font-size:38px;color:#d9e8ea;margin-top:40px;line-height:1.35}}'
        f'.b{{display:inline-block;margin-top:56px;background:{cor};color:#000;border-radius:60px;padding:28px 70px;font-family:Mono;font-weight:700;font-size:32px;letter-spacing:.2em}}</style></head><body>'
        f'<div class="top"><div class="brand"><img src="{LOGO}">SITH.IA</div><div class="tag">05 / 05</div></div>'
        f'<div class="w"><h1>{fmt(c["titulo"], cor)}</h1><div class="s">{html.escape(c["sub"])}</div><span class="b">{html.escape(c["botao"])} &rarr;</span></div>'
        f'<div class="foot"><span>SALVE PRA NÃO PERDER</span><span>CRIATIVIDADE · TECNOLOGIA · RESULTADOS</span></div></body></html>')

def main(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    pasta = ROOT / d.get("pasta_imagens", "criativos/fontes/prompt-teste")
    out = ROOT / "criativos/gerados" / Path(d.get("pasta_imagens", "criativos/fontes/prompt-teste")).name / d["id"]; out.mkdir(parents=True, exist_ok=True)
    htmls = [capa(d, pasta, 5), antes_depois(d, pasta, 5), prompt_slide(d, 5), ajustes(d, 5), cta(d, 5)]
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, h in enumerate(htmls, 1):
            pg.set_content(h); pg.wait_for_timeout(200); pg.screenshot(path=str(out / f"slide-{i:02d}.png"))
        b.close()
    print("ok", out)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "conteudo/calendario/prompt-teste.json")
