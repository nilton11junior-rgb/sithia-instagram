#!/usr/bin/env python3
"""Renderiza o post de PORTFÓLIO (coluna 2, estilo bastidor + peças) em 1080x1350.
Uso: python3 src/render_portfolio_foto.py conteudo/calendario/portfolio-burger.json
Slides: 1 bastidor (monitor com as 3 peças), 2-4 peças em tela cheia, 5 processo, 6 CTA.
Saída: criativos/gerados/portfolio-burger/<id>/slide-01..06.png
Regras: peças sem cor nem logo da SITH.IA; conceito rotulado; sem marca real."""
import base64, html, json, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "marca/fontes"
def b64(p): return base64.b64encode(Path(p).read_bytes()).decode()
FONTS = "".join(
    f"@font-face{{font-family:'{n}';font-weight:{w};src:url(data:font/woff2;base64,{b64(F/f)}) format('woff2')}}"
    for n, w, f in [("Anton", 400, "anton-latin-400-normal.woff2"), ("Script", 400, "great-vibes-latin-400-normal.woff2"),
                    ("Mono", 400, "jetbrains-mono-latin-400-normal.woff2"), ("Mono", 700, "jetbrains-mono-latin-700-normal.woff2")])
def fmt(t, cor): return re.sub(r"\*(.+?)\*", rf'<em style="color:{cor};font-style:normal">\1</em>', html.escape(t))

BASE = lambda cor: f"""{FONTS}*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;overflow:hidden;position:relative;background:#120d09;color:#fff;font-family:'Inter','Helvetica',sans-serif}}
.foot{{position:absolute;left:80px;right:80px;bottom:64px;display:flex;justify-content:space-between;font-family:'Mono';font-size:20px;letter-spacing:.15em;color:#ffffffcc;z-index:5}}
.acc{{color:{cor}}}"""

def uri(pasta, nome): return "data:image/jpeg;base64," + b64(pasta / nome)

def bastidor(d, pasta, n):
    cor, b, im = d["cor"], d["bastidor"], d["imagens"]
    thumbs = "".join(f'<div style="flex:1;border-radius:10px;overflow:hidden;position:relative"><img src="{uri(pasta, im[k])}" style="width:100%;height:100%;object-fit:cover;{d.get("pessoa_thumb","transform:scale(1.35);transform-origin:80% 100%") if k=="pessoa" else ""}"></div>'
                     for k in ("produto", "pessoa", "detalhe"))
    return (f'<html><head><meta charset="utf-8"><style>{BASE(cor)}'
        f'body{{background:radial-gradient(ellipse at 50% 30%,#2b1d12 0,#0d0906 70%)}}'
        f'.mon{{position:absolute;left:90px;top:300px;width:900px;height:600px;background:#0a0a0a;border-radius:26px;padding:18px;box-shadow:0 40px 90px #000c,0 0 0 3px #2a2a2a}}'
        f'.scr{{width:100%;height:100%;background:#1b1713;border-radius:12px;overflow:hidden;display:flex;flex-direction:column}}'
        f'.bar{{height:44px;background:#2a231c;display:flex;align-items:center;padding:0 18px;gap:10px;font-family:Mono;font-size:15px;color:#ffffff88;letter-spacing:.1em}}'
        f'.dot{{width:12px;height:12px;border-radius:50%;background:#ffffff33}}'
        f'.row{{flex:1;display:flex;gap:16px;padding:18px}}'
        f'.stand{{position:absolute;left:470px;top:900px;width:140px;height:90px;background:linear-gradient(#1c1c1c,#0c0c0c)}}'
        f'.base{{position:absolute;left:380px;top:985px;width:320px;height:16px;border-radius:10px;background:#1a1a1a}}'
        f'.kb{{position:absolute;left:210px;top:1040px;width:660px;height:70px;border-radius:14px;background:linear-gradient(#171717,#0b0b0b);box-shadow:0 20px 40px #000a}}'
        f'.tag{{position:absolute;top:110px;left:0;right:0;text-align:center;font-family:Mono;font-size:24px;letter-spacing:.3em;color:{cor}}}'
        f'.tit{{position:absolute;top:165px;left:40px;right:40px;text-align:center;white-space:nowrap;font-family:Anton;font-size:56px;line-height:1.05;letter-spacing:.01em;text-transform:uppercase}}'
        f'.sub{{position:absolute;left:0;right:0;top:1165px;text-align:center;font-family:Mono;font-size:24px;letter-spacing:.12em;color:#ffffffbb}}'
        f'</style></head><body>'
        f'<div class="tag">{html.escape(b["tag"])}</div><div class="tit">{html.escape(b["titulo"])}</div>'
        f'<div class="mon"><div class="scr"><div class="bar"><span class="dot"></span><span class="dot"></span><span class="dot"></span>&nbsp;&nbsp;campanha_conceito / peças</div><div class="row">{thumbs}</div></div></div>'
        f'<div class="stand"></div><div class="base"></div><div class="kb"></div>'
        f'<div class="sub">{html.escape(b["sub"])}</div>'
        f'<div class="foot"><span>ARRASTE PRO LADO &rarr;</span><span>@SITH.IA.OFICIAL</span></div></body></html>')

