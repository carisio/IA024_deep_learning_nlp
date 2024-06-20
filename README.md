# Repositório para a disciplina IA024:  Deep Learning para Processamento de Linguagem Natural
*Leandro Carísio Fernandes*


Observação: Os cadernos Jupyter foram exportados do Colab. Caso o link do Colab não esteja funcionando, basta importar o caderno Jupyter no Colab.

<br>

## 0. Seleção para aluno especial

Projeto: Análise de sentimentos da base IMDB (rede neural MLP de duas camadas)

Artigo para leitura: Até a página 12 do artigo [On the Opportunities and Risks of Foundation Models](https://arxiv.org/pdf/2108.07258.pdf)

- [Enunciado do exercício](./0%20-%20selecao%20-%20mlp%20para%20analise%20de%20sentimentos%20imdb/relatorio/enunciado%20-%20[versao%20final]%20Processo%20Seletivo%20para%20Disciplina%20IA-024%201S2024.docx)
- [Relatório PDF](./0%20-%20selecao%20-%20mlp%20para%20analise%20de%20sentimentos%20imdb/relatorio/relatorio%20-%20Processo%20Seletivo%20IA024%201S2024.pdf) / [Relatório DOCX](./0%20-%20selecao%20-%20mlp%20para%20analise%20de%20sentimentos%20imdb/relatorio/relatorio%20-%20Processo%20Seletivo%20IA024%201S2024.docx)
- Implementação: [Jupyter notebook](./0%20-%20selecao%20-%20mlp%20para%20analise%20de%20sentimentos%20imdb/notebook/AnaliseSentimentosBagOfWords_Carisio.ipynb) / [Colab](https://colab.research.google.com/drive/1GKMh43uoZUr6noazUjH7muRgajV4kVXz?usp=sharing) / [Resultado execução PDF](./0%20-%20selecao%20-%20mlp%20para%20analise%20de%20sentimentos%20imdb/notebook/AnaliseSentimentosBagOfWords-Carisio.pdf)
- [Tópicos relevantes da leitura do artigo](./0%20-%20selecao%20-%20mlp%20para%20analise%20de%20sentimentos%20imdb/leitura/Topicos%20relevantes%20-%20On%20the%20Opportunities%20and%20Risks%20of%20Foundation%20Models.pdf)


Observações:

- No notebook o cálculo da loss considerou apenas o último batch (em vez de acumular a loss de todas as amostras e de todos os batchs).

<br> 

## 1. Rede proposta por Bengio et al

Projeto: Implementar o modelo de linguagem inspirado no artigo de Bengio et al ([A neural probabilistic language model](https://www.jmlr.org/papers/volume3/bengio03a/bengio03a.pdf)).

- Implementação: [Jupyter notebook](./1%20-%20modelo%20de%20linguagem%20-%20bengio/notebook/[IA24_Aula1]_Bengio.ipynb) / [Colab](https://colab.research.google.com/drive/166oq8hm0D9PinBYgxMiAYwWSvCsUG-Po?usp=sharing)
- Tópicos relevantes da leitura do artigo: [Word](./1%20-%20modelo%20de%20linguagem%20-%20bengio/leitura/[Aula%201]%20Bengio%20-%20Principais%20contribuições%20do%20artigo.docx) / [PDF](./1%20-%20modelo%20de%20linguagem%20-%20bengio/leitura/[Aula%201]%20Bengio%20-%20Principais%20contribuições%20do%20artigo.pdf)

<br> 

## 2. Mecanismo de auto-atenção e encoding posicional

Projeto: Implementar o mecanismo de auto-atenção e de encoding posicional proposto no artigo [Attention is all you need]() e usá-los na rede implementada na última atividade (modelo de Bengio).

- Implementação: [Jupyter notebook](./2%20-%20auto-atencao%20e%20encoding%20posicional/notebook/%5BIA24_Aula2%5D_Bengio_com_mecanismo_de_aten%C3%A7%C3%A3o.ipynb) / [Colab](https://colab.research.google.com/drive/1asoxTqrJe2Bnmg2nNa4nM8I6oW6puJJ1?usp=sharing)
- Tópicos relevantes da leitura do artigo: [Word](./2%20-%20auto-atencao%20e%20encoding%20posicional/leitura/[Aula%202]%20Auto-atenção%20-%20Principais%20contribuições%20do%20artigo.docx) / [PDF](./2%20-%20auto-atencao%20e%20encoding%20posicional/leitura/[Aula%202]%20Auto-atenção%20-%20Principais%20contribuições%20do%20artigo.pdf)

<br> 

## 3. GPT-2

Leitura da semana: [Language Models are Unsupervised Multitask Learners](https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)

Projeto: Modelo de linguagem baseado no GPT-2

- Implementação: [Jupyter notebook](./3%20-%20gpt-2/notebook/[IA24_Aula3]_Modelo_de_Linguagem_com_auto_atenção_e_máscara_causal.ipynb) / [Colab](https://colab.research.google.com/drive/1JN5Fl63652-_flF1BtPgcTECTUzSUK6d?usp=sharing)
- Tópicos relevantes da leitura do artigo: [Word](./3%20-%20gpt-2/leitura/[Aula%203]%20GPT-2%20-%20Principais%20contribuições%20do%20artigo.docx) / [PDF](./3%20-%20gpt-2/leitura/[Aula%203]%20GPT-2%20-%20Principais%20contribuições%20do%20artigo.pdf)

<br> 

## 4. Fine-tuning de um modelo BERT para análise de sentimentos

Leitura da semana: [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/pdf/1810.04805.pdf)

Projeto: Fine-tuning de um modelo BERT para análise de sentimentos

- Implementação: [Jupyter notebook](./4%20-%20fine-tuning%20bert/notebook/[IA24_Aula4]_Fine_tuning_do_BERT_no_IMDB.ipynb) / [Colab](https://colab.research.google.com/drive/1CDqL-jC1rt7rwnWjUB0m1uSvLOa5viSj?usp=sharing)
- Tópicos relevantes da leitura do artigo: [Word](./4%20-%20fine-tuning%20bert/leitura/[Aula%204]%20BERT%20-%20Principais%20contribuições%20do%20artigo.docx) / [PDF](./4%20-%20fine-tuning%20bert/leitura/[Aula%204]%20BERT%20-%20Principais%20contribuições%20do%20artigo.pdf)

<br> 

## 5. Implementação de camada LoRA numa rede simples (BoW, camada linear, ReLU, camada linear) para análise de sentimento na base do IMDB

Leitura da semana: [LoRA: Low-rank adaptation of large language models](https://arxiv.org/pdf/2106.09685.pdf)

Projeto: Implementação de uma camada LoRA

- Implementação: [Jupyter notebook](./5%20-%20lora/notebook/[IA24_Aula5]_Analise_sentimento_IMDB_com_BoW_e_Lora.ipynb) / [Colab](https://colab.research.google.com/drive/1Nv99o2zjyQj49HREOmA6CZrKrQ9-7rQg?usp=sharing)
- Tópicos relevantes da leitura do artigo: [Word](./5%20-%20lora/leitura/[Aula%205]%20LoRA%20-%20Principais%20contribuições%20do%20artigo.docx) / [PDF](./5%20-%20lora/leitura/[Aula%205]%20LoRA%20-%20Principais%20contribuições%20do%20artigo.pdf)

<br> 

## 6. Fine-tuning do Phi 1.5 usando QLoRA para análise de sentimento na base do IMDB

Leitura da semana: [LoRA: Low-rank adaptation of large language models](https://arxiv.org/pdf/2106.09685.pdf)

Projeto: Fine-tuning do Phi 1.5 usando QLoRA

- Implementação: [Jupyter notebook](./6%20-%20qlora/notebook/[IA24_Aula6]_Fine_tuning_Phi_1_5_for_sentence_classification_using_QLoRA_Carisio.ipynb) / [Colab](https://colab.research.google.com/drive/1avjYjbe4DDZeD-qQ05x27H04Yuik-4E_?usp=sharing)
- Tópicos relevantes da leitura do artigo: [Word](./6%20-%20qlora/leitura/[Aula%206]%20QLoRA%20-%20Principais%20contribuições%20do%20artigo.docx) / [PDF](./6%20-%20qlora/leitura/[Aula%206]%20QLoRA%20-%20Principais%20contribuições%20do%20artigo.pdf)

<br> 

## 7. Análise de sentimento na base do IMDB com Llama-3 70B

Leitura da semana: [A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications](https://arxiv.org/pdf/2402.07927)

Projeto: Uso do Llama-3 70B e algumas técnicas de engenharia de prompt para fazer análise de sentimentos na base do IMDB.

- Implementação: [Jupyter notebook](./7%20-%20survey%20prompt%20engineering/notebook/[IA24_Aula7]_Análise_de_sentimentos_IMDB_Llama_3_70B.ipynb)
- Tópicos relevantes da leitura do artigo: [Word](./7%20-%20survey%20prompt%20engineering/leitura/[Aula%207]%20Survey%20of%20prompt%20engineering%20-%20Principais%20contribuições%20do%20artigo.docx) / [PDF](./7%20-%20survey%20prompt%20engineering/leitura/[Aula%207]%20Survey%20of%20prompt%20engineering%20-%20Principais%20contribuições%20do%20artigo.pdf)

<br> 

## 8. RAG

Leitura da semana: [Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/pdf/2312.10997)

Projeto: Reproduzir o Visconde

- Implementação: [Jupyter notebook](./8%20-%20visconde/notebook/[IA24_Aula8]_Visconde.ipynb) / [Colab](https://colab.research.google.com/drive/1T71cOJor1erwag0G8r92LZT5_pRxtmLZ?usp=sharing)
- Tópicos relevantes da leitura do artigo: [Word](./8%20-%20visconde/leitura/[Aula%208]%20RAG%20for%20LLM%20-%20a%20survey%20-%20Principais%20contribuições%20do%20artigo.docx) / [PDF](./8%20-%20visconde/leitura/[Aula%208]%20RAG%20for%20LLM%20-%20a%20survey%20-%20Principais%20contribuições%20do%20artigo.pdf)

<br> 


## 9. ReAct

Leitura da semana: [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/pdf/2210.03629)

Projeto: Implementar o ReAct com o notebook anterior: fazer um prompt que chama um agente -- um buscador --, refina a pesquisa até ter a possibilidade de dar a resposta e, no fim, responder.

- Implementação: [Jupyter notebook](./9%20-%20react/notebook/[IA24_Aula9]_ReAct.ipynb) / [Colab](https://colab.research.google.com/drive/18k-cDgt_Aci4oitecD1u4BvU0wSiRcFD?usp=sharing)
- Tópicos relevantes da leitura do artigo: [Word](./9%20-%20react/leitura/[Aula%209]%20ReAct%20-%20Principais%20contribuições%20do%20artigo.docx) / [PDF](./9%20-%20react/leitura/[Aula%209]%20ReAct%20-%20Principais%20contribuições%20do%20artigo.pdf)

<br> 

## 10. RAGAS

Leitura da semana: [RAGAS: Automated Evaluation of Retrieval Augmented Generation](https://arxiv.org/pdf/2309.15217)

Projeto: Implementar o RAGAS para avaliar 50 respostas do dataset do IIRC.

- Implementação: [Jupyter notebook](./10%20-%20ragas/notebook/[IA24_Aula10]_RAGAS.ipynb) / [Colab](https://colab.research.google.com/drive/17ntxRsTuxouvvUZn2kALfeQBd4cBRua9?usp=sharing)
- Tópicos relevantes da leitura do artigo: [Word](./10%20-%20ragas/leitura/[Aula%2010]%20RAGAS%20-%20Principais%20contribuições%20do%20artigo.docx) / [PDF](./10%20-%20ragas/leitura/[Aula%2010]%20RAGAS%20-%20Principais%20contribuições%20do%20artigo.pdf)

<br> 

## 11. Multiagentes

Leitura da semana: [Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://arxiv.org/pdf/2305.14325)

- Tópicos relevantes da leitura do artigo: [Word](./11%20-%20multiagentes/leitura/[Aula%2011]%20Multiagentes%20-%20Principais%20contribuições%20do%20artigo.docx) / [PDF](./11%20-%20multiagentes/leitura/[Aula%2011]%20Multiagentes%20-%20Principais%20contribuições%20do%20artigo.pdf)

<br>

## Projeto final 

Descrição do projeto: Criação de um dataset para sumarização de longos documentos em português. A ideia é criar triplas (transcrições, notícias, metadadados de notícias) de audiências públicas da Câmara dos Deputados.

Apresentações:
  - [Plano de trabalho](./projeto%20final/--%20apresentacoes%20--/1%20-%20Plano%20de%20trabalho.pdf)
  - [Experimento com o ChatGPT e proposta de avaliação](./projeto%20final/--%20apresentacoes%20--/2%20-%20Experimento%20e%20proposta%20avaliacao.pdf)
  - [Resultados do experimento e proposta de medição de alucinação](./projeto%20final/--%20apresentacoes%20--/3%20-%20Caracteristicas%20do%20dataset%20-%20resultado%20experimento%20-%20proposta%20medicao%20alucinacao.pdf)

Arquivos finais:
  - [Dataset (dataset.jsonl)](./projeto%20final/--%20arquivos%20finais%20--/o%20dataset/dataset.jsonl)
  - [Experimento: Extração de sumários com o ChatGPT](./projeto%20final/--%20arquivos%20finais%20--/experimento%20chatgpt/results_experiment_chatgpt.jsonl)
  - Resultados das avaliações