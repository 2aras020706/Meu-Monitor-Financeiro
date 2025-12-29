import streamlit as st
import pandas as pd
import random
import time

# Configuração da página
st.set_page_config(page_title="Monitor de Mercado Simulado", layout="wide")

# Estilos CSS
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    .card {
        background-color: #1a1a1a;
        border: 2px solid #5a189a;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 0 20px rgba(90, 24, 154, 0.5);
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("MONITOR DE MERCADO")

# Função para gerar dados simulados
def gerar_dados_simulados():
    return {
        "WIN": random.randint(110000, 120000),
        "ESI": round(random.uniform(5.0, 5.5), 2),
        "NQI": random.randint(15000, 16000)
    }

# 1. Crie o espaço vazio FORA do loop
placeholder = st.empty()

# 2. Inicie o loop de atualização
while True:
    with placeholder.container():
        dados = gerar_dados_simulados()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'<div class="card"><h3>WIN (Ibovespa)</h3><h2>{dados["WIN"]}</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="card"><h3>ESI (Dólar)</h3><h2>R$ {dados["ESI"]}</h2></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="card"><h3>NQI (Nasdaq)</h3><h2>{dados["NQI"]}</h2></div>', unsafe_allow_html=True)

    # Tempo de espera para a próxima atualização (2 segundos)
    time.sleep(2)
