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
    transcript = data['transcricao']
    trans_words, trans_chars = count_words_and_chars(transcript)
    
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
        'transcript_words': trans_words,
        'transcript_chars': trans_chars,
        'article_words': art_words,
        'article_chars': art_chars,
        'num_people': num_people,
        'num_opinions': num_opinions,
        'percentage_words_article_transcript': art_words/trans_words
    })

# Cria um dataframe com as estatísticas do dataset
pd_stats = pd.DataFrame(dataset_stats)
pd.set_option('display.max_columns', None)
estatisticas = pd_stats.describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95])
print(estatisticas)


# Plota gráficos individuais para quantidades de palavras na transcrição
# e na matéria
# Extraindo os dados para os gráficos
ids = pd_stats['id'].tolist()
transcript_words = pd_stats['transcript_words'].tolist()
article_words = pd_stats['article_words'].tolist()
num_people = pd_stats['num_people'].tolist()
num_opinions = pd_stats['num_opinions'].tolist()
percentage_words_article_transcript = pd_stats['percentage_words_article_transcript'].tolist()

# Gráfico de Barras para Contagem de Palavras nas Transcrições
plt.figure(figsize=(10, 6))
plt.bar(ids, transcript_words, label='Transcript words')
plt.axhline(y=estatisticas.loc['25%', 'transcript_words'], color='r', linestyle='--', label='Q1 (25th percentile)')
plt.axhline(y=estatisticas.loc['50%', 'transcript_words'], color='g', linestyle='-', label='Median (50th percentile)')
plt.axhline(y=estatisticas.loc['75%', 'transcript_words'], color='b', linestyle='--', label='Q3 (75th percentile)')
plt.xlabel('ID')
plt.xlim(1, 206)
plt.ylabel('Word Count')
plt.legend()
plt.show()

# Gráfico de Barras para Contagem de Palavras nas Matérias
plt.figure(figsize=(10, 6))
plt.bar(ids, article_words, label='Article words')
plt.axhline(y=estatisticas.loc['25%', 'article_words'], color='r', linestyle='--', label='Q1 (25th percentile)')
plt.axhline(y=estatisticas.loc['50%', 'article_words'], color='g', linestyle='-', label='Median (50th percentile)')
plt.axhline(y=estatisticas.loc['75%', 'article_words'], color='b', linestyle='--', label='Q3 (75th percentile)')
plt.xlabel('ID')
plt.xlim(1, 206)
plt.ylabel('Word Count')
plt.legend()
plt.show()

# Gráfico de Barras da relação entre a contagem de palavras nas matérias e a contagem de palavras nas transcrições
plt.figure(figsize=(10, 6))
plt.bar(ids, percentage_words_article_transcript)
plt.axhline(y=estatisticas.loc['25%', 'percentage_words_article_transcript'], color='r', linestyle='--', label='Q1 (25th percentile)')
plt.axhline(y=estatisticas.loc['25%', 'percentage_words_article_transcript'], color='g', linestyle='-', label='Median (50th percentile)')
plt.axhline(y=estatisticas.loc['25%', 'percentage_words_article_transcript'], color='b', linestyle='--', label='Q3 (75th percentile)')
plt.xlabel('ID')
plt.xlim(1, 206)
plt.ylabel('Relative size')
plt.legend()
plt.show()

# Gráfico de Barras para Contagem de Pessoas e Opiniões
plt.figure(figsize=(10, 6))
plt.bar(ids, num_opinions, label='Number of opinions', alpha=0.7)
plt.bar(ids, num_people, label='Number of individuals')
plt.xlabel('ID')
plt.ylabel('Count')
plt.xticks(range(1, 207, 10))
plt.xlim(1, 206)
plt.legend()
plt.show()

# Plota CDFs
# Gerar dados de exemplo
data1 = np.array(transcript_words)
data2 = np.array(article_words)

# Calcular as CDFs
data1_sorted = np.sort(data1)
cdf1 = np.arange(1, len(data1_sorted) + 1) / len(data1_sorted)

data2_sorted = np.sort(data2)
cdf2 = np.arange(1, len(data2_sorted) + 1) / len(data2_sorted)

# Determinar o máximo dos dados
max_data1 = 50000
max_data2 = 1200

# Definir as cores tradicionais do matplotlib
color1 = plt.get_cmap('tab10')(0)  # Azul padrão
color2 = plt.get_cmap('tab10')(1)  # Laranja padrão

# Plotar a primeira CDF
fig, ax1 = plt.subplots()

line1, = ax1.plot(data1_sorted, cdf1, label='Transcript', color=color1)
ax1.set_xlabel('Transcript words', color=color1)
ax1.set_ylabel('CDF', color='black')
ax1.tick_params(axis='x', labelcolor=color1)
ax1.tick_params(axis='y', labelcolor='black')
ax1.grid(True, which='both', linestyle='--', linewidth=0.5, color='lightgrey')
ax1.set_ylim(0, 1)
ax1.set_xlim(0, max_data1)

# Adicionar linhas de grade no eixo Y de 0 a 1 com passos de 0.1
ax1.set_yticks(np.arange(0, 1.1, 0.1))

# Criar um segundo eixo X
ax2 = ax1.twiny()

# Plotar a segunda CDF
line2, = ax2.plot(data2_sorted, cdf2, label='Article', color=color2)
ax2.set_xlabel('Article words', color=color2)
ax2.tick_params(axis='x', labelcolor=color2)
ax2.grid(True, which='both', linestyle='--', linewidth=0.5, color='lightgrey')
ax2.set_xlim(0, max_data2)

# Sincronizar a quantidade de ticks dos eixos X
num_ticks = 7
ax1_ticks = np.linspace(ax1.get_xlim()[0], ax1.get_xlim()[1], num_ticks)
ax2_ticks = np.linspace(ax2.get_xlim()[0], ax2.get_xlim()[1], num_ticks)

ax1.set_xticks(ax1_ticks)
ax2.set_xticks(ax2_ticks)

# Dobrar o número de linhas de grade no eixo X
ax1_minor_ticks = np.linspace(ax1.get_xlim()[0], ax1.get_xlim()[1], num_ticks * 2 - 1)
ax2_minor_ticks = np.linspace(ax2.get_xlim()[0], ax2.get_xlim()[1], num_ticks * 2 - 1)

ax1.set_xticks(ax1_minor_ticks, minor=True)
ax2.set_xticks(ax2_minor_ticks, minor=True)

fig.tight_layout()

# Adicionar legendas
lines = [line1, line2]
labels = [line.get_label() for line in lines]
plt.legend(lines, labels, loc='lower right')
#plt.savefig('fig_cdf_transcript_article.png', dpi=400)
plt.show()