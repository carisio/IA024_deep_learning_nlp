# Esse arquivo percorre todas as opiniões geradas no experimento feito no
# ChatGPT e tenta verificar se houve alucinação nelas.
#
# Basicamente é feito o seguinte:
# 1. Itera o experimento
#   1.1 Para cada experimento, itera o autor
#       1.1.1 Indexa no FAISS os chunks das transcrições desse autor 
#               (gerado no 2_gera_embeddings_chunks_transcricao_por_autor.py)
#       1.1.1 Para cada autor, itera as opiniões geradas no experimento
#           1.1.1.1 Gera os embeddings da opinião
#           1.1.1.2 Pesquisa no FAISS os chunks mais próximos da opinião
#           1.1.1.3 Envia para o ChatGPT perguntando se é possível inferir 
#                   aquela opinião a partir dos chunks. Se não for possível,
#                   considera que houve alucinação
#
# Este foi o primeiro prompt testado para detectar alucinação.
# Com o resultado desse arquivo, no próximo (arquivo 5) eu faço a verificação
# manual da alucinação e, por fim, no arquivo 6 eu começo a testar outros
# prompts para ver a questão da alucinação (pois, como aí já teremos a 
# verificação manual, fica mais fácil de comparar).
import json
import pickle
import os
import faiss
import numpy as np
from openai import OpenAI

OPENAI_API = '' # Não subir de jeito nenhum pro git!
#modelo = "gpt-4o-2024-05-13"
modelo = "gpt-4o-mini-2024-07-18"
client = OpenAI(api_key=OPENAI_API)

arquivo_experimento = '../-- arquivos finais --/experimento chatgpt/results_experiment_chatgpt.jsonl'
arquivo_experimento_com_analise_alucinacao = './results_experimento_chatgpt_com_analise_alucinacao_parte_{parte}.jsonl'
arquivo_pareamento_nome_no_experimento_e_na_transcricao = './pareamento_nome_experimento_e_transcricao.json'


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

def carregar_resultado_de_experimento_e_adaptar_com_analise_alucinacao():
    resultado_experimento = carregar_jsonl(arquivo_experimento)
    for r in resultado_experimento:
        for autor in r['metadados_extraidos']['envolvidos']:
            novo_formato_opinioes = []
            for opiniao in autor['opinioes']:
                novo_formato_opinioes.append({
                    'opiniao': opiniao,
                    'embeddings': None,
                    'chunks_proximos': None,
                    'distancia_chunks': None,
                    'eh_alucinacao': None
                    })
            autor['opinioes'] = novo_formato_opinioes
    return resultado_experimento

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

###################################################################
# Pareamento do nome do autor no experimento e na transcrição
with open(arquivo_pareamento_nome_no_experimento_e_na_transcricao, 'r') as arquivo_json:
    pareamento_nome_experimento_e_transcricao = json.load(arquivo_json)

###################################################################
# Carrega os resultados dos experimentos com a análise da alucinação.
# A ideia desse arquivo é que ele seja o mesmo do resultado do
# experimento, mas injetaremos nele informações para checar a alucinação.
# Dessa forma, se o arquivo ainda não existir, abrimos o resultado
# do experimento e faremos uma conversão das informações
resultado_experimento = []
if os.path.exists(arquivo_experimento_com_analise_alucinacao.format(parte=1)):
    print('Restaurando arquivo de experimento com análise de alucinação')
    resultado_experimento = carregar_resultado_experimento_com_analise_alucinacao()
else:
    print('Criando arquivo de experimento com análise de alucinação')
    resultado_experimento = carregar_resultado_de_experimento_e_adaptar_com_analise_alucinacao()
    salvar_resultado_experimento_com_analise_alucinacao()
    

###################################################################
# Agora faz a análise:
#
# 1. Itera o experimento
#   1.1 Para cada experimento, itera o autor
#       1.1.1 Indexa no FAISS os chunks das transcrições desse autor 
#               (gerado no 2_gera_embeddings_chunks_transcricao_por_autor.py)
#       1.1.1 Para cada autor, itera as opiniões geradas no experimento
#           1.1.1.1 Gera os embeddings da opinião
#           1.1.1.2 Pesquisa no FAISS os chunks mais próximos da opinião
#           1.1.1.3 Envia para o ChatGPT perguntando se é possível inferir 
#                   aquela opinião a partir dos chunks. Se não for possível,
#                   considera que houve alucinação
# 
def get_embeddings_opiniao(opiniao, model="text-embedding-3-small"):
    if opiniao['embeddings'] is None:
        print('\tGerando embeddings')
        texto = opiniao['opiniao'].replace("\n", " ")
        emb = client.embeddings.create(input = [texto], model=model).data[0].embedding 
        opiniao['embeddings'] = emb
        salvar_resultado_experimento_com_analise_alucinacao()
    else:
        print('\tRetornando embeddings')
    return opiniao['embeddings']

