# Produto: automação do Instagram da SITH.IA

## O que é
Repositório que cria e publica, todos os dias, carrosséis no Instagram **@sith.ia.oficial**. A SITH.IA é o estúdio criativo com IA do Nilton e do Bruno.
- **Renda principal:** sites e rebranding.
- **Outros serviços:** campanhas com IA, vídeos e influencer virtual.

## Para quem
- **Público do perfil:** empresas e creators que querem presença digital (clientes pagantes) e pessoas interessadas em IA (alcance).
- **Usuário do repositório:** um agente de IA (Claude) que produz tudo. O Nilton só aprova no chat.

## Fluxos críticos (observados)
1. **Planejar:** rodízio diário notícia → portfólio → prompt. Horários BRT: dias úteis 12h, fim de semana 10h. Regras em `CLAUDE.md`.
2. **Produzir:** gerar imagens no ChatGPT, escrever o JSON em `conteudo/calendario/`, rodar `src/render_*.py` e `src/export_jpg.py`.
3. **Aprovar:** mostrar ao Nilton. Só com o OK dele o post recebe `"aprovado": true`.
4. **Publicar:** o GitHub Actions (`.github/workflows/publish.yml`) publica pela Graph API no horário e grava `estado/published.json`.

## Fora do escopo
- Responder comentários e DMs.
- Anúncios pagos.
- Reels/vídeo (pendente em `docs/pendencias.md`).
- Relatórios de alcance.

## Critérios de aceite de um post
- Segue o fluxo obrigatório de `CLAUDE.md`, com referência, qualidade, personagem certo e legenda com o plugin.
- `python3 scripts/check.py` sem erro: JSON válido, data com fuso, imagens existentes, de 2 a 10 slides JPEG, legenda dentro dos limites.
- Aprovado pelo Nilton no chat antes do horário.

## Próxima entrega
- Plano 19–25/10: `docs/conteudo/plano-2026-10-19.md`.
- Peças do perfil aguardando aprovação: fixado de serviços e destaques.
