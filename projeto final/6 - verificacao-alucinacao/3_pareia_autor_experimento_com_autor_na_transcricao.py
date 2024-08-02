# Esse arquivo tenta descobrir a relação (pareamento) do nome de um autor
# no experimento com o nome gerado na transcrição.
# O que o ocorre é que o nome pode estar ligeiramente diferente, então
# é necessário tentar encontrar o nome correto.
# Por exemplo, na transcrição pode estar escrito Professor João Pereira Silva e,
# no experimento, esse nome pode estar como João P. Silva ou Joao Pereira Silva ou
# JOÃO PEREIRA SILVA.
# A ideia é usar um LLM para encontrar as associações corretas

import json
import pickle
import os
from openai import OpenAI

OPENAI_API = '' # Não subir de jeito nenhum pro git!
client = OpenAI(api_key=OPENAI_API)
modelo = "gpt-4o-2024-05-13"

# Carrega o resultado do experimento
arquivo_resultado_experimento = '../-- arquivos finais --/experimento chatgpt/results_experiment_chatgpt.jsonl'
resultado_experimento = []
with open(arquivo_resultado_experimento , encoding='utf-8') as fin:
    for line in fin:
        resultado_experimento.append(json.loads(line))

# Método para carregar a lista de autores extraídas da transcrição
def carrega_autores_na_transcricao(id):
    with open(f'./transcricao_por_autor/transcricao_por_autor_id_{id}.pkl', 'rb') as f:
        transcricao_por_autor = pickle.load(f)
        autores_na_transcricao = list(transcricao_por_autor.keys())
    return autores_na_transcricao

# Método que chama o GPT-4o e tenta fazer o pareamento
msg_sistema_gpt = """
Você é um assistente que tenta encontrar um nome em uma lista de nomes.
O nome que você tentará encontrar com certeza está na lista de nomes fornecidos.
Entretanto, nem sempre o nome estará escrito de forma idêntica.
Pode ser que na lista um sobrenome esteja omitido ou abreviado. 
Pode ocorrer qualificações (por exemplo, professor etc) junto ao nome.
Pode também ter diferenças de acentuações.
O seu papel é identificar na lista o nome fornecido.

O retorno deverá ser sempre no formato JSON com apenas uma propriedade, "nome_na_lista".
Essa propriedade deve ser o nome copiado exatamente igual na lista fornecida e deve ser
o mais próximo possível semânticamente do nome a ser encontrado.
Não forneça nada além disso.
""".strip()
msg_user = """
NOME A SER ENCONTRADO: {nome_no_experimento}

LISTA DE NOMES PARA PESQUISAR:
{str_lista_nomes}
""".strip()
def get_autor_mais_provavel(nome_no_experimento, nomes_autores_na_transcricao):
    # Apenas chama o GPT se o nome no experimento em maiúsculo
    # não existir na lista de nomes na transcrição
    if nome_no_experimento.upper() in nomes_autores_na_transcricao:
        return nome_no_experimento.upper()
    
    print('Chamando GPT...')
    response = client.chat.completions.create(
        model=modelo,
        messages=[
            {
              "role": "system",
              "content": msg_sistema_gpt
            },
            {
              "role": "user",
              "content": msg_user.format(nome_no_experimento=nome_no_experimento, str_lista_nomes="\n".join(nomes_autores_na_transcricao))
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
    return(retorno_json['nome_na_lista'])

# Mantém o pareamento entre o nome do autor no experimento e na transcrição
if os.path.exists('./pareamento_nome_experimento_e_transcricao.json'):
    with open('./pareamento_nome_experimento_e_transcricao.json', 'r') as arquivo_json:
        pareamento_nome_experimento_e_transcricao = json.load(arquivo_json)
else:
    pareamento_nome_experimento_e_transcricao = {}

# Varre todos os experimentos e encontra o pareamento
for r in resultado_experimento:
    # Carrega informações de cada experimento
    id = r['id']
    metadados_extraidos = r['metadados_extraidos']
    envolvidos = metadados_extraidos['envolvidos']

    # Se já foi feito o tratamento, simplesmente ignora
    if f'{id}' in pareamento_nome_experimento_e_transcricao.keys():
        print(f'Já existe o pareamento para o id {id}')
        continue
    print(f'Pareando id {id}')
    
    # Carrega os nomes possíveis na transcrição
    nomes_autores_na_transcricao = carrega_autores_na_transcricao(id)

    # Faz os pareamentos    
    pareamentos = []
    for e in envolvidos:
        nome_no_experimento = e['nome']
        nome_na_transcricao = get_autor_mais_provavel(nome_no_experimento, nomes_autores_na_transcricao)
        pareamentos.append({'nome_no_experimento': nome_no_experimento, 'nome_na_transcricao': nome_na_transcricao})

    pareamento_nome_experimento_e_transcricao[id] = pareamentos
    

    # Atualiza o arquivo com os resultados do pareamento para essa id
    with open('./pareamento_nome_experimento_e_transcricao.json', 'w') as arquivo_json:
        json.dump(pareamento_nome_experimento_e_transcricao, arquivo_json, ensure_ascii=False, indent=4)