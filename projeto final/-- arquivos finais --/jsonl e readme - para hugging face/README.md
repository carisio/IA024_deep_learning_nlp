# PublicHearingBR: A Brazilian Portuguese Dataset of Public Hearing Transcripts for Summarization of Long Documents

PublicHearingBR is a Portuguese dataset that can be used for two types of tasks: summarization of long documents (LDS) and natural language inference (NLI). Two files are provided: PublicHearingBR_LDS.jsonl and PublicHearingBR_NLI.jsonl.

The script `load_dataset.py` can be used to load the datasets and print their structure, as described in the next two sections.

For more details about the dataset, refer to the paper: _"PublicHearingBR: A Brazilian Portuguese Dataset of Public Hearing Transcripts for Summarization of Long Documents"_.

## 1. PublicHearingBR_LDS - Long Document Summarization

The file PublicHearingBR_LDS.jsonl contains 206 samples for testing long document summarization (public hearing transcripts). Considering that `phbr_lds` is the dataset loaded from the jsonl file:

- `phbr_lds[0]` is the first sample in the dataset. Its structure is a dictionary with 4 attributes:
    - `id`: an integer indicating the sample number (sequential from 1 to 206)
    - `transcricao`: text extracted from the public hearing transcript (long document)
    - `materia`: text extracted from the news article (summary)
    - `metadados`: a dictionary containing the structured summary extracted from the article (structured summary). The `metadados` dictionary has two keys:
        - `assunto`: the main topic of the article
        - `envolvidos`: a list of dictionaries containing all the people mentioned in the news article and some details:
            - `cargo`: the person's position
            - `nome`: the person's name
            - `opinioes`: a list of strings containing the opinions expressed by the people

The following code prints the entire metadata structure:

```python
for sample in phbr_lds:
    id = sample['id']
    transcricao = sample['transcricao'] # long document
    materia = sample['materia']         # Summary
    metadados = sample['metadados']     # Structured summary
    
    print(f"\n########## ID: {id}")
    for envolvido in metadados['envolvidos']:
        cargo = envolvido['cargo']
        nome = envolvido['nome']
        opinioes = envolvido['opinioes']
        
        print(f"\n\tNome: {nome}")
        print(f"\tCargo: {cargo}")
        print(f"\tOpiniões:")
        for opiniao in opinioes:
            print(f"\t\t- {opiniao}")
```		
			
## 2. PublicHearingBR_NLI - Natural Language Inference

The file PublicHearingBR_NLI.jsonl contains 4,238 samples for testing natural language inference. Each of these samples contains an opinion and a set of texts. Additionally, there is a flag indicating whether the opinion can be inferred from this set of texts.

Considering that `phbr_nli` is the dataset extracted from the jsonl:

- `phbr_nli[0]` is the first sample in the dataset. Its structure is a dictionary with 2 attributes:
    - `id`: an integer indicating, in `phbr_lds`, which sample the `metadados_extraidos` refers to. In practice, it is a reference ID only, and it does not need to be used.
    - `metadados_extraidos`: it is a structure similar to the `metadados` structure in `phbr_lds`. However, there are some differences. This structure was generated by the transcription summarization experiment conducted with ChatGPT, as described in the article, and it has 3 parameters:
        - `assunto`: a string that represents the main topic of the transcript.
        - `envolvidos`: a list with a structure similar to the same field in the `phbr_lds` dataset. In other words, it contains the following data:
            - `nome`: a string indicating the person's name extracted from the transcription by the experiment
            - `cargo`: the person's position extracted from the transcription by the experiment.
            - `opinioes`: A list of the person's opinions. Each element of this list is a dictionary (this differs from the `opinioes` field in the `phbr_lds` dataset) with the following structure:
                - `opiniao`: the opinion extracted by the experiment
                - `chunks_proximos`: a list containing four chunks. The task is to determine whether it is possible to infer the opinion from these four chunks
                - `verificacao_alucinacao`: a dictionary containing the hallucination verification. This dictionary has a key `verificacao_manual`, which is the manual annotation of this information, a boolean indicating whether the opinion is a hallucination or not (i.e., whether it can be inferred from the nearby chunks). Additionally, this structure includes the results of tests with the three prompts described in the article.

The following code prints all the opinions, nearby chunks, and an indication of whether it is a hallucination or not:

```python
    for sample in phbr_nli[0:n]:
        id = sample['id']
        metadados_extraidos = sample['metadados_extraidos']
        
        print(f"\n########## ID: {id}")
        for envolvido in metadados_extraidos['envolvidos']:
            nome = envolvido['nome']
            cargo = envolvido['cargo']
            
            print(f"\n\t\tNome: {nome}")
            for n_opiniao, opiniao in enumerate(envolvido['opinioes'], 1):
                desc_opiniao = opiniao['opiniao']
                chunks_proximos = opiniao['chunks_proximos']
                verificao_alucinacao = opiniao['verificacao_alucinacao']
                verificacao_manual = verificao_alucinacao['verificacao_manual']
                verificacao_automatica_prompt_1 = verificao_alucinacao['prompt_1_gpt-4o-mini-2024-07-18']['alucinacao']
                verificacao_automatica_prompt_2 = verificao_alucinacao['prompt_2_gpt-4o-mini-2024-07-18']['alucinacao']
                verificacao_automatica_prompt_3 = verificao_alucinacao['prompt_3_gpt-4o-mini-2024-07-18']['alucinacao']
                
                print(f"\t\t - {n_opiniao}:{desc_opiniao}")
                print(f"\t\t\t Alucinação (manual):   {verificacao_manual}")
                print(f"\t\t\t Alucinação (prompt 1): {verificacao_automatica_prompt_1}")
                print(f"\t\t\t Alucinação (prompt 2): {verificacao_automatica_prompt_2}")
                print(f"\t\t\t Alucinação (prompt 3): {verificacao_automatica_prompt_3}")
```