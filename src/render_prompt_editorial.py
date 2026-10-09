#!/usr/bin/env python3
"""Post de PROMPT no padrão cinematográfico/editorial (4 slides, 1080x1350):
  1 capa (foto de herói em tela cheia + título grande + rótulos de canto)
  2 foto do resultado inteira (limpa)
  3 prompt (foto menor + painel com o texto do prompt)
  4 fechamento / CTA
Uso: python3 src/render_prompt_editorial.py conteudo/calendario/<post>.json
JSON (tipo "prompt-editorial"): id, cor, pasta_imagens, imagem (nome do arquivo em pasta_imagens),
  capa{linha1, linha2, tagline}, prompt_titulo, prompt_texto, ficha[lista curta], cta{titulo, sub, botao}
Saída: criativos/gerados/<pasta>/<id>/slide-01..04.png (depois: python3 src/export_jpg.py <pasta>)"""
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

def uri(p):
    ext = "jpeg" if str(p).lower().endswith((".jpg", ".jpeg")) else "png"
    return f"data:image/{ext};base64,{b64(p)}"

def base(cor):
    return (f"{FONTS}*{{margin:0;padding:0;box-sizing:border-box}}"
        f"body{{width:1080px;height:1350px;overflow:hidden;position:relative;background:#050607;color:#fff;font-family:'Mono',monospace}}"
        f".hero{{position:absolute;inset:0;width:1080px;height:1350px;object-fit:cover}}"
        f".lab{{position:absolute;font-size:21px;letter-spacing:.22em;text-transform:uppercase;text-shadow:0 2px 14px #000c;z-index:5}}"
        f".tl{{top:56px;left:60px;display:flex;align-items:center;gap:14px}}.tl img{{height:44px}}"
        f".tr{{top:62px;right:60px}}.bl{{bottom:56px;left:60px}}.br{{bottom:56px;right:60px}}"
        f".acc{{color:{cor}}}")

def corners(n, total, esq="DESLIZE PARA MAIS &rarr;", dir_="@SITH.IA.OFICIAL"):
    return (f'<div class="lab tl"><img src="{LOGO}">SITH.IA</div><div class="lab tr">{n:02d} / {total:02d}</div>'
            f'<div class="lab bl">{esq}</div><div class="lab br">{dir_}</div>')


