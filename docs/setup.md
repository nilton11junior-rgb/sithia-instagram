# Setup do vibe-coding-toolkit neste projeto

- **Data:** 18/10/2026.
- **Toolkit:** github.com/soumatheusgomes/vibe-coding-toolkit, revisão `de66fe371a49f5a4d3b521759e5c401f390b6424` (17/10/2026). O clone ficou numa pasta temporária, fora do repositório.
- **Método:** prompt 12 ("existing project setup").
- **Escopo escolhido pelo Nilton:** enxuto, sem instalar nada.
- **Cliente:** Claude (Cowork, sessão na nuvem). Modelo principal: o da sessão. Subagentes com modelos mais leves (Sonnet para ler o catálogo, Haiku para o teste do harness), escolhidos pelo coordenador.
- **Fontes:** só a cópia do toolkit e a documentação oficial. O Context7 não está disponível, por decisão do Nilton, e isso fica registrado como limitação.

## O que mudou
| Antes | Depois |
|---|---|
| Só `CLAUDE.md` (longo, com histórico misturado) | `AGENTS.md` curto (comandos, regras, mapa) + `CLAUDE.md` que importa `@AGENTS.md`. O histórico foi para `docs/erros-e-acertos/historico-claude-md.md`. |
| Sem PRODUCT, arquitetura, qualidade ou setup | `PRODUCT.md`, `docs/architecture.md`, `docs/design.md`, `docs/onboarding.md`, `docs/quality.md` e este arquivo. |
| Sem verificação automática nem testes | `scripts/check.py` (compila, ruff, 350 linhas, calendário) + `tests/test_check.py` (8 casos) + `pyproject.toml` (ruff E/F/I). |
| `requirements.txt` sem Pillow e rembg | Completo (o CI continua instalando só `requests`, que é o que o robô usa). |
| 13 avisos de imports + 1 variável ambígua nos `src/*.py` | Corrigidos sem mudar o comportamento. Os renders foram testados de novo. |
| Regras conflitantes (5 a 8 hashtags, CTA "toda segunda", fluxo semanal de 19h) | Apontam para a regra atual. Os docs antigos foram marcados como desatualizados, sem apagar nada. |

Os 9 destinos do manifest: `README.md`, `PRODUCT.md`, `AGENTS.md`, `CLAUDE.md`, `docs/architecture.md`, `docs/design.md`, `docs/onboarding.md`, `docs/quality.md` e `docs/setup.md`. Os docs em português que já existiam (`docs/marca/`, `docs/conteudo/`, `docs/erros-e-acertos/`, `docs/automacao/`) continuam canônicos para o assunto deles e foram ligados por link.

## Matriz de cobertura do catálogo
Legenda: ✅ aplicado e verificado · ♻️ equivalente reaproveitado · ➖ não se aplica · ⏸ depende de decisão.

| Componente | Situação | Motivo / evidência |
|---|---|---|
| 01 Superpowers | ♻️ | Plugin não instalado. O equivalente agent-skills (spec, plan, build, review) já está disponível, e o método de brainstorm → desenho → aprovação foi seguido à mão. |
| 02 Orquestração de subagentes | ✅ | Regras em `AGENTS.md` (Delegação e revisão). Usado neste setup: catálogo (Sonnet), avaliação do harness (Haiku). |
| 03 RTK | ➖ | Binário global. Projeto pequeno, sem ganho que justifique. |
| 04 Ponytail | ➖ | A regra de "mudança mínima" já está no `AGENTS.md`. |
| 05 Caveman | ➖ | O dono não é técnico e o chat é em português: resposta telegráfica atrapalha. |
| 06 ESLint/Biome + 350 linhas | ♻️ | Sem JavaScript. Equivalente: ruff + `scripts/check.py`, com aviso acima de 350 linhas (maior arquivo: 196). |
| 07 Graphify | ➖ | Repositório pequeno (12 scripts). Exigiria CLI global. |
| 08 Memória Obsidian | ➖ | Sem necessidade concreta nem cofre autorizado. |
| 09 Memória do Claude | ♻️ | Ver "Memória" abaixo. |
| 10 Hooks | ➖ | O toolkit proíbe hook de Git por padrão. A proteção de push está como regra no `AGENTS.md` e no fluxo de aprovação. |
| 11 agent-browser | ♻️ | Playwright (renders) + extensão Claude in Chrome. |
| 12 Context7 | ⏸ | Fora do escopo enxuto, por decisão do Nilton (exige conta e plugin). Usar a documentação oficial. |
| 13 Anthropic skills | ♻️ | Skills de pdf, docx e skill-creator já disponíveis no cliente. Usadas sob demanda, sem instalar nada. |
| 14 Chrome DevTools MCP | ♻️ | Extensão Claude in Chrome e Playwright MCP já cobrem. |
| 15 Codex | ➖ | O cliente é o Claude. O `AGENTS.md` fica pronto caso o Codex seja usado no futuro. |
| 16 Vercel skills / find-skills | ➖ | Sem React nem Next. |
| 17 Next.js runtime/bundle | ➖ | Sem Next.js. |
| 18 PostgreSQL | ➖ | Sem banco. |
| 19 gh-fix-ci | ♻️ | Skill do Codex. O workflow é depurado lendo a aba Actions (ver `docs/erros-e-acertos/`). |
| 20 Revisão de segurança | ✅ | Fonte e forma de chamar registradas em a seção "Revisão de segurança" de `docs/quality.md`. Sem `differential-review`; a revisão é feita por leitura manual. |
| 21 shadcn/ui | ➖ | Sem interface web. |
| 22 Sentry MCP | ➖ | Sem Sentry. |
| Templates AGENTS/CLAUDE/project-docs | ✅ | Adaptados em português. |
| `task-handoff.md.template` | ➖ por ora | Só para trabalho de várias sessões sem registro equivalente. Hoje esse papel fica com a doc do projeto no Claude e `docs/pendencias.md`. |
| Avaliação do harness (07/14) | ✅ parcial | Ver abaixo. |

