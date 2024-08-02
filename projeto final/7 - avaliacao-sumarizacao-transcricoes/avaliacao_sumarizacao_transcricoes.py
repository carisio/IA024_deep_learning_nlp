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

# Remove do dataframe os dados do id == 111
df_metricas = df_metricas[df_metricas['id'] != 111]

print(df_metricas.describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95]))



# Agora gera novamente as mesmas métricas, mas removendo todas as opiniões que são alucinações
id = []
recall = []
precisao = []
alucinacao = []

for r in evaluations:
    # Extrai os dados originais do experimento
    id_i = r['id']
    metricas_i = r['metricas']
    total_opinioes_esperadas_i = metricas_i['total_opinioes_esperadas']
    total_opinioes_preditas_i = metricas_i['total_opinioes_preditas']
    opinioes_esperadas_mapeadas_i = metricas_i['opinioes_esperadas_mapeadas']
    opinioes_preditas_mapeadas_i = metricas_i['opinioes_preditas_mapeadas']
    
    # Extrai o total de opiniões que são alucinações
    alucinacao_i = [h for h in hallucinations if h['id'] == id_i][0]
    total_opinioes_alucinadas_i = alucinacao_i['metricas']['total_opinioes_alucinadas']
    
    # Remove as opiniões que são alucinações
    total_opinioes_preditas_i = total_opinioes_preditas_i - total_opinioes_alucinadas_i
    total_opinioes_alucinadas_i = 0
    
    # Calcula recall, precisão e alucinação
    # Desconsidera o cálculo para a id 111. É o caso em que o cálculo de
    # alucinação não funciona
    if id_i != 111:
        id.append(id_i)
        recall.append(opinioes_esperadas_mapeadas_i/total_opinioes_esperadas_i)
        precisao.append(opinioes_preditas_mapeadas_i/total_opinioes_preditas_i)
        alucinacao.append(0)
    
df_metricas_sem_alucinacao = pd.DataFrame({
    "id": id,
    "recall": recall,
    "precisao": precisao,
    "alucinacao": alucinacao
})
print(df_metricas_sem_alucinacao.describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95]))