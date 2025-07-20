# Script para imprimir estatísticas do estudo sobre alucinação das opiniões

import json
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats

arquivo_resultado_alucinacoes = './results_experimento_chatgpt_com_analise_alucinacao.jsonl'

prompt_1_gpt_4_o_mini = "prompt_1_gpt-4o-mini-2024-07-18"
prompt_1_gpt4_o = "prompt_1_gpt-4o-2024-08-06"
prompt_1_deepseek = "prompt_1_deepseek-chat"
prompt_1_sabia = "prompt_1_sabia-3.1-2025-05-08"

prompt_2_gpt_4_o_mini = "prompt_2_gpt-4o-mini-2024-07-18"
prompt_2_gpt4_o = "prompt_2_gpt-4o-2024-08-06"
prompt_2_deepseek = "prompt_2_deepseek-chat"
prompt_2_sabia = "prompt_2_sabia-3.1-2025-05-08"

prompt_3_gpt_4_o_mini = "prompt_3_gpt-4o-mini-2024-07-18"
prompt_3_gpt4_o = "prompt_3_gpt-4o-2024-08-06"
prompt_3_deepseek = "prompt_3_deepseek-chat"
prompt_3_sabia = "prompt_3_sabia-3.1-2025-05-08"

def ic(dados):
    media = np.mean(dados)
    desvio_padrao = np.std(dados, ddof=1)  # ddof=1 para amostra
    n = len(dados)
    
    # Nível de confiança (por exemplo, 95%)
    alpha = 0.05
    t_critico = stats.t.ppf(1 - alpha/2, df=n-1)
    
    # Erro padrão da média
    erro_padrao = desvio_padrao / np.sqrt(n)
    
    # Intervalo de confiança
    limite_inferior = media - t_critico * erro_padrao
    limite_superior = media + t_critico * erro_padrao
    return limite_inferior, limite_superior

# Dá o mesmo resultado do método anterior, só usei para confirmar
def ic_bootstrap(dados):
    B = 5000
    alpha = 0.05
    bootstraped_value = np.zeros(B)
    n = len(dados)
      
    # Use a for-loop
    for i in range(0, B):
        # Resample
        resampled = np.random.choice(dados, size=n, replace=True)
        # Apply the p quantile function
        bootstraped_value[i] = np.mean(resampled)
    
    return np.quantile(bootstraped_value, [alpha/2, 1-alpha/2])

def carregar_resultado_alucinacoes():
    dados_jsonl = []
    with open(arquivo_resultado_alucinacoes, encoding='utf-8') as fin:
        for line in fin:
            dados_jsonl.append(json.loads(line))
    return dados_jsonl

def imprime_analise_estatistica_alucinacao(prompt, texto='', n=None):
    n = len(resultado_experimento) if n is None else n
    
    alucinacao_real = []
    alucinacao_automatica = []
    
    for resultado in resultado_experimento[:n]:
        for envolvido in resultado['metadados_extraidos']['envolvidos']:
            for opiniao in envolvido['opinioes']:
                verificacao_alucinacao = opiniao['verificacao_alucinacao']
                if prompt in verificacao_alucinacao.keys():
                    verificacao_manual = verificacao_alucinacao['verificacao_manual']
                    verificacao_automatica = verificacao_alucinacao[prompt]['alucinacao']
                    
                    alucinacao_real.append(verificacao_manual)
                    alucinacao_automatica.append(verificacao_automatica)
                
    cm = confusion_matrix(alucinacao_real, alucinacao_automatica)
    if (len(cm) == 0):
        return 1, 1, 1, 0, 0
        
    total_opinioes = len(alucinacao_real)
    total_alucinacao = sum(alucinacao_real)
    total_opinioes_validas = total_opinioes - total_alucinacao
    
    total_alucinacao_detectada = cm[1][1]
    perc_alucinacao_detectada = 100.*cm[1][1]/total_alucinacao
    total_falso_positivo = cm[0][1]
    perc_falso_positivo = 100.*cm[0][1]/total_opinioes_validas
    
    print(f'##### {texto} #####\n')
    print(cm, '\n')
    
    print('##### Valores reais #####')
    print(f'Total de alucinação: {total_alucinacao} ({100.*total_alucinacao/total_opinioes:.2f})%')
    print(f'Total opiniões válidas: {total_opinioes_validas} ({100.*total_opinioes_validas/total_opinioes:.2f})%')
    
    print('\n##### Checando a detecção de alucinações #####')
    print(f'Alucinações detectadas corretamente: {total_alucinacao_detectada} ({perc_alucinacao_detectada:.2f}%)')
    print(f'Alucinações não detectadas: {cm[1][0]} ({100.*cm[1][0]/total_alucinacao:.2f}%)')
    
    print('\n##### Checando as opiniões válidas #####')
    print(f'Opiniões válidas detectadas corretamente: {cm[0][0]} ({100.*cm[0][0]/total_opinioes_validas:.2f}%)')
    print(f'Opiniões válidas não detectadas: {total_falso_positivo} ({perc_falso_positivo:.2f}%)\n\n')
    
    return total_opinioes, total_alucinacao, total_opinioes_validas,\
            total_alucinacao_detectada, total_falso_positivo

