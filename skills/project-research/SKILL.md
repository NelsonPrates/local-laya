---
name: project-research
description: Pesquisar e registrar evidências antes do planejamento de desenvolvimento ou manutenção de local-laya, incluindo upstream Layla, Docker, APIs, dependências e workflows de agentes. Use como primeira etapa SDD, antes de propor implementação.
---

# Pesquisa para desenvolvimento e manutenção

Produza um `research.md` que permita ao planejador decidir sem repetir descobertas. Use `references/research-template.md` como formato mínimo e copie/adapte seu conteúdo para `docs/sdd/<mudanca>/research.md` na raiz do projeto.

1. Releia o pedido e a autorização da sessão. Identifique a decisão técnica a resolver e os critérios do usuário; reduza a pesquisa a isso.
2. Confira `AGENTS.md`, os arquivos envolvidos, testes existentes, revisões travadas e resultados reproduzíveis. Procure com `rg`; quando não existir clone/upstream, consulte fontes oficiais. Não exponha configurações privadas nem tokens no relatório público.
3. Verifique APIs e comportamentos dependentes de versão em código upstream/documentação primária. Registre URL, revisão/versão, data de consulta, evidência e implicação; diferencie fato, hipótese e escolha técnica. Execute apenas experimentos pequenos, reversíveis e dentro do escopo autorizado.
4. Compare somente alternativas plausíveis pelos critérios relevantes: simplicidade, compatibilidade com o repo, manutenção, recursos e licença. Recomende a menor opção suficiente, explicando o custo concreto.
5. Registre lacunas que alteram o plano e proponha como resolvê-las. Pare quando houver evidência suficiente para os critérios de aceitação; não prolongue a pesquisa para catalogar tudo.

A pesquisa não implementa produto nem faz merges, releases ou downloads grandes de modelos. Sua entrega é evidência e uma recomendação, não um plano já aprovado. Encaminhe ao papel `docs/workflow/tech-planner.md` quando estiver disponível. Se a skill foi copiada para outro local, encontre esse papel na raiz do projeto alvo, sem depender de `../../..` do local da skill.
