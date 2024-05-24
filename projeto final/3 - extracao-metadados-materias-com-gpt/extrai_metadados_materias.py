import os
from openai import OpenAI

OPENAI_API = '' # Não subir de jeito nenhum pro git!

SOBREESCREVER_METADADOS = False

modelo = "gpt-3.5-turbo-0125"
modelo = "gpt-4o-2024-05-13"

diretorio_metadados = f'./metadados-materias-{modelo}'
os.makedirs(diretorio_metadados , exist_ok=True)

msg_sistema_gpt = """
Você é um assistente que analisa matérias escritas pela Agência Câmara, da Câmara dos Deputados. Seu papel é identificar na matéria os seguintes itens:

- Tópico principal que está sendo tratado
- O nome das pessoas envolvidas
- O que cada pessoa defende
- O que cada pessoa disse (em caso de existir citação direta)

Desconsidere o nome dos jornalistas ou editores da matéria. As únicas pessoas que interessam são as que estão no corpo da matéria.

O retorno deve ser no formato JSON, com duas propriedades: 

- "assunto": uma string que indica o assunto principal da matéria
- "envolvidos": uma lista de objetos que indica as pessoas envolvidas na matéria. O objeto deve ter três propriedades:
    -- "nome": string, indica nome da pessoa
    -- "cargo": string, indica cargo que a pessoa ocupa, juntamente com o órgão, a entidade ou a empresa em que ela trabalha, se estiver disponível
    -- "opinioes": lista de string indicando todas as opiniões que a pessoa defendeu e que estão indicadas no texto. As opiniões devem ser listadas de forma detalhada. Se for uma citação direta, o texto indicada na lista DEVE OBRIGATORIAMENTE ser idêntico ao contido na matéria, incluindo as aspas.
""".strip()

def extrai_metadados_com_gpt(txt_materia):
    client = OpenAI(api_key=OPENAI_API)
    
    response = client.chat.completions.create(
      model=modelo,
      messages=[
        {
          "role": "system",
          "content": msg_sistema_gpt
        },
        {
          "role": "user",
          "content": txt_materia
        },
      ],
      response_format={ "type": "json_object" },
      temperature=0.02,
      max_tokens=4095,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response.choices[0].message.content
    
for i in range(1, 212):
    print(f'*************** Extraindo metadados da matéria {i} ***************')
    
    with open(f'../2 - extracao-texto/materias/materia_{i}.txt', 'r', encoding='utf-8') as file:
        txt_materia = file.read()
    
    caminho_arquivo = os.path.join(diretorio_metadados, f'materia_{i}.json')

    # Se o arquivo de metadados já existe e não for pra sobreescrever, passa pro
    # próximo arquivo
    if os.path.exists(caminho_arquivo) and not SOBREESCREVER_METADADOS:
        continue
        
    # Extrai os metadados com o GPT
    metadados_json = extrai_metadados_com_gpt(txt_materia)
    
    with open(caminho_arquivo, 'w', encoding='utf-8') as file:
        file.write(metadados_json)