import os
import json

# Diretórios
resultado_dir = './resultados'
output_file = 'results_experiment_chatgpt.jsonl'

# Abre o arquivo de saída
with open(output_file, 'w', encoding='utf-8') as outfile:
    # Itera sobre o intervalo de IDs
    for i in range(1, 207):
        print(i)
        # Define os nomes dos arquivos
        resultado_file = os.path.join(resultado_dir, f'resultado_{i}.txt')

        # Lê o conteúdo dos arquivos
        with open(resultado_file, 'r', encoding='utf-8') as mf:
            metadados_content = json.load(mf)

        # Cria o dicionário para o JSONL
        entry = {
            'id': i,
            'metadados_extraidos': metadados_content
        }

        # Escreve a entrada no arquivo JSONL
        outfile.write(json.dumps(entry, ensure_ascii=False) + '\n')

print("Arquivo JSONL gerado com sucesso!")