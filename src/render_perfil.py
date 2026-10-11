#!/usr/bin/env python3
"""Peças do perfil @sith.ia.oficial (11/10/2026):
- post fixado "O que a SITH.IA cria" (carrossel 1080x1350) em criativos/gerados/perfil/fixado-servicos/
- destaques: capas + stories 1080x1920 em criativos/gerados/perfil/destaques/
Uso: python3 src/render_perfil.py"""
import base64, html
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
FT = ROOT / "marca/fontes"; FO = ROOT / "criativos/fontes"
OUT = ROOT / "criativos/gerados/perfil"
def b64(p): return base64.b64encode(Path(p).read_bytes()).decode()
def img(rel): return "data:image/jpeg;base64," + b64(FO / rel)
LOGO = "data:image/png;base64," + b64(ROOT / "marca/assets/logo.png")
ROXO = "#9B6BFF"
FONTS = "".join(
    f"@font-face{{font-family:'{n}';font-weight:{w};src:url(data:font/woff2;base64,{b64(FT/f)}) format('woff2')}}"
    for n, w, f in [("Anton", 400, "anton-latin-400-normal.woff2"),
                    ("Mono", 400, "jetbrains-mono-latin-400-normal.woff2"), ("Mono", 700, "jetbrains-mono-latin-700-normal.woff2")])
def em(t): return html.escape(t).replace("[", f'<em style="color:{ROXO};font-style:normal">').replace("]", "</em>")

def pagina(w, h, corpo, css=""):
    return (f'<html><head><meta charset="utf-8"><style>{FONTS}*{{margin:0;padding:0;box-sizing:border-box}}'
            f"body{{width:{w}px;height:{h}px;overflow:hidden;position:relative;background:#07060b;color:#fff;font-family:'Mono',monospace}}"
            f".bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}"
            f".top{{position:absolute;top:56px;left:64px;right:64px;display:flex;justify-content:space-between;align-items:center;z-index:5;font-size:21px;letter-spacing:.25em;text-shadow:0 2px 12px #000}}"
            f".top .b{{display:flex;gap:12px;align-items:center;font-weight:700}}.top img{{height:40px}}"
            f".bot{{position:absolute;bottom:50px;left:64px;right:64px;display:flex;justify-content:space-between;z-index:5;font-size:19px;letter-spacing:.2em;color:#ffffffcc;text-shadow:0 2px 12px #000}}"
            f".tag{{display:inline-block;font-size:20px;letter-spacing:.25em;color:{ROXO};border:1px solid {ROXO}99;border-radius:40px;padding:10px 22px;background:#0009}}"
            f"h1,h2{{font-family:Anton;font-weight:400;text-transform:uppercase;line-height:1.02}}"
            f"{css}</style></head><body>{corpo}</body></html>")

def topo(d): return f'<div class="top"><span class="b"><img src="{LOGO}">SITH.IA</span><span>{d}</span></div>'

# ---------- carrossel fixado (v2, 11/10/2026: renders 3D roxos, sem fotos de campanha) ----------
SERV = [
    ("SITES E LANDING PAGES", "Sites que [viram cliente]", "Site institucional, landing page de vendas e loja virtual. Rápido, lindo no celular e pronto para anúncio.", ["Site institucional", "Landing page", "Loja virtual"], "fixado-servicos/sites.jpg"),
    ("REBRANDING", "Sua marca com [cara profissional]", "Logo, cores, tipografia e manual da marca. A mudança que faz o cliente confiar em você antes da primeira conversa.", ["Logo", "Identidade visual", "Manual da marca"], "fixado-servicos/rebranding.jpg"),
    ("CAMPANHAS COM IA", "Fotos de campanha [sem estúdio]", "Produto, modelo e cenário criados com IA para lançamento, datas comemorativas e anúncios.", ["Foto de produto", "Lançamentos", "Datas do ano"], "fixado-servicos/campanhas.jpg"),
    ("VÍDEOS E REELS", "Vídeo que [para o scroll]", "Reels, anúncios e vídeos de lançamento com movimento, trilha e a identidade da sua marca.", ["Reels", "Anúncios", "Vídeo de lançamento"], "fixado-servicos/videos.jpg"),
    ("INFLUENCER VIRTUAL", "Um [rosto digital] para a sua marca", "Personagem ou avatar que aparece em todo post e vídeo, sempre igual, sem agenda de gravação.", ["Personagem", "Avatar do dono", "Conteúdo recorrente"], "fixado-servicos/influencer.jpg"),
]