def get_nome_autor_na_transcricao(id_experimento, nome_autor_no_experimento):
    lista_pares_nomes = pareamento_nome_experimento_e_transcricao[f'{id_experimento}']
    nome_na_transcricao = None

    for par in lista_pares_nomes:
        if par['nome_no_experimento'] == nome_autor_no_experimento:
            nome_na_transcricao = par['nome_na_transcricao']
            nome_na_transcricao = nome_na_transcricao.replace('\xa0', ' ')
            break
    if nome_na_transcricao is None:
        print("Não deve chegar aqui. É pra ter pareamento em todos os casos")
        
    return nome_na_transcricao

def corrige_chaves_substituindo_xa0_por_espaco(d):
    novo_dict = {}
    for chave, valor in d.items():
        nova_chave = chave.replace('\xa0', ' ')
        novo_dict[nova_chave] = valor
    return novo_dict

def get_transcricao_do_autor(id_experimento, nome_autor_no_experimento):
    # Converte o nome do autor no experimento para a transcrição
    nome_autor_transcricao = get_nome_autor_na_transcricao(id_experimento, nome_autor_no_experimento)
    # Abre as transcrições por autor desse experimento
    with open(f'./transcricao_por_autor/transcricao_por_autor_id_{id_experimento}.pkl', 'rb') as f:
        transcricao_por_autor = pickle.load(f)
    # Corrige eventual índice que tem o caractere \xa0, substituindo-o por espaço em branco
    transcricao_por_autor = corrige_chaves_substituindo_xa0_por_espaco(transcricao_por_autor)
    
    if nome_autor_transcricao in transcricao_por_autor:
        return transcricao_por_autor[nome_autor_transcricao]
    else:
        # Se não existir a transcrição para esse nome, é pq
        # estamos diante de uma alucinação. Retorna None e trata daí pra frente
        return None
  
     
def get_faiss_index_para_autor(id_experimento, nome_autor_no_experimento):
    transcricao_do_autor = get_transcricao_do_autor(id_experimento, nome_autor_no_experimento)
    if transcricao_do_autor is None:
        return None, None

    dimensao_embeddings = len(transcricao_do_autor['embeddings'][0]) # Tamanho dos embeddings no modelo usado
    
    # Extrai todos os embeddings
    embeddings_para_indexar = []
    for emb in transcricao_do_autor['embeddings']:
        embeddings_para_indexar.append(emb)
    embeddings_para_indexar = np.array(embeddings_para_indexar)
    
    # Cria o índice com os dados
    index = faiss.IndexFlatL2(dimensao_embeddings)
    index.add(embeddings_para_indexar)
    
    return transcricao_do_autor, index

def get_chunks_proximos(opiniao, transcricao_do_autor, indice_do_autor, k=2):
    # É necessário tratar o caso do índice não existir
    if indice_do_autor is None:
        chunks = []
        D = np.array([[]])
    else:
        D, I = indice_do_autor.search(np.array([opiniao['embeddings']]), k)
        chunks = [transcricao_do_autor['chunks'][i] for i in I[0]]
    return chunks, D[0].tolist()

