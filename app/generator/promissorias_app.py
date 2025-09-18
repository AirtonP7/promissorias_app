import streamlit as st
from datetime import date, datetime
from app.core.generator import gerar_promissorias
from app.export.pdf_exporter import export_promissorias_pdf
from app.core.utils import formatar_cpf, formatar_cnpj, format_currency
import time

# ---------------------------
# Funções auxiliares
# ---------------------------
#def formatar_cnpj(cnpj: str) -> str:
    #numeros = "".join(filter(str.isdigit, cnpj))
    #if len(numeros) != 14:
        #return cnpj
    #return f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}/{numeros[8:12]}-{numeros[12:]}"

#def formatar_cpf(cpf: str) -> str:
    #numeros = "".join(filter(str.isdigit, cpf))
    #if len(numeros) != 11:
        #return cpf
    #return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"

# ---------------------------
# Limpar campos do formulário
# ---------------------------
def limpar_formulario():
    for key in ["nome_devedor", "valor_total", "num_parcelas", "data_primeira", "intervalo",
                "nome_empresa", "cnpj_empresa", "cpf_emitente"]:
        if key in st.session_state:
            del st.session_state[key]

# ---------------------------
# Função para exibir spinner CSS
# ---------------------------
def mostrar_spinner_css(legenda="Gerando PDF..."):
    st.markdown(
        f"""
        <style>
        .overlay {{
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(255,255,255,0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            flex-direction: column;
        }}
        .loader {{
            border: 8px solid #f3f3f3;
            border-top: 8px solid #0E5A31;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            animation: spin 1s linear infinite;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        .spinner-text {{
            margin-top: 15px;
            font-size: 18px;
            font-weight: bold;
            color: #0E5A31;
        }}
        </style>
        <div class="overlay">
            <div class="loader"></div>
            <div class="spinner-text">{legenda}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------
# Função principal do app
# ---------------------------
def gerar_promissoria_app():
    st.header("📄 Gerador de Promissórias")
    st.subheader("Preencha os dados para gerar suas promissórias")

    with st.form("form_promissoria"):
        # Campos com session_state para permitir limpar
        nome_devedor = st.text_input("Nome do Devedor", key="nome_devedor")
        valor_total = st.number_input("Valor total da dívida (R$)", min_value=0.0, step=0.01, key="valor_total")
        num_parcelas = st.number_input("Número de parcelas", min_value=1, step=1, key="num_parcelas")
        data_primeira = st.date_input("Data da 1ª parcela", value=date.today(), key="data_primeira")
        intervalo = st.number_input("Intervalo entre parcelas (dias)", min_value=1, step=1, key="intervalo")

        st.header("Dados da Empresa / Beneficiário")
        nome_empresa = st.text_input("Nome da Empresa Credora / Beneficiário", key="nome_empresa")
        cnpj_empresa = st.text_input("CNPJ da Empresa Credora / Beneficiário", key="cnpj_empresa", max_chars=14, placeholder="00.000.000/0000-00")
        cpf_emitente = st.text_input("CPF do Emitente", key="cpf_emitente", max_chars=11, placeholder="000.000.000-00")

        col1, col2 = st.columns([1,1])
        with col1:
            submitted = st.form_submit_button("Gerar Promissórias")
        #with col2:
            #limpar = st.form_submit_button("Limpar Dados")

    #if limpar:
        #limpar_formulario()
        #st.rerun()

    #TRATAMENTO
    if submitted:
        if not all([nome_devedor, nome_empresa, cnpj_empresa, cpf_emitente]):
            st.error("⚠️ Preencha todos os campos obrigatórios!")
            return

        # ---------------------------
        # Validação de CPF e CNPJ
        # ---------------------------
        cnpj_numeros = "".join(filter(str.isdigit, cnpj_empresa))
        cpf_numeros = "".join(filter(str.isdigit, cpf_emitente))

        if len(cnpj_numeros) != 14:
            st.error("❌ O CNPJ deve conter exatamente 14 números.")
            return

        if len(cpf_numeros) != 11:
            st.error("❌ O CPF deve conter exatamente 11 números.")
            return

        # ---------------------------
        # Formatar CNPJ e CPF
        # ---------------------------
        cnpj_empresa_formatado = formatar_cnpj(cnpj_numeros)
        cpf_emitente_formatado = formatar_cpf(cpf_numeros)

        # Carregar template base
        with open("app/assets/templates/promissoria.txt", "r", encoding="utf-8") as f:
            modelo_texto = f.read()

        modelo_texto = modelo_texto.replace("{nome_empresa}", nome_empresa)
        modelo_texto = modelo_texto.replace("{cnpj_empresa}", cnpj_empresa_formatado)
        modelo_texto = modelo_texto.replace("{cpf_emitente}", cpf_emitente_formatado)

        # --- Gerar promissórias ---
        promissorias = gerar_promissorias(
            nome_devedor=nome_devedor,
            valor_total=valor_total,
            num_parcelas=num_parcelas,
            data_primeira=data_primeira,
            intervalo=intervalo,
            nome_beneficiario=nome_empresa,
            cnpj_empresa=cnpj_empresa_formatado,    # corpo
            cpf_emitente=cpf_emitente_formatado,    # rodapé
            modelo_texto=modelo_texto
        )


        # --- Gerar nome dinâmico do PDF ---
        agora = datetime.now()
        data_hora = agora.strftime("%d-%m-%Y_%H-%M")
        nome_arquivo = f"Promissoria_{nome_devedor.replace(' ', '_')}_{data_hora}.pdf"

        # --- Exportar PDF estilizado com spinner ---
        logo_path = "app/assets/images/logo.png"

        # Exibir overlay spinner CSS
        spinner_placeholder = st.empty()
        with spinner_placeholder.container():
            mostrar_spinner_css("⏳ Gerando PDF das promissórias...")
            pdf_path = export_promissorias_pdf(promissorias, filename=nome_arquivo, logo_path=logo_path)
            time.sleep(1)  # garante que o spinner apareça

        # Remove spinner e mostra sucesso
        spinner_placeholder.empty()
        st.success(f"✅ PDF gerado com sucesso: {nome_arquivo}")

        # Botão de download
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📥 Baixar PDF",
                data=pdf_file,
                file_name=nome_arquivo,
                mime="application/pdf"
            )    

            

