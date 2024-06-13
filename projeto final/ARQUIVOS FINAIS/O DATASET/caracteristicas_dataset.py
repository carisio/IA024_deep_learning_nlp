import json
import matplotlib.pyplot as plt

# Função para contar palavras e caracteres
def count_words_and_chars(text):
    words = text.split()
    num_words = len(words)
    num_chars = len(text)
    return num_words, num_chars


dataset = []
with open('dataset.jsonl', encoding='utf-8') as fin:
    for line in fin:
        dataset.append(json.loads(line))

dataset_stats = []
for data in dataset:
    # Quantidade de palavras e caracteres da transcrição
    transcription = data['transcricao']
    trans_words, trans_chars = count_words_and_chars(transcription)
    
    # Quantidade de palavras e caracteres da matéria
    article = data['materia']
    art_words, art_chars = count_words_and_chars(article)

    # Total de pessoas nos metadados
    metadados = data['metadados']
    envolvidos = metadados.get('envolvidos', [])
    num_people = len(envolvidos)
    
    # Total de opiniões nos metadados
    num_opinions = sum(len(person['opinioes']) for person in envolvidos)
    
    # Adiciona os resultados à lista
    dataset_stats.append({
        'id': data['id'],
        'transcription_words': trans_words,
        'transcription_chars': trans_chars,
        'article_words': art_words,
        'article_chars': art_chars,
        'num_people': num_people,
        'num_opinions': num_opinions
    })

# Extraindo os dados para os gráficos
ids = [entry['id'] for entry in dataset_stats]
transcription_words = [entry['transcription_words'] for entry in dataset_stats]
transcription_chars = [entry['transcription_chars'] for entry in dataset_stats]
article_words = [entry['article_words'] for entry in dataset_stats]
article_chars = [entry['article_chars'] for entry in dataset_stats]
num_people = [entry['num_people'] for entry in dataset_stats]
num_opinions = [entry['num_opinions'] for entry in dataset_stats]
percentage_words_article_transcription = [article_words[i]/transcription_words[i] for i in range(len(article_words))]

# Gráfico de Barras para Contagem de Palavras nas Transcrições
plt.figure(figsize=(10, 6))
plt.bar(ids, transcription_words, label='Transcription Words')
plt.xlabel('ID')
plt.xlim(1, 206)
plt.ylabel('Word Count')
plt.title('Word Count in Transcriptions')
plt.show()

# Gráfico de Barras para Contagem de Palavras nas Matérias
plt.figure(figsize=(10, 6))
plt.bar(ids, article_words, label='Article Words')
plt.xlabel('ID')
plt.xlim(1, 206)
plt.title('Word Count in Articles')
plt.legend()
plt.show()

# Gráfico de Barras da relação entre a contagem de palavras nas matérias e a contagem de palavras nas transcrições
plt.figure(figsize=(10, 6))
plt.bar(ids, percentage_words_article_transcription)
plt.xlabel('ID')
plt.xlim(1, 206)
plt.title('Relative size of article in relation to the transcription (in words)')
plt.legend()
plt.show()

# Gráfico de Barras para Contagem de Pessoas e Opiniões
plt.figure(figsize=(10, 6))
plt.bar(ids, num_opinions, label='Number of Opinions', alpha=0.7)
plt.bar(ids, num_people, label='Number of People')
plt.xlabel('ID')
plt.ylabel('Count')
plt.xticks(range(1, 207, 10))
plt.title('Number of People and Opinions in Metadata')
plt.xlim(1, 206)
plt.legend()
plt.show()