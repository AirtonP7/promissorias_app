import streamlit as st
from datetime import date, timedelta, datetime
from app.export.contrato_exporter import export_contrato_pdf
from app.core.utils import formatar_cpf, formatar_cnpj, format_currency
import time


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


def gerar_contrato_app():
    st.header("📜 Gerador de Contrato")
    st.subheader("Preencha os dados do contrato")

    with st.form("form_contrato"):
        # Dados do CREDOR
        st.markdown("### Dados do CREDOR")
        nome_empresa = st.text_input("Nome da Empresa (CREDOR)")
        cnpj_empresa = st.text_input(
            "CNPJ da Empresa",
            max_chars=14,
            placeholder="00.000.000/0000-00"
        )

        # Dados do DEVEDOR
        st.markdown("### Dados do DEVEDOR")
        nome_devedor = st.text_input("Nome do Devedor")
        cpf_cnpj_devedor = st.text_input(
            "CPF ou CNPJ do Devedor",
            max_chars=14,
            placeholder="000.000.000-00 ou 00.000.000/0000-00"
        )

        # Dados do empréstimo
        st.markdown("### Dados do Empréstimo")
        valor_total = st.number_input("Valor total do empréstimo (R$)", min_value=0.0, step=0.01)
        num_parcelas = st.number_input("Número de parcelas", min_value=1, step=1)
        data_primeira = st.date_input("Data da primeira parcela", value=date.today())
        intervalo = st.number_input("Intervalo entre parcelas (dias)", min_value=1, step=1)

        # Data do contrato
        data_contrato = st.date_input("Data do contrato", value=date.today())

        submitted = st.form_submit_button("Gerar Contrato")

    if submitted:
        # ---------------------------
        # Valida campos obrigatórios
        # ---------------------------
        if not all([nome_empresa, cnpj_empresa, nome_devedor, cpf_cnpj_devedor, valor_total, num_parcelas]):
            st.error("⚠️ Preencha todos os campos obrigatórios!")
            return

        # ---------------------------
        # Validação de CNPJ do CREDOR
        # ---------------------------
        cnpj_numeros = "".join(filter(str.isdigit, cnpj_empresa))
        if len(cnpj_numeros) != 14:
            st.error("❌ O CNPJ do CREDOR deve conter exatamente 14 números.")
            return

        # ---------------------------
        # Validação do DEVEDOR (CPF ou CNPJ)
        # ---------------------------
        devedor_numeros = "".join(filter(str.isdigit, cpf_cnpj_devedor))
        if len(devedor_numeros) == 11:
            cpf_cnpj_formatado = formatar_cpf(devedor_numeros)
        elif len(devedor_numeros) == 14:
            cpf_cnpj_formatado = formatar_cnpj(devedor_numeros)
        else:
            st.error("❌ O CPF do DEVEDOR deve ter 11 números ou o CNPJ 14 números.")
            return

        # ---------------------------
        # Formata CNPJ do CREDOR
        # ---------------------------
        cnpj_empresa_formatado = formatar_cnpj(cnpj_numeros)

        # ---------------------------
        # Calcula datas das parcelas
        # ---------------------------
        parcelas = []
        for i in range(int(num_parcelas)):
            vencimento = data_primeira + timedelta(days=i * int(intervalo))
            valor_parcela = valor_total / int(num_parcelas)
            parcelas.append({
                "numero": i + 1,
                "vencimento": vencimento.strftime("%d/%m/%Y"),
                "valor": valor_parcela
            })

        # ---------------------------
        # Monta dicionário para exportação
        # ---------------------------
        contrato_data = {
            "nome_empresa": nome_empresa,
            "cnpj_empresa": cnpj_empresa_formatado,
            "nome_devedor": nome_devedor,
            "cpf_devedor": cpf_cnpj_formatado,
            "valor_total": valor_total,
            "num_parcelas": int(num_parcelas),
            "parcelas": parcelas,
            "data_contrato": data_contrato.strftime("%d/%m/%Y"),
        }

        # ---------------------------
        # Exportar PDF
        # ---------------------------
        spinner_placeholder = st.empty()
        with spinner_placeholder.container():
            mostrar_spinner_css("⏳ Gerando PDF do Contrato...")
            agora = datetime.now().strftime("%d-%m-%Y_%H-%M")
            nome_arquivo = f"Contrato_{nome_devedor.replace(' ', '_')}_{agora}.pdf"
            pdf_path = export_contrato_pdf(contrato_data, filename=nome_arquivo)
            time.sleep(1)

        spinner_placeholder.empty()
        st.success(f"✅ PDF gerado com sucesso: {nome_arquivo}")

        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📥 Baixar Contrato PDF",
                data=pdf_file,
                file_name=nome_arquivo,
                mime="application/pdf"
            )
