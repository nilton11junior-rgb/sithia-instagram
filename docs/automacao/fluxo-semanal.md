# Fluxo semanal

Tempo estimado: 30 a 45 minutos por semana.

## Domingo (ou sexta anterior)
1. Ler `docs/erros-e-acertos/erros.md` e `docs/pendencias.md`.
2. Copiar `conteudo/modelos/semana-modelo.json` para `conteudo/calendario/semana-AAAA-MM-DD.json` (data da segunda-feira).
3. Preencher: `semana`, e para cada post `id`, `publicar_em` (com `-03:00`), `legenda` e `slides`.
4. Gerar: `python src/render.py conteudo/calendario/semana-AAAA-MM-DD.json`.
5. Conferir capa, um miolo e o CTA de cada carrossel em `criativos/gerados/AAAA-MM-DD/`.
6. Testar: `python src/publish.py conteudo/calendario/semana-AAAA-MM-DD.json --dry-run`.
7. Commit e push. O agendador do GitHub publica no horário.

## Durante a semana
- Conferir no Instagram se o post saiu no horário.
- Responder comentários e DMs.

## Fim da semana
- Anotar alcance, salvamentos e DMs de cada post.
- Registrar o que funcionou em `acertos.md` e o que falhou em `erros.md`.

## Campos do JSON
| Campo | Descrição |
|---|---|
| `tipo: capa` | `kicker`, `titulo`, `sub` |
| `tipo: item` | `num`, `titulo`, `texto` |
| `tipo: cta` | `titulo`, `sub`, `botao` |

Use `*palavra*` para destacar em azul.