def hud_layer(d, hero_path, cor, n_line="01"):
    """Camada HUD (estilo vigilância) com a marca SITH.IA por cima da foto."""
    from PIL import Image
    import io
    h = d.get("hud")
    if not h: return ""
    W, H = 1080, 1350
    px, py, pw, ph_ = h["passaporte"]
    im = Image.open(hero_path).convert("RGB"); iw, ih = im.size
    crop = im.crop((int(px*iw), int(py*ih), int((px+pw)*iw), int((py+ph_)*ih))).resize((260, 300))
    buf = io.BytesIO(); crop.save(buf, "JPEG", quality=90)
    pas = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    def box(r, label=None, lab_side="right"):
        x, y, w, h2 = [r[0]*W, r[1]*H, r[2]*W, r[3]*H]
        lab = ""
        if label:
            lab = f'<div class="hl" style="left:{x+w+14}px;top:{y-6}px">{html.escape(label)}</div>'
        return f'<div class="bx" style="left:{x}px;top:{y}px;width:{w}px;height:{h2}px"></div>{lab}'
    boxes = box(h["rosto"]) + box(h["objeto"], h.get("obj_label", "OBJ: CAFÉ")) + box(h["mao"])
    css = (f".hl{{position:absolute;font-size:23px;letter-spacing:.06em;color:#fff;text-shadow:0 0 6px #000,0 2px 14px #000;z-index:6}}"
        f".bx{{position:absolute;border:4px dashed {cor};z-index:6;box-shadow:0 0 0 1px #0008}}"
        f".cn{{position:absolute;width:62px;height:62px;border:0 solid {cor};z-index:6}}"
        f".card{{position:absolute;left:62px;bottom:200px;width:470px;background:#f1f1f3;border:4px solid {cor};border-radius:20px;overflow:hidden;z-index:7;color:#111;font-family:'Mono'}}"
        f".card .hd{{background:{cor};color:#fff;text-align:center;font-size:21px;letter-spacing:.04em;padding:9px 0;font-weight:700}}"
        f".card .bd{{display:flex;gap:22px;padding:18px 22px}}.card .tx{{flex:1;font-size:15px;line-height:1.55}}"
        f".card .id{{font-size:30px;font-weight:700;margin-bottom:6px}}.card img{{width:128px;height:147px;object-fit:cover;border-radius:6px}}"
        f".card .pp{{font-size:22px;margin-top:10px;font-weight:700;letter-spacing:.08em}}"
        f".sig{{position:absolute;left:62px;top:150px;border-left:5px solid {cor};padding-left:20px;font-size:25px;line-height:1.5;color:#fff;z-index:6;text-shadow:0 0 6px #000,0 2px 14px #000}}"
        f".top1{{position:absolute;left:62px;right:62px;top:56px;font-size:23px;letter-spacing:.03em;color:#fff;z-index:6;text-shadow:0 0 6px #000,0 2px 14px #000}}"
        f".pid{{position:absolute;top:96px;font-size:26px;color:{cor};z-index:6}}")
    corners = ("".join(f'<div class="cn" style="{pos};border-width:{bw}"></div>' for pos, bw in [
        ("left:36px;top:92px", "5px 0 0 5px"), ("right:36px;top:92px", "5px 5px 0 0"),
        ("left:36px;bottom:92px", "0 0 5px 5px"), ("right:36px;bottom:92px", "0 5px 5px 0")]))
    return (f"<style>{css}</style>{corners}{boxes}"
        f'<div class="top1">SITHIA_LINE_{n_line} //signal node active / SITH.IA / {h.get("data","2026/10/08")}</div>'
        f'<div class="pid" style="left:82px;display:none">person_01</div>'
        f'<div class="card"><div class="hd">{html.escape(h.get("card_titulo","ATIVIDADE OFFLINE DETECTADA"))}</div>'
        f'<div class="bd"><div class="tx"><div class="id">ID: {html.escape(h.get("id","S-2210-01"))}</div>'
        + "".join(f"<div>{html.escape(l)}</div>" for l in h["linhas"]) +
        f'<div class="pp">SITH.IA ID</div></div><img src="{pas}"></div></div>'
        f'<div class="sig">signal strength: 92%<br>noise level: minimal<br>output filter: active<br><br>SITHIA_FEED</div>')

def capa(d, img, hero_path):
    c, cor = d["capa"], d["cor"]
    hud = hud_layer(d, hero_path, d.get("cor_hud", cor))
    return (f'<html><head><meta charset="utf-8"><style>{base(cor)}'
        f".shade{{position:absolute;inset:0;background:linear-gradient(180deg,#0006 0,#0000 20%,#0000 60%,#000c 100%)}}"
        f".t{{position:absolute;right:62px;bottom:120px;text-align:right;font-family:'Anton';line-height:.95;text-transform:uppercase;text-shadow:0 6px 40px #000d;z-index:8}}"
        f".t .a{{font-size:92px;display:block}}.t .b{{font-size:92px;display:block;color:{cor}}}"
        f'.lab{{display:none}}</style></head><body><img class="hero" src="{img}"><div class="shade"></div>{hud}'
        f'<div class="t"><span class="a">{html.escape(c["linha1"])}</span><span class="b">{html.escape(c["linha2"])}</span></div>'
        f'</body></html>')

def resultado(d, img):
    cor = d["cor"]
    return (f'<html><head><meta charset="utf-8"><style>{base(cor)}'
        f".shade{{position:absolute;inset:0;background:linear-gradient(180deg,#0008 0,#0000 14%,#0000 86%,#0009 100%)}}"
        f'</style></head><body><img class="hero" src="{img}"><div class="shade"></div>'
        f'{corners(2, 4, "O RESULTADO", "SALVE ESSE PROMPT")}</body></html>')

