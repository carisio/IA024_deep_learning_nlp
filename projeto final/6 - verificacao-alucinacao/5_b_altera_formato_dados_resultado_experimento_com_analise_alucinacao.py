# A ideia desse arquivo é ler os resultados que estão em 4 arquivos e 
# alterar o formato de dados. As alterações são:
# - Remoção dos embeddings dos chunks próximos da opinião
# - Remoção da distância dos chunks próximos para a opinião
# - Criação de um novo parâmetro verificacao_alucinacao para o formato:
#     verificacao_alucinacao: {
#       "manual": True/False,
#       "prompt_1_gpt-4o-mini-2024-07-18": {
#               "alucinacao": True/False
#               "explicacao": string
#           }
#       }
# - Remoção dos outros atributos sobre alucinação (visto que serão condensados
#      na estrutura acima)

import json

arquivo_experimento_com_analise_alucinacao = './results_experimento_chatgpt_com_analise_alucinacao_parte_{parte}.jsonl'
arquivo_saida = './results_experimento_chatgpt_com_analise_alucinacao.jsonl'

resultado_experimento = []

###################################################################
# Funções auxiliares para carregar e salvar um jsonl
def carregar_jsonl(nome_arquivo):
    dados_jsonl = []
    with open(nome_arquivo , encoding='utf-8') as fin:
        for line in fin:
            dados_jsonl.append(json.loads(line))
    return dados_jsonl

def salvar_jsonl_final(lista):
    with open(arquivo_saida, 'w', encoding='utf-8') as arquivo:
        for item in lista:
            linha = json.dumps(item, ensure_ascii=False)
            arquivo.write(linha + '\n')
            
def carregar_resultado_experimento_com_analise_alucinacao():
    resultado_experimento = carregar_jsonl(arquivo_experimento_com_analise_alucinacao.format(parte=1))
    resultado_experimento.extend(carregar_jsonl(arquivo_experimento_com_analise_alucinacao.format(parte=2)))
    resultado_experimento.extend(carregar_jsonl(arquivo_experimento_com_analise_alucinacao.format(parte=3)))
    resultado_experimento.extend(carregar_jsonl(arquivo_experimento_com_analise_alucinacao.format(parte=4)))
    return resultado_experimento

resultado_experimento = carregar_resultado_experimento_com_analise_alucinacao()

for resultado in resultado_experimento:
    for envolvido in resultado['metadados_extraidos']['envolvidos']:
        for opiniao in envolvido['opinioes']:
            verificacao_manual = opiniao['eh_alucinacao'] if opiniao['concordancia_com_analise_alucinacao'] else not opiniao['eh_alucinacao']
            opiniao['verificacao_alucinacao'] = {
                "verificacao_manual": verificacao_manual,
                "prompt_1_gpt-4o-mini-2024-07-18": {
                    "alucinacao": opiniao['eh_alucinacao'],
                    "explicacao": opiniao['explicacao_para_eh_alucinacao']
                }
            }
            del opiniao['embeddings']
            del opiniao['distancia_chunks']
            del opiniao['eh_alucinacao']
            del opiniao['explicacao_para_eh_alucinacao']
            del opiniao['concordancia_com_analise_alucinacao']

salvar_jsonl_final(resultado_experimento)