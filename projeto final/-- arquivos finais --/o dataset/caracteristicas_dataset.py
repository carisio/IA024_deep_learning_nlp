import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
        'num_opinions': num_opinions,
        'percentage_words_article_transcription': art_words/trans_words
    })

# Imprimindo algumas estatísticas
pd_stats = pd.DataFrame(dataset_stats)
pd.set_option('display.max_columns', None)
print(pd_stats.describe())

# Extraindo os dados para os gráficos
transcription_words = pd_stats['transcription_words'].tolist()
article_words = pd_stats['article_words'].tolist()
num_people = pd_stats['num_people'].tolist()
num_opinions = pd_stats['num_opinions'].tolist()
percentage_words_article_transcription = pd_stats['percentage_words_article_transcription'].tolist()

# Calcula os quartis
transcription_q1 = np.percentile(transcription_words, 25)
transcription_median = np.median(transcription_words)
transcription_q3 = np.percentile(transcription_words, 75)
article_q1 = np.percentile(article_words, 25)
article_median = np.median(article_words)
article_q3 = np.percentile(article_words, 75)
percentage_words_article_transcription_q1 = np.percentile(percentage_words_article_transcription, 25)
percentage_words_article_transcription_median = np.median(percentage_words_article_transcription)
percentage_words_article_transcription_q3 = np.percentile(percentage_words_article_transcription, 75)
num_people_q1 = np.percentile(num_people, 25)
num_people_median = np.median(num_people)
num_people_q3 = np.percentile(num_people, 75)
num_opnions_q1 = np.percentile(num_opinions, 25)
num_opnions_median = np.median(num_opinions)
num_opnions_q3 = np.percentile(num_opinions, 75)

# Gráfico de Barras para Contagem de Palavras nas Transcrições
plt.figure(figsize=(10, 6))
plt.bar(ids, transcription_words, label='Transcription Words')
plt.axhline(y=transcription_q1, color='r', linestyle='--', label='Q1 (25th percentile)')
plt.axhline(y=transcription_median, color='g', linestyle='-', label='Median (50th percentile)')
plt.axhline(y=transcription_q3, color='b', linestyle='--', label='Q3 (75th percentile)')
plt.xlabel('ID')
plt.xlim(1, 206)
plt.ylabel('Word Count')
plt.title('Word Count in Transcriptions')
plt.legend()
plt.show()

# Gráfico de Barras para Contagem de Palavras nas Matérias
plt.figure(figsize=(10, 6))
plt.bar(ids, article_words, label='Article Words')
plt.axhline(y=article_q1, color='r', linestyle='--', label='Q1 (25th percentile)')
plt.axhline(y=article_median, color='g', linestyle='-', label='Median (50th percentile)')
plt.axhline(y=article_q3, color='b', linestyle='--', label='Q3 (75th percentile)')
plt.xlabel('ID')
plt.xlim(1, 206)
plt.title('Word Count in Articles')
plt.legend()
plt.show()

# Gráfico de Barras da relação entre a contagem de palavras nas matérias e a contagem de palavras nas transcrições
plt.figure(figsize=(10, 6))
plt.bar(ids, percentage_words_article_transcription)
plt.axhline(y=percentage_words_article_transcription_q1, color='r', linestyle='--', label='Q1 (25th percentile)')
plt.axhline(y=percentage_words_article_transcription_median, color='g', linestyle='-', label='Median (50th percentile)')
plt.axhline(y=percentage_words_article_transcription_q3, color='b', linestyle='--', label='Q3 (75th percentile)')
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