def prompt_slide(d, img):
    cor = d["cor"]
    ficha = "".join(f'<span class="chip">{html.escape(x)}</span>' for x in d["ficha"])
    return (f'<html><head><meta charset="utf-8"><style>{base(cor)}'
        f"body{{background:#07090a}}"
        f".ph{{position:absolute;left:0;top:0;width:1080px;height:520px;object-fit:cover;object-position:50% 4%}}"
        f".fade{{position:absolute;left:0;top:300px;width:1080px;height:260px;background:linear-gradient(180deg,#0000,#07090a)}}"
        f".card{{position:absolute;left:60px;right:60px;top:470px;bottom:130px}}"
        f".h{{font-family:'Anton';font-size:84px;line-height:1;text-transform:uppercase}}"
        f".h em{{font-style:normal;color:{cor}}}"
        f".box{{margin-top:26px;border:2px solid {cor}88;background:#0d1214;border-radius:22px;padding:30px 34px;font-size:27px;line-height:1.5;color:#e9f1f2}}"
        f".chips{{margin-top:22px;display:flex;flex-wrap:wrap;gap:12px}}"
        f".chip{{border:2px solid #fff4;border-radius:40px;padding:9px 20px;font-size:20px;letter-spacing:.08em;color:#fffc}}"
        f'</style></head><body><img class="ph" src="{img}"><div class="fade"></div>'
        f'{corners(3, 4, "COPIE E COLE &rarr;", "ANEXE SUA FOTO")}'
        f'<div class="card"><div class="h">{fmt(d["prompt_titulo"], cor)}</div>'
        f'<div class="box">{html.escape(d["prompt_texto"])}</div><div class="chips">{ficha}</div></div></body></html>')

def cta(d, img):
    cor, c = d["cor"], d["cta"]
    return (f'<html><head><meta charset="utf-8"><style>{base(cor)}'
        f".bg{{position:absolute;inset:-40px;width:1160px;height:1430px;object-fit:cover;filter:blur(18px) brightness(.38) saturate(1.1)}}"
        f".w{{position:absolute;left:60px;right:60px;top:440px}}"
        f"h1{{font-family:'Anton';font-size:150px;line-height:.98;font-weight:400;text-transform:uppercase}}"
        f".s{{font-size:32px;line-height:1.45;color:#e6eef0;margin-top:36px}}"
        f".b{{display:inline-block;margin-top:50px;background:{cor};color:#000;border-radius:60px;padding:26px 60px;font-weight:700;font-size:30px;letter-spacing:.18em}}"
        f'</style></head><body><img class="bg" src="{img}">'
        f'{corners(4, 4, "SALVE PARA USAR DEPOIS", "SIGA @SITH.IA.OFICIAL")}'
        f'<div class="w"><h1>{fmt(c["titulo"], cor)}</h1><div class="s">{html.escape(c["sub"])}</div><span class="b">{html.escape(c["botao"])}</span></div></body></html>')

def main(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    pasta = ROOT / d["pasta_imagens"]
    img = uri(pasta / d["imagem"]); hero_path = pasta / d["imagem"]
    img2 = uri(pasta / d["imagem2"]) if d.get("imagem2") else img
    out = ROOT / "criativos/gerados" / Path(d["pasta_imagens"]).name / d["id"]; out.mkdir(parents=True, exist_ok=True)
    htmls = [capa(d, img, hero_path), resultado(d, img2), prompt_slide(d, img), cta(d, img2)]
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, h in enumerate(htmls, 1):
            pg.set_content(h); pg.wait_for_timeout(250); pg.screenshot(path=str(out / f"slide-{i:02d}.png"))
        b.close()
    print("ok", out)

if __name__ == "__main__":
    main(sys.argv[1])
