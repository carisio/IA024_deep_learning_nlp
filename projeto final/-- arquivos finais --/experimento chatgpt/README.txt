Os resultados do experimento com o ChatGPT pode ser acessado de duas formas:

1 - Acessando os arquivos da pasta resultados.
2 - Acessando o arquivo results_experiment_chatgpt.jsonl. Essa forma é preferível, pois já tem todos os dados agrupados.

O arquivo results_experiment_chatgpt.jsonl foi gerado com o script gerar_jsonl_resultado_experimento_chatgpt.py. Esse script lê os txt da pasta resultados e agrega em um único jsonl.

Para ler o arquivo:

import json

results_experiment_chatgpt = []
with open('results_experiment_chatgpt.jsonl', encoding='utf-8') as fin:
    for line in fin:
        results_experiment_chatgpt.append(json.loads(line))