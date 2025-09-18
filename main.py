import streamlit as st
import os
from app.generator.promissorias_app import gerar_promissoria_app
from app.generator.contrato_app import gerar_contrato_app
from app.falar_desenvolvedor.contato_dev import render

# ===============================
# Configuração da Página
# ===============================
st.set_page_config(
    page_title="GrupoMax | Gerador de Documentos",
    page_icon="app/assets/images/dh.png",
    layout="wide"
)

# ===============================
# CSS Customizado
# ===============================
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #1E1E2F;
    padding: 20px 15px;
}
.sidebar-title {
    color: #FFFFFF;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 5px;
}
.sidebar-subtitle {
    color: #A0A0B2;
    text-align: center;
    font-size: 14px;
    margin-bottom: 20px;
}
div[role="radiogroup"] > label {
    background-color: #2B2B40;
    color: #FFFFFF !important;
    border-radius: 10px;
    padding: 10px 15px;
    margin: 5px 0;
    transition: all 0.3s ease-in-out;
    border: 1px solid #3C3C55;
}
div[role="radiogroup"] > label:hover {
    background-color: #3A3A55;
    border: 1px solid #5A5A7A;
}
div[role="radiogroup"] > label[data-selected="true"] {
    background-color: #6C63FF !important;
    border: 1px solid #857CFF;
    color: #FFFFFF !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# Função Sidebar Menu
# ===============================
def sidebar_menu():
    logo1_path = os.path.join("app", "assets", "images", "logo.png")
    logo2_path = os.path.join("app", "assets", "images", "dh.png")

    col1, col2 = st.columns(2)
    with col1:
        st.image(logo1_path, width=100)
    with col2:
        st.image(logo2_path, width=100)

    st.markdown("""
        <div style="margin-top: 30px; text-align: center;">
            <div class="sidebar-title">DH | GrupoMax</div>
            <div class="sidebar-subtitle">
                Sistema de Geração de Promissórias e Contrato Particular
            </div>
        </div>
        <hr style="margin-top:15px; margin-bottom:10px; border:0px solid #444;">
    """, unsafe_allow_html=True)

    st.markdown("---")

    menu = st.radio(
        "",
        ["📜 Gerar Promissória", "📑 Gerar Contrato", "👨🏽‍💻 Falar com Desenvolvedor"],
        label_visibility="collapsed"
    )
    return menu

# ===============================
# Roteamento Principal
# ===============================
with st.sidebar:
    menu = sidebar_menu()

if menu == "📜 Gerar Promissória":
    gerar_promissoria_app()

elif menu == "📑 Gerar Contrato":
    gerar_contrato_app() 

elif menu == "👨🏽‍💻 Falar com Desenvolvedor":
    render()


st.sidebar.markdown("---", unsafe_allow_html=True)

st.sidebar.markdown("""
    <div style="text-align: center; margin-top: 10px; color: #aaa;">
        <div style="font-size:16px; font-weight:bold;">v1.0.0</div>
        <div style="font-size:17px;">Airton Pereira © 2025</div>
    </div>
""", unsafe_allow_html=True)
