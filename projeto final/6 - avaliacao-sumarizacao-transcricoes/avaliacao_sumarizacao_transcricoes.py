import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Métricas precisão e recall:
evaluations = []
with open('evaluation_results.jsonl', encoding='utf-8') as fin:
    for line in fin:
        evaluations.append(json.loads(line))


recall = [r['metricas']['recall'] for r in evaluations]
evaluations[0]['metricas']
df_metricas = pd.DataFrame({
    "id": [r['id'] for r in evaluations],
    "recall": [r['metricas']['recall'] for r in evaluations],
    "precisao": [r['metricas']['precisao'] for r in evaluations],
})

# Resultados das alucinação:
hallucinations = []
with open('hallucination_results.jsonl', encoding='utf-8') as fin:
    for line in fin:
        hallucinations.append(json.loads(line))


df_alucinacao = pd.DataFrame({
    "id": [h['id'] for h in hallucinations],
    "alucinacao": [h['metricas']['proporcao_alucinacao'] for h in hallucinations]
})

# Agrega num único df a precisão, recall e alucinação:
df_metricas = pd.merge(df_metricas, df_alucinacao, on='id', how='outer')

print(df_metricas.describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95]))