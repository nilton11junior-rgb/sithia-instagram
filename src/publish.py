#!/usr/bin/env python3
"""Publica carrosséis no Instagram (Graph API) quando chega o horário 'publicar_em'.

Variáveis de ambiente:
  IG_USER_ID         ID da conta Instagram Business/Creator
  IG_ACCESS_TOKEN    token de longa duração (permissão instagram_business_content_publish)
  IG_GRAPH_HOST      opcional; padrão https://graph.instagram.com
  PUBLIC_BASE_URL    URL pública de criativos/gerados  (ex: https://raw.githubusercontent.com/USER/REPO/main/criativos/gerados)

Uso:
  python3 src/publish.py conteudo/calendario/semana-2026-10-05.json            # publica o que já venceu
  python3 src/publish.py conteudo/calendario/semana-2026-10-05.json --dry-run  # só mostra o que faria
  --dry-run --ignore-time   simula também posts ainda não vencidos (só para teste)
Aceita dois formatos de arquivo: {"semana":..., "posts":[...]} ou um único post (JSON com "id" e "slides").
As imagens são os JPEG slide-NN.jpg em criativos/gerados/**/<id>/ (gere com src/export_jpg.py).
Estado dos posts já publicados: estado/published.json (não republica duas vezes)."""
import json, os, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "estado" / "published.json"
# Login do Instagram (sem Página do Facebook): graph.instagram.com. Facebook Login: graph.facebook.com
API = os.environ.get("IG_GRAPH_HOST", "https://graph.instagram.com").rstrip("/") + "/v21.0"

def call(method, path, **params):
    params["access_token"] = os.environ["IG_ACCESS_TOKEN"]
    r = requests.request(method, f"{API}/{path}", params=params, timeout=60)
    if not r.ok:
        raise RuntimeError(f"{path}: {r.status_code} {r.text}")
    return r.json()

def wait_ready(container_id, tries=30):
    for _ in range(tries):
        st = call("GET", container_id, fields="status_code")["status_code"]
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"container {container_id} status {st}")
        time.sleep(4)
    raise TimeoutError(container_id)

def slides_do_post(post_id):
    """Acha a pasta criativos/gerados/**/<id>/ e devolve (caminho relativo, lista de JPEGs)."""
    gerados = ROOT / "criativos" / "gerados"
    pastas = [p for p in gerados.rglob(post_id) if p.is_dir()]
    if not pastas:
        raise FileNotFoundError(f"sem pasta de slides para {post_id} em criativos/gerados")
    pasta = pastas[0]
    jpgs = sorted(pasta.glob("slide-*.jpg"))
    if not 2 <= len(jpgs) <= 10:
        raise ValueError(f"{post_id}: carrossel precisa de 2 a 10 JPEG, achei {len(jpgs)} (rode src/export_jpg.py)")
    return pasta.relative_to(gerados).as_posix(), jpgs

def publish_post(post, base):
    uid = os.environ["IG_USER_ID"]
    rel, jpgs = slides_do_post(post["id"])
    children = []
    for j in jpgs:
        c = call("POST", f"{uid}/media", image_url=f"{base}/{rel}/{j.name}", is_carousel_item="true")["id"]
        children.append(c)
    for c in children:
        wait_ready(c)
    parent = call("POST", f"{uid}/media", media_type="CAROUSEL",
                  children=",".join(children), caption=post["legenda"])["id"]
    wait_ready(parent)
    return call("POST", f"{uid}/media_publish", creation_id=parent)["id"]

def salvar_estado_no_git():
    """Grava o estado no repositório logo após cada publicação (só no GitHub Actions),
    assim um erro em outro post não faz o robô republicar este."""
    if not os.environ.get("GITHUB_ACTIONS"):
        return
    try:
        run = lambda *a: subprocess.run(a, cwd=ROOT, check=True, capture_output=True)
        run("git", "config", "user.name", "sith-bot")
        run("git", "config", "user.email", "bot@users.noreply.github.com")
        run("git", "add", "estado/published.json")
        run("git", "commit", "-m", "estado: post publicado")
        run("git", "pull", "--rebase")
        run("git", "push")
    except Exception as e:
        print(f"aviso: não consegui salvar o estado no git agora: {e}")

def posts_do_arquivo(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data["posts"] if "posts" in data else [data]

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    ignore_time = dry and "--ignore-time" in sys.argv
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    now = datetime.now(timezone.utc)
    base = os.environ.get("PUBLIC_BASE_URL", "").rstrip("/")
    falhas = []
    for post in posts_do_arquivo(args[0]):
        due = datetime.fromisoformat(post["publicar_em"])
        if post["id"] in state:
            continue
        if not post.get("aprovado", False):
            print(f"sem aprovação do Nilton, não publica: {post['id']}")
            continue
        if due > now and not ignore_time:
            print(f"aguardando {post['id']} ({post['publicar_em']})")
            continue
        if dry:
            rel, jpgs = slides_do_post(post["id"])
            print(f"[dry-run] publicaria {post['id']} ({len(jpgs)} slides, legenda {len(post['legenda'])} caracteres)")
            for j in jpgs:
                print(f"   {base or '<PUBLIC_BASE_URL>'}/{rel}/{j.name}")
            continue
        try:
            media_id = publish_post(post, base)
        except Exception as e:  # um post com erro não trava os outros; falha vira exit 1 no final
            print(f"ERRO ao publicar {post['id']}: {e}")
            falhas.append(post["id"])
            continue
        info = {"media_id": media_id, "em": now.isoformat()}
        try:  # confirmação: o Instagram precisa devolver o link do post recém-publicado
            info["permalink"] = call("GET", media_id, fields="permalink")["permalink"]
        except Exception as e:
            print(f"aviso: publicado mas não consegui confirmar o link de {post['id']}: {e}")
        state[post["id"]] = info
        STATE.write_text(json.dumps(state, indent=2))
        salvar_estado_no_git()
        print(f"publicado {post['id']} -> {media_id} {info.get('permalink', '')}")
    if falhas:
        sys.exit(1)

if __name__ == "__main__":
    main()
