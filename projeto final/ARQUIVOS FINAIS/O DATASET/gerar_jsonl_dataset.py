import os
import json

# Diretórios
materias_dir = './materias'
metadados_dir = './metadados'
transcricoes_dir = './transcricoes'
output_file = 'dataset.jsonl'

# Abre o arquivo de saída
with open(output_file, 'w', encoding='utf-8') as outfile:
    # Itera sobre o intervalo de IDs
    for i in range(1, 207):
        print(i)
        # Define os nomes dos arquivos
        materia_file = os.path.join(materias_dir, f'materia_{i}.txt')
        metadados_file = os.path.join(metadados_dir, f'metadados_{i}.json')
        transcricao_file = os.path.join(transcricoes_dir, f'transcricao_{i}.txt')

        # Lê o conteúdo dos arquivos
        with open(materia_file, 'r', encoding='utf-8') as mf:
            materia_content = mf.read()
        
        with open(metadados_file, 'r', encoding='utf-8') as metf:
            metadados_content = json.load(metf)
        
        with open(transcricao_file, 'r', encoding='utf-8') as tf:
            transcricao_content = tf.read()

        # Cria o dicionário para o JSONL
        entry = {
            'id': i,
            'materia': materia_content,
            'metadados': metadados_content,
            'transcricao': transcricao_content
        }

        # Escreve a entrada no arquivo JSONL
        outfile.write(json.dumps(entry, ensure_ascii=False) + '\n')

print("Arquivo JSONL gerado com sucesso!")