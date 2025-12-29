import streamlit as st
import pandas as pd
import random
import time

# Configuração da página
st.set_page_config(page_title="Monitor de Mercado Pro", layout="wide")

# Estilos CSS Avançados
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    .card {
        background-color: #1a1a1a;
        border: 2px solid #5a189a;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        color: white;
        text-align: center;
    }
    .metric-value { font-size: 24px; font-weight: bold; color: #00ff88; }
    .pressure-bar {
        background: linear-gradient(90deg, #ff4b4b 0%, #4b4bff 100%);
        height: 20px; border-radius: 10px; margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def gerar_dados():
    return {
        "WIN": random.randint(110000, 120000),
        "ESI": round(random.uniform(5.0, 5.5), 2),
        "NQI": random.randint(15000, 16000),
        "NQ": random.randint(18000, 18500),
        "ES": random.randint(5200, 5300),
        "VIX": round(random.uniform(12.0, 25.0), 2),
        "PRESSAO": random.randint(0, 100),
        "TENDENCIA": random.choice(["ALTA", "BAIXA", "LATERAL"])
    }

st.title("📊 MONITOR DE MERCADO COMPLETO")

placeholder = st.empty()

while True:
    with placeholder.container():
        d = gerar_dados()
        
        # Linha 1: Ativos Originais
        col1, col2, col3 = st.columns(3)
        col1.markdown(f'<div class="card">WIN<br><span class="metric-value">{d["WIN"]}</span></div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="card">ESI<br><span class="metric-value">R$ {d["ESI"]}</span></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="card">NQI<br><span class="metric-value">{d["NQI"]}</span></div>', unsafe_allow_html=True)

        # Linha 2: Novos Ativos (NQ, ES, VIX)
        col4, col5, col6 = st.columns(3)
        col4.markdown(f'<div class="card">NASDAQ (NQ)<br><span class="metric-value">{d["NQ"]}</span></div>', unsafe_allow_html=True)
        col5.markdown(f'<div class="card">S&P 500 (ES)<br><span class="metric-value">{d["ES"]}</span></div>', unsafe_allow_html=True)
        col6.markdown(f'<div class="card" style="border-color: #ff4b4b;">VIX<br><span class="metric-value" style="color: #ff4b4b;">{d["VIX"]}</span></div>', unsafe_allow_html=True)

        # Linha 3: Pressão e Tendência
        c_pres, c_tend = st.columns([2, 1])
        with c_pres:
            st.markdown(f'<div class="card">MEDIDOR DE PRESSÃO ({d["PRESSAO"]}%)<div class="pressure-bar" style="width: {d["PRESSAO"]}%"></div></div>', unsafe_allow_html=True)
        with c_tend:
            cor_t = "#00ff88" if d["TENDENCIA"] == "ALTA" else "#ff4b4b" if d["TENDENCIA"] == "BAIXA" else "#ffff00"
            st.markdown(f'<div class="card">TENDÊNCIA<br><span class="metric-value" style="color: {cor_t};">{d["TENDENCIA"]}</span></div>', unsafe_allow_html=True)

        # Alertas
        if d["VIX"] > 20:
            st.error(f"⚠️ ALERTA: Volatilidade Alta! VIX em {d['VIX']}")

    time.sleep(2)
