# Atribuição

Este projeto fornece scripts e instruções independentes para integrar o
[PapaKoftes/Layla](https://github.com/PapaKoftes/Layla), de seus respectivos autores.
Não há código-fonte upstream vendorizado neste repositório. O Dockerfile obtém
o projeto durante a compilação e mantém seu arquivo `LICENSE` em `/opt/layla/LICENSE`.

Layla usa a **Layla Non-Commercial Source License**. Sua licença não é substituída
pela MIT dos scripts próprios de local-layla. Uso comercial do Layla depende
dos termos e da autorização de seus titulares. O nome é usado aqui para
identificar a integração, sem afiliação oficial.

Modelos GGUF são fornecidos pelo usuário ou obtidos pela configuração do app,
e continuam sujeitos à licença do modelo. Dependências instaladas na imagem
mantêm suas respectivas licenças.

## Superpowers

`vendor/superpowers/` contém as skills de [obra/superpowers](https://github.com/obra/superpowers),
em revisão `bb92a77741419a4ab5f06e711a283343f1ada0c3`. A licença MIT original
está preservada em `vendor/superpowers/LICENSE`; a origem e os hashes constam
em `source.lock.json`. Os arquivos upstream não foram adaptados. O contrato
SDD deste projeto explicita sua ordem pesquisa → plano → execução e prevalece
sobre defaults da biblioteca quando houver diferença.
