# Spec: agente QA/testes

Adicionar o papel compartilhado `qa-test`, adaptadores Codex/Claude e a skill própria `project-qa`. O usuário pediu o agente e seleção de skills de inspiração; nomes, artefatos e estratégia abaixo são decisões técnicas locais.

## Aceitação

- A1: QA participa do plano depois da pesquisa e verifica a entrega depois da execução Superpowers, antes da integração Gitflow. Definir responsabilidade, handoff e retorno por defeito sem substituir revisão de código.
- A2: Seleção baseada em fontes primárias: testing-strategy e três skills Superpowers, webapp-testing condicional. Preservar a stack unittest e a cópia vendorizada.
- A3: Agentes Codex/Claude apontam ao mesmo contrato, sem fixar modelo. QA executa testes e escreve apenas artefatos/testes atribuídos, com isolamento e um escritor por arquivo.
- A4: A skill copiada é autocontida; instalação inclui seus recursos, preserva destinos existentes e descoberta funciona para ambos os provedores.
- A5: Relatório distingue pass/fail/blocked/not-run, liga evidência ao commit/ambiente e não aprova teste obrigatório omitido. Definir revalidação após correção/integração e separar API saudável de inferência real.

Fora do escopo: mudar o produto Layla, adicionar frameworks/browser, executar modelo GGUF, modificar Superpowers, publicar versão/tag ou configurar proteção remota. A exigência de QA é um contrato dos agentes; esta mudança não cria um gate automatizado de leitura do relatório.
