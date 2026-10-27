---
name: layla-docker
description: Criar scripts e orientar a instalação, configuração e operação local do PapaKoftes/Layla em Docker Compose, com modelo GGUF e dados persistentes. Use para preparar ou diagnosticar o container; para conversar com uma instância pronta, use layla-local.
---

# Layla em Docker

Use o gerador incluído para produzir uma instalação independente e explicar seus comandos ao usuário. O projeto alvo é [PapaKoftes/Layla](https://github.com/PapaKoftes/Layla); não confundir com Layla-Server, o app móvel ou Ollama.

1. Verifique Python 3.10+, Docker Engine/Desktop em execução e Compose v2 (`docker info`, `docker compose version`). Se faltarem, consulte as instruções oficiais para o sistema do usuário; não instale pacotes de outro sistema.
2. Escolha um diretório de instalação. Use um GGUF já fornecido pelo usuário ou prepare somente a interface para seleção/download posterior. Não invente URLs de modelos nem baixe vários GB sem que isso faça parte do pedido.
3. Execute, a partir desta pasta de skill:

   ```bash
   python3 scripts/setup.py --output ~/local-laya-runtime --model /caminho/modelo.gguf
   ```

   `--model` é opcional. `--port 8001` resolve uma porta ocupada. O gerador copia o GGUF e preserva instalações existentes recusando sobrescrita; não apagar dados para contornar essa recusa.
4. No diretório gerado, execute `./layla config` e, se a instalação foi solicitada, `./layla up`. A primeira compilação CPU pode levar vários minutos e baixar dependências grandes. Explique o progresso e os erros observados.
5. Consulte `./layla health`, abra `http://127.0.0.1:PORTA/ui` e use `./layla ready`. Só declare a inferência pronta quando `model_loaded` for verdadeiro e uma mensagem simples tiver resposta do modelo. API acessível e container healthy não comprovam inferência.

Leia [references/operations.md](references/operations.md) para modelo, limites, atualização, backup e problemas de Docker. Os arquivos em `assets/container/` são templates editáveis; adapte-os quando o usuário pedir scripts diferentes, mantendo a coerência entre volumes e caminhos.

Os defaults são CPU, `n_gpu_layers=0`, porta publicada somente em `127.0.0.1`, dados em `/data`, modelos em `/data/models` e workspace em `/workspace`. Não montar a pasta pessoal inteira nem o socket Docker. Não apresentar essa imagem CPU como aceleração CUDA; GPU exige outra imagem e validação específica.

Mantenha o SHA do upstream explícito e verificado. Não usar `latest` como se fosse uma revisão estável. Uma nova revisão exige conferir Docker, schemas e prontidão. As dependências Python e a imagem base ainda são resolvidas durante o build; o SHA sozinho não torna o build byte a byte reproduzível.
