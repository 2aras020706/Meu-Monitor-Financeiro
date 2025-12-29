import streamlit as st
import pandas as pd
import random
import time

# Configuração da página
st.set_page_config(page_title="Monitor de Mercado Simulado", layout="wide")

# --- DESIGN DOS CARDS (CSS) ---
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
    .symbol { font-size: 24px; font-weight: bold; color: #ffffff; }
    .price { font-size: 32px; font-weight: bold; color: #00ff00; }
    h1 { color: white; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>MONITOR DE MERCADO</h1>", unsafe_allow_html=True)

# 1. Função para gerar os dados
def gerar_dados_simulados():
    return {
        "VIX": random.uniform(15, 25),
        "ES": random.uniform(4000, 5000),
        "NQ": random.uniform(15000, 16000)
    }

# 2. Criar o placeholder (espaço vazio que será atualizado)
placeholder = st.empty()

# 3. Loop de atualização em tempo real
while True:
    dados = gerar_dados_simulados()
    
    with placeholder.container():
        # Criamos 3 colunas para os cards ficarem lado a lado
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="symbol">VIX</div>
                <div class="price">{dados['VIX']:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="card">
                <div class="symbol">ES (S&P 500)</div>
                <div class="price">{dados['ES']:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="card">
                <div class="symbol">NQ (NASDAQ)</div>
                <div class="price">{dados['NQ']:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
            
    # Espera 2 segundos antes de rodar o loop de novo
    time.sleep(2)