CSS_FX = (".bg{top:-40px;left:70px;width:940px!important;height:auto!important;-webkit-mask-image:radial-gradient(ellipse 75% 70% at 50% 42%,#000 60%,transparent 100%)}"
          ".sh{position:absolute;inset:0;background:linear-gradient(180deg,#07060b80 0,#0000 12%,#0000 46%,#07060bd9 58%,#07060b 70%)}"
          ".n{font-family:Anton;font-size:30px;letter-spacing:.2em;color:#9B6BFF;margin-bottom:10px}"
          ".chips{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}.chips span{font-size:21px;letter-spacing:.06em;color:#fff;border:1px solid #9B6BFF88;background:#9B6BFF1f;border-radius:40px;padding:10px 20px}")

def fx_capa(n, w=1080, h=1350):
    css = CSS_FX + (f".w{{position:absolute;left:64px;right:64px;bottom:{140 if h==1350 else 300}px;z-index:5}}h1{{font-size:{128 if h==1350 else 140}px;margin-top:26px}}"
                    ".s{font-size:28px;line-height:1.45;color:#e8e8e8;margin-top:24px}")
    return pagina(w, h, f'<img class="bg" src="{img("fixado-servicos/capa.jpg")}"><div class="sh"></div>{topo(f"01 / {n:02d}")}'
        f'<div class="w"><span class="tag">O QUE FAZEMOS</span><h1>{em("Sua marca no [próximo nível]")}</h1>'
        f'<div class="s">5 serviços da SITH.IA para empresas que querem vender mais com presença digital.</div></div>'
        f'<div class="bot"><span>DESLIZE &rarr;</span><span>@SITH.IA.OFICIAL</span></div>', css)

def fx_serv(s, i, n, w=1080, h=1350):
    rot, tit, txt, itens, foto = s
    css = CSS_FX + (f".w{{position:absolute;left:64px;right:64px;bottom:{130 if h==1350 else 300}px;z-index:5}}h2{{font-size:{100 if h==1350 else 112}px;margin-top:22px}}"
                    ".s{font-size:27px;line-height:1.5;color:#ececec;margin-top:22px;max-width:930px}")
    chips = "".join(f"<span>{html.escape(c)}</span>" for c in itens)
    return pagina(w, h, f'<img class="bg" src="{img(foto)}"><div class="sh"></div>{topo(f"{i:02d} / {n:02d}")}'
        f'<div class="w"><div class="n">SERVIÇO {i-1:02d}</div><span class="tag">{html.escape(rot)}</span><h2>{em(tit)}</h2>'
        f'<div class="s">{html.escape(txt)}</div><div class="chips">{chips}</div></div>'
        f'<div class="bot"><span>{"DESLIZE &rarr;" if h==1350 else "SITH.IA · SERVIÇOS"}</span><span>@SITH.IA.OFICIAL</span></div>', css)

