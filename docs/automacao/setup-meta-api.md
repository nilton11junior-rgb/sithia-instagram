# Configuração da API da Meta (uma vez)

Caminho escolhido: **Login do Instagram** (API do Instagram com Login do Instagram). Não precisa de Página do Facebook. Host da API: `graph.instagram.com`.

## Requisitos
- Conta do Instagram **Profissional** (Comercial ou Criador de conteúdo). O @ já aparece com "Painel profissional".
- Conta de desenvolvedor em developers.facebook.com (entra com o Facebook).

## Passos
1. Entrar em developers.facebook.com e concluir o registro de desenvolvedor.
2. Criar um app (tipo Empresa/Business) e adicionar o produto **Instagram**, na opção **API com Login do Instagram**.
3. Em "Configuração da API", adicionar a conta @ como **testador do Instagram** (Funções do app) e aceitar o convite no Instagram: Configurações > Apps e sites > Convites de testador.
4. Gerar o token na própria tela de configuração (permissões: `instagram_business_basic` e `instagram_business_content_publish`).
5. Trocar por um token de **longa duração** (60 dias) e anotar a data de vencimento.
6. Anotar o `IG_USER_ID` (ID da conta Instagram, mostrado na tela de configuração).
7. Guardar token e ID só em Secrets do GitHub (`IG_USER_ID`, `IG_ACCESS_TOKEN`) ou no `.env` local. Nunca em arquivo versionado.

## Modo desenvolvimento
Enquanto o app está em modo de desenvolvimento, ele publica na conta de quem é testador/administrador do app, sem precisar de revisão da Meta. Para uso só na conta da SITH.IA isso basta.

## Cuidados
- O token vence em 60 dias. Crie lembrete para renovar com 10 dias de antecedência.
- O repositório precisa ser público para as imagens abrirem por URL (ou troque a hospedagem das imagens).
- Limites da Meta: carrossel de 2 a 10 itens; 100 publicações por API a cada 24h (carrossel conta como uma).
- Se a Meta mudar nomes de menus, a documentação oficial da Instagram Platform prevalece sobre este guia.

Fonte dos requisitos: documentação de Content Publishing da Instagram Platform (developers.facebook.com/docs/instagram-platform/content-publishing).
