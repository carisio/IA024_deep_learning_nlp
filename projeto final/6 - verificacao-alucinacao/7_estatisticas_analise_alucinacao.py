# Script para imprimir estatísticas do estudo sobre alucinação das opiniões

import json
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

arquivo_resultado_alucinacoes = './results_experimento_chatgpt_com_analise_alucinacao.jsonl'

prompt_1 = "prompt_1_gpt-4o-mini-2024-07-18"
prompt_1_gpt4_o = "prompt_1_gpt-4o-2024-08-06"

prompt_2 = "prompt_2_gpt-4o-mini-2024-07-18"
prompt_2_gpt4_o = "prompt_2_gpt-4o-2024-08-06"

prompt_3 = "prompt_3_gpt-4o-mini-2024-07-18"
prompt_3_gpt4_o = "prompt_3_gpt-4o-2024-08-06"

def carregar_resultado_alucinacoes():
    dados_jsonl = []
    with open(arquivo_resultado_alucinacoes, encoding='utf-8') as fin:
        for line in fin:
            dados_jsonl.append(json.loads(line))
    return dados_jsonl

def imprime_analise_estatistica_alucinacao(prompt, texto='', n=None):
    n = len(resultado_experimento) if n is None else n
    
    alucinacao_real = []
    alucinacao_automatica = []
    
    for resultado in resultado_experimento[:n]:
        for envolvido in resultado['metadados_extraidos']['envolvidos']:
            for opiniao in envolvido['opinioes']:
                verificacao_alucinacao = opiniao['verificacao_alucinacao']
                verificacao_manual = verificacao_alucinacao['verificacao_manual']
                verificacao_automatica = verificacao_alucinacao[prompt]['alucinacao']
                
                alucinacao_real.append(verificacao_manual)
                alucinacao_automatica.append(verificacao_automatica)
                
    cm = confusion_matrix(alucinacao_real, alucinacao_automatica)

    total_alucinacao = sum(alucinacao_real)
    total_nao_alucinacao = len(alucinacao_real) - total_alucinacao
    
    total_alucinacao_detectada = cm[1][1]
    perc_alucinacao_detectada = 100.*cm[1][1]/total_alucinacao
    total_falso_positivo = cm[0][1]
    perc_falso_positivo = 100.*cm[0][1]/total_nao_alucinacao
    
    print(f'##### {texto} #####\n')
    print(cm, '\n')
    
    print('##### Valores reais #####')
    print(f'Total de alucinação: {total_alucinacao} ({100.*total_alucinacao/(total_alucinacao+total_nao_alucinacao):.2f})%')
    print(f'Total não alucinação: {total_nao_alucinacao} ({100.*total_nao_alucinacao/(total_alucinacao+total_nao_alucinacao):.2f})%')
    
    print('\n##### Checando a detecção de alucinações #####')
    print(f'Alucinações detectadas corretamente: {total_alucinacao_detectada} ({perc_alucinacao_detectada:.2f}%)')
    print(f'Alucinações não detectadas: {cm[1][0]} ({100.*cm[1][0]/total_alucinacao:.2f}%)')
    
    print('\n##### Checando as opiniões que não são alucinações #####')
    print(f'Não alucinações detectadas corretamente: {cm[0][0]} ({100.*cm[0][0]/total_nao_alucinacao:.2f}%)')
    print(f'Não alucinações não detectadas: {total_falso_positivo} ({perc_falso_positivo:.2f}%)\n\n')
    
    return total_alucinacao_detectada, perc_alucinacao_detectada, total_falso_positivo, perc_falso_positivo

