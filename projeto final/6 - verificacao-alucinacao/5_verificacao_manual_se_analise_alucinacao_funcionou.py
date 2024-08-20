# A ideia desse arquivo é facilitar a verificação manual da análise de alucinação
# Basicamente, ele vai iterando tudo e perguntando se a análise feita está correta ou não
import json
import os

arquivo_experimento_com_analise_alucinacao = './results_experimento_chatgpt_com_analise_alucinacao_parte_{parte}.jsonl'

resultado_experimento = []

###################################################################
# Funções auxiliares para carregar e salvar um jsonl
def carregar_jsonl(nome_arquivo):
    dados_jsonl = []
    with open(nome_arquivo , encoding='utf-8') as fin:
        for line in fin:
            dados_jsonl.append(json.loads(line))
    return dados_jsonl

def salvar_jsonl(nome_arquivo, lista):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        for item in lista:
            linha = json.dumps(item, ensure_ascii=False)
            arquivo.write(linha + '\n')

def carregar_resultado_experimento_com_analise_alucinacao():
    resultado_experimento = carregar_jsonl(arquivo_experimento_com_analise_alucinacao.format(parte=1))
    resultado_experimento.extend(carregar_jsonl(arquivo_experimento_com_analise_alucinacao.format(parte=2)))
    resultado_experimento.extend(carregar_jsonl(arquivo_experimento_com_analise_alucinacao.format(parte=3)))
    resultado_experimento.extend(carregar_jsonl(arquivo_experimento_com_analise_alucinacao.format(parte=4)))
    return resultado_experimento

def salvar_resultado_experimento_com_analise_alucinacao():
    salvar_jsonl(arquivo_experimento_com_analise_alucinacao.format(parte=1), resultado_experimento[0:50])
    salvar_jsonl(arquivo_experimento_com_analise_alucinacao.format(parte=2), resultado_experimento[50:100])
    salvar_jsonl(arquivo_experimento_com_analise_alucinacao.format(parte=3), resultado_experimento[100:150])
    salvar_jsonl(arquivo_experimento_com_analise_alucinacao.format(parte=4), resultado_experimento[150:])
    print('* Arquivo jsonl com o resultado atualizado *')
    
def avalia_manualmente_opiniao(opniao, pre_texto_informativo):
    try:
        from IPython import get_ipython
        get_ipython().magic('clear')
    except:
        pass

    print(f"\t\t{pre_texto_informativo}")
    texto_opiniao = opiniao['opiniao']
    chunks_proximos = opiniao['chunks_proximos']
    analise_alucinacao = ">>>>>>>> SIM <<<<<<<<" if opiniao['eh_alucinacao'] else "não"
    explicacao_para_eh_alucinacao = opiniao['explicacao_para_eh_alucinacao']

    print(f'\t\tTexto para avaliar: {texto_opiniao}\n')
    print('Chunks extraídos:')
    for i, chunk in enumerate(chunks_proximos):
        print(f'\t\t{i}. {chunk}\n')
    print(f'\t\tÉ alucinação? {analise_alucinacao}\n')
    print(f'\t\tExplicação: {explicacao_para_eh_alucinacao}\n')
    
    print(f'\t\tÉ alucinação? {analise_alucinacao}')
    concordancia_manual = input('Concorda com a análise? (S/N)').upper()
    # Apenas preenche o campo se for S ou N
    if concordancia_manual == 'S':
        opiniao['concordancia_com_analise_alucinacao'] = True
    elif concordancia_manual == 'N':
        opiniao['concordancia_com_analise_alucinacao'] = False

    
# Carrega resultado do experimento
resultado_experimento = carregar_resultado_experimento_com_analise_alucinacao()
for resultado in resultado_experimento:
    id_resultado = resultado['id']
    print(f'########## TRATANDO ID {id_resultado} ##########')
    
    num_envolvido = 0
    for envolvido in resultado['metadados_extraidos']['envolvidos']:
        num_envolvido += 1
        nome = envolvido['nome']
        print(f'\t{nome}')
        
        houve_analise_opinioes = False
        num_opiniao_envolvido = 0
        for opiniao in envolvido['opinioes']:
            num_opiniao_envolvido += 1
            if 'concordancia_com_analise_alucinacao' not in opiniao.keys():
                pre_texto_informativo = f"Opinião {num_opiniao_envolvido}/{len(envolvido['opinioes'])} de {nome} {num_envolvido}/{len(resultado['metadados_extraidos']['envolvidos'])}, id #{id_resultado}"
                avalia_manualmente_opiniao(opiniao, pre_texto_informativo)
                houve_analise_opinioes = True

        if houve_analise_opinioes:
            print('Atualizando arquivo com as análises...')
            salvar_resultado_experimento_com_analise_alucinacao()