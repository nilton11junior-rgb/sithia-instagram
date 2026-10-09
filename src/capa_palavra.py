#!/usr/bin/env python3
"""Capa com PALAVRA GIGANTE atrás da pessoa (efeito de profundidade, estilo pôster).
Recorta a pessoa da foto (rembg), põe a palavra entre o fundo e a pessoa e salva um JPEG 1080x1350.
Uso: python3 src/capa_palavra.py <foto> <saida.jpg> "GPT-6" [cor_palavra] [topo_px] [tamanho_px]
Requer: pip install "rembg[cpu]" (baixa o modelo isnet-general-use na 1a vez)."""
import base64, io, sys
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
from rembg import remove, new_session

ROOT = Path(__file__).resolve().parent.parent
def b64(b): return base64.b64encode(b).decode()

def main(foto, saida, palavra, cor="#ffffff", topo=120, tam=430):
    im = Image.open(foto).convert("RGB")
    # corta para 4:5 centralizado e redimensiona para 1080x1350
    w, h = im.size; alvo = 4 / 5
    if w / h > alvo:
        nw = int(h * alvo); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / alvo); im = im.crop((0, 0, w, nh))
    im = im.resize((1080, 1350), Image.LANCZOS)
    cut = remove(im, session=new_session("isnet-general-use"))
    from PIL import ImageFilter  # encolhe a borda 2px para não sobrar halo do fundo
    a = cut.getchannel("A").filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1)); cut.putalpha(a)
    bf, bc = io.BytesIO(), io.BytesIO()
    im.save(bf, "JPEG", quality=95); cut.save(bc, "PNG")
    anton = b64((ROOT / "marca/fontes/anton-latin-400-normal.woff2").read_bytes())
    html = (f"<html><head><style>@font-face{{font-family:A;src:url(data:font/woff2;base64,{anton})}}"
            f"*{{margin:0;padding:0}}body{{width:1080px;height:1350px;position:relative;overflow:hidden;background:#000}}"
            f"img{{position:absolute;left:0;top:0;width:1080px;height:1350px}}"
            f".w{{position:absolute;left:0;right:0;top:{topo}px;text-align:center;font-family:A;font-size:{tam}px;line-height:1;"
            f"color:{cor};letter-spacing:-.01em;text-shadow:0 10px 60px #0008}}</style></head><body>"
            f'<img src="data:image/jpeg;base64,{b64(bf.getvalue())}"><div class="w">{palavra}</div>'
            f'<img src="data:image/png;base64,{b64(bc.getvalue())}"></body></html>')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        pg.set_content(html); pg.wait_for_timeout(300)
        png = pg.screenshot(); b.close()
    Image.open(io.BytesIO(png)).convert("RGB").save(saida, "JPEG", quality=94)
    print("ok", saida)

if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[1], a[2], a[3] if len(a) > 3 else "#ffffff",
         int(a[4]) if len(a) > 4 else 120, int(a[5]) if len(a) > 5 else 430)
