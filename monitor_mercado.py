import streamlit as st
import pandas as pd
import random
import time

# Configuração da página
st.set_page_config(page_title="Monitor de Mercado - NQ, ES, VIX", layout="wide")

# Estilos CSS para manter o visual neon
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
    .vix-card { border-color: #ff4b4b; box-shadow: 0 0 20px rgba(255, 75, 75, 0.3); }
</style>
""", unsafe_allow_html=True)

st.title("MONITOR DE MERCADO EM TEMPO REAL")

# Função para gerar dados que simulam a realidade atual dos ativos
def gerar_dados_mercado():
    return {
        "NQ": random.randint(18000, 18500),      # Nasdaq 100 Futuro
        "ES": random.randint(5200, 5300),        # S&P 500 Futuro
        "VIX": round(random.uniform(12.0, 18.0), 2) # Índice de Medo (VIX)
    }

placeholder = st.empty()

while True:
    with placeholder.container():
        dados = gerar_dados_mercado()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'''<div class="card">
                <h3>NASDAQ (NQ)</h3>
                <h2 style="color: #00ff88;">{dados["NQ"]}</h2>
            </div>''', unsafe_allow_html=True)
            
        with col2:
            st.markdown(f'''<div class="card">
                <h3>S&P 500 (ES)</h3>
                <h2 style="color: #00ff88;">{dados["ES"]}</h2>
            </div>''', unsafe_allow_html=True)
            
        with col3:
            # O VIX geralmente é exibido em vermelho ou laranja por indicar risco
            st.markdown(f'''<div class="card vix-card">
                <h3>VIX (VOLATILIDADE)</h3>
                <h2 style="color: #ff4b4b;">{dados["VIX"]}</h2>
            </div>''', unsafe_allow_html=True)

    time.sleep(2)
