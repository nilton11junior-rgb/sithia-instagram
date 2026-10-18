@AGENTS.md

# Claude: regras específicas do SITH.IA Instagram

O `AGENTS.md` (importado acima) traz comandos, regras gerais e o mapa das docs. Aqui fica só o que é do jeito de trabalhar do Claude neste projeto.

## APROVAÇÕES (regra do Nilton, 16/10/2026) — PRIORIDADE MÁXIMA
- Cada pedido de aprovação de post vai numa mensagem SEPARADA, só com aquele post (slides + legenda + dia/hora), sem misturar outros assuntos. Se misturar, ele não vê.
- Aprovação de post é sempre a prioridade nº 1: pedir com antecedência para o post ficar agendado; outros assuntos (perfil, fixado, ideias) vêm depois, cada um na sua mensagem.

## FLUXO OBRIGATÓRIO PARA PLANEJAR QUALQUER POST (regra do Nilton, 09/10/2026)
Vale para notícia, prompt e portfólio, sem exceção:
1. TEMA: pesquisar e escolher o melhor tema para o momento atual (o que está em alta agora, fresco, relevante para o público).
2. REFERÊNCIAS: buscar no Pinterest (pasta PROMPTS: br.pinterest.com/nexusgeralia/prompts/ e busca no próprio Pinterest) estilos de ALTA qualidade para aquele tema e formato.
3. QUALIDADE: SEMPRE a melhor qualidade possível. Nada de imagem procedural ou "ok"; se não está no nível das referências, refazer.
4. IMAGEM: gerar no ChatGPT, adaptando a referência escolhida ao Nilton (guia marca/personagens/nilton-guia-2026-10.png (Bruno: bruno-guia-2026-10.jpg); guias antigos ficam como histórico) e à marca SITH.IA (sem logos/personagens de terceiros).
- Imagens do ChatGPT: NUNCA deixar na pasta Downloads do Nilton. Levar a imagem direto para o repositório (página de upload do GitHub, dados passados pelo endereço da página) e guardar cópia no PC em sithia-automacao-instagram/imagens-ia/<post>/ (pedido do Nilton, 11/10/2026: sem passar pelos Downloads).
- ChatGPT: usar SEMPRE a pasta (projeto) "Bs mind" → chat "Criar prompt cinematográfico" (pedido do Nilton, 11/10/2026).
5. CARROSSEL: montar o carrossel completo (slides + legenda) e mostrar ao Nilton para aprovar.
6. LEGENDA COM O PLUGIN marketing-instagram (pedido do Nilton, 11/10/2026). Skills em instagram-skills: ig-carousel-planner, ig-caption-writer, ig-hashtag-strategist e ig-humanizer.
   - Gancho que se sustenta sozinho nos primeiros 125 caracteres.
   - UM CTA só, de preferência de envio ("manda para…") ou de salvamento; nada de "comente o número/SIM".
   - 5 hashtags: #sithia + 3 de nicho + no máximo 1 ampla, variando por tema.
   - Passar no humanizer: sem frase-ponte ("O resultado?", "O mais curioso:"), sem staccato, no máximo 1 travessão.
   - Nunca inventar número ou fato.
   - Plano semanal: ig-content-planner (meta de salvamentos + envios; ver docs/conteudo/plano-*.md).

## Glossário
- Quando o Nilton diz "sith", ele fala da **SITH.IA**: a empresa e o perfil do Instagram.
- Grafia certa: **SITH.IA**. @ do Instagram: **@sith.ia.oficial**. Nunca escrever "SITH.AI" nem "sitth".

## Grade do Instagram (3 colunas fixas) — ESTRATÉGIA DIÁRIA desde 03/10/2026
- **Um post por dia**, girando os 3 modelos na sequência: notícia → portfólio → prompt → notícia… (a grade de 3 colunas continua alinhada).
- Horários (BRT, decisão do Nilton com base em pesquisa de horários de pico): **dias úteis 12h; sábado e domingo 10h**.
- Primeira rodada: sáb 03/10 notícia, dom 04/10 portfólio, seg 05/10 prompt. Depois: ter 06 notícia, qua 07 portfólio, qui 08 prompt, e assim por diante.
- Produzir em lotes (3 a 4 posts por vez) para nunca faltar post aprovado. Conteúdo/CTA não pode citar dia fixo ("toda segunda"); usar "toda semana" ou "todo dia".
- Colunas da grade: coluna 1 = **prompt**, coluna 2 = **portfólio**, coluna 3 = **notícia** (publicar na ordem notícia → portfólio → prompt; o mais novo fica à esquerda).
- Os 3 posts fixados ocupam a primeira linha; a grade só alinha se continuarem 3 fixados e a quantidade de posts não fixados for múltiplo de 3.
- Referências: hoje vêm do Pinterest (fluxo obrigatório, item 2); peça referência ao Nilton quando for um modelo de post totalmente novo.