# Funções auxiliar para extrair coisas dos resultados
# total_opinioes
# total_alucinacao
# total_opinioes_validas
# total_alucinacao_detectada
# total_falso_positivo
def get_resultados_alucinacoes(resultados, modelo, num_prompts):
    resultados_modelo = resultados[modelo]
    percentual_alucinacoes_por_prompt = []
    ic_inf_por_prompt = []
    ic_sup_por_prompt = []
    for i in range(num_prompts):
        total_alucinacoes = resultados_modelo[i][1]
        total_alucinacao_detectada = resultados_modelo[i][3]
        perc_alucinacoes_detectadas = total_alucinacao_detectada/total_alucinacoes
        
        ic_inf, ic_sup = ic([1]*total_alucinacao_detectada + [0]*(total_alucinacoes-total_alucinacao_detectada))
        percentual_alucinacoes_por_prompt.append(100*perc_alucinacoes_detectadas)
        ic_inf_por_prompt.append(100*ic_inf)
        ic_sup_por_prompt.append(100*ic_sup)
        
    return percentual_alucinacoes_por_prompt, ic_inf_por_prompt, ic_sup_por_prompt
        
def get_resultados_falsos_positivos_alucinacoes(resultados, modelo, num_prompts):
    resultados_modelo = resultados[modelo]
    percentual_falsos_positivos_alucinacoes_por_prompt = []
    ic_inf_por_prompt = []
    ic_sup_por_prompt = []
    for i in range(num_prompts):
        total_opinioes_validas = resultados_modelo[i][2]
        total_falso_positivo = resultados_modelo[i][4]
        perc_falso_positivo = total_falso_positivo/total_opinioes_validas
        
        ic_inf, ic_sup = ic([1]*total_falso_positivo + [0]*(total_opinioes_validas-total_falso_positivo))
        percentual_falsos_positivos_alucinacoes_por_prompt.append(100*perc_falso_positivo)
        ic_inf_por_prompt.append(100*ic_inf)
        ic_sup_por_prompt.append(100*ic_sup)
        
    return percentual_falsos_positivos_alucinacoes_por_prompt, ic_inf_por_prompt, ic_sup_por_prompt