def como_funciona(i, n, w=1080, h=1350, titulo="Seu projeto começa [na DM]"):
    passos = [("01", "Briefing", "Você conta o que precisa: site, marca, campanha ou vídeo."),
              ("02", "Proposta", "Mandamos o plano, o prazo e o investimento."),
              ("03", "Entrega", "Projeto pronto, revisado com você e no ar.")]
    lis = "".join(f'<div class="p"><b>{a}</b><div><h3>{b}</h3><span>{c}</span></div></div>' for a, b, c in passos)
    css = CSS_FX + (f".bg{{opacity:.55}}.w{{position:absolute;left:64px;right:64px;bottom:{120 if h==1350 else 300}px;z-index:5}}"
           f"h1{{font-size:{108 if h==1350 else 124}px}}.p{{display:flex;gap:26px;align-items:flex-start;margin-top:30px}}"
           f".p b{{font-family:Anton;font-weight:400;font-size:52px;color:{ROXO};min-width:76px}}"
           ".p h3{font-family:Anton;font-weight:400;font-size:40px;text-transform:uppercase}.p span{font-size:25px;line-height:1.45;color:#ddd}"
           f".btn{{display:inline-block;margin-top:44px;background:{ROXO};color:#000;font-weight:700;font-size:27px;letter-spacing:.14em;padding:22px 46px;border-radius:60px}}")
    return pagina(w, h, f'<img class="bg" src="{img("fixado-servicos/cta.jpg")}"><div class="sh"></div>{topo(f"{i:02d} / {n:02d}" if h==1350 else "ORÇAMENTO")}'
        f'<div class="w"><h1>{em(titulo)}</h1>{lis}<span class="btn">MANDE &quot;PROJETO&quot; NA DM</span></div>'
        f'<div class="bot"><span>SALVE E MANDE PARA O SEU SÓCIO</span><span>@SITH.IA.OFICIAL</span></div>', css)

# ---------- destaques ----------
ICONES = {
    "comece": '<path d="M70 40 L130 40 L95 100 L130 100 L70 160 L95 110 L60 110 Z" fill="none" stroke="#fff" stroke-width="9" stroke-linejoin="round"/>',
    "servicos": '<path d="M100 30 L115 85 L170 100 L115 115 L100 170 L85 115 L30 100 L85 85 Z" fill="none" stroke="#fff" stroke-width="9" stroke-linejoin="round"/>',
    "portfolio": '<rect x="35" y="45" width="130" height="110" rx="14" fill="none" stroke="#fff" stroke-width="9"/><circle cx="75" cy="85" r="13" fill="#fff"/><path d="M45 145 L90 105 L115 128 L135 110 L160 140" fill="none" stroke="#fff" stroke-width="9" stroke-linejoin="round"/>',
    "orcamento": '<path d="M40 50 h120 a14 14 0 0 1 14 14 v62 a14 14 0 0 1 -14 14 h-70 l-34 28 v-28 h-16 a14 14 0 0 1 -14 -14 v-62 a14 14 0 0 1 14 -14 z" fill="none" stroke="#fff" stroke-width="9" stroke-linejoin="round"/><circle cx="72" cy="96" r="8" fill="#fff"/><circle cx="100" cy="96" r="8" fill="#fff"/><circle cx="128" cy="96" r="8" fill="#fff"/>',
    "prompts": '<path d="M70 60 L35 100 L70 140 M130 60 L165 100 L130 140 M112 45 L88 155" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>',
}

def capa_destaque(k):
    css = (".o{position:absolute;left:50%;top:50%;width:760px;height:760px;margin:-380px 0 0 -380px;border-radius:50%;"
           f"background:radial-gradient(circle at 50% 40%,#2a1650 0,#120a24 55%,#07060b 100%);box-shadow:0 0 160px {ROXO}66,inset 0 0 0 6px {ROXO}aa}}"
           ".o svg{position:absolute;left:50%;top:50%;width:400px;height:400px;margin:-200px 0 0 -200px;filter:drop-shadow(0 0 30px #9B6BFFaa)}")
    return pagina(1080, 1920, f'<div class="o"><svg viewBox="0 0 200 200">{ICONES[k]}</svg></div>', css)

def story_foto(foto, tag, titulo, sub):
    css = (".sh{position:absolute;inset:0;background:linear-gradient(180deg,#07060bb0 0,#0000 16%,#0000 52%,#07060bee 78%,#07060b 100%)}"
           ".w{position:absolute;left:64px;right:64px;bottom:280px;z-index:5}h2{font-size:104px;margin-top:24px}.s{font-size:30px;line-height:1.5;color:#eee;margin-top:22px}")
    return pagina(1080, 1920, f'<img class="bg" src="{img(foto)}"><div class="sh"></div>{topo("")}'
        f'<div class="w"><span class="tag">{html.escape(tag)}</span><h2>{em(titulo)}</h2><div class="s">{html.escape(sub)}</div></div>'
        f'<div class="bot"><span>SITH.IA</span><span>@SITH.IA.OFICIAL</span></div>', css)

