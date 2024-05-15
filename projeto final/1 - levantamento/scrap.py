import pandas as pd
import requests
import os
import time

def download_arquivo(link, pasta_destino, nome_arquivo, max_tentativas=10):    
    if link == '':
        print('O link está vazio. Desconsidera.')
        return
    
    # Verifique se a pasta de destino existe, se não, crie-a
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    caminho_arquivo_para_salvar = os.path.join(pasta_destino, nome_arquivo)
    
    # Se o arquivo já existe, sai
    if os.path.exists(caminho_arquivo_para_salvar):
        print(f'{nome_arquivo} já existe')
        return
        
    tentativas = 0
    while tentativas < max_tentativas:
        try:
            response = requests.get(link)
            if response.status_code == 200:
                with open(caminho_arquivo_para_salvar, 'wb') as f:
                    f.write(response.content)
                print(f"{nome_arquivo} salvo")
                break # Se salvou, sai do loop de tentativas
            elif response.status_code == 504:
                print(f"Erro 504: Tentando novamente em 2 segundos...")
                time.sleep(2)  # Aguarda 2 segundos antes de tentar novamente
                tentativas += 1
            else:
                print(f"[ERRO {response.status_code}] Não foi possível salvar'{nome_arquivo}'")
                break  # Sai do loop se o status code não for 200 nem 503
        except Exception as e:
            print(f"Erro ao acessar '{link}': {e}")
    
    time.sleep(1)

df_links = pd.read_csv('materias.csv', sep=";")
df_links.ATA = df_links.ATA.fillna("")

for i, row in df_links .iterrows():
    id = row['ID']
    link_materia = row['MATERIA']
    link_transcricao = row['TRANSCRICAO']
    link_ata = row['ATA']

    print(f'*************** Fazendo os downloads para id {id} ***************')
    download_arquivo(link_ata, './atas/', f'ata_{id}.html')
    #download_arquivo(link_materia, './materias/', f'materia_{id}.html')
    #download_arquivo(link_transcricao, './transcricoes/', f'transcricao_{id}.html')
    print('\n')