## Autonomia e aprovação (regra do Nilton)
- Post de notícia: eu escolho a notícia em alta (mundial e Brasil, tudo sobre IA/tecnologia) e produzo o post inteiro. Regras em `docs/conteudo/modelos-de-post/noticia-tech.md`.
- Antes de publicar, SEMPRE mostrar o post final (slides + legenda) e esperar o OK do Nilton. Só então `"aprovado": true` no JSON. Sem aprovação, nada é publicado.
- Prazo: posso preparar o post na véspera ou no próprio dia (eu decido), desde que o Nilton aprove antes das 19h. Reconfirmar fatos no dia.

- Post de portfólio: antes de criar, perguntar ao Nilton se há projeto real da SITH.IA. Se não, criar um conceito fictício (marca inventada, legenda com "conceito") que gere engajamento. Regras em `docs/conteudo/modelos-de-post/portfolio.md`.

## Antes de qualquer tarefa
1. Ler `docs/erros-e-acertos/erros.md` e `docs/pendencias.md`.
2. Para criativos, ler `docs/marca/identidade-visual.md`.

## Regras fixas
- Todo carrossel novo: capa, miolo, e último slide com CTA ("Chame na DM").
- Palavra-chave do título entre asteriscos (`*IA*`) vira azul.
- Slides gerados ficam em `criativos/gerados/<tipo>/<id>/`.
- Depois de mudar calendário ou script: rodar `python3 scripts/check.py` (e `src/publish.py <json> --dry-run` se mexeu no robô).
- Ao trabalhar na pasta do OneDrive pelo Claude (Cowork): só dá para criar/sobrescrever arquivos, não mover nem apagar. Definir o destino final dos arquivos antes de gravar; se algo precisar sair, pedir ao Nilton e listar os nomes exatos.
- Antes de publicar uma semana: abrir capa, um miolo e o CTA de cada carrossel e conferir.

## Memória
Aprendeu algo (erro, acerto, decisão)? Registre em `docs/erros-e-acertos/` usando `_modelo.md`, mais recente no topo.

## Personagens
- Pessoas nos posts são sempre **Nilton** e/ou **Bruno** (sócio), alternando a cada post. Guias de rosto: `marca/personagens/nilton-guia-2026-10.png` e `bruno-guia-2026-10.jpg` (fora do Git; ver o README de lá).
- Modelos aprovados: prompt "pack de estilos" (11/10), portfólio com capa cinematográfica (11/10), notícia com palavra gigante na capa (09/10).

## Legendas (regra do Nilton, 03/10/2026)
- Legenda nunca em bloco único. Estrutura: gancho (1 linha) → parágrafos curtos de 1–2 frases → chamada para ação em linhas separadas ("Salve este post.", "Siga @sith.ia.oficial…", "Chama na DM.") → fontes (só notícia) → **hashtags sempre por último**, separadas por linha em branco.
- Listas curtas com "→". No máximo 1 emoji no gancho. Linhas em branco entre os blocos.
- Desde 11/10/2026 vale **um CTA só** (item 6 do fluxo obrigatório); a estrutura acima continua.

## Padrão visual das capas (aprovado em 09/10/2026)
Todos os posts seguem docs/conteudo/padrao-visual-capa.md: foto cinematográfica com o Nilton (boca fechada, sério, pele retocada natural), palavra gigante atrás da pessoa (src/capa_palavra.py), imagens geradas no ChatGPT e referências da pasta PROMPTS do Pinterest.

## Histórico
Regras antigas (Gemini, fila de 03/10, escolha de modelo) foram para `docs/erros-e-acertos/historico-claude-md.md`.
