import pandas as pd
import requests
import io
from poisson_predictor import prever_resultado_poisson

def carregar_dataframe_futebol():
    """
    Carrega os dados históricos de futebol de várias temporadas em um único DataFrame
    a partir de um repositório GitHub.
    """
    BASE_URL = 'https://raw.githubusercontent.com/datasets/football-datasets/master/datasets/premier-league/'
    temporadas = {
        '2020-21': 'season-2021.csv', # Este arquivo pode não existir ou ter outro nome
        '2021-22': 'season-2122.csv',
        '2022-23': 'season-2223.csv',
        '2023-24': 'season-2324.csv',
        '2024-25': 'season-2425.csv',
    }

    # Tentativa de encontrar arquivos mais recentes ou com nomenclatura diferente
    # O repositório GitHub usa um formato como 'season-YYMM.csv' ou 'season-YYYY.csv'
    # Vamos tentar um formato mais genérico para as últimas temporadas.
    # A partir de 2020, o formato parece ser 'season-YYYY.csv' (ex: season-2021.csv)
    # Mas o repositório parece ter dados até 2019-2020. Vamos ajustar as temporadas para o que está disponível.
    # Verificando o repositório, os arquivos são nomeados como season-YYMM.csv, ex: season-1920.csv
    # Para as temporadas mais recentes, pode ser necessário ajustar a fonte ou a nomenclatura.
    # Por enquanto, vou tentar com as temporadas mais recentes que parecem seguir um padrão similar.
    # Vou usar as temporadas 2016-17 a 2019-20 para garantir que os arquivos existam no repositório.
    # Se o usuário precisar de dados mais recentes, precisaremos de uma fonte diferente.

    temporadas_github = {
        '2016-17': 'season-1617.csv',
        '2017-18': 'season-1718.csv',
        '2018-19': 'season-1819.csv',
        '2019-20': 'season-1920.csv',
    }

    lista_dfs = []

    print("Carregando dados das temporadas do GitHub...")
    for nome, arquivo in temporadas_github.items():
        url = BASE_URL + arquivo
        try:
            resposta = requests.get(url)
            resposta.raise_for_status() # Levanta um erro para códigos de status HTTP ruins
            df_temp = pd.read_csv(io.StringIO(resposta.text))
            df_temp["Temporada"] = nome
            lista_dfs.append(df_temp)
            print(f'  Temporada {nome}: {len(df_temp)} partidas carregadas')
        except requests.exceptions.RequestException as e:
            print(f'Erro ao carregar a temporada {nome} de {url}: {e}')
            print('Continuando com as próximas temporadas...')
        except pd.errors.EmptyDataError:
            print(f'Erro: O arquivo CSV da temporada {nome} está vazio ou malformado.')
            print('Continuando com as próximas temporadas...')

    if not lista_dfs:
        raise ValueError("Nenhum DataFrame foi carregado com sucesso. Verifique as URLs ou a disponibilidade dos dados.")

    df_final = pd.concat(lista_dfs, ignore_index=True)
    print(f'Total de partidas carregadas: {len(df_final)}')
    return df_final

if __name__ == '__main__':
    try:
        df = carregar_dataframe_futebol()

        # Exemplo de uso da função com times reais do dataset
        # É importante escolher times que existam nos dados carregados.
        # Times comuns nas temporadas 2016-2020 incluem Manchester Utd, Liverpool, Chelsea, Arsenal, Man City.
        time_casa_exemplo = 'Man United'
        time_fora_exemplo = 'Liverpool'

        print(f"\nPrevisão para o jogo: {time_casa_exemplo} vs {time_fora_exemplo}")
        resultados = prever_resultado_poisson(df, time_casa_exemplo, time_fora_exemplo)

        print("\n--- Resultados da Previsão --- ")
        print(f"Probabilidade de Vitória do {time_casa_exemplo}: {resultados['Vitoria Casa']:.2%}")
        print(f"Probabilidade de Empate:                     {resultados['Empate']:.2%}")
        print(f"Probabilidade de Vitória do {time_fora_exemplo}:   {resultados['Vitoria Fora']:.2%}")
        print(f"Lambda esperado para gols do {time_casa_exemplo}: {resultados['Lambda Casa']:.2f}")
        print(f"Lambda esperado para gols do {time_fora_exemplo}: {resultados['Lambda Fora']:.2f}")

        # Opcional: Exibir a matriz de probabilidades (apenas para inspeção)
        # print("\nMatriz de Probabilidades de Placar:")
        # print(pd.DataFrame(resultados["Matriz de Probabilidades"],
        #                    index=[f'Gols {time_casa_exemplo} {i}' for i in range(resultados["Matriz de Probabilidades"].shape[0])],
        #                    columns=[f'Gols {time_fora_exemplo} {j}' for j in range(resultados["Matriz de Probabilidades"].shape[1])]))

    except ValueError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
