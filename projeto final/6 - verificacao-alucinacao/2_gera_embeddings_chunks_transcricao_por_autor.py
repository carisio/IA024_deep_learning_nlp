# Esse código pega os chunks das falas e gera os embeddings correspondentes

import json
import pickle
from openai import OpenAI

OPENAI_API = '' # Não subir de jeito nenhum pro git!
client = OpenAI(api_key=OPENAI_API)

# Carrega o dataset
arquivo_dataset = '..\-- arquivos finais --\o dataset\dataset.jsonl'
dataset = []
with open(arquivo_dataset, encoding='utf-8') as fin:
    for line in fin:
        dataset.append(json.loads(line))

def gera_embeddings(chunk, model="text-embedding-3-small"):
   chunk = chunk.replace("\n", " ")
   return client.embeddings.create(input = [chunk], model=model).data[0].embedding


for d in dataset:
    # Extrai as falas e armazena no dicionário
    id = d['id']
    print(f'Gerando embeddings para ID {id}')

    # Abre o arquivo de transcrição por autor para essa id
    with open(f'./transcricao_por_autor/transcricao_por_autor_id_{id}.pkl', 'rb') as f:
        transcricao_por_autor = pickle.load(f)

    
    # Itera sobre todos os autores. Para cada autor, itera nos chunks e gera os embeddings
    # Cria uma nova propriedades embeddings, pareada com as do chunks
    for autor in transcricao_por_autor.keys():
        if 'embeddings' in transcricao_por_autor[autor]:
            print(f'\tJá foi gerado os embeddings para o autor {autor}. Pulando...')
            continue
        else:
            print(f'\tGerando embeddings para o autor {autor}')
        
        embeddings = []
        for chunk in transcricao_por_autor[autor]['chunks']:
            embeddings.append(gera_embeddings(chunk))
        transcricao_por_autor[autor]['embeddings'] = embeddings
            
        with open(f'./transcricao_por_autor/transcricao_por_autor_id_{id}.pkl', 'wb') as f:
            pickle.dump(transcricao_por_autor, f)