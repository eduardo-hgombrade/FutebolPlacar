# models/predictor.py
import pandas as pd
import numpy as np
from scipy.stats import poisson

def prever_resultado_poisson(df: pd.DataFrame, time_casa: str, time_fora: str, max_gols: int = 5) -> dict:
    """
    Calcula as probabilidades de vitória e o placar mais provável
    usando a Distribuição de Poisson.
    """
    # Verificação de segurança: checar se os times existem no histórico
    if time_casa not in df['HomeTeam'].values or time_fora not in df['AwayTeam'].values:
        return {'erro': 'Um ou ambos os times não foram encontrados no histórico.'}

    # 1. Médias de gols do time da casa e do visitante
    gols_casa_marcados = df[df["HomeTeam"] == time_casa]["FTHG"].mean()
    gols_casa_sofridos = df[df["HomeTeam"] == time_casa]["FTAG"].mean()

    gols_fora_marcados = df[df["AwayTeam"] == time_fora]["FTAG"].mean()
    gols_fora_sofridos = df[df["AwayTeam"] == time_fora]["FTHG"].mean()

    # 2. Médias gerais da liga (servem como referência)
    media_geral_casa = df["FTHG"].mean()
    media_geral_fora = df["FTAG"].mean()

    # 3. Força de ataque e defesa de cada time
    forca_ataque_casa = gols_casa_marcados / media_geral_casa
    forca_defesa_casa = gols_casa_sofridos / media_geral_fora
    forca_ataque_fora = gols_fora_marcados / media_geral_fora
    forca_defesa_fora = gols_fora_sofridos / media_geral_casa

    # 4. Lambda = gols esperados para o confronto específico
    lambda_casa = forca_ataque_casa * forca_defesa_fora * media_geral_casa
    lambda_fora = forca_ataque_fora * forca_defesa_casa * media_geral_fora

    # 5. Matriz de probabilidades de cada placar possível
    prob_matriz = np.zeros((max_gols + 1, max_gols + 1))
    for i in range(max_gols + 1):
        for j in range(max_gols + 1):
            prob_matriz[i, j] = poisson.pmf(i, lambda_casa) * poisson.pmf(j, lambda_fora)

    # 6. Probabilidades de Vitória, Empate e Derrota
    prob_vitoria_casa = np.sum(np.tril(prob_matriz, -1))
    prob_empate       = np.sum(np.diag(prob_matriz))
    prob_vitoria_fora = np.sum(np.triu(prob_matriz, 1))

    # 7. --- NOVO: placar mais provável ---
    # Encontra o índice do maior valor na matriz (placar com maior chance)
    idx_max = np.unravel_index(np.argmax(prob_matriz), prob_matriz.shape)
    gols_previstos_casa = idx_max[0]
    gols_previstos_fora = idx_max[1]
    placar_previsto = f"{gols_previstos_casa} x {gols_previstos_fora}"
    # ------------------------------------

    return {
        # Probabilidades originais do grupo (mantidas)
        'vitoria_casa': round(prob_vitoria_casa * 100, 2),
        'empate':       round(prob_empate * 100, 2),
        'vitoria_fora': round(prob_vitoria_fora * 100, 2),
        # Novos campos para o placar exato
        'lambda_casa':          round(lambda_casa, 2),
        'lambda_fora':          round(lambda_fora, 2),
        'gols_previstos_casa':  gols_previstos_casa,
        'gols_previstos_fora':  gols_previstos_fora,
        'placar_previsto':      placar_previsto,
    }