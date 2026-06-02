# setup_db.py
import sqlite3
import pandas as pd
import os

# Cria a pasta database se ela não existir
if not os.path.exists('database'):
    os.makedirs('database')

print("Lendo o arquivo CSV...")
df = pd.read_csv('dados_tratados.csv')

print("Criando o banco de dados SQLite...")
conn = sqlite3.connect('database/futebolplacar.db')

# Salva o histórico de partidas (igual ao original do grupo)
df.to_sql('partidas', conn, if_exists='replace', index=False)

# --- NOVO: tabela para salvar as previsões geradas ---
conn.execute('''
    CREATE TABLE IF NOT EXISTS previsoes (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        data_hora   TEXT    DEFAULT (datetime('now')),
        time_casa   TEXT    NOT NULL,
        time_fora   TEXT    NOT NULL,
        gols_casa   REAL    NOT NULL,
        gols_fora   REAL    NOT NULL,
        placar      TEXT    NOT NULL,
        prob_casa   REAL,
        prob_empate REAL,
        prob_fora   REAL
    )
''')
# -----------------------------------------------------

conn.commit()
conn.close()

print("✅ Banco de dados 'futebolplacar.db' criado com sucesso na pasta 'database'!")
print("   Tabelas criadas: 'partidas' e 'previsoes'")