# Método que chama o GPT-4o e tenta fazer o pareamento
msg_sistema_gpt = """
Você é um assistente que analisa se uma opinião pode ser completamente inferida a partir de um texto.

O retorno da sua análise deverá ser sempre no formato JSON e conterá duas propriedades:
    - "explicacao": Uma string com o seu raciocínio explicando o porque a opinião pode ou não ser inferida pelo texto;
    - "opiniao_inferida": Um boolean (true ou false) sintetizando sua explicação: true, se a opinião puder ser inferida a partir do texto, ou false, se não puder.

Não forneça nada além do JSON com as propriedades acima.
""".strip()
msg_user = """
###### TEXTO:
{texto}

###### OPINIÃO PARA ANALISAR:
{opiniao}
""".strip()
def verifica_alucinacao_usando_gpt(opiniao):
    print('\tChamando GPT...')
    response = client.chat.completions.create(
        model=modelo,
        messages=[
            {
              "role": "system",
              "content": msg_sistema_gpt
            },
            {
              "role": "user",
              "content": msg_user.format(texto="\n\n".join(opiniao['chunks_proximos']), opiniao=opiniao['opiniao'])
            },
        ],
        response_format={ "type": "json_object" },
        temperature=0.02,
        max_tokens=4095,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
    retorno_str_json = response.choices[0].message.content
    retorno_json = json.loads(retorno_str_json)
    eh_alucinacao = not retorno_json['opiniao_inferida']
    explicacao = retorno_json['explicacao']
    return eh_alucinacao, explicacao

def verifica_alucinacao(opiniao):
    # Se a lista de chunks próximos for de tamanho 0, já considera que há alucinação, 
    # pois significa que não tinha nada na transcrição
    if len(opiniao['chunks_proximos']) == 0:
        print('************ Alucinou')
        eh_alucinacao = True
        explicacao = 'Não há chunks próximos'
    else:
        eh_alucinacao, explicacao = verifica_alucinacao_usando_gpt(opiniao)
    return eh_alucinacao, explicacao

# Faz a análise de alucinação
for r in resultado_experimento:
    print(f'### Análise para id {r["id"]} ###')
    for autor in r['metadados_extraidos']['envolvidos']:
        print(f'\tAnálise para o autor: {autor["nome"]}')
        
        # Indexa no FAISS a transcricao do autor
        transcricao_do_autor, indice_do_autor = get_faiss_index_para_autor(r['id'], autor['nome'])
        
        # Itera as opiniões e guarda os chunks mais próximos
        for opiniao in autor['opinioes']:
            embeddings_opiniao = get_embeddings_opiniao(opiniao)
            
            # Pega as opiniões mais próximas
            if opiniao['chunks_proximos'] is None:
                print('\tExtraindo chunks próximos')
                chunks_proximos, distancia = get_chunks_proximos(opiniao, transcricao_do_autor, indice_do_autor, k=2)
                opiniao['chunks_proximos'] = chunks_proximos
                opiniao['distancia_chunks'] = distancia
            
            # Verifica se é alucinação
            if opiniao['eh_alucinacao'] is None:
                print('\tVerificando alucinação')
                eh_alucinacao, explicacao = verifica_alucinacao(opiniao)
                opiniao['eh_alucinacao'] = eh_alucinacao
                opiniao['explicacao_para_eh_alucinacao'] = explicacao
               
            # Trecho para forçar o recálculo de tudo. Já considera RAG com k=4 docs
            recalcular_tudo = False
            if 'explicacao_para_eh_alucinacao' not in opiniao.keys():
                print('\tVerificando se houve alucinação')
                chunks_proximos, distancia = get_chunks_proximos(opiniao, transcricao_do_autor, indice_do_autor, k=4)
                opiniao['chunks_proximos'] = chunks_proximos
                opiniao['distancia_chunks'] = distancia
                eh_alucinacao, explicacao = verifica_alucinacao(opiniao)
                opiniao['eh_alucinacao'] = eh_alucinacao
                opiniao['explicacao_para_eh_alucinacao'] = explicacao
            else:
                print('Já tem a explicação')
                
# Calcula a porcentagem de alucinação em cada experimento
total_opinioes = []
total_alucinacoes = []
porcentagem_alucinacoes = []
for r in resultado_experimento:
    total_opinioes_no_experimento = 0
    total_alucinacoes_no_experimento = 0
    for autor in r['metadados_extraidos']['envolvidos']:
        total_opinioes_no_experimento += len(autor['opinioes'])
        for opiniao in autor['opinioes']:
            total_alucinacoes_no_experimento += (1. if opiniao['eh_alucinacao'] else 0.)
    total_opinioes.append(total_opinioes_no_experimento)
    total_alucinacoes.append(total_alucinacoes_no_experimento)
    porcentagem_alucinacoes.append(total_alucinacoes_no_experimento/total_opinioes_no_experimento)
    
print("Média:\t", np.mean(porcentagem_alucinacoes))
print("Q5:\t\t", np.percentile(porcentagem_alucinacoes, 5))
print("Q25:\t", np.percentile(porcentagem_alucinacoes, 25))
print("Q50:\t", np.percentile(porcentagem_alucinacoes, 50))
print("Q75:\t", np.percentile(porcentagem_alucinacoes, 75))
print("Q95:\t", np.percentile(porcentagem_alucinacoes, 95))

salvar_resultado_experimento_com_analise_alucinacao()