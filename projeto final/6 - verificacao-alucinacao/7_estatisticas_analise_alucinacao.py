# Script para imprimir estatísticas do estudo sobre alucinação das opiniões

import json
from sklearn.metrics import confusion_matrix

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
    print(f'##### {texto} #####\n')
    print(cm, '\n')
    
    print('##### Valores reais #####')
    print(f'Total de alucinação: {total_alucinacao} ({100.*total_alucinacao/(total_alucinacao+total_nao_alucinacao):.2f})%')
    print(f'Total não alucinação: {total_nao_alucinacao} ({100.*total_nao_alucinacao/(total_alucinacao+total_nao_alucinacao):.2f})%')
    
    print('\n##### Checando a detecção de alucinações #####')
    print(f'Alucinações detectadas corretamente: {cm[1][1]} ({100.*cm[1][1]/total_alucinacao:.2f}%)')
    print(f'Alucinações não detectadas: {cm[1][0]} ({100.*cm[1][0]/total_alucinacao:.2f}%)')
    
    print('\n##### Checando as opiniões que não são alucinações #####')
    print(f'Não alucinações detectadas corretamente: {cm[0][0]} ({100.*cm[0][0]/total_nao_alucinacao:.2f}%)')
    print(f'Não alucinações não detectadas: {cm[0][1]} ({100.*cm[0][1]/total_nao_alucinacao:.2f}%)\n\n')
    
resultado_experimento = carregar_resultado_alucinacoes()

n = 206
#imprime_analise_estatistica_alucinacao(prompt_1, 'Prompt 1', n)
#imprime_analise_estatistica_alucinacao(prompt_2, 'Prompt 2', n)
#imprime_analise_estatistica_alucinacao(prompt_3, 'Prompt 3', n)

#imprime_analise_estatistica_alucinacao(prompt_1_gpt4_o, 'Prompt 1 GPT4o', n)
imprime_analise_estatistica_alucinacao(prompt_2_gpt4_o, 'Prompt 2 GPT4o', n)
imprime_analise_estatistica_alucinacao(prompt_3_gpt4_o, 'Prompt 1 GPT4o', n)
