# FutebolPlacar
# Sistema de Previsão de Resultados de Futebol

## 1. Identificação do Projeto
* **Nome do Projeto:** Sistema de Previsão de Resultados de Futebol
* **Responsável:** Eduardo
* **Instituição:** Unimetrocamp Wyden
* **Matéria:** Desenvolvimento Rápido de Aplicações em Python
* **Professor:** Mauro Rodrigues Alves Nogueira
* **Integrantes do Grupo:** Eduardo, Pedro, Vinícius, Rafael, Luana
* **Versão do Documento:** 1.0

---

## 2. Descrição do Projeto
O projeto consiste no desenvolvimento de um software capaz de calcular probabilidades de vitória entre dois clubes de futebol. A aplicação utiliza dados históricos provenientes de arquivos CSV contendo resultados de partidas da Premier League ao longo de várias temporadas.

Com base nesses dados, é aplicado um modelo de cálculo que permite ao usuário selecionar dois times e obter uma previsão estatística de qual equipe possui maior probabilidade de vencer. Futuramente, o sistema integrará técnicas de Machine Learning para aprimorar a precisão das análises de forma automática.

---

## 3. Objetivo Geral
Desenvolver um sistema inteligente e funcional capaz de prever probabilidades de resultados de partidas de futebol com base em processamento de dados históricos e variáveis estatísticas.

---

## 4. Objetivos Específicos
* Permitir a seleção de dois clubes para comparação direta.
* Processar dados históricos de partidas extraídos de arquivos CSV.
* Calcular probabilidades de vitória com base em métricas como gols e desempenho.
* Exibir os resultados de forma clara e intuitiva ao usuário.
* Integrar dados estatísticos como chutes e posse de bola.
* Implementar modelos de Machine Learning para refinamento das previsões.

---

## 5. Justificativa
A análise de dados esportivos é uma área em constante crescimento, sendo essencial para analistas e entusiastas. O sistema busca fornecer uma ferramenta automatizada que auxilie na previsão de resultados com base em dados reais, utilizando inteligência artificial para permitir o aprendizado contínuo conforme novos dados são inseridos.

---

## 6. Escopo do Projeto

### 6.1 O que está incluído
* Leitura e processamento de dados em formato CSV.
* Interface web para seleção de times e exibição de resultados.
* Algoritmo de cálculo de probabilidades e uso de estatísticas.
* Implementação inicial de modelo de Machine Learning.
* Sistema adaptável para inserção de novos dados.

### 6.2 O que não está incluído
* Previsões em tempo real com dados de partidas ao vivo.
* Integração com sistemas de casas de apostas.
* Cobertura de ligas mundiais além da Premier League nesta fase inicial.
* Versão de aplicativo mobile (foco exclusivo em plataforma Web).

---

## 7. Entregas (Deliverables)
* Sistema funcional (Aplicação Web).
* Base de dados integrada via CSV.
* Algoritmo de cálculo de probabilidade estruturado.
* Interface de usuário (Front-end).
* Documentação técnica do sistema.
* Protótipo de modelo de Machine Learning.

---

## 8. Requisitos

### 8.1 Requisitos Funcionais
* O sistema deve permitir a seleção de dois clubes para o confronto.
* O sistema deve calcular a probabilidade de vitória de cada equipe.
* O sistema deve exibir os resultados na interface web.
* O sistema deve carregar os dados a partir de arquivos CSV pré-definidos.

### 8.2 Requisitos Não Funcionais
* Interface de usuário simples e de fácil navegação.
* Processamento rápido dos cálculos estatísticos.
* Sistema confiável e com validação de dados de entrada.
* Escalabilidade para suportar futuras ligas de futebol.

---

## 9. Stakeholders (Partes Interessadas)
* Usuários finais (torcedores, estudantes e analistas).
* Desenvolvedores do projeto.
* Instituição de ensino Unimetrocamp Wyden.

---

## 10. Cronograma (Macro)

| Etapa | Descrição |
| :--- | :--- |
| **Planejamento** | Definição do escopo e arquitetura do projeto. |
| **Desenvolvimento** | Criação do backend, processamento CSV e interface. |
| **Testes** | Validação das probabilidades e estabilidade do sistema. |
| **Entrega** | Apresentação final e disponibilização da documentação. |

---

## 11. Restrições
* Limitação de tempo para o desenvolvimento dentro do período letivo.
* Conhecimento técnico da equipe em algoritmos preditivos avançados.
* Dependência da disponibilidade e integridade dos dados contidos nos arquivos CSV.

---

## 12. Critérios de Aceitação
* O sistema deve realizar os cálculos de probabilidade sem erros de execução.
* A interface deve ser funcional e apresentar os resultados de forma legível.
* O modelo de Machine Learning deve demonstrar capacidade de evolução na precisão.

---

## 13. Divisão de Tarefas
* **Eduardo:** Modelagem do banco de dados SQLite e integração com Python.
* **Pedro:** Processamento de arquivos CSV e lógica do cálculo de probabilidade.
* **Vinícius:** Desenvolvimento da interface web (HTML/CSS) e rotas Flask.
* **Rafael:** Integração com Power BI e criação dos dashboards analíticos.
* **Luana:** Documentação técnica, prototipagem de Machine Learning e organização do repositório.

---

## 14. Ambiente e Tecnologias
* **Linguagem:** Python 3.10+
* **Framework Web:** Flask ou FastAPI.
* **Manipulação de Dados:** Pandas / NumPy.
* **Banco de Dados:** SQLite.
* **Visualização:** Power BI Desktop.
* **IDE:** VS Code.
