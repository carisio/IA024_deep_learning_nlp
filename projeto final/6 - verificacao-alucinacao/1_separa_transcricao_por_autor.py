# Esse arquivo pega todas as transcrições no dataset e, em cada uma delas,
# separa as falas por autor.
# Ao fazer isso, também já quebra as falas em chunks de texto (5 frases, 
# com sobreposição de 1 frase)
# A ideia é que isso será usado em um RAG para verificar se uma
# ideia extraída do sistema de sumarização é uma alucinação ou não.

import json
import re
import spacy
import pickle

# Antes de executar esse script, para usar o spacy, é necessário instalar esse pacote:
# python -m spacy download pt_core_news_sm


# Carrega o dataset
arquivo_dataset = '..\-- arquivos finais --\o dataset\dataset.jsonl'
dataset = []
with open(arquivo_dataset, encoding='utf-8') as fin:
    for line in fin:
        dataset.append(json.loads(line))

# Dada uma transcrição, extrai as falas de cada autor
def extrair_falas_por_autor(transcricao):
    dict_falas = {}
    orador_atual = None
    
    # Expressões regulares para identificar o início de uma fala
    regex_orador = re.compile(r'^(O SR\.|A SRA\.)\s(.*?)(?:\s?\(.*?\))?\s*-\s*')
    
    parágrafos = transcricao.split('\n')
    
    for paragrafo in parágrafos:
        paragrafo = paragrafo.strip()
        if not paragrafo:
            continue
    
        match = regex_orador.match(paragrafo)
        if match:
            # Extrai o que está depois do orador_atual
            # Nesse ponto, orador_atual contém todo o texto do tipo "O SR. FULANO (XXXX)- "
            orador_atual = match.group(0)
            fala = paragrafo[len(orador_atual):].strip()
            
            # A regex pega toda a qualificação do orador atual. Agora precisamos
            # ajustar para buscar apenas o nome do orador
            if orador_atual.startswith('O SR. PRESIDENTE(') or orador_atual.startswith('A SRA. PRESIDENTE('):
                orador_atual = orador_atual[orador_atual.index('(')+1:orador_atual.rindex('.')].upper()
            elif '(' in orador_atual:
                orador_atual = orador_atual[orador_atual.index('.')+2:orador_atual.index('(')]
            elif '-' in orador_atual:
                orador_atual = orador_atual[orador_atual.index('.')+2:orador_atual.index('-')]
            # Em alguns casos, terá sobrado o qualificador Ministro/Ministra
            if orador_atual.startswith('MINISTR'):
                orador_atual = orador_atual[9:]
            # Há também outros qualificadores que poderíamos tirar aqui (por exemplo,
            # professor, coronel etc).
            # Mas vamos mantê-los e confiar que o GPT conseguirá pareá-los. Até porque
            # a ideia é que ele consiga parear um nome com o nome da pessoa
                
            # Remove eventuais espaços em branco
            orador_atual = orador_atual.strip()
                
            
            if orador_atual in dict_falas:
                dict_falas[orador_atual]['texto_completo'] += '\n' + fala
            else:
                dict_falas[orador_atual] = { 'texto_completo': fala }
        elif orador_atual:
            dict_falas[orador_atual]['texto_completo'] += '\n' + paragrafo

    return dict_falas

# Função para quebrar um texto em chunks
def gerar_chunks(texto, num_frases=5, sobreposicao=1):
    # Carrega o modelo de linguagem em português
    nlp = spacy.load('pt_core_news_sm')
    
    # Processa o texto com spaCy
    doc = nlp(texto)
    
    # Extrai as frases do texto
    frases = [sent.text for sent in doc.sents]
    
    # Gera os chunks
    chunks = []
    for i in range(0, len(frases), num_frases - sobreposicao):
        chunk = frases[i:i + num_frases]
        chunks.append(' '.join(chunk))
        if(i+num_frases >= len(frases)):
            break        

    return chunks

# Percorre todo o dataset e extrai as falas de cada autor
transcricao_por_autor_por_id = {}
for d in dataset:
    # Extrai as falas e armazena no dicionário
    transcricao_por_autor_por_id[d['id']] = extrair_falas_por_autor(d['transcricao'])
    
# Para cada autor, vamos gerar chunks de texto. A ideia é usar depois esses chunks em um RAG
total_chunks = 0
for id in transcricao_por_autor_por_id.keys():
    print(f'Gerando chunks para id {id}')
    for autor in transcricao_por_autor_por_id[id].keys():
        texto_completo_do_autor = transcricao_por_autor_por_id[id][autor]['texto_completo']
        transcricao_por_autor_por_id[id][autor]['chunks'] = gerar_chunks(texto_completo_do_autor)
        total_chunks += len(transcricao_por_autor_por_id[id][autor]['chunks'])

print(f'Total de chunks gerados: {total_chunks}')

# Salvar o dicionário em vários arquivos pickle
for id in transcricao_por_autor_por_id.keys():
    with open(f'./transcricao_por_autor/transcricao_por_autor_id_{id}.pkl', 'wb') as f:
        pickle.dump(transcricao_por_autor_por_id[id], f)
