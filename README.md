# FutebolPlacar
# Projeto RAD: Sistema de Análise de Dados de Futebol (ETL & Dashboards)

Este projeto foi desenvolvido como parte da disciplina de **Desenvolvimento Rápido de Aplicações (RAD) em Python**. O objetivo é demonstrar a integração entre coleta de dados via API, persistência em banco de dados relacional e visualização analítica através de interface web e Business Intelligence.

---

## ⚽ Tema do Projeto

**Análise de dados de uma API pública de Futebol (Placar, Ranking de times), integrada a um banco de dados e exibida em Power BI.**

O sistema realiza o consumo de dados esportivos em tempo real, processa essas informações em um ambiente Python e as disponibiliza tanto em uma interface web simplificada quanto em um dashboard analítico avançado para suporte à decisão e análise de desempenho de clubes.

---

## 📝 Justificativa do Tema

A escolha do tema "Futebol" deve-se à alta disponibilidade de dados dinâmicos e à complexidade inerente à atualização constante de tabelas e placares, o que representa um excelente cenário para o uso de metodologias RAD. 

**Finalidade e Benefícios:**
* **Acadêmico:** Aplicar conceitos de consumo de APIs REST, manipulação de bancos de dados SQL e desenvolvimento de interfaces web rápidas.
* **Portfólio:** Demonstra a capacidade do grupo de construir um pipeline de dados completo (ETL - Extração, Transformação e Carga).
* **Mercado de Trabalho:** Simula um cenário real de engenharia de dados, onde informações brutas são transformadas em insights visuais para o usuário final.

---

## 🎯 Objetivos do Projeto

1.  **Integração de Dados:** Consumir dados de uma API pública e persistir as informações relevantes em um banco de dados relacional.
2.  **Visualização Web:** Criar uma interface básica para consulta rápida de rankings e placares diretamente do banco de dados.
3.  **Análise de BI:** Exportar os dados tratados para o Power BI para a criação de gráficos de desempenho e tendências.
4.  **Automação:** Garantir que o fluxo entre a API e a interface seja fluido e de baixa manutenção.

---

## 👥 Divisão de Tarefas

A equipe distribuiu as responsabilidades de forma a cobrir todas as camadas da aplicação:

* **Eduardo:** Responsável pela **modelagem do banco de dados** e a lógica de integração/persistência com Python.
* **Pedro:** Responsável pelo **consumo da API pública** e scripts de tratamento de dados (limpeza e normalização).
* **Vinícius:** Responsável pelo desenvolvimento da **interface web** utilizando Flask (HTML/CSS).
* **Rafael:** Responsável pela **integração com Power BI**, extração de dados e criação dos dashboards analíticos.
* **Luana:** Responsável pela **documentação técnica**, organização do repositório Git e revisão final do código.

---

## 🛠 Ambiente e Tecnologias

* **Linguagem:** [Python 3.10+](https://www.python.org/)
* **Framework Web:** [Flask](https://flask.palletsprojects.com/) (Back-end leve e rápido).
* **Banco de Dados:** [SQLite](https://www.sqlite.org/index.html) (Embutido, dispensa instalação de servidor complexo).
* **Front-end:** HTML5 e CSS3 (Opcionalmente utilizando Bootstrap para agilidade).
* **Visualização:** Power BI Desktop.
* **IDE Sugerida:** Visual Studio Code (VS Code).

---

## 🔄 Fluxo de Informações

O projeto segue o seguinte fluxo de dados:

1.  **Extração:** O script Python (executado por Pedro) faz uma requisição `GET` para a API de futebol e recebe um arquivo JSON.
2.  **Carga (Load):** O módulo de integração (desenvolvido por Eduardo) lê o JSON, filtra os dados necessários e os insere no banco de dados SQLite.
3.  **Exposição Web:** O servidor Flask (Vinícius) consulta o banco de dados e renderiza as informações em tabelas HTML para o usuário.
4.  **Análise BI:** O Power BI (Rafael) conecta-se ao banco de dados SQLite ou consome um export `CSV/JSON` gerado pelo Python para montar os gráficos de desempenho.

---

## 📂 Estrutura de Pastas Sugerida

```text
/projeto-rad
├── /api
│   └── api_consumer.py    # Script de conexão com a API
├── /database
│   ├── schema.sql         # Script de criação das tabelas
│   └── futebol.db         # Arquivo do banco de dados SQLite
├── /web
│   ├── /static            # Arquivos CSS e Imagens
│   ├── /templates         # Arquivos HTML (index.html, etc)
│   └── app.py             # Servidor Flask
├── /powerbi
│   └── dashboard_futebol.pbix # Arquivo do Power BI
├── requirements.txt       # Bibliotecas necessárias (pip install)
└── main.py                # Ponto de entrada para atualizar os dados
