# SITH.IA — Automação de Instagram

Projeto que cria e publica carrosséis no Instagram da SITH.IA (criação de conteúdo visual com IA para marcas, negócios e creators).

**Fluxo:** escrever o conteúdo (JSON) → gerar os slides (PNG) → revisar → publicar no horário marcado.

## Estrutura

```
sithia-automacao-instagram/
├── README.md                  ← você está aqui
├── CLAUDE.md                  ← regras do projeto para o Claude (e para o VS Code)
├── docs/                      ← toda a documentação
│   ├── erros-e-acertos/       ← memória do projeto (ler antes de cada semana)
│   ├── marca/                 ← identidade visual
│   ├── conteudo/              ← pilares, formatos, guia de legendas
│   ├── automacao/             ← configuração da API da Meta e rotina semanal
│   └── pendencias.md          ← o que falta resolver
├── marca/
│   ├── assets/                ← logo e fontes
│   └── referencias/           ← artes e prints de referência
├── conteudo/
│   ├── calendario/            ← uma semana por arquivo (semana-AAAA-MM-DD.json)
│   └── modelos/               ← modelo para copiar
├── criativos/
│   └── gerados/<semana>/<post>/slide-NN.png   ← saída do render
├── src/
│   ├── render.py              ← gera os slides
│   └── publish.py             ← publica no Instagram
├── automacao/
│   └── github-workflow-publish.yml   ← agendador (mover para .github/workflows/)
└── estado/
    └── published.json         ← posts já publicados (não apagar)
```

## Uso rápido

```bash
pip install -r requirements.txt
playwright install chromium

python src/render.py conteudo/calendario/semana-2026-10-05.json
python src/publish.py conteudo/calendario/semana-2026-10-05.json --dry-run
```

Rotina completa da semana: [docs/automacao/fluxo-semanal.md](docs/automacao/fluxo-semanal.md).
Configuração única da Meta: [docs/automacao/setup-meta-api.md](docs/automacao/setup-meta-api.md).

## Primeiros passos no VS Code

1. Abrir a pasta do projeto.
2. Ler `docs/pendencias.md` e `docs/erros-e-acertos/erros.md`.
3. Mover `automacao/github-workflow-publish.yml` para `.github/workflows/publish.yml`.
4. Copiar `.env.example` para `.env` e preencher (só para testes locais; nunca subir o `.env`).
