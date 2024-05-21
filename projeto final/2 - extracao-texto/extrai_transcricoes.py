from bs4 import BeautifulSoup
import re
import os

def extrair_transcricao(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Encontra todas as tags <td> com a classe "justificado"
    tds_justificado = soup.find_all('td', class_='justificado')
    
    # Para cada <td> com a classe "justificado", encontra os divs com a classe "principalStyle"
    texto = []
    for td in tds_justificado:
        divs_principalStyle = td.find_all('div', class_='principalStyle')
        for div in divs_principalStyle:
            texto.append(div.get_text(strip=True))
    
    # Junta os textos com quebras de linha duplas para separá-los em parágrafos
    texto_final = '\n\n'.join(texto)
    
    return texto_final

os.makedirs('./transcricoes', exist_ok=True)

transcricoes_para_resolver_manualmente = []
for i in range(1, 212):
    print(f'*************** Tratando a transcrição {i} ***************')
    
    with open(f'../1 - levantamento/transcricoes/transcricao_{i}.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    try:
        texto = extrair_transcricao(html_content)
    
        caminho_arquivo = os.path.join('./transcricoes', f'transcricao_{i}.txt')
    
        with open(caminho_arquivo, 'w', encoding='utf-8') as file:
            file.write(texto)
    except:
        print(f'[ERRO] na transcrição {i}')
        transcricoes_para_resolver_manualmente.append(i)

print('Transcrições para resolver manualmente:')
print(transcricoes_para_resolver_manualmente)
