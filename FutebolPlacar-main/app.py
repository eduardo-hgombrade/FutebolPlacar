# app.py
from flask import Flask, render_template, request, jsonify
import pandas as pd
import sqlite3
from models.predictor import prever_resultado_poisson

app = Flask(__name__)

# --- CARREGA O BANCO DE DADOS (igual ao original) ---
try:
    conn = sqlite3.connect('database/futebolplacar.db', check_same_thread=False)
    df_futebol = pd.read_sql_query('SELECT * FROM partidas', conn)
    times_disponiveis = sorted(list(
        set(df_futebol['HomeTeam'].unique()) | set(df_futebol['AwayTeam'].unique())
    ))
    conn.close()
except sqlite3.OperationalError:
    df_futebol = pd.DataFrame()
    times_disponiveis = []
    print("Aviso: Banco de dados não encontrado. Rode o script setup_db.py primeiro.")


# --- ROTA PRINCIPAL (igual ao original) ---
@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    erro = None
    time_casa_selecionado = ""
    time_fora_selecionado = ""

    if request.method == 'POST':
        time_casa_selecionado = request.form.get('time_casa')
        time_fora_selecionado = request.form.get('time_fora')

        if time_casa_selecionado == time_fora_selecionado:
            erro = "Por favor, selecione times diferentes para o confronto."
        else:
            resultado = prever_resultado_poisson(df_futebol, time_casa_selecionado, time_fora_selecionado)

            if 'erro' in resultado:
                erro = resultado['erro']
                resultado = None

    return render_template('index.html',
                           times=times_disponiveis,
                           resultado=resultado,
                           erro=erro,
                           time_casa=time_casa_selecionado,
                           time_fora=time_fora_selecionado)


# --- ROTA DE ESTATÍSTICAS POR TIME (nova) ---
@app.route('/estatisticas', methods=['GET', 'POST'])
def estatisticas():
    time_selecionado = None
    stats = None
    ultimos_jogos = []

    if request.method == 'POST':
        time_selecionado = request.form.get('time')

        if time_selecionado:
            # Jogos como mandante e visitante
            casa = df_futebol[df_futebol['HomeTeam'] == time_selecionado]
            fora = df_futebol[df_futebol['AwayTeam'] == time_selecionado]

            jogos    = len(casa) + len(fora)
            vitorias = len(casa[casa['FTHG'] > casa['FTAG']]) + len(fora[fora['FTAG'] > fora['FTHG']])
            empates  = len(casa[casa['FTHG'] == casa['FTAG']]) + len(fora[fora['FTAG'] == fora['FTHG']])
            derrotas = len(casa[casa['FTHG'] < casa['FTAG']]) + len(fora[fora['FTAG'] < fora['FTHG']])

            gols_marcados = int(casa['FTHG'].sum()) + int(fora['FTAG'].sum())
            gols_sofridos = int(casa['FTAG'].sum()) + int(fora['FTHG'].sum())
            pontos        = (vitorias * 3) + empates
            aproveitamento = round((pontos / (jogos * 3)) * 100, 1) if jogos > 0 else 0

            stats = {
                'jogos':          jogos,
                'vitorias':       vitorias,
                'empates':        empates,
                'derrotas':       derrotas,
                'gols_marcados':  gols_marcados,
                'gols_sofridos':  gols_sofridos,
                'saldo_gols':     gols_marcados - gols_sofridos,
                'pontos':         pontos,
                'aproveitamento': aproveitamento,
            }

            # Últimos 5 jogos do time
            jogos_casa = df_futebol[df_futebol['HomeTeam'] == time_selecionado][['Date','HomeTeam','AwayTeam','FTHG','FTAG']].copy()
            jogos_fora = df_futebol[df_futebol['AwayTeam'] == time_selecionado][['Date','HomeTeam','AwayTeam','FTHG','FTAG']].copy()
            todos = pd.concat([jogos_casa, jogos_fora]).sort_values('Date', ascending=False).head(5)

            for _, row in todos.iterrows():
                if row['HomeTeam'] == time_selecionado:
                    res = 'V' if row['FTHG'] > row['FTAG'] else ('E' if row['FTHG'] == row['FTAG'] else 'D')
                else:
                    res = 'V' if row['FTAG'] > row['FTHG'] else ('E' if row['FTAG'] == row['FTHG'] else 'D')

                ultimos_jogos.append({
                    'data':      row['Date'],
                    'mandante':  row['HomeTeam'],
                    'visitante': row['AwayTeam'],
                    'placar':    f"{int(row['FTHG'])} x {int(row['FTAG'])}",
                    'resultado': res,
                })

    return render_template('estatisticas.html',
                           times=times_disponiveis,
                           time_selecionado=time_selecionado,
                           stats=stats,
                           ultimos_jogos=ultimos_jogos)


# --- API PARA O POWER BI (igual ao original) ---
@app.route('/api/estatisticas', methods=['GET'])
def api_estatisticas():
    try:
        conn = sqlite3.connect('database/futebolplacar.db', check_same_thread=False)
        df_api = pd.read_sql_query('SELECT * FROM partidas', conn)
        conn.close()
        return jsonify(df_api.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"erro": f"Erro na base de dados: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)