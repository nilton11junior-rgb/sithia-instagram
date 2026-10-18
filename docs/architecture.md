# Arquitetura

## Mapa
```
conteudo/calendario/*.json      ← um post por arquivo (ou semana-*.json com "posts": [...])
criativos/fontes/<post>/        ← imagens de entrada (geradas no ChatGPT)
src/render_*.py                 ← HTML+CSS → PNG 1080x1350 (Playwright/Chromium)
src/capa_palavra.py             ← capa com palavra gigante atrás da pessoa (rembg + Playwright)
src/export_jpg.py               ← PNG → slide-NN.jpg (o que o Instagram recebe)
criativos/gerados/**/<id>/      ← saída versionada (o JPG vai público via raw.githubusercontent)
src/espera.py                   ← quantos segundos faltam para o próximo post aprovado (≤ 5h30)
src/publish.py                  ← Graph API: cria itens, carrossel e publica; grava estado
estado/published.json           ← posts já publicados (dono: o robô)
.github/workflows/publish.yml   ← robô (cron */15 + reforços 05h07–11h07 BRT + push no calendário + manual)
scripts/check.py, tests/        ← verificação local (sem rede)
```

## Renders por tipo de post
| Tipo | Script | Campos principais do JSON |
|---|---|---|
| Notícia | `render_noticia.py` | `imagem_capa`, `slides[]` (capa, fato, ponte, cta) |
| Portfólio | `render_portfolio_foto.py` | `pasta_imagens`, `imagens{}`, `capa{}`, `peças[]`, `processo` |
| Prompt (pack) | `render_prompt_pack.py` | `pasta_imagens`, `capa{}`, `estilos[]`, `cta{}` |
| Perfil (fixado/destaques) | `render_perfil.py` | sem JSON; peças fixas no código |
| Antigos | `render.py`, `render_portfolio.py`, `render_prompt.py`, `render_prompt_editorial.py` | formatos anteriores; ficam para refazer posts antigos |

## Limites e decisões
- **Publicação:**
  - Só posts com `"aprovado": true` e horário vencido.
  - O id em `estado/published.json` impede republicar.
  - O workflow espera até 5h30 pelo horário exato, porque o agendador do GitHub atrasa ou para. Ver `docs/erros-e-acertos/`.
- **Segredos:** `IG_USER_ID` e `IG_ACCESS_TOKEN` existem só nos Secrets do GitHub. O token vale 60 dias e precisa ser renovado antes de ~01/12/2026.
- **Repositório público:**
  - Fichas de rosto (`marca/personagens/`) e PNGs gerados ficam fora do Git (`.gitignore`).
  - Os JPGs entram no Git de propósito, porque a Graph API busca as imagens por URL pública.
- **Imagens do ChatGPT:** vão direto ao repositório pela página de upload do GitHub, sem passar pelos Downloads do Nilton. Cópia em `imagens-ia/` no PC, fora do Git.
- `automacao/github-workflow-publish.yml` é uma cópia antiga e obsoleta. A versão que roda é `.github/workflows/publish.yml`.
