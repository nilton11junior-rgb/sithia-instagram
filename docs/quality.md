# Qualidade

## Comandos
| O quê | Comando | Observação |
|---|---|---|
| Verificação completa | `python3 scripts/check.py` | Sai com código 1 se houver ERRO. Não publica, não usa rede, não lê segredos. |
| Autotestes da verificação | `pytest -q` | Testam as regras do calendário (`tests/test_check.py`). |
| Lint | `ruff check src scripts tests` | Configurado em `pyproject.toml`. Já roda dentro do check. |
| Simular publicação | `python3 src/publish.py <json> --dry-run` | Não chama a API. |
| Tipos / build | não existem | São scripts Python soltos, sem empacotamento. |

## O que o `check.py` garante
- Todos os `.py` compilam.
- O ruff passa com as regras `E`, `F` e `I`.
- Cada `.py` com mais de 350 linhas gera um **aviso** (é a referência do toolkit, não reprova).
- Para cada post do calendário:
  - o JSON é válido e o `id` é único;
  - `publicar_em` está em ISO com fuso;
  - `aprovado` é booleano;
  - a legenda não está vazia e tem até 2.200 caracteres;
  - há no máximo 30 hashtags. Acima de 5 é **aviso** e só vale para post ainda não publicado.
- Para post **não publicado**:
  - as imagens citadas existem;
  - se estiver aprovado, tem de 2 a 10 `slide-NN.jpg` em `criativos/gerados/**/<id>/`, que é o que o robô exige.
- Avisos servem para medir regras novas sem quebrar posts antigos. Uma regra só vira erro quando não houver violação antiga.

## Linha de base (18/10/2026, antes do setup)
- Compilação: ok. JSON do calendário: todos válidos. Testes: não existiam.
- `ruff` com a config global da máquina: 30 avisos.
- Com a config do projeto (E/F/I): 84 avisos.
  - 70 E501: linhas longas de HTML/CSS. Ficaram ignoradas de propósito; não vale reformatar os renders.
  - 12 de ordem de imports e 1 import sem uso: corrigidos.
  - 1 variável `l` ambígua: corrigida.
- Maior arquivo: `src/render_portfolio.py`, com 196 linhas.

## Revisão de segurança
Use em mudanças no robô de publicação, nos segredos ou no workflow, ou para fazer uma linha de base periódica.
- **Fonte:** prompt 13 do vibe-coding-toolkit, revisão `de66fe371a49f5a4d3b521759e5c401f390b6424`, (arquivo `docs/prompts/13-security-review.md` do toolkit, não deste repositório). Para atualizar, leia a versão atual do `main` e registre a nova revisão aqui.
- **Como chamar (colar no chat):** "Leia https://raw.githubusercontent.com/soumatheusgomes/vibe-coding-toolkit/main/docs/prompts/13-security-review.md e execute o bloco "Prompt" neste repositório, em modo repositório, com relatório redigido fora do repositório."
- **Limites deste projeto:**
  - a revisão só lê o repositório;
  - não chama a Graph API nem testa o token;
  - o relatório fica fora do repositório, porque ele é público;
  - correções exigem um pedido separado.
- O skill `differential-review` não está instalado. A revisão de diff é feita por leitura manual do código, e isso deve ser registrado no relatório.

## Revisão de mudanças
- Proporcional ao risco.
- Mudança no robô, nos segredos ou no workflow: revisão independente (subagente só leitura) com cenário de falha concreto.
- Mudança só de conteúdo: o `check.py` e a conferência visual dos slides (capa, um slide do meio e o CTA) bastam.
