import pandas as pd
import numpy as np
from scipy.stats import poisson

def prever_resultado_poisson(df: pd.DataFrame, time_casa: str, time_fora: str, max_gols: int = 5) -> dict:
    """
    Prevê a probabilidade de vitória do time da casa, empate e vitória do time visitante
    usando a distribuição de Poisson, com base nos dados históricos de gols.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados históricos das partidas.
                           Deve conter as colunas 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG'.
        time_casa (str): Nome do time da casa.
        time_fora (str): Nome do time visitante.
        max_gols (int): Número máximo de gols a considerar para a matriz de probabilidades.
                        Por padrão, considera de 0 a 5 gols para cada lado.

    Returns:
        dict: Um dicionário contendo as probabilidades de 'Vitoria Casa', 'Empate' e 'Vitoria Fora'.
    """

    # 1. Calcular as Médias de Gols
    # Média de gols marcados pelo time da casa jogando em casa
    gols_casa_marcados_media = df[df["HomeTeam"] == time_casa]["FTHG"].mean()
    # Média de gols sofridos pelo time da casa jogando em casa
    gols_casa_sofridos_media = df[df["HomeTeam"] == time_casa]["FTAG"].mean()

    # Média de gols marcados pelo time visitante jogando fora
    gols_fora_marcados_media = df[df["AwayTeam"] == time_fora]["FTAG"].mean()
    # Média de gols sofridos pelo time visitante jogando fora
    gols_fora_sofridos_media = df[df["AwayTeam"] == time_fora]["FTHG"].mean()

    # Média de gols marcados por todos os times em casa
    media_geral_casa_marcados = df["FTHG"].mean()
    # Média de gols marcados por todos os times fora
    media_geral_fora_marcados = df["FTAG"].mean()

    # 2. Estimar Lambda (λ) para o confronto específico
    # Força de ataque do time da casa
    forca_ataque_casa = gols_casa_marcados_media / media_geral_casa_marcados
    # Força de defesa do time da casa
    forca_defesa_casa = gols_casa_sofridos_media / media_geral_fora_marcados

    # Força de ataque do time visitante
    forca_ataque_fora = gols_fora_marcados_media / media_geral_fora_marcados
    # Força de defesa do time visitante
    forca_defesa_fora = gols_fora_sofridos_media / media_geral_casa_marcados

    # Lambda esperado para gols do time da casa
    lambda_casa = forca_ataque_casa * forca_defesa_fora * media_geral_casa_marcados
    # Lambda esperado para gols do time visitante
    lambda_fora = forca_ataque_fora * forca_defesa_casa * media_geral_fora_marcados

    # 3. Distribuição de Poisson e Matriz de Probabilidades
    prob_matriz = np.zeros((max_gols + 1, max_gols + 1))

    for i in range(max_gols + 1):
        for j in range(max_gols + 1):
            prob_casa = poisson.pmf(i, lambda_casa)
            prob_fora = poisson.pmf(j, lambda_fora)
            prob_matriz[i, j] = prob_casa * prob_fora

    # 4. Resultados Separados
    prob_vitoria_casa = 0
    prob_empate = 0
    prob_vitoria_fora = 0

    for i in range(max_gols + 1):
        for j in range(max_gols + 1):
            if i > j:  # Vitória da Casa
                prob_vitoria_casa += prob_matriz[i, j]
            elif i == j:  # Empate
                prob_empate += prob_matriz[i, j]
            else:  # Vitória do Visitante
                prob_vitoria_fora += prob_matriz[i, j]

    return {
        'Vitoria Casa': prob_vitoria_casa,
        'Empate': prob_empate,
        'Vitoria Fora': prob_vitoria_fora,
        'Lambda Casa': lambda_casa,
        'Lambda Fora': lambda_fora,
        'Matriz de Probabilidades': prob_matriz
    }

if __name__ == '__main__':
    # Exemplo de uso (o DataFrame 'df' precisaria ser carregado aqui)
    print("Este script contém a função 'prever_resultado_poisson'.")
    print("Para usá-la, você precisa carregar seu DataFrame de futebol e passá-lo como argumento.")
    print("Exemplo de como carregar o DataFrame e usar a função:")
    print("\nimport pandas as pd")
    print("from poisson_predictor import prever_resultado_poisson")
    print("\n# Carregue seu DataFrame 'df' aqui (ex: df = pd.read_csv('seus_dados.csv'))")
    print("# Ou use a lógica de carregamento do seu notebook footeboll.ipynb")
    print("\n# Exemplo de DataFrame (apenas para demonstração da estrutura esperada)")
    print("data = {'HomeTeam': ['TimeA', 'TimeB', 'TimeA', 'TimeC'],")
    print("        'AwayTeam': ['TimeB', 'TimeA', 'TimeC', 'TimeA'],")
    print("        'FTHG': [2, 1, 3, 0],")
    print("        'FTAG': [1, 2, 1, 1]}")
    print("df_exemplo = pd.DataFrame(data)")
    print("\n# Exemplo de chamada da função")
    print("resultados = prever_resultado_poisson(df_exemplo, 'TimeA', 'TimeC')")
    print("print(resultados)")
