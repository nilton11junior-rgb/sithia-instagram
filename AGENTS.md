# SITH.IA Instagram — instruções para agentes de IA

Idioma de trabalho, docs e conteúdo: **português do Brasil**. O dono (Nilton) não é técnico: ele só aprova posts no chat.

## Produto e stack
- O que é e para quem: `PRODUCT.md`. Como as peças se conectam: `docs/architecture.md`.
- Stack: Python 3.12 (CI) / 3.13 (sandbox), Playwright (HTML → PNG), Pillow, rembg, requests; GitHub Actions publica via Instagram Graph API. Sem site, sem banco, sem JavaScript.
- Setup e decisões do toolkit: `docs/setup.md`.

## Comandos
- Instalar: `pip install -r requirements.txt && playwright install chromium`
- Verificar tudo (não publica, sem rede): `python3 scripts/check.py`
- Autotestes da verificação: `pytest -q`
- Lint: `ruff check src scripts tests` (já roda dentro do check)
- Gerar slides: `python3 src/render_<tipo>.py conteudo/calendario/<post>.json` e depois `python3 src/export_jpg.py <pasta de saída>`
- Simular publicação: `python3 src/publish.py conteudo/calendario/<post>.json --dry-run`
- Build/tipos: não existem (scripts Python soltos).

## Regras que nunca mudam
- **Push publica.** Todo push em `conteudo/calendario/**` acorda o robô e publica posts aprovados vencidos. Push só com autorização do Nilton para aquele conteúdo; nunca marcar `"aprovado": true` sem o OK dele no chat.
- **Aprovação de post vem primeiro** e vai sozinha numa mensagem (slides + legenda + dia/hora). Detalhes em `CLAUDE.md`.
- Nunca colocar token, senha ou `.env` no repositório (ele é público). Nunca imprimir segredos.
- Nunca editar à mão `estado/published.json` (o robô é o dono). Exceção só com pedido do Nilton (ex.: post de teste apagado no Instagram), registrando em `docs/erros-e-acertos/decisoes.md`.
- Texto de slide e legenda só no JSON do calendário, nunca no código.
- Sem marcas, logos ou personagens reais de terceiros; portfólio é conceito fictício rotulado. Nada de Boticário.

## Como trabalhar
- Ler as instruções e o código relevante antes de mudar algo; separar fato observado de suposição.
- Mudança mínima suficiente, reaproveitando os renders existentes. Sem abstrações ou dependências que ninguém pediu.
- Definir o critério de pronto antes; rodar `python3 scripts/check.py` depois de mudar calendário ou script.
- Não transformar suposição em fato nem integração pendente em resultado simulado. Fato de notícia é reconfirmado em fonte.
- Continuar o trabalho autorizado; um bloqueio para só o que depende dele. Respeitar pausa e cancelamento.
- Publicar, mandar mensagem a terceiros, gastar dinheiro (ex.: créditos) e apagar coisas exigem autorização explícita. Instalar ferramenta não autoriza nada disso.
- Ao retomar trabalho de outra sessão: conferir arquivos, `git status` e o que já foi publicado (`estado/published.json`) antes de confiar em resumos.
- **Início de toda sessão ou retomada:** rodar `python3 scripts/check.py`. Se aparecer o aviso `fila:`, a primeira coisa a dizer ao Nilton é que a fila está curta (qual dia fica sem post) e propor produzir o próximo, antes de responder outros assuntos.

## Delegação e revisão
- Subagente só quando isolar contexto ou paralelizar ajuda; tarefa simples se faz direto.
- Cada tarefa delegada recebe objetivo, arquivos permitidos, critério de aceite e formato de retorno. Um escritor por arquivo; revisores só leem. O coordenador confere o diff e roda o check.
- Modelo mais leve para buscas e leitura; capacidade maior para segurança, tokens/segredos e decisões ambíguas.
- Revisão proporcional ao risco; para mudanças no robô de publicação ou em segredos, usar o roteiro da seção "Revisão de segurança" em `docs/quality.md`.

## Mapa de documentação (cada doc é dono de um assunto)
- `PRODUCT.md` escopo · `docs/architecture.md` estrutura e decisões · `docs/design.md` visual · `docs/onboarding.md` preparar a máquina · `docs/quality.md` verificações e revisão · `docs/setup.md` toolkit e evidências.
- Conteúdo e marca: `docs/conteudo/`, `docs/marca/identidade-visual.md`, `docs/conteudo/padrao-visual-capa.md`.
- Memória do projeto: `docs/erros-e-acertos/` (erros, acertos, decisões; modelo em `_modelo.md`, mais recente no topo) e `docs/pendencias.md`.
- Atualizar o doc responsável junto com a mudança; não duplicar regra em vários arquivos.
