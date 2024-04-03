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

Projeto: 

- Implementação: [Jupyter notebook](./3%20-%20gpt-2/notebook/[IA24_Aula3]_Modelo_de_Linguagem_com_auto_atenção_e_máscara_causal.ipynb) / [Colab](https://colab.research.google.com/drive/1JN5Fl63652-_flF1BtPgcTECTUzSUK6d?usp=sharing)
- Tópicos relevantes da leitura do artigo: [Word](./3%20-%20gpt-2/leitura/[Aula%203]%20GPT-2%20-%20Principais%20contribuições%20do%20artigo.docx) / [PDF](./3%20-%20gpt-2/leitura/[Aula%203]%20GPT-2%20-%20Principais%20contribuições%20do%20artigo.pdf)