## Memória (onde fica e como carrega)
- **Índice curto:** `AGENTS.md` + `CLAUDE.md`. O cliente carrega `CLAUDE.md` automaticamente, e ele importa o `AGENTS.md`.
- **Detalhes sob demanda:**
  - `docs/erros-e-acertos/` (erros, acertos, decisões, histórico);
  - `docs/pendencias.md`;
  - a doc do projeto no Claude (`claude/sithia-instagram-estado-do-projeto.md`), que o Claude lê em toda sessão nova.
- **Quando invalidar:** mudança de horário, regra de aprovação, personagem, estilo visual ou robô. Ao mudar, atualize o doc dono e marque o antigo como substituído, com data.

## Evidências (18/10/2026)
- **Antes:**
  - compilação ok, JSON ok, sem testes;
  - ruff com a config do projeto: 84 avisos (70 de linha longa, ignorados de propósito; 14 corrigidos).
- **Depois:**
  - `pytest -q`: **8 passed** (um caso a mais após a revisão independente: hashtags coladas e legenda que não é texto);
  - ruff: 0;
  - `python3 scripts/check.py`: **1 erro**, esperado: o post de segunda 19/10 ainda está sem a imagem da capa porque está em produção. Mais 4 avisos de hashtags em rascunhos antigos não publicados.
- **Fumaça:** `render_prompt_pack.py` e `render_noticia.py` rodaram depois das mudanças. `publish.py --dry-run` rodou sem chamar a API.
- **Avaliação do harness:** subagente novo, modelo Haiku, sem histórico. É um contexto limpo, não um cliente reiniciado.
  - Achou sozinho `AGENTS.md` → `CLAUDE.md` → docs.
  - Respondeu certo os 6 cenários: não dar push sem aprovação, comando único de verificação, segredos só nos Secrets, não editar `published.json`, dono de cada doc, limite de hashtags.
  - Apontou 5 inconsistências: hashtags 5 vs 5–8, `docs/setup.md` faltando, fluxo semanal desatualizado, exceção do `published.json`, dono da renovação do token. As quatro primeiras foram corrigidas e a última virou pendência.
- **Não executado:**
  - reinício real do cliente;
  - o teste do Context7 (fora do escopo);
  - casos do harness que dependem do Node (script `validate-harness.mjs` do toolkit).

## Pendências e decisões futuras
- **Renovação do token do Instagram antes de ~01/12/2026:** é do Nilton, na Meta. Falta escolher como lembrar. Este setup não cria tarefas agendadas.
- **Rodar o `scripts/check.py` no GitHub Actions:** proposta para decidir depois. Seria um passo antes de publicar, que pararia o robô se o calendário estiver quebrado. Mexe no robô, então precisa do OK do Nilton.
- **Context7:** reavaliar se o projeto passar a mexer muito em API (Graph API, Playwright).
- **Apagar `automacao/github-workflow-publish.yml`** (obsoleto, marcado em `automacao/LEIA-ME.md`): decisão do Nilton.

## Como manter ou repetir
- Repetir o setup: colar de novo o atalho do prompt 12 no chat. Ele detecta o estado atual e não duplica nada.
- Depois de mudar script ou calendário: `python3 scripts/check.py`.
- Atualizar o toolkit: comparar a revisão nova com `de66fe3`, ler o que mudou no catálogo e registrar aqui.

## Revisão independente (18/10/2026)
Subagente só de leitura (Sonnet) revisou o diff contra `HEAD`. Nenhum problema bloqueante. Três achados leves, todos resolvidos:
- regras da grade (colunas e fixados) que tinham ido só para o histórico: devolvidas ao `CLAUDE.md`;
- a contagem de hashtags coladas (`#a#b`) passou a ser feita por regex;
- legenda que não é texto agora gera erro limpo.
Segurança: nada encontrado no escopo revisado. Isso não garante que o projeto seja seguro.
