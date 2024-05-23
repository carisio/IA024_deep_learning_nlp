from bs4 import BeautifulSoup
import re
import os

def extrair_materia(html_content):
    # Pra quebrar no final da matéria as informações da reportagem e edição
    html_content = html_content.replace('<br>', '\n')
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extrair o título
    titulo = soup.find('h1', class_='g-artigo__titulo').get_text(strip=True)
    
    # Extrair o sutiã (descrição)
    sutia = soup.find('p', class_='g-artigo__descricao')
    sutia = sutia.get_text(strip=True) if sutia is not None else ""
    
    # Extrair o texto da matéria
    texto_div = soup.find('div', class_='js-article-read-more')
    paragrafos = texto_div.find_all('p')
    
    # Filtrar para pegar apenas o último nível de <p> tags
    texto = '\n\n'.join(p.get_text(strip=False) for p in paragrafos if not p.find_all('p'))
    
    # Substitui os múltiplos espaços em branco por vazio. E depois quebras de linha
    texto = re.sub(r' {2,}', '', texto)
    texto = re.sub(r'\n{4,}', '', texto)
    
    return titulo, sutia, texto

os.makedirs('./materias', exist_ok=True)

materias_para_resolver_manualmente = []
for i in range(1, 212):
    print(f'*************** Tratando a matéria {i} ***************')
    
    with open(f'../1 - levantamento/materias/materia_{i}.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    try:
        titulo, sutia, texto = extrair_materia(html_content)
        texto_completo = f"{titulo}\n{sutia}\n\n{texto}"
    
        caminho_arquivo = os.path.join('./materias', f'materia_{i}.txt')
    
        with open(caminho_arquivo, 'w', encoding='utf-8') as file:
            file.write(texto_completo)
    except:
        print(f'[ERRO] na matéria {i}')
        materias_para_resolver_manualmente.append(i)
        
print('Matérias para resolver manualmente:')
print(materias_para_resolver_manualmente)