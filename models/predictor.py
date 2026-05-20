# models/predictor.py
import pandas as pd
import numpy as np
from scipy.stats import poisson

def prever_resultado_poisson(df: pd.DataFrame, time_casa: str, time_fora: str, max_gols: int = 5) -> dict:
    """
    Calcula a probabilidade de vitória usando a distribuição de Poisson.
    O código foi estruturado para evitar erros caso os times não existam no histórico.
    """
    # Verificação de segurança: checar se os times existem no DataFrame
    if time_casa not in df['HomeTeam'].values or time_fora not in df['AwayTeam'].values:
        return {'erro': 'Um ou ambos os times não foram encontrados no histórico.'}

    # 1. Calculamos o desempenho histórico do time da casa (Ataque e Defesa)
    gols_casa_marcados = df[df["HomeTeam"] == time_casa]["FTHG"].mean()
    gols_casa_sofridos = df[df["HomeTeam"] == time_casa]["FTAG"].mean()

    # 2. Calculamos o desempenho histórico do time visitante (Ataque e Defesa)
    gols_fora_marcados = df[df["AwayTeam"] == time_fora]["FTAG"].mean()
    gols_fora_sofridos = df[df["AwayTeam"] == time_fora]["FTHG"].mean()

    # Médias globais do campeonato para criar um "fator de força"
    media_geral_casa = df["FTHG"].mean()
    media_geral_fora = df["FTAG"].mean()

    # 3. Força de ataque e defesa (compara o time com a média da liga)
    forca_ataque_casa = gols_casa_marcados / media_geral_casa
    forca_defesa_casa = gols_casa_sofridos / media_geral_fora
    forca_ataque_fora = gols_fora_marcados / media_geral_fora
    forca_defesa_fora = gols_fora_sofridos / media_geral_casa

    # 4. Cálculo do Lambda (Expectativa real de gols para o confronto)
    lambda_casa = forca_ataque_casa * forca_defesa_fora * media_geral_casa
    lambda_fora = forca_ataque_fora * forca_defesa_casa * media_geral_fora

    # 5. Criando a matriz de resultados possíveis usando Poisson
    prob_matriz = np.zeros((max_gols + 1, max_gols + 1))
    for i in range(max_gols + 1):
        for j in range(max_gols + 1):
            prob_matriz[i, j] = poisson.pmf(i, lambda_casa) * poisson.pmf(j, lambda_fora)

    # 6. Agrupando as probabilidades de Vitória, Empate e Derrota
    prob_vitoria_casa = np.sum(np.tril(prob_matriz, -1)) # Abaixo da diagonal principal
    prob_empate = np.sum(np.diag(prob_matriz))           # Na diagonal principal
    prob_vitoria_fora = np.sum(np.triu(prob_matriz, 1))  # Acima da diagonal principal

    # Retornamos em formato de dicionário para facilitar o consumo via API/Front
    return {
        'vitoria_casa': round(prob_vitoria_casa * 100, 2),
        'empate': round(prob_empate * 100, 2),
        'vitoria_fora': round(prob_vitoria_fora * 100, 2),
    }