def story_quem():
    css = (".f{position:absolute;top:150px;width:520px;height:900px;object-fit:cover;border-radius:28px;border:2px solid #9B6BFF88}"
           ".a{left:30px;transform:rotate(-3deg)}.b{right:30px;top:230px;transform:rotate(3deg)}"
           ".sh{position:absolute;inset:0;background:linear-gradient(180deg,#0000 40%,#07060b 66%)}"
           ".w{position:absolute;left:64px;right:64px;bottom:250px;z-index:5}h1{font-size:112px;margin-top:24px}.s{font-size:30px;line-height:1.5;color:#eee;margin-top:22px}")
    return pagina(1080, 1920, f'<img class="f a" src="{img("portfolio-arcade/pessoa.jpg")}"><img class="f b" src="{img("portfolio-perfume/pessoa.jpg")}"><div class="sh"></div>{topo("")}'
        f'<div class="w"><span class="tag">COMECE AQUI</span><h1>{em("Somos a [SITH.IA]")}</h1>'
        f'<div class="s">Estúdio criativo com IA do Nilton e do Bruno. Criamos campanhas, vídeos e personagens para marcas, sem estúdio e sem sessão de fotos.</div></div>'
        f'<div class="bot"><span>VEJA OS DESTAQUES &rarr;</span><span>@SITH.IA.OFICIAL</span></div>', css)

def main():
    n = len(SERV) + 2
    fixado = [fx_capa(n)] + [fx_serv(s, i + 2, n) for i, s in enumerate(SERV)] + [como_funciona(n, n)]
    dest = {
        "1-comece-aqui": [capa_destaque("comece"), story_quem()],
        "2-servicos": [capa_destaque("servicos"), fx_capa(1, 1080, 1920)] + [fx_serv(s, i + 2, len(SERV) + 1, 1080, 1920) for i, s in enumerate(SERV)],
        "3-portfolio": [capa_destaque("portfolio"),
                        story_foto("portfolio-perfume/pessoa.jpg", "CONCEITO · PERFUME", "Campanha de [perfume de luxo]", "Marca fictícia criada pela SITH.IA. Produto, rosto e detalhe, sem estúdio."),
                        story_foto("portfolio-tenis/produto.jpg", "CONCEITO · TÊNIS", "Lançamento de [tênis]", "Marca fictícia criada pela SITH.IA. Produto, ação e detalhe."),
                        story_foto("portfolio-arcade/pessoa.jpg", "CONCEITO · DATA COMEMORATIVA", "Dia das Crianças [fliperama]", "Campanha conceito para quem cresceu no fliperama."),
                        story_foto("portfolio-burger/burger-produto.jpg", "CONCEITO · HAMBURGUERIA", "Cardápio com [cara de anúncio]", "Fotos de produto para delivery e feed.")],
        "4-orcamento": [capa_destaque("orcamento"), como_funciona(1, 1, 1080, 1920, "Peça seu [orçamento]")],
        "5-prompts": [capa_destaque("prompts"),
                      story_foto("prompt-pack-mono/capa.jpg", "PROMPTS GRÁTIS", "Packs de [prompts] no feed", "Copie, cole no ChatGPT ou no Gemini e anexe sua foto."),
                      story_foto("prompt-pack-filme/capa.jpg", "PROMPTS GRÁTIS", "Você como [protagonista]", "Um prompt para cada estilo, toda semana no feed.")],
    }
    with sync_playwright() as p:
        b = p.chromium.launch()
        def shot(h, path, w, hh):
            pg = b.new_page(viewport={"width": w, "height": hh}); pg.set_content(h); pg.wait_for_timeout(300)
            path.parent.mkdir(parents=True, exist_ok=True); pg.screenshot(path=str(path)); pg.close()
        for i, h in enumerate(fixado, 1): shot(h, OUT / "fixado-servicos" / f"slide-{i:02d}.png", 1080, 1350)
        for nome, hs in dest.items():
            for i, h in enumerate(hs):
                shot(h, OUT / "destaques" / nome / ("capa.png" if i == 0 else f"story-{i:02d}.png"), 1080, 1920)
        b.close()
    print("ok", OUT)

if __name__ == "__main__":
    main()
