---
name: project-qa
description: Planejar e executar QA de mudanças de local-layla, mapear critérios de aceitação a testes e relatar evidências antes de integração ou release. Usar na revisão do plano e após implementação, inclusive para regressões de scripts, skills, API local e Docker.
---

# QA de desenvolvimento e manutenção

Transforme critérios de aceitação em evidência reproduzível. Leia o pedido, o contrato do projeto alvo, pesquisa, spec/plano e diff atribuídos. Se esta skill foi instalada fora do repo, procure esses artefatos na raiz do projeto alvo; todos os recursos desta skill são relativos a esta pasta, sem exigir checkout ou Superpowers instalado.

## Planejar os testes

Depois da pesquisa e junto ao plano técnico, escolha o menor conjunto que detecta falhas plausíveis. Leia [a matriz por tipo de mudança](references/test-matrix.md). Para cada critério, registre cenário, nível de teste, comando/procedimento, resultado esperado, ambiente e se é obrigatório. Cubra erro/limite quando puder causar regressão concreta. Reutilize unittest e ferramentas existentes; não adicionar dependência, teste de prosa ou etapa sem benefício demonstrável.

Devolva a matriz ao planejador/coordenador. Para uma mudança pequena ela pode ficar no próprio plano; quando for extensa, escreva `qa-plan.md` no diretório SDD atribuído. Não mude spec/plano compartilhados se outro agente for dono. A execução de implementação continua com a skill Superpowers escolhida no plano do projeto.

## Verificar a entrega

1. Confirme SHA/base, diff, escopo, ambiente e matriz antes de rodar. Se houver mudanças não commitadas, registre-as; não apresente o SHA sozinho como identidade do conteúdo testado. Use checkout/worktree estável sem outro escritor; para tarefas paralelas, receba arquivos e recursos exclusivos do coordenador.
2. Rode as verificações obrigatórias aplicáveis, leia resultado e exit code. Teste comportamento observável: dados preservados, resposta HTTP, conflito recusado, serviço acessível. Um mock prova o contrato simulado; não prova inferência, Docker ou browser real.
3. Para falha, reproduza e registre entrada, passos mínimos, esperado/obtido, evidência e impacto. Diferencie defeito de produto, problema de teste e bloqueio ambiental sem adivinhar causa. Encaminhe ao implementador; não modifique produto, enfraqueça asserções ou faça retries até parecer verde. Registre intermitência. Depois da correção, reexecute o cenário e a regressão afetada.
4. Preencha [o relatório](references/report-template.md) em `docs/sdd/<mudanca>/qa-report.md`, ou no caminho atribuído. Registre comandos reais, resultados, commit, limitações e decisão por critério: **pass**, **fail**, **blocked** ou **not-run**. `pass` exige evidência atual; requisito obrigatório sem ambiente/evidência é `blocked`; `not-run` exige razão e classificação de escopo. Um check verde não compensa outro obrigatório omitido.
5. Recomende **pass** para integração somente quando todos os critérios/checks obrigatórios aplicáveis passarem e não houver defeito bloqueador aberto. Havendo falha obrigatória, recomende **fail**; sem falhas mas com verificação obrigatória indisponível, **blocked**. Fora do escopo pode ser `not-run` com justificativa. Entregue o relatório ao coordenador; QA não faz merge, tag ou release.

Evidência vale para o conteúdo testado. Alteração posterior de código, testes, configuração ou dependências exige revalidar os checks afetados e registrar o novo SHA. Um commit só de relatório/controle não invalida automaticamente resultados: examine o diff e explique o reaproveitamento. Verifique novamente o resultado combinado de branches; CI/testes de cada feature isolada não demonstram a combinação.

## Limites e continuidade

Escreva apenas relatório/matriz e testes expressamente atribuídos. Novos testes devem detectar um defeito plausível; se forem necessários, use tarefa/worktree própria e confirme que entram na validação final. Diagnóstico não autoriza correções silenciosas de produto. Não baixar modelos grandes, aprovar ações pendentes do Layla, alterar credenciais ou publicar remotamente para testar sem autorização correspondente. Preserve dados existentes e registre evidência sem tokens, dados pessoais ou conteúdo privado.

O papel de QA verifica aceitação/risco; revisão de código verifica a implementação e continua no fluxo existente. Em sessão sem delegação, o coordenador pode aplicar esta skill em uma passagem separada, registrando que foi autoavaliação.
