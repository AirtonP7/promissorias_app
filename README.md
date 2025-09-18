# 📄💰 Gerador de Promissórias & Contratos

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-app-red?logo=streamlit)
![Status](https://img.shields.io/badge/Status-Em%20produção-success)
![Último commit](https://img.shields.io/github/last-commit/AirtonP7/agendamento_rescisao)



## ✨ Visão Geral

O **Gerador de Promissórias & Contratos** é uma aplicação profissional feita em **Python + Streamlit** que automatiza a criação de promissórias parceladas e contratos personalizados em PDF.
Com ele, você economiza **tempo**, gera documentos **confiáveis** e apresenta para clientes de forma **premium** e **estilizada**.

---

## 🎯 Funcionalidades

✔️ Formulário interativo com validação automática.
✔️ Geração de promissórias em PDF com design profissional.
✔️ CNPJ (corpo) e CPF (rodapé) tratados de forma independente
✔️ Valores por extenso em português.
✔️ Mascaras de CPF e CNPJ.
✔️ Limites de caracteres.
✔️ Numeração automática das parcelas.
✔️ Inserção de **logos personalizadas** no documento
✔️ Nome de arquivo dinâmico:
✔️ Overlay animado de carregamento ao gerar PDFs.
✔️ Exportação de contrato com tabela de vencimentos.
✔️ Compatível com **Render, Heroku, Docker ou local**
✔️ **Download imediato** do arquivo PDF
✔️ Pré-visualização interativa antes da exportação

---

## 🖼️ Interface

Abaixo estão os principais painéis da interface do sistema:

### 💰 Gerar Promissorias
![Painel | Gerar Promissorias](assets/images/PAINEL_GERAR_PROMISSORIA.png)

### 📜 Gerar Contrato
![Painel | Gerar Contrato](assets/images/PAINEL_GERAR_CONTRATO.png)

### 👨🏾‍💻 Contato com o Desenvolvedor
![Painel| Falar com o Desenvolvedor](assets/images/PAINEL_FALAR_COM_DESENVOLVEDOR.png)

### ✉ Promissoria
![Promissoria](assets/images/PROMISSORIA_GERADA.png)

### 📑 Contrato
![ContratoE](assets/images/CONTRATO_GERADO.png)


---


## 🏗️ Estrutura do Projeto

## 🗂 Estrutura do Projeto

```bash
promissorias_app/
    ├── .streamlit/
    │   └── config.toml
│── main.py
│── estrutura.txt
│── README.md
│── requirements.txt
│
└── app/
    ├── assets/
    │   ├── images/
    │   │   ├── CONTRATO_GERADO.png
    │   │   ├── dh.png
    │   │   ├── logo.png
    │   │   ├── PAINEL_FALAR_COM_DESENVOLVEDOR.png
    │   │   ├── PAINEL_GERAR_CONTRATO.png
    │   │   ├── PAINEL_GERAR_PROMISSORIA.png
    │   │   └── PROMISSORIA_GERADA.png
    │   │
    │   └── templates/
    │       ├── contrato.txt
    │       └── promissoria.txt
    │
    ├── core/
    │   ├── generator.py
    │   ├── number_to_words.py
    │   ├── parser.py
    │   ├── utils.py
    │
    ├── export/
    │   ├── contrato_exporter.py
    │   ├── pdf_exporter.py
    │
    ├── falar_desenvolvedor/
    │   ├── contato_dev.py
    │
    ├── generator/
    │   ├── contrato_app.py
    │   ├── promissorias_app.py
    │
    └── utils/
        ├── email_utils.py

## ⚙️ Tecnologias Utilizadas
- [🐍 Python 3.11+](https://www.python.org/) – Linguagem principal do projeto
- [🎨 Streamlit](https://streamlit.io/) – Criação da interface web interativa
- [📑 ReportLab](https://www.reportlab.com/dev/) – Geração e estilização dos PDFs
- [🔢 Num2Words](https://pypi.org/project/num2words/) – Conversão de números para texto por extenso
- [🛠️ Custom Utils](app/core/utils.py) – Funções auxiliares (formatação de CPF, CNPJ e valores monetários)

---

## 📦 Instalação Local

### 1. Clonar o repositório
git clone https://github.com/SEU_USUARIO/promissoria_app.git
cd promissoria_app
2. Criar ambiente virtual
Copiar código
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
3. Instalar dependências
Copiar código
pip install -r requirements.txt
4. Configurar variáveis de ambiente
Crie um arquivo .env na raiz (baseado em .env.example) com:


5. Rodar aplicação localmente
Copiar código
streamlit run main.py
O sistema abrirá em http://localhost:8501.

### ☁️ Deploy no Streamlit Cloud

1. Faça push do projeto para o **GitHub**.
2. Acesse [Streamlit Cloud](https://streamlit.io/cloud) e faça login.
3. Clique em **New app**.
4. Conecte o repositório do GitHub onde está o projeto.
5. Configure:
   - **Main file path**: `main.py` (ou o nome do seu arquivo principal)
   - **Python version**: 3.11
   - **Requirements file**: `requirements.txt`
6. Clique em **Deploy** 🎉
7. Após alguns minutos, seu app estará disponível em uma URL no formato: 
    https://<seu-usuario>-<nome-do-projeto>.streamlit.app



🧑🏽‍💻 Desenvolvedor
Airton Pereira
📩 airtonpereiradev@gmail.com
💼 GitHub: AirtonP7

📌 Licença
Este projeto tem todos os direitos reservados ao desenvolvedor Airton Pereira.
Não é permitido uso ou redistribuição sem autorização prévia.
