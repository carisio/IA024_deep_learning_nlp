# Script para imprimir estatísticas do estudo sobre alucinação das opiniões

import json
from sklearn.metrics import confusion_matrix

arquivo_resultado_alucinacoes = './results_experimento_chatgpt_com_analise_alucinacao.jsonl'

prompt_1 = "prompt_1_gpt-4o-mini-2024-07-18"

def carregar_resultado_alucinacoes():
    dados_jsonl = []
    with open(arquivo_resultado_alucinacoes, encoding='utf-8') as fin:
        for line in fin:
            dados_jsonl.append(json.loads(line))
    return dados_jsonl

def imprime_analise_estatistica_alucinacao(prompt):
    alucinacao_real = []
    alucinacao_automatica = []
    
    for resultado in resultado_experimento:
        for envolvido in resultado['metadados_extraidos']['envolvidos']:
            for opiniao in envolvido['opinioes']:
                verificacao_alucinacao = opiniao['verificacao_alucinacao']
                verificacao_manual = verificacao_alucinacao['verificacao_manual']
                verificacao_automatica = verificacao_alucinacao[prompt]['alucinacao']
                
                alucinacao_real.append(verificacao_manual)
                alucinacao_automatica.append(verificacao_automatica)
                
    cm = confusion_matrix(alucinacao_real, alucinacao_automatica)
    print(cm)

    total_alucinacao = sum(alucinacao_real)
    total_nao_alucinacao = len(alucinacao_real) - total_alucinacao
    print('')
    print('##### Valores reais #####')
    print(f'Total de alucinação: {total_alucinacao} ({100.*total_alucinacao/(total_alucinacao+total_nao_alucinacao):.2f})%')
    print(f'Total não alucinação: {total_nao_alucinacao} ({100.*total_nao_alucinacao/(total_alucinacao+total_nao_alucinacao):.2f})%')
    
    print('\n##### Checando a detecção de alucinações #####')
    print(f'Alucinações detectadas corretamente: {cm[1][1]} ({100.*cm[1][1]/total_alucinacao:.2f}%)')
    print(f'Alucinações não detectadas: {cm[1][0]} ({100.*cm[1][0]/total_alucinacao:.2f}%)')
    
    print('\n##### Checando as opiniões que não são alucinações #####')
    print(f'Não alucinações detectadas corretamente: {cm[0][0]} ({100.*cm[0][0]/total_nao_alucinacao:.2f}%)')
    print(f'Não alucinações não detectadas: {cm[0][1]} ({100.*cm[0][1]/total_nao_alucinacao:.2f}%)')
    
resultado_experimento = carregar_resultado_alucinacoes()

cm = imprime_analise_estatistica_alucinacao(prompt_1)