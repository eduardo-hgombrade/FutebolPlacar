# setup_db.py
import sqlite3
import pandas as pd
import os

# Cria a pasta database se ela não existir
if not os.path.exists('database'):
    os.makedirs('database')

print("Lendo o arquivo CSV...")
# Lê o CSV que vocês geraram na Etapa 2
df = pd.read_csv('dados_tratados.csv')

print("Criando o banco de dados SQLite...")
# Conecta (ou cria) o arquivo do banco de dados dentro da pasta database
conn = sqlite3.connect('database/futebolplacar.db')

# Salva o DataFrame inteiro como uma tabela chamada 'partidas'
# if_exists='replace' garante que se rodarmos de novo, ele atualiza a tabela
df.to_sql('partidas', conn, if_exists='replace', index=False)

# Fecha a conexão
conn.close()

print("✅ Banco de dados 'futebolplacar.db' criado com sucesso na pasta 'database'!")