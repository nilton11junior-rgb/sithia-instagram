# Erros

Mais recente primeiro. Modelo em [_modelo.md](_modelo.md).

### 2026-10-02 · Enviar arquivo para o Facebook exige o usuário escolher na janela do Windows  `#processo` `#automacao`
- **O que aconteceu:** o navegador do Claude abre a tela de carregar foto, mas não consegue escolher o arquivo na janela do sistema. O envio foi feito pelo Nilton.
- **Causa:** a janela de seleção de arquivo é do Windows, fora da página.
- **Impacto:** foto de perfil e capa dependeram de uma ação manual (cerca de 10 segundos cada).
- **Como corrigimos:** o Claude deixou os arquivos prontos em `marca/assets/` com nomes claros e abriu a tela certa; o Nilton escolheu o arquivo.
- **Como evitar daqui para frente:** deixar sempre os arquivos prontos, com o tamanho certo, em `marca/assets/`, e avisar o nome exato do arquivo. Não tentar colar imagem em base64 pelo navegador: copiar texto longo pode corromper o arquivo.
- **Envolve:** `marca/assets/perfil-facebook.jpg`, `marca/assets/capa-facebook.jpg`

### 2026-10-02 · Logo enviada com 150x150 pixels foi recusada pelo Facebook  `#criativo` `#marca`
- **O que aconteceu:** o Nilton tentou subir `logo.jpg` (150x150) e o Facebook não aceitou pelo tamanho.
- **Causa:** imagem pequena demais para foto de perfil.
- **Como corrigimos:** foi usado `perfil-facebook.jpg` (1080x1080), gerado do original.
- **Como evitar daqui para frente:** foto de perfil sempre com pelo menos 1000x1000 pixels.
- **Envolve:** `marca/assets/`

### 2026-10-02 · Reorganizar sem poder mover nem apagar arquivos antigos  `#processo`
- **O que aconteceu:** ao reestruturar as pastas, o Claude só conseguiu criar e sobrescrever arquivos na pasta do OneDrive. Não há como mover, renomear ou apagar. Os arquivos da primeira versão ficaram duplicados (`render.py`, `publish.py`, `publish-workflow.yml`, `assets/`, `content/`, `out/`).
- **Causa:** as ferramentas de acesso à pasta só gravam arquivos. O controle do Explorador de Arquivos pela tela também falhou (a janela não apareceu) e é limitado a cliques simples.
- **Impacto:** a limpeza dependeu do Nilton apagar os 6 itens na mão. Feito em 2026-10-02 e conferido pela listagem da pasta.
- **Como corrigimos:** o Nilton apagou os itens antigos; o Claude conferiu que só ficou a estrutura nova.
- **Como evitar daqui para frente:** definir a estrutura final de pastas **antes** de gravar qualquer arquivo na pasta do projeto. Se algo precisar sair do lugar, avisar o Nilton logo, listando os nomes exatos. Não tentar controlar o Explorador pela tela. No VS Code, mover e apagar é trivial: reorganizar lá.
- **Envolve:** raiz da pasta `sithia-automacao-instagram`

### 2026-10-01 · Arquivo de workflow não pôde ser gravado em `.github/`  `#automacao`
- **O que aconteceu:** ao copiar o projeto para o OneDrive, o sistema recusou gravar `.github/workflows/publish.yml` (pasta protegida).
- **Causa:** pastas de configuração do Git são bloqueadas para escrita remota.
- **Impacto:** o agendamento automático não foi criado no lugar final.
- **Como corrigimos:** o arquivo ficou em `automacao/github-workflow-publish.yml`.
- **Como evitar daqui para frente:** ao subir para o GitHub (VS Code), mover o arquivo para `.github/workflows/publish.yml`. Quem está no VS Code faz isso normalmente.
- **Envolve:** `automacao/github-workflow-publish.yml`

### 2026-10-01 · Fonte da marca não estava disponível no ambiente  `#criativo` `#marca`
- **O que aconteceu:** o Google Fonts não pôde ser acessado na geração dos slides.
- **Causa:** o ambiente de geração tem acesso de rede restrito.
- **Impacto:** os slides usam **Poppins** (instalada localmente), que é parecida com a fonte da marca, mas não é necessariamente a mesma.
- **Como corrigimos:** adotamos Poppins como substituta provisória.
- **Como evitar daqui para frente:** confirmar a fonte oficial da SITH.IA e guardar o arquivo em `marca/assets/`. Registrar a resposta em `docs/marca/identidade-visual.md`.
- **Envolve:** `src/render.py`

### 2026-10-01 · Logo recortada de uma arte pronta  `#criativo` `#marca`
- **O que aconteceu:** não havia arquivo original da logo, então ela foi recortada da arte "O que fazemos".
- **Causa:** só tínhamos artes finalizadas como referência.
- **Impacto:** a logo tem resolução baixa (cerca de 90x110 px) e fundo removido por luminosidade. Em tamanho pequeno fica boa; ampliada perde nitidez.
- **Como corrigimos:** usamos a logo só em tamanho pequeno (84 px de altura nos slides).
- **Como evitar daqui para frente:** substituir `marca/assets/logo.png` pelo PNG transparente original ou por SVG.
- **Envolve:** `marca/assets/logo.png`

### 2026-10-01 · Instagram não aceita arquivo local para publicar  `#meta-api` `#automacao`
- **O que aconteceu (previsto antes de ocorrer):** a API do Instagram só publica imagens a partir de URL pública.
- **Causa:** a Graph API busca a imagem na internet; não recebe upload direto.
- **Impacto:** os slides precisam estar hospedados antes da publicação.
- **Como corrigimos:** o fluxo sobe `criativos/gerados/` para um repositório público e usa a URL "raw".
- **Como evitar daqui para frente:** nunca tentar publicar antes de subir as imagens. Se o repositório precisar ser privado, trocar a hospedagem (S3, Cloudinary ou Supabase Storage).
- **Envolve:** `src/publish.py`

### 2026-10-01 · Nome do perfil diferente do nome da marca  `#marca`
- **RESOLVIDO em 2026-10-02:** @ trocado para **sith.ia.oficial** (os mais simples, sith.ia, sithia e sith_ia, estavam ocupados). Resta o Linktree, que ainda diz "SITH.AI".
- **O que aconteceu:** no print do perfil, o @ aparece como **sitth.ia** (dois "t"), enquanto a marca é **SITH.IA**.
- **Causa:** ainda não confirmado: pode ser o @ real, pode ser erro de digitação na criação.
- **Impacto:** risco de menção, link ou legenda com o @ errado.
- **Como evitar daqui para frente:** confirmar o @ oficial e registrar em `docs/marca/identidade-visual.md`. Usar sempre o mesmo em legendas.
- **Envolve:** perfil do Instagram
