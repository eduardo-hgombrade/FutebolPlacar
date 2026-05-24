# app.py
from flask import Flask, render_template, request
import pandas as pd
from models.predictor import prever_resultado_poisson

app = Flask(__name__)

# Carregamos os dados de forma global na inicialização do servidor.
# Isso evita ler o CSV do disco a cada requisição, deixando o sistema muito mais rápido.
try:
    df_futebol = pd.read_csv('dados_tratados.csv')
    # Extraímos a lista de times únicos para preencher os 'selects' do HTML automaticamente
    times_disponiveis = sorted(list(set(df_futebol['HomeTeam'].unique()) | set(df_futebol['AwayTeam'].unique())))
except FileNotFoundError:
    df_futebol = pd.DataFrame()
    times_disponiveis = []
    print("Aviso: 'dados_tratados.csv' não encontrado. Certifique-se de gerá-lo primeiro.")

@app.route('/', methods=['GET', 'POST'])
def index():
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