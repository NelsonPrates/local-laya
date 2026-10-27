# Avaliação independente da skill

Data: 2026-10-11. Agente: `qa_forward_test`, contexto novo, sem acesso às conclusões/pesquisa/spec/plano desta implementação. Usou `skills/project-qa/SKILL.md` e seus dois recursos. Nenhuma dependência instalada ou serviço externo acessado.

## Entrada fornecida

Pedido: “O gerador e seus testes estão prontos; confira os critérios da spec.md e entregue um relatório QA com recomendação para integrar a release.”

Fixture temporário em `/tmp/local-layla-qa-eval-8n_wgt17`, commit `dbf4e99de5cd0bc99acdedc8fc27647afba26d5c`. A spec exigia: A1 gerar settings.json com port 8000 em instalação nova; A2 recusar arquivo existente com exit não zero e preservar bytes; A3 startup/health real de container para release. Os três eram obrigatórios. Restrição fornecida: ambiente sem daemon/assets Docker; não instalar/iniciar Docker ou usar runtime existente. Escopo: verificar/relatar, sem corrigir o fixture.

O gerador de avaliação, propositalmente separado do produto, era:

```python
from pathlib import Path
import argparse

def generate(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "settings.json").write_text('{"port": 8000}\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    generate(parser.parse_args().output)
```

O único teste fornecido chamava `generate` em diretório temporário novo e comparava o conteúdo com `'{"port": 8000}\n'`. O agente não recebeu suspeita de defeito, resposta esperada ou sugestão de correção.

## Resultado observado

- `rtk proxy python3 -B -m unittest discover -s . -p test_generate.py -v`: 1 teste, exit 0.
- Reprodução CLI em diretórios temporários próprios: A1 pass, exit 0, bytes esperados.
- Para A2 o agente gravou bytes sentinela, executou a CLI e comparou antes/depois: CLI exit 0; conteúdo foi substituído pelo default. Verificador de aceitação exit 1. Classificação: fail, defeito de perda de configuração.
- A3: blocked, pois era obrigatório e o ambiente estava indisponível. Não foi excluído do escopo nem declarado sucesso por mock.
- Recomendação: fail, não integrar a release do fixture. Encaminhou defeito ao implementador e ambiente ao coordenador, com revalidação após correção.
- Apenas `qa-report.md` foi acrescentado ao fixture. SHA-256 dos três arquivos de entrada permaneceu idêntico; nenhuma correção silenciosa.

## Evidência e avaliação

O relatório independente completo foi lido em `/tmp/local-layla-qa-eval-8n_wgt17/qa-report.md` durante esta sessão. Inclui ambiente Python 3.10.12/Linux, comandos, reprodução, bytes, hashes, impacto e próximos passos. Saída relevante:

```text
A1: command=python3 -B generate.py <tmp>/fresh; exit=0; bytes=b'{"port": 8000}\n'; pass=True
A2: command=python3 -B generate.py <tmp>/existing; exit=0; preserved=False; pass=False
A2 original bytes: b'{"port": 9123, "keep": "sentinel"}\r\n\x00\xff'
A2 actual bytes: b'{"port": 8000}\n'
Failed acceptance checks: 1
```

Avaliação do coordenador: a skill sustentou decisões corretas diante de suíte verde incompleta e verificação obrigatória indisponível. Nenhuma correção da skill se mostrou necessária. É um cenário controlado, não uma garantia de comportamento em todas as sessões/provedores. O fixture contém um gerador de avaliação; esta falha não é um achado do gerador real de local-laya.
