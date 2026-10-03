# Regras do projeto SITH.IA Instagram

Idioma de trabalho e de todo o conteúdo: **português do Brasil**.

## Glossário
- Quando o Nilton diz "sith", ele fala da **SITH.IA**: a empresa e o perfil do Instagram.
- Grafia certa: **SITH.IA**. @ do Instagram: **@sith.ia.oficial**. Nunca escrever "SITH.AI" nem "sitth".

## Grade do Instagram (3 colunas fixas) — ESTRATÉGIA DIÁRIA desde 03/10/2026
- **Um post por dia**, girando os 3 modelos na sequência: notícia → portfólio → prompt → notícia… (a grade de 3 colunas continua alinhada).
- Horários (BRT, decisão do Nilton com base em pesquisa de horários de pico): **dias úteis 12h; sábado e domingo 10h**.
- Primeira rodada: sáb 03/10 notícia, dom 04/10 portfólio, seg 05/10 prompt. Depois: ter 06 notícia, qua 07 portfólio, qui 08 prompt, e assim por diante.
- Produzir em lotes (3 a 4 posts por vez) para nunca faltar post aprovado. Conteúdo/CTA não pode citar dia fixo ("toda segunda"); usar "toda semana" ou "todo dia".
- (Abaixo, o texto antigo da grade semanal: valem as colunas, ignore "segunda, quarta, sexta" e "19h".)
- Coluna 1: post de **prompt**. Coluna 2: **portfólio**. Coluna 3: **notícias de tecnologia**.
- Ordem de publicação para manter as colunas: notícia, depois portfólio, depois prompt (o mais novo fica à esquerda). Sugestão: segunda, quarta, sexta.
- Os 3 posts fixados ocupam a primeira linha; a grade só alinha se continuarem 3 fixados e a quantidade de posts não fixados for múltiplo de 3.
- Antes de criar qualquer modelo de post (prompt, portfólio, notícia): pedir a referência ao Nilton e montar junto com ele.

## Autonomia e aprovação (regra do Nilton)
- Post de notícia: eu escolho a notícia em alta (mundial e Brasil, tudo sobre IA/tecnologia) e produzo o post inteiro. Regras em `docs/conteudo/modelos-de-post/noticia-tech.md`.
- Antes de publicar, SEMPRE mostrar o post final (slides + legenda) e esperar o OK do Nilton. Só então `"aprovado": true` no JSON. Sem aprovação, nada é publicado.
- Prazo: posso preparar o post na véspera ou no próprio dia (eu decido), desde que o Nilton aprove antes das 19h. Reconfirmar fatos no dia.

- Post de portfólio: antes de criar, perguntar ao Nilton se há projeto real da SITH.IA. Se não, criar um conceito fictício (marca inventada, legenda com "conceito") que gere engajamento. Regras em `docs/conteudo/modelos-de-post/portfolio.md`.

## Antes de qualquer tarefa
1. Ler `docs/erros-e-acertos/erros.md` e `docs/pendencias.md`.
2. Para criativos, ler `docs/marca/identidade-visual.md`.

## Regras fixas
- Texto de slide e legenda só em `conteudo/calendario/*.json`. Nunca no código.
- Todo carrossel novo: capa, miolo, e último slide com CTA ("Chame na DM").
- Palavra-chave do título entre asteriscos (`*IA*`) vira azul.
- Imagens geradas ficam só em `criativos/gerados/<semana>/<post>/`.
- Nunca apagar nem editar à mão `estado/published.json`.
- Nunca colocar token, senha ou `.env` no repositório.
- Depois de mudar calendário ou script: rodar `src/publish.py ... --dry-run`.
- Ao trabalhar na pasta do OneDrive pelo Claude (Cowork): só dá para criar/sobrescrever arquivos, não mover nem apagar. Definir o destino final dos arquivos antes de gravar; se algo precisar sair, pedir ao Nilton e listar os nomes exatos.
- Antes de publicar uma semana: abrir capa, um miolo e o CTA de cada carrossel e conferir.

## Memória
Aprendeu algo (erro, acerto, decisão)? Registre em `docs/erros-e-acertos/` usando `_modelo.md`, mais recente no topo.

## Comandos
- Gerar: `python src/render.py conteudo/calendario/<semana>.json`
- Testar publicação: `python src/publish.py conteudo/calendario/<semana>.json --dry-run`

## Modelo do chat (decisão do Nilton, 02/10/2026)
- Para montar posts (prompt, portfólio, notícia) o ideal é o Opus: o Nilton troca com `/model`. Claude não consegue trocar o modelo sozinho, então avisa quando for começar um post.
- No dia a dia (organização, ajustes pequenos, conversa) usar o Sonnet para gastar menos token.
- Post de PROMPT (modelo de teste "retrato cinema") aprovado em 02/10/2026 como padrão visual da coluna 1.

## Personagens (decisão do Nilton, 02/10/2026)
- Pessoas nos posts são sempre **Nilton** e/ou **Bruno** (sócio), usando as fichas em `marca/personagens/` (ver o README de lá). Anexar a ficha no Gemini e conferir o rosto antes de usar.
- Post de PORTFÓLIO (burger, estilo bastidor + peças em tela cheia) aprovado em 02/10/2026 como padrão visual da coluna 2.
- Post de NOTÍCIA (OpenAI Astra/Sol, 5 slides, capa gerada com IA) aprovado em 02/10/2026 como primeiro modelo da coluna 3. Melhorar no próximo (capa em resolução maior).

## Legendas (regra do Nilton, 03/10/2026)
- Legenda nunca em bloco único. Estrutura: gancho (1 linha) → parágrafos curtos de 1–2 frases → chamada para ação em linhas separadas ("Salve este post.", "Siga @sith.ia.oficial…", "Chama na DM.") → fontes (só notícia) → **hashtags sempre por último**, separadas por linha em branco.
- Listas curtas com "→". No máximo 1 emoji no gancho. Linhas em branco entre os blocos.
- Aplicado nos 3 posts aprovados (prompt, portfólio, notícia).

## Automação (03/10/2026)
- Repositório público: github.com/nilton11junior-rgb/sithia-instagram. Robô: `.github/workflows/publish.yml` (a cada 30 min). Segredos `IG_USER_ID` e `IG_ACCESS_TOKEN` no GitHub. Token vale 60 dias: renovar antes de ~01/12/2026.
- Teste real feito em 03/10: o robô publicou o post de prompt no @sith.ia.oficial (funcionou). Nilton apagou o post à mão; data devolvida para 09/10 e `estado/published.json` zerado.
- O robô grava `estado/published.json` no GitHub. Antes de qualquer `git push` da pasta local, fazer `git pull`.