def peca(d, pasta, n, chave, idx, estilo):
    cor = d["cor"]; p = d["peças"][idx]
    return (f'<html><head><meta charset="utf-8"><style>{BASE(cor)}'
        f'.img{{position:absolute;{estilo}}}'
        f'.shade{{position:absolute;inset:0;background:linear-gradient(180deg,#0009 0,#0000 22%,#0000 62%,#000d 100%)}}'
        f'.rot{{position:absolute;top:70px;left:80px;font-family:Mono;font-size:24px;letter-spacing:.25em;text-shadow:0 2px 14px #000}}'
        f'.txt{{position:absolute;left:80px;right:80px;bottom:140px;font-family:Anton;font-size:84px;line-height:1.05;text-transform:uppercase;text-shadow:0 6px 40px #000c}}'
        f'.txt i{{display:block;width:90px;height:6px;background:{cor};margin-bottom:26px}}'
        f'</style></head><body><img class="img" src="{uri(pasta, d["imagens"][chave])}"><div class="shade"></div>'
        f'<div class="rot">{html.escape(p["rotulo"])}</div><div class="txt"><i></i>{html.escape(p["texto"])}</div>'
        f'<div class="foot"><span>CONCEITO CRIADO COM IA</span><span>{n}/6</span></div></body></html>')

def processo(d, pasta, n):
    cor, pr = d["cor"], d["processo"]
    passos = "".join(f'<div class="p"><div class="n">{a}</div><div><div class="t">{html.escape(b)}</div><div class="x">{html.escape(c)}</div></div></div>' for a, b, c in pr["passos"])
    return (f'<html><head><meta charset="utf-8"><style>{BASE(cor)}'
        f'.tit{{position:absolute;top:150px;left:80px;right:80px;font-family:Anton;font-size:104px;line-height:1.02;text-transform:uppercase}}'
        f'.lista{{position:absolute;top:520px;left:80px;right:80px;display:flex;flex-direction:column;gap:34px}}'
        f'.p{{display:flex;gap:34px;align-items:center;border:2px solid #ffffff26;border-radius:28px;padding:34px 38px;background:#ffffff0d}}'
        f'.n{{font-family:Anton;font-size:84px;color:{cor};min-width:110px}}'
        f'.t{{font-family:Mono;font-weight:700;font-size:30px;letter-spacing:.12em;margin-bottom:10px}}'
        f'.x{{font-size:30px;line-height:1.35;color:#ffffffcc}}'
        f'</style></head><body><div class="tit">{fmt(pr["titulo"], cor)}</div><div class="lista">{passos}</div>'
        f'<div class="foot"><span>COMO A SITH.IA CRIA</span><span>{n}/6</span></div></body></html>')

def cta(d, pasta, n):
    cor, c = d["cor"], d["cta"]
    return (f'<html><head><meta charset="utf-8"><style>{BASE(cor)}'
        f'body{{background:radial-gradient(ellipse at 50% 80%,#3a2512 0,#120d09 70%)}}'
        f'.tit{{position:absolute;top:300px;left:80px;right:80px;font-family:Anton;font-size:120px;line-height:1.03;text-transform:uppercase}}'
        f'.btn{{position:absolute;top:900px;left:80px;background:{cor};color:#1a1008;font-family:Mono;font-weight:700;font-size:32px;letter-spacing:.18em;padding:28px 56px;border-radius:70px}}'
        f'.nota{{position:absolute;top:1060px;left:80px;right:80px;font-family:Mono;font-size:24px;letter-spacing:.08em;color:#ffffffaa}}'
        f'</style></head><body><div class="tit">{fmt(c["titulo"], cor)}</div><div class="btn">{html.escape(c["botao"])}</div>'
        f'<div class="nota">{html.escape(c["nota"])}</div>'
        f'<div class="foot"><span>@SITH.IA.OFICIAL</span><span>{n}/6</span></div></body></html>')

def main(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    pasta = ROOT / d["pasta_imagens"]
    out = ROOT / "criativos/gerados" / Path(d["pasta_imagens"]).name / d["id"]; out.mkdir(parents=True, exist_ok=True)
    cover = "width:1080px;height:1350px;object-fit:cover;left:0;top:0"
    pessoa = d.get("pessoa_estilo", "width:1250px;height:auto;left:-250px;top:-250px")  # burger: empurra o letreiro do fundo pra fora do quadro
    slides = [bastidor(d, pasta, 1), peca(d, pasta, 2, "produto", 0, cover), peca(d, pasta, 3, "pessoa", 1, pessoa),
              peca(d, pasta, 4, "detalhe", 2, cover), processo(d, pasta, 5), cta(d, pasta, 6)]
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={"width": 1080, "height": 1350})
        for i, h in enumerate(slides, 1):
            pg.set_content(h); pg.wait_for_timeout(400); pg.screenshot(path=str(out / f"slide-{i:02d}.png"))
        br.close()
    print("ok", out)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "conteudo/calendario/portfolio-burger.json"))
