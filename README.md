# SITH.IA — Automação de Instagram

Projeto que cria e publica carrosséis no Instagram da SITH.IA (criação de conteúdo visual com IA para marcas, negócios e creators).

**Fluxo:** escrever o conteúdo (JSON) → gerar os slides (PNG) → revisar → publicar no horário marcado.

## Documentação
- Regras para agentes de IA: [AGENTS.md](AGENTS.md) (e [CLAUDE.md](CLAUDE.md), específico do Claude).
- Produto e escopo: [PRODUCT.md](PRODUCT.md) · Arquitetura: [docs/architecture.md](docs/architecture.md) · Visual: [docs/design.md](docs/design.md).
- Preparar a máquina: [docs/onboarding.md](docs/onboarding.md) · Verificações: [docs/quality.md](docs/quality.md) · Setup do toolkit: [docs/setup.md](docs/setup.md).
- Memória do projeto: [docs/erros-e-acertos/](docs/erros-e-acertos/) e [docs/pendencias.md](docs/pendencias.md).

## Uso rápido

```bash
pip install -r requirements.txt
playwright install chromium

python3 scripts/check.py                                                  # verifica tudo (não publica)
python3 src/render_prompt_pack.py conteudo/calendario/prompt-pack-halloween.json
python3 src/publish.py conteudo/calendario/prompt-pack-halloween.json --dry-run
```

⚠️ Push em `conteudo/calendario/` acorda o robô e publica os posts aprovados que já venceram.

Rotina da semana: [docs/automacao/fluxo-semanal.md](docs/automacao/fluxo-semanal.md). Configuração da Meta: [docs/automacao/setup-meta-api.md](docs/automacao/setup-meta-api.md).

## Próxima entrega
Ver [PRODUCT.md](PRODUCT.md#próxima-entrega).
