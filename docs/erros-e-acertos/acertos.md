# Acertos

Mais recente primeiro. Modelo em [_modelo.md](_modelo.md).

### 2026-10-02 · Procurar o arquivo original antes de recortar  `#criativo` `#marca`
- **O que fizemos:** nos arquivos do projeto havia a foto de perfil original do Instagram (1254x1254). Usamos ela no Facebook e extraímos dela uma logo nítida com fundo transparente.
- **Resultado:** logo em alta resolução em `marca/assets/logo.png`, foto de perfil e capa do Facebook iguais à identidade do Instagram.
- **Por que funcionou:** o original sempre é melhor que um recorte de arte pronta.
- **Como repetir:** antes de recortar algo de uma arte, abrir todos os arquivos do projeto e procurar o original.

### 2026-10-01 · Separar conteúdo (JSON) de design (código)  `#processo` `#automacao`
- **O que fizemos:** textos e horários ficam em `conteudo/calendario/*.json`; o visual fica em `src/render.py`.
- **Resultado:** uma semana nova é só copiar o modelo e trocar os textos; os 3 carrosséis de exemplo saíram em segundos.
- **Por que funcionou:** quem escreve não mexe em código, e quem mexe no design não perde o conteúdo.
- **Como repetir:** nunca escrever texto de slide direto no código.

### 2026-10-01 · Identidade visual copiada das artes que já existiam  `#criativo` `#marca`
- **O que fizemos:** extraímos do post "O que fazemos" e do perfil: fundo preto, azul-índigo, títulos brancos grossos com palavra-chave em azul, rótulos com letras espaçadas, brilho no canto inferior.
- **Resultado:** os carrosséis novos combinam com os posts fixados do perfil.
- **Por que funcionou:** consistência faz o perfil parecer uma marca, não um conjunto de posts soltos.
- **Como repetir:** consultar `docs/marca/identidade-visual.md` antes de criar um formato novo.

### 2026-10-01 · Modo de teste antes de publicar (`--dry-run`)  `#automacao`
- **O que fizemos:** o publicador tem um modo que só mostra o que faria, sem postar.
- **Resultado:** deu para validar datas e arquivos sem risco de publicar errado.
- **Por que funcionou:** publicar no Instagram não tem "desfazer" prático.
- **Como repetir:** rodar sempre `--dry-run` depois de mudar o calendário ou o script.

### 2026-10-01 · Registro de posts já publicados  `#automacao`
- **O que fizemos:** `estado/published.json` guarda o ID de cada post publicado.
- **Resultado:** o agendador roda a cada 30 minutos sem risco de postar o mesmo carrossel duas vezes.
- **Por que funcionou:** a automação é idempotente: rodar de novo não repete efeito.
- **Como repetir:** nunca apagar esse arquivo sem necessidade; ele é a memória do que já saiu.

### 2026-10-01 · Conferir os slides visualmente antes de entregar  `#criativo` `#processo`
- **O que fizemos:** abrimos capa, slide de item e CTA e checamos quebra de linha, contraste e margens.
- **Resultado:** nenhum texto cortado ou ilegível nos exemplos.
- **Por que funcionou:** erro de layout só aparece olhando a imagem, não o código.
- **Como repetir:** olhar pelo menos capa, um miolo e o CTA de cada carrossel novo.
