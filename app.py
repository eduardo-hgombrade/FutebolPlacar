# app.py
from flask import Flask, render_template, request
import pandas as pd
import sqlite3 # <-- Nova importação
from models.predictor import prever_resultado_poisson

app = Flask(__name__)

# --- NOVA INTEGRAÇÃO COM O BANCO DE DADOS SQLITE ---
try:
    # 1. Abre a conexão com o banco de dados
    conn = sqlite3.connect('database/futebolplacar.db', check_same_thread=False)
    
    # 2. Faz uma Query SQL para puxar os dados usando o pandas
    df_futebol = pd.read_sql_query('SELECT * FROM partidas', conn)
    
    # 3. Extrai a lista de times únicos para o HTML
    times_disponiveis = sorted(list(set(df_futebol['HomeTeam'].unique()) | set(df_futebol['AwayTeam'].unique())))
    
    # 4. Fecha a conexão
    conn.close()
    
except sqlite3.OperationalError:
    df_futebol = pd.DataFrame()
    times_disponiveis = []
    print("Aviso: Banco de dados não encontrado. Rode o script setup_db.py primeiro.")
# ---------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
def index():
# ... (O restante do seu código da rota continua exatamente igual)
    """
    Rota principal. Se for GET, apenas mostra a tela. 
    Se for POST, o usuário enviou o formulário e calculamos a previsão.
    """
    resultado = None
    erro = None
    time_casa_selecionado = ""
    time_fora_selecionado = ""

    if request.method == 'POST':
        # Captura os times que o usuário escolheu no Front-end
        time_casa_selecionado = request.form.get('time_casa')
        time_fora_selecionado = request.form.get('time_fora')

        if time_casa_selecionado == time_fora_selecionado:
            erro = "Por favor, selecione times diferentes para o confronto."
        else:
            # Chama a inteligência do nosso sistema
            resultado = prever_resultado_poisson(df_futebol, time_casa_selecionado, time_fora_selecionado)
            
            if 'erro' in resultado:
                erro = resultado['erro']
                resultado = None

    # O render_template envia todas essas variáveis para o nosso arquivo HTML
    return render_template('index.html', 
                           times=times_disponiveis, 
                           resultado=resultado, 
                           erro=erro,
                           time_casa=time_casa_selecionado,
                           time_fora=time_fora_selecionado)

if __name__ == '__main__':
    # Rodamos o servidor no modo debug para facilitar o desenvolvimento
    app.run(debug=True)