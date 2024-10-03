Há duas formas de ler o dataset nesse repositório:

1 - acessando os arquivos das pastas transcricoes/materias/metadados.
2 - Acessando o arquivo dataset.jsonl. Essa forma é preferível, pois já tem todos os dados agrupados.

O arquivo dataset.jsonl foi gerado com o script gerar_jsonl_dataset.py. Esse script lê as matérias, metadados e transcrições e agrupa tudo em um jsonl.

Para ler o dataset:

import json

dataset = []
with open('dataset.jsonl', encoding='utf-8') as fin:
    for line in fin:
        dataset.append(json.loads(line))
        
Além disso, o script caracteristicas_dataset possui algumas informações estatísticas sobre as características do dataset.