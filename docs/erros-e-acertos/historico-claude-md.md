# Histórico do antigo CLAUDE.md (movido em 18/10/2026)

Trechos que eram válidos em datas passadas e saíram do CLAUDE.md no setup do toolkit. Ficam aqui como memória; **o que vale hoje está em `AGENTS.md` e `CLAUDE.md`.**

## Modelo do chat (decisão do Nilton, 02/10/2026)
- Para montar posts (prompt, portfólio, notícia) o ideal é o Opus: o Nilton troca com `/model`. Claude não consegue trocar o modelo sozinho, então avisa quando for começar um post.
- No dia a dia (organização, ajustes pequenos, conversa) usar o Sonnet para gastar menos token.
- Post de PROMPT (modelo de teste "retrato cinema") aprovado em 02/10/2026 como padrão visual da coluna 1.

## Automação (03/10/2026)
- Repositório público: github.com/nilton11junior-rgb/sithia-instagram. Robô: `.github/workflows/publish.yml` (a cada 30 min). Segredos `IG_USER_ID` e `IG_ACCESS_TOKEN` no GitHub. Token vale 60 dias: renovar antes de ~01/12/2026.
- Teste real feito em 03/10: o robô publicou o post de prompt no @sith.ia.oficial (funcionou). Nilton apagou o post à mão; data devolvida para 09/10 e `estado/published.json` zerado.
- O robô grava `estado/published.json` no GitHub. Antes de qualquer `git push` da pasta local, fazer `git pull`.

## Fila e lições (03/10/2026)
- Agendado e aprovado: notícia Astra (publicada 03/10), portfólio burger (dom 04/10 10h), prompt retrato cinema (seg 05/10 12h), portfólio barbearia (qua 07/10 12h), prompt foto de perfil (qui 08/10 12h). Faltam: notícia ter 06/10 (montar na segunda, com notícia do dia).
- O agendador (cron) do GitHub Actions é pouco confiável e atrasa horas. Se um post não sair no horário: Actions > publicar-instagram > Run workflow (o robô publica tudo que já venceu).
- Gemini: o Chrome bloqueia vários downloads. Para pegar imagem em tamanho original, exibir a imagem a 100% num overlay e tirar capturas em faixas (topo e base), depois juntar com PIL.
- Gemini recusa prompts de "navalha na barba/pele"; usar objetos (escova, espuma, tigela).
- Imagens de pessoas: continuar a conversa "Barbearia Premium: Nilton e Bruno" no Gemini (já tem as referências) em vez de reenviar fichas.

## Comandos
- Gerar: `python src/render.py conteudo/calendario/<semana>.json`
- Testar publicação: `python src/publish.py conteudo/calendario/<semana>.json --dry-run`

## Texto antigo da grade semanal (antes do post diário)
(Valiam as colunas; "segunda, quarta, sexta" e "19h" foram substituídos pelo post diário.)
- Coluna 1: post de **prompt**. Coluna 2: **portfólio**. Coluna 3: **notícias de tecnologia**.
- Ordem de publicação para manter as colunas: notícia, depois portfólio, depois prompt (o mais novo fica à esquerda). Sugestão: segunda, quarta, sexta.
- Os 3 posts fixados ocupam a primeira linha; a grade só alinha se continuarem 3 fixados e a quantidade de posts não fixados for múltiplo de 3.
- Antes de criar qualquer modelo de post (prompt, portfólio, notícia): pedir a referência ao Nilton e montar junto com ele.

