# Relatório QA: <mudanca>

Data/agente: <UTC ou timezone explícito; identidade>. Modo: <independente ou autoavaliação>.
Alvo: <SHA completo testado>, base: <SHA>; worktree: <limpa ou diff/arquivos não commitados identificados>.
Ambiente: <SO, versões relevantes, serviço simulado/real, pré-requisitos>.
Escopo: <critérios e mudanças>; fora do escopo: <razão>.

| Critério/check | Obrigatório? | Comando ou procedimento real | Esperado | Obtido e exit code | Estado | Evidência |
| --- | --- | --- | --- | --- | --- | --- |
| <ID> | <sim/não e motivo> | <comando executado ou não executado> | <resultado observável> | <resultado real/indisponível> | <pass/fail/blocked/not-run> | <saída curta ou artefato sem segredo> |

## Defeitos e bloqueios

Para cada ocorrência: impacto, arquivo/entrada, passos mínimos, esperado/obtido, frequência, evidência e próximo responsável. Se não reproduzido, não inventar causa. Falha pré-existente continua visível; anotar comparação com a base quando feita.

## Decisão

<pass/fail/blocked>, porque <critérios obrigatórios e defeitos>. Listar checks fora do escopo não executados e riscos residuais relevantes. Não preencher pass com base em relato de outro agente ou em execução antiga sem verificar sua aplicabilidade.

## Revalidação

Após correção/integração: <novo SHA, diff relevante, checks repetidos e resultado>. Se apenas relatório/controle mudou, identificar o diff que permite reaproveitar evidências. O coordenador recebe a recomendação e decide integração dentro da autorização da sessão.
