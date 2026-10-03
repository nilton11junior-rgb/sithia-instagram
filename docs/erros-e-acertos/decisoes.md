# Decisões

Mais recente primeiro. Modelo em [_modelo.md](_modelo.md).

### 2026-10-02 · Claude escolhe a notícia; Nilton só aprova o post final  `#processo` `#automacao`
- **Contexto:** o Nilton quer tempo livre e controle do que vai ao ar.
- **Escolha:** o Claude pesquisa e decide a notícia em alta e monta o post completo; o Nilton revisa o resultado e autoriza a publicação.
- **Motivo:** menos trabalho para ele, sem risco de postar algo que ele não viu.
- **Como funciona:** campo `aprovado` em cada post do JSON (padrão `false`); `src/publish.py` só publica com `true`.
- **Revisar quando:** a qualidade dos posts estiver estável e ele quiser aprovar em lote.

### 2026-10-02 · Nova bio do Instagram  `#marca`
- **Contexto:** a bio antiga não citava sites nem o que o perfil vai publicar (prompts, portfólio, notícias).
- **Opções consideradas:** A (direta com a grade), B (com ícones por linha), C (com chamada para a DM).
- **Escolha:** B, escolhida pelo Nilton: três linhas, 131 de 150 caracteres.
- **Motivo:** deixa claro quem a SITH.IA atende e o que faz, e a seta aponta para o link.
- **Revisar quando:** começar a vender aulas ou mudar a oferta; testar a versão C (com "Chame na DM") se as DMs ficarem baixas.

### 2026-10-02 · Novo @ do Instagram: sith.ia.oficial  `#marca`
- **Contexto:** o @ estava como sitth.ia (dois "t") porque o nome certo não estava livre.
- **Opções livres testadas:** sith.ia.oficial, sith.ia.studio, sithiaoficial, sithia.studio, sithia.ai, sith.iaa. Ocupados: sith.ia, sithia, sith_ia.
- **Escolha:** **sith.ia.oficial**, escolhida pelo Nilton.
- **Motivo:** mantém SITH.IA com o ponto e passa ideia de perfil oficial.
- **Cuidado:** o endereço do perfil mudou para instagram.com/sith.ia.oficial; links antigos para sitth.ia deixam de funcionar. A Meta costuma permitir voltar ao nome anterior por um tempo curto.
- **Revisar quando:** o @ sith.ia ficar disponível.

### 2026-10-02 · Grade fixa de 3 colunas: prompt, portfólio, notícia  `#criativo` `#processo`
- **Contexto:** o Nilton quer que cada coluna do perfil tenha sempre o mesmo tipo de post.
- **Escolha:** coluna 1 = prompt, coluna 2 = portfólio, coluna 3 = notícias de tecnologia. Publicar na ordem notícia, portfólio, prompt (segunda, quarta, sexta).
- **Motivo:** o Instagram põe o post mais novo à esquerda; terminar cada trio com o prompt mantém a ordem. Hoje há 3 fixados e 3 posts não fixados, então a grade já está alinhada.
- **Antes de criar:** pedir a referência de cada tipo ao Nilton e montar os modelos juntos, na identidade da SITH.IA.
- **Revisar quando:** mudar a quantidade de fixados ou postar fora do trio.

### 2026-10-01 · Estrutura de pastas do projeto  `#processo`
- **Contexto:** o projeto vai para o VS Code e precisa crescer sem virar bagunça.
- **Opções consideradas:** tudo na raiz; separar só código e saída; separar por função.
- **Escolha:** separar por função: `docs/`, `marca/`, `conteudo/`, `criativos/`, `src/`, `automacao/`, `estado/`.
- **Motivo:** cada pasta responde a uma pergunta (o que escrevemos, como fica, quem publica) e as imagens geradas ficam separadas do código.
- **Revisar quando:** entrar um segundo formato (Reels) ou uma segunda conta.

### 2026-10-01 · Formato principal: carrossel  `#criativo`
- **Contexto:** o perfil tem posts estáticos e vídeos; era preciso escolher o formato para automatizar.
- **Opções consideradas:** imagem única, Reels, carrossel, mix.
- **Escolha:** carrosséis.
- **Motivo:** escolha do dono do perfil. Carrossel é educativo, gera salvamento e dá para produzir em lote sem vídeo.
- **Revisar quando:** após 4 semanas, comparar alcance e salvamentos com os Reels.

### 2026-10-01 · Ritmo: 3 a 4 posts por semana  `#processo`
- **Contexto:** o perfil é novo (4 posts, 51 seguidores).
- **Escolha:** segunda, quarta e sexta às 19h (horário de Brasília), com um quarto post opcional.
- **Motivo:** ritmo sustentável e previsível. O horário das 19h é um ponto de partida, não uma verdade.
- **Revisar quando:** houver dados do Insights do Instagram sobre o horário de melhor alcance.

### 2026-10-01 · Publicação pela API oficial da Meta  `#meta-api` `#automacao`
- **Contexto:** automatizar postagem exige acessar a conta.
- **Opções consideradas:** API oficial da Meta; automação por navegador; ferramenta de agendamento de terceiros.
- **Escolha:** API oficial (Graph API) com agendador no GitHub Actions.
- **Motivo:** automação por navegador arrisca bloqueio da conta; a API é o caminho permitido e estável.
- **Revisar quando:** a Meta mudar permissões ou o token expirar (a cada 60 dias).

### 2026-10-01 · Fonte provisória: Poppins  `#marca`
- **Contexto:** a fonte exata da marca não foi confirmada.
- **Escolha:** Poppins até haver confirmação.
- **Motivo:** visual próximo da tipografia geométrica das artes atuais.
- **Revisar quando:** a fonte oficial for definida (ver erro de 2026-10-01).