def plota_resultados_llms(resultados,
                          num_prompts=None,
                          nome_prompts=None):
    """
    Plota gráficos com resultados de alucinações e falsos positivos para múltiplos modelos.

    Parâmetros:
        resultados_alucinacao (dict): dicionário com nome do modelo como chave e lista de percentuais como valor.
        resultados_falso_positivo (dict): dicionário no mesmo formato que resultados_alucinacao.
        prompts (list, opcional): nomes dos prompts; se None, serão usados Prompt 1, Prompt 2, etc.
    """
    sns.set_palette('muted')

    # Verifica quantos prompts há (só acessa a primeira chave e pega o tamanho dela)
    if num_prompts is None:
        num_prompts = len(next(iter(resultados.values())))
    if nome_prompts is None:
        nome_prompts = [f'Prompt {i+1}' for i in range(num_prompts)]
    
    modelos = list(resultados.keys())
    n_modelos = len(modelos)
    x = np.arange(num_prompts)
    bar_width = 0.7 / n_modelos  # Largura ajustada para múltiplos modelos (originalmente estava 0.35)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
       
    # Gráfico 1: Alucinações
    for i, modelo in enumerate(modelos):
        resultados_alucinacao_do_modelo = get_resultados_alucinacoes(
            resultados, modelo, num_prompts)
        media_alucinacao_detectada = resultados_alucinacao_do_modelo[0]
        ic_inf = resultados_alucinacao_do_modelo[1]
        ic_sup = resultados_alucinacao_do_modelo[2]
            
        deslocamento = (i - n_modelos/2) * bar_width + bar_width/2
        # Média
        ax1.bar(x + deslocamento, media_alucinacao_detectada, bar_width, label=modelo)
        
        # Intervalos de confiança para os prompts       
        pos_x = x + deslocamento
        ax1.vlines(pos_x, ic_inf, ic_sup, color='black', linewidth=2)
        cap_size = bar_width / 2
        ax1.hlines(ic_inf, pos_x - cap_size/2, pos_x + cap_size/2, color='black', linewidth=2)
        ax1.hlines(ic_sup, pos_x - cap_size/2, pos_x + cap_size/2, color='black', linewidth=2)
            
    ax1.set_ylim(0, 100)
    ax1.set_ylabel('(%)')
    ax1.set_title('Hallucinations detected (%)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(nome_prompts)
    ax1.legend()

    # Gráfico 2: Falsos positivos
    for i, modelo in enumerate(modelos):
        resultados_falso_positivos_alucinacao_do_modelo = get_resultados_falsos_positivos_alucinacoes(
            resultados, modelo, num_prompts)
        media_falso_positivo_alucinacao = resultados_falso_positivos_alucinacao_do_modelo[0]
        ic_inf = resultados_falso_positivos_alucinacao_do_modelo[1]
        ic_sup = resultados_falso_positivos_alucinacao_do_modelo[2]

        deslocamento = (i - n_modelos/2) * bar_width + bar_width/2
        # Média
        ax2.bar(x + deslocamento, media_falso_positivo_alucinacao, bar_width, label=modelo)

        # Intervalos de confiança para os prompts       
        pos_x = x + deslocamento
        ax2.vlines(pos_x, ic_inf, ic_sup, color='black', linewidth=2)
        cap_size = bar_width / 2
        ax2.hlines(ic_inf, pos_x - cap_size/2, pos_x + cap_size/2, color='black', linewidth=2)
        ax2.hlines(ic_sup, pos_x - cap_size/2, pos_x + cap_size/2, color='black', linewidth=2)
        
    ax2.set_ylim(0, 40)
    ax2.set_ylabel('(%)')
    ax2.set_title('Valid opinions tagged as hallucinations (%)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(nome_prompts)
    ax2.legend()

    plt.tight_layout()
    plt.show()
    
resultado_experimento = carregar_resultado_alucinacoes()

n = 206

# Retorno:
# total_opinioes
# total_alucinacao
# total_opinioes_validas
# total_alucinacao_detectada
# total_falso_positivo
resultados_p1_4o_mini = imprime_analise_estatistica_alucinacao(prompt_1_gpt_4_o_mini, 'Prompt 1 GPT4o-mini', n)
resultados_p2_4o_mini = imprime_analise_estatistica_alucinacao(prompt_2_gpt_4_o_mini, 'Prompt 2 GPT4o-mini', n)
resultados_p3_4o_mini = imprime_analise_estatistica_alucinacao(prompt_3_gpt_4_o_mini, 'Prompt 3 GPT4o-mini', n)

resultados_p1_4o = imprime_analise_estatistica_alucinacao(prompt_1_gpt4_o, 'Prompt 1 GPT4o', n)
resultados_p2_4o = imprime_analise_estatistica_alucinacao(prompt_2_gpt4_o, 'Prompt 2 GPT4o', n)
resultados_p3_4o = imprime_analise_estatistica_alucinacao(prompt_3_gpt4_o, 'Prompt 3 GPT4o', n)

resultados_p1_ds = imprime_analise_estatistica_alucinacao(prompt_1_deepseek, 'Prompt 1 DeepSeek', n)
resultados_p2_ds = imprime_analise_estatistica_alucinacao(prompt_2_deepseek, 'Prompt 2 DeepSeek', n)
resultados_p3_ds = imprime_analise_estatistica_alucinacao(prompt_3_deepseek, 'Prompt 3 DeepSeek', n)

resultados_p1_sabia = imprime_analise_estatistica_alucinacao(prompt_1_sabia, 'Prompt 1 Sabiá', n)
resultados_p2_sabia = imprime_analise_estatistica_alucinacao(prompt_2_sabia, 'Prompt 2 Sabiá', n)
resultados_p3_sabia = imprime_analise_estatistica_alucinacao(prompt_3_sabia, 'Prompt 3 Sabiá', n)

resultados = {
    'GPT-4o mini': [resultados_p1_4o_mini, resultados_p2_4o_mini, resultados_p3_4o_mini],
    'GPT-4o': [resultados_p1_4o, resultados_p2_4o, resultados_p3_4o],
    'DeepSeek-R3': [resultados_p1_ds, resultados_p2_ds, resultados_p3_ds],
    'Sabiá': [resultados_p1_sabia, resultados_p2_sabia, resultados_p3_sabia]
}

plota_resultados_llms(resultados)


#antigo = 'prompt_1_sabia-3-2024-12-11'
#novo = 'prompt_1_sabia-3-2024-12-11'
#tem_antigo = 0
#tem_novo = 0

#for resultado in resultado_experimento:
#    for envolvido in resultado['metadados_extraidos']['envolvidos']:
#        for opiniao in envolvido['opinioes']:
###            verificacao_alucinacao = opiniao['verificacao_alucinacao']
  #          verificacao_manual = verificacao_alucinacao['verificacao_manual']
  #          tem_antigo = tem_antigo + (1 if antigo in verificacao_alucinacao.keys() else 0)
  #          tem_novo = tem_novo + (1 if novo in verificacao_alucinacao.keys() else 0)
#print(tem_antigo)
#print(tem_novo)