def plota_resultados_gpt(resultados_alucinacao_gpt_4o_mini,
                         resultados_alucinacao_gpt_4o,
                         resultados_falso_positivo_gpt_4o_mini,
                         resultados_falso_positivo_gpt_4o):
    # Definindo a paleta de cores global usando seaborn
    sns.set_palette('muted')  # Paleta de cores para todos os gráficos
    
    # Dados de exemplo: resultados dos experimentos (duas execuções)
    prompts = ['Prompt 1', 'Prompt 2', 'Prompt 3']
    
    # Definindo a posição das barras
    bar_width = 0.35
    x = np.arange(len(prompts))  # Posições dos grupos
    
    # Criando dois gráficos lado a lado
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))  # Dois gráficos em uma linha
    
    # Gráfico 1: Percentual de alucinações detectadas
    ax1.bar(x - bar_width/2, resultados_alucinacao_gpt_4o_mini, bar_width, label='GPT-4o mini')
    ax1.bar(x + bar_width/2, resultados_alucinacao_gpt_4o, bar_width, label='GPT-4o')
    #ax1.set_xlabel('Experimentos')
    ax1.set_ylabel('(%)')
    ax1.set_title('Hallucinations detected (%)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(prompts)
    ax1.legend()
    
    # Gráfico 2: Falsos positivos
    ax2.bar(x - bar_width/2, resultados_falso_positivo_gpt_4o_mini, bar_width, label='GPT-4o mini')
    ax2.bar(x + bar_width/2, resultados_falso_positivo_gpt_4o, bar_width, label='GPT-4o')
    #ax2.set_xlabel('Experimentos')
    ax2.set_ylabel('(%)')
    ax2.set_title('False positives (%)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(prompts)
    ax2.legend()
    
    # Ajustar o layout para não sobrepor os gráficos
    plt.tight_layout()
    
    # Exibir os gráficos
    plt.show()


resultado_experimento = carregar_resultado_alucinacoes()

n = 206

t_alu_p_1_4o_mini, p_alu_p_1_4o_mini, t_fp_p_1_4o_mini, p_fp_p_1_4o_mini = imprime_analise_estatistica_alucinacao(prompt_1, 'Prompt 1', n)
t_alu_p_2_4o_mini, p_alu_p_2_4o_mini, t_fp_p_2_4o_mini, p_fp_p_2_4o_mini = imprime_analise_estatistica_alucinacao(prompt_2, 'Prompt 2', n)
t_alu_p_3_4o_mini, p_alu_p_3_4o_mini, t_fp_p_3_4o_mini, p_fp_p_3_4o_mini = imprime_analise_estatistica_alucinacao(prompt_3, 'Prompt 3', n)

t_alu_p_1_4o, p_alu_p_1_4o, t_fp_p_1_4o, p_fp_p_1_4o = imprime_analise_estatistica_alucinacao(prompt_1_gpt4_o, 'Prompt 1 GPT4o', n)
t_alu_p_2_4o, p_alu_p_2_4o, t_fp_p_2_4o, p_fp_p_2_4o = imprime_analise_estatistica_alucinacao(prompt_2_gpt4_o, 'Prompt 2 GPT4o', n)
t_alu_p_3_4o, p_alu_p_3_4o, t_fp_p_3_4o, p_fp_p_3_4o = imprime_analise_estatistica_alucinacao(prompt_3_gpt4_o, 'Prompt 3 GPT4o', n)

resultados_alucinacao_gpt_4o = [p_alu_p_1_4o, p_alu_p_2_4o, p_alu_p_3_4o]
resultados_alucinacao_gpt_4o_mini = [p_alu_p_1_4o_mini, p_alu_p_2_4o_mini, p_alu_p_3_4o_mini]
resultados_falso_positivo_gpt_4o = [p_fp_p_1_4o, p_fp_p_2_4o, p_fp_p_3_4o]
resultados_falso_positivo_gpt_4o_mini = [p_fp_p_1_4o_mini, p_fp_p_2_4o_mini, p_fp_p_3_4o_mini]

plota_resultados_gpt(resultados_alucinacao_gpt_4o_mini, resultados_alucinacao_gpt_4o, resultados_falso_positivo_gpt_4o_mini, resultados_falso_positivo_gpt_4o)