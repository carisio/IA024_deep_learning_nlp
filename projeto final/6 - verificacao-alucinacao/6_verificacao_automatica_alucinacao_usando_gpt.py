# Script para analisar o nível de alucinação usando o GPT
# A ideia é testar prompts de sistema que pedem para o GPT verificar se uma
# opinião pode ser inferida a partir de um conjunto de chunks

import json
from openai import OpenAI

arquivo_resultado_alucinacoes = './results_experimento_chatgpt_com_analise_alucinacao.jsonl'

OPENAI_API = '' # Não subir de jeito nenhum pro git!
client = OpenAI(api_key=OPENAI_API)

# Prompts para testar
prompt_1 = {
    "nome_experimento": "prompt_1_gpt-4o-mini-2024-07-18",
    "modelo": "gpt-4o-mini-2024-07-18", 
    "atributo_opiniao_inferida": "opiniao_inferida",
    
    "propriedades_para_salvar": {
        # salvar_como: resultado_no_json
        "explicacao": "explicacao"
    },
    
    "prompt_sistema": """
Você é um assistente que analisa se uma opinião pode ser completamente inferida a partir de um texto.

O retorno da sua análise deverá ser sempre no formato JSON e conterá duas propriedades:
    - "explicacao": Uma string com o seu raciocínio explicando o porque a opinião pode ou não ser inferida pelo texto;
    - "opiniao_inferida": Um boolean (true ou false) sintetizando sua explicação: true, se a opinião puder ser inferida a partir do texto, ou false, se não puder.

Não forneça nada além do JSON com as propriedades acima.
""".strip()
}

prompt_2 = {
    "nome_experimento": "prompt_2_gpt-4o-mini-2024-07-18",
    "modelo": "gpt-4o-mini-2024-07-18", 
    "atributo_opiniao_inferida": "opiniao_inferida",
    
    "propriedades_para_salvar": {
        # salvar_como: resultado_no_json
        "explicacao": "explicacao",
        "trechos_para_basear_analise": "trechos_para_basear_analise"
    },
    
    "prompt_sistema": """
Você é um assistente especializado em análise de texto. Sua tarefa é verificar se uma opinião pode ser COMPLETAMENTE inferida a partir de um texto fornecido. Para isso, siga as etapas abaixo:

1. Identifique, no texto, os trechos que podem servir para suportar a opinião analisada;
2. Verifique se TODA a opinião é suportada pelos trechos selecionados. NÃO FAÇA SUPOSIÇÕES.
3. Forneça uma resposta direta (boolean). A resposta deve indicar se TODA a opinião pode ser inferida DIRETAMENTE do texto, sem o uso de suposições.

O retorno da sua análise deverá ser sempre no formato JSON e conterá três propriedades referentes aos passos anteriores:
    - "trechos_para_basear_analise": Uma lista de strings com os trechos que podem servir para suportar a opinião;
    - "explicacao": Uma string com o seu raciocínio explicando o porque a opinião pode ou não ser inferida pelo texto;
    - "opiniao_inferida": Um boolean (true ou false) sintetizando sua explicação: true, se a opinião puder ser inferida a partir do texto, ou false, se não puder.
    
Não forneça nada além do JSON com as propriedades acima.
""".strip()
}
    
prompt_3 = {
    "nome_experimento": "prompt_3_gpt-4o-mini-2024-07-18",
    "modelo": "gpt-4o-mini-2024-07-18", 
    "atributo_opiniao_inferida": "opiniao_inferida",
    
    "propriedades_para_salvar": {
        # salvar_como: resultado_no_json
        "explicacao": "explicacao",
        "trechos_para_basear_analise": "trechos_para_basear_analise"
    },
    
    "prompt_sistema": """
Você é um assistente especializado em análise de discursos. Sua tarefa é verificar se uma opinião pode ser COMPLETAMENTE inferida a partir de um trechos de texto. A sua análise deve seguir as etapas abaixo:

1. Identifique, nos trechos de texto, frases que suportam a opinião analisada.
2. Verifique se TODA a opinião é suportada pelas frases selecionadas. Não faça suposições e inferências indiretas.
3. Forneça uma resposta direta (boolean). A resposta deve indicar se TODA a opinião pode ser inferida DIRETAMENTE do texto. Caso você tenha dúvidas ou apenas parte da opinião puder ser inferida, responda que a opinião não pode ser inferida.

O retorno da sua análise deverá ser sempre no formato JSON e conterá três propriedades referentes aos passos anteriores:
    - "trechos_para_basear_analise": Uma lista com potenciais frases que suportam a opinião;
    - "explicacao": Uma string com o seu raciocínio explicando se TODA a opinião pode ou não ser inferida pelo texto;
    - "opiniao_inferida": Um boolean (true ou false) sintetizando sua explicação: true, se TODA a opinião puder ser inferida a partir do texto, ou false, se não puder ou se for inconclusivo.
    
Não forneça nada além do JSON com as propriedades acima.
""".strip()
}
    
prompt_1_gpt4_o = prompt_1.copy()
prompt_1_gpt4_o['nome_experimento'] = "prompt_1_gpt-4o-2024-08-06"
prompt_1_gpt4_o['modelo'] = "gpt-4o-2024-08-06"

prompt_2_gpt4_o = prompt_2.copy()
prompt_2_gpt4_o['nome_experimento'] = "prompt_2_gpt-4o-2024-08-06"
prompt_2_gpt4_o['modelo'] = "gpt-4o-2024-08-06"

prompt_3_gpt4_o = prompt_3.copy()
prompt_3_gpt4_o['nome_experimento'] = "prompt_3_gpt-4o-2024-08-06"
prompt_3_gpt4_o['modelo'] = "gpt-4o-2024-08-06"
    
# A mensagem de usuário. Ela sempre é a mesma, independente do prompt testado
msg_user = """
###### TEXTO:
{texto}

###### OPINIÃO PARA ANALISAR:
{opiniao}
""".strip()

def carregar_resultado_alucinacoes():
    dados_jsonl = []
    with open(arquivo_resultado_alucinacoes, encoding='utf-8') as fin:
        for line in fin:
            dados_jsonl.append(json.loads(line))
    return dados_jsonl

def salvar_resultado_alucinacoes(resultado_experimento):
    with open(arquivo_resultado_alucinacoes, 'w', encoding='utf-8') as arquivo:
        for item in resultado_experimento:
            linha = json.dumps(item, ensure_ascii=False)
            arquivo.write(linha + '\n')

def verifica_alucinacoes_na_opiniao(opiniao, prompt):
    print('\tChamando GPT...')
    response = client.chat.completions.create(
        model=prompt['modelo'],
        messages=[
            {
              "role": "system",
              "content": prompt['prompt_sistema']
            },
            {
              "role": "user",
              "content": msg_user.format(texto="\n\n".join(opiniao['chunks_proximos']), opiniao=opiniao['opiniao'])
            },
        ],
        response_format={ "type": "json_object" },
        temperature=0.02,
        max_tokens=4095,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
    # Abre o retorno em string e converte para json
    retorno_str_json = response.choices[0].message.content
    retorno_json = json.loads(retorno_str_json)
    
    # Verifica se o GPT acha que a opinião pode ser inferida dos chunks
    # Com base nisso, calcula se é alucinação
    atributo_opiniao_inferida = prompt['atributo_opiniao_inferida']
    eh_alucinacao = not retorno_json[atributo_opiniao_inferida]
    
    # Salva os resultados do experimento na opinião
    nome_experimento = prompt['nome_experimento']
    opiniao['verificacao_alucinacao'][nome_experimento] = {
        "alucinacao": eh_alucinacao,
    }
    # Salva os outros atributos do retorno do GPT que é pra salvar
    for salvar_como in prompt['propriedades_para_salvar'].keys():
        opiniao['verificacao_alucinacao'][nome_experimento][salvar_como] = retorno_json[prompt['propriedades_para_salvar'][salvar_como]]

def analise_alucinacao_experimentos(prompt):
    n_opiniao = 0
    total_opiniao = 4238 # Fixo no dataset
    
    # Faz a análise de alucinação
    for r in resultado_experimento:
        print(f'### Análise para id {r["id"]} ###')
        for autor in r['metadados_extraidos']['envolvidos']:
            for opiniao in autor['opinioes']:
                n_opiniao += 1                
                print(f'\tOpinião {n_opiniao} ({100.*n_opiniao/total_opiniao:.2f})%')
                if prompt['nome_experimento'] in opiniao['verificacao_alucinacao'].keys():
                    print('\tAlucinação já verificada. Pulando...')
                else:
                    print('\tVerificando alucinação com GPT...')
                    verifica_alucinacoes_na_opiniao(opiniao, prompt)
                    print('\tSalvando jsonl...')
                    salvar_resultado_alucinacoes(resultado_experimento)

resultado_experimento = carregar_resultado_alucinacoes()

#analise_alucinacao_experimentos(prompt_2)
analise_alucinacao_experimentos(prompt_2_gpt4_o)
analise_alucinacao_experimentos(prompt_3_gpt4_o)
analise_alucinacao_experimentos(prompt_1_gpt4_o)