from bs4 import BeautifulSoup
import re
import os

def extrair_atas(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Encontra todos os parágrafos e outros elementos de texto relevantes
    paragrafos = soup.find_all('p')
    
    # Extrai o texto e junta todos os parágrafos
    texto = '\n\n'.join(p.get_text(strip=True) for p in paragrafos)
    
    return texto

os.makedirs('./atas', exist_ok=True)

atas_para_resolver_manualmente = []
for i in range(1, 212):
    print(f'*************** Tratando a ata {i} ***************')
    arquivo_html = f'../1 - levantamento/atas/ata_{i}.html'
    
    if not os.path.exists(arquivo_html):
        continue

    with open(arquivo_html, 'r') as file:
        html_content = file.read()
    
    try:
        texto = extrair_atas(html_content)
    
        caminho_arquivo = os.path.join('./atas', f'ata_{i}.txt')
    
        with open(caminho_arquivo, 'w', encoding='utf-8') as file:
            file.write(texto)
    except:
        print(f'[ERRO] na matéria {i}')
        atas_para_resolver_manualmente.append(i)
        
print('Atas para resolver manualmente:')
print(atas_para_resolver_manualmente)