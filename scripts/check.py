#!/usr/bin/env python3
"""Verificação única do projeto (não publica nada, não usa rede, não lê segredos).

Roda, nesta ordem:
  1. compilação de todos os .py (erros de sintaxe);
  2. ruff (lint), se estiver instalado;
  3. limite de 350 linhas por arquivo .py (referência do vibe-coding-toolkit);
  4. validação do calendário (conteudo/calendario/*.json) — ver validar_post().

Uso:  python3 scripts/check.py           (sai com código 1 se houver ERRO)
Avisos (AVISO) não reprovam: servem para acompanhar regras novas sem quebrar posts antigos."""
import json
import py_compile
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIMITE_LINHAS = 350
LIMITE_LEGENDA = 2200  # limite do Instagram
LIMITE_HASHTAGS_IG = 5  # limite do Instagram desde 18/12/2025 (antes eram 30); também é a regra do projeto


def _pasta_slides(post_id):
    pastas = [p for p in (ROOT / "criativos" / "gerados").rglob(post_id) if p.is_dir()]
    return pastas[0] if pastas else None


def _imagens_referenciadas(p):
    """Arquivos de imagem que o post cita e que o render precisa encontrar."""
    refs = []
    if p.get("imagem_capa"):
        refs.append(ROOT / p["imagem_capa"])
    pasta = p.get("pasta_imagens")
    if pasta:
        base = ROOT / pasta
        nomes = [p.get("capa", {}).get("imagem")] if isinstance(p.get("capa"), dict) else []
        nomes += [e.get("imagem") for e in p.get("estilos", [])]
        imgs = p.get("imagens")
        if isinstance(imgs, dict):
            nomes += list(imgs.values())
        refs += [base / n for n in nomes if n]
    return refs


def validar_post(p, publicados, ids_vistos):
    """Devolve (erros, avisos) de um post do calendário."""
    erros, avisos = [], []
    pid = p.get("id")
    if not pid:
        return ["post sem 'id'"], []
    if pid in ids_vistos:
        erros.append(f"{pid}: id repetido em outro post")
    ids_vistos.add(pid)
    try:
        quando = datetime.fromisoformat(p.get("publicar_em", ""))
        if quando.tzinfo is None:
            erros.append(f"{pid}: publicar_em sem fuso horário (use -03:00)")
    except ValueError:
        erros.append(f"{pid}: publicar_em inválido ({p.get('publicar_em')!r})")
    if not isinstance(p.get("aprovado", False), bool):
        erros.append(f"{pid}: 'aprovado' precisa ser true ou false")
    legenda = p.get("legenda", "")
    if not isinstance(legenda, str):
        return erros + [f"{pid}: legenda precisa ser texto"], avisos
    if not legenda.strip():
        erros.append(f"{pid}: legenda vazia")
    if len(legenda) > LIMITE_LEGENDA:
        erros.append(f"{pid}: legenda com {len(legenda)} caracteres (máx. {LIMITE_LEGENDA})")
    n_tags = len(re.findall(r"#\w+", legenda))
    if n_tags > LIMITE_HASHTAGS_IG and pid not in publicados:
        erros.append(f"{pid}: {n_tags} hashtags (o Instagram aceita até {LIMITE_HASHTAGS_IG} desde 18/12/2025)")
    if pid in publicados:
        return erros, avisos  # já publicado: imagens antigas podem ter saído do repositório
    for img in _imagens_referenciadas(p):
        if not img.exists():
            erros.append(f"{pid}: imagem não encontrada: {img.relative_to(ROOT)}")
    if p.get("aprovado") is True:
        pasta = _pasta_slides(pid)
        jpgs = sorted(pasta.glob("slide-*.jpg")) if pasta else []
        if not 2 <= len(jpgs) <= 10:
            erros.append(f"{pid}: aprovado mas tem {len(jpgs)} slides JPEG em criativos/gerados "
                         "(o robô precisa de 2 a 10; rode src/export_jpg.py)")
    return erros, avisos


def validar_calendario():
    estado = ROOT / "estado" / "published.json"
    publicados = json.loads(estado.read_text(encoding="utf-8")) if estado.exists() else {}
    erros, avisos, vistos = [], [], set()
    for f in sorted((ROOT / "conteudo" / "calendario").glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            erros.append(f"{f.name}: JSON inválido ({e})")
            continue
        for p in d["posts"] if "posts" in d else [d]:
            e, a = validar_post(p, publicados, vistos)
            erros += [f"{f.name}: {x}" for x in e]
            avisos += [f"{f.name}: {x}" for x in a]
    return erros, avisos


def main():
    erros, avisos = [], []
    pys = sorted(p for p in ROOT.rglob("*.py") if ".venv" not in p.parts)
    for f in pys:
        try:
            py_compile.compile(str(f), doraise=True)
        except py_compile.PyCompileError as e:
            erros.append(f"compilação: {e.msg}")
        n = len(f.read_text(encoding="utf-8").splitlines())
        if n > LIMITE_LINHAS:
            avisos.append(f"{f.relative_to(ROOT)}: {n} linhas (referência {LIMITE_LINHAS})")
    if shutil.which("ruff"):
        r = subprocess.run(["ruff", "check", "--quiet", "src", "scripts", "tests"], cwd=ROOT,
                           capture_output=True, text=True)
        if r.returncode:
            erros.append("ruff:\n" + (r.stdout or r.stderr).strip())
    else:
        avisos.append("ruff não instalado: lint não rodou (pip install ruff)")
    e, a = validar_calendario()
    erros += e
    avisos += a
    for a in avisos:
        print("AVISO", a)
    for e in erros:
        print("ERRO ", e)
    print(f"{len(erros)} erro(s), {len(avisos)} aviso(s)")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
