# Onboarding (preparar e rodar do zero)

1. **Python:** 3.12 ou mais novo.
2. **Dependências:** `pip install -r requirements.txt`, depois `playwright install chromium`. O rembg baixa o modelo de recorte na primeira vez (precisa de rede).
3. **Ferramentas de verificação (opcional, recomendado):** `pip install ruff pytest`.
4. **Conferir:** `python3 scripts/check.py` deve terminar com `0 erro(s)` (avisos são permitidos) e `pytest -q` deve passar. Um post em produção ainda sem imagem aparece como ERRO até a imagem entrar; isso é esperado.
5. **Gerar um post de exemplo:** `python3 src/render_prompt_pack.py conteudo/calendario/prompt-pack-halloween.json`, depois `python3 src/export_jpg.py criativos/gerados/prompt-pack-halloween/dom-prompt-pack-halloween`.
6. **Simular publicação:** `python3 src/publish.py conteudo/calendario/<post>.json --dry-run`. Isso não chama a API.
7. **Testar publicação de verdade:** só no GitHub Actions, com os Secrets `IG_USER_ID` e `IG_ACCESS_TOKEN`. Localmente, copie `.env.example` para `.env` (nunca versionar). Passo a passo da Meta em `docs/automacao/setup-meta-api.md`.

Antes de qualquer `git push`, faça `git pull`: o robô grava `estado/published.json` no GitHub. E lembre que **push no calendário publica** (ver `AGENTS.md`).
