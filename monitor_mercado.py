import streamlit as st
import pandas as pd
import random
import time

# Configuração da página
st.set_page_config(page_title="Monitor de Mercado Pro + Som", layout="wide")

# CSS para o visual e animação
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
    .metric-value { font-size: 26px; font-weight: bold; color: #00ff88; }
    .pressure-bar {
        background: linear-gradient(90deg, #ff4b4b 0%, #4b4bff 100%);
        height: 20px; border-radius: 10px; margin: 10px 0; transition: width 0.5s;
    }
</style>
""", unsafe_allow_html=True)

# Função para emitir som (usando um link de áudio público)
def play_sound(url):
    st.markdown(f'<audio src="{url}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)

def gerar_dados():
    return {
        "WIN": random.randint(110000, 120000),
        "ESI": round(random.uniform(5.0, 5.5), 2),
        "NQI": random.randint(15000, 16000),
        "NQ": random.randint(18000, 18500),
        "ES": random.randint(5200, 5300),
        "VIX": round(random.uniform(12.0, 25.0), 2),
        "PRESSAO": random.randint(10, 90),
        "TENDENCIA": random.choice(["ALTA", "BAIXA", "LATERAL"])
    }

st.title("📊 MONITOR DE MERCADO COM ALERTAS SONOROS")

placeholder = st.empty()
last_tendencia = None

while True:
    with placeholder.container():
        d = gerar_dados()
        
        # Lógica de Som: Se a tendência mudar, toca um alerta
        if last_tendencia != d["TENDENCIA"]:
            if d["TENDENCIA"] == "ALTA":
                play_sound("https://www.soundjay.com/buttons/sounds/button-3.mp3")
            elif d["TENDENCIA"] == "BAIXA":
                play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")
            last_tendencia = d["TENDENCIA"]

        # Interface
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="card">WIN<br><span class="metric-value">{d["WIN"]}</span></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="card">ESI<br><span class="metric-value">R$ {d["ESI"]}</span></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="card">NQI<br><span class="metric-value">{d["NQI"]}</span></div>', unsafe_allow_html=True)

        c4, c5, c6 = st.columns(3)
        c4.markdown(f'<div class="card">NASDAQ (NQ)<br><span class="metric-value">{d["NQ"]}</span></div>', unsafe_allow_html=True)
        c5.markdown(f'<div class="card">S&P 500 (ES)<br><span class="metric-value">{d["ES"]}</span></div>', unsafe_allow_html=True)
        c6.markdown(f'<div class="card" style="border-color: #ff4b4b;">VIX<br><span class="metric-value" style="color: #ff4b4b;">{d["VIX"]}</span></div>', unsafe_allow_html=True)

        cp, ct = st.columns([2, 1])
        cp.markdown(f'<div class="card">PRESSÃO ({d["PRESSAO"]}%)<div class="pressure-bar" style="width: {d["PRESSAO"]}%"></div></div>', unsafe_allow_html=True)
        
        cor_t = "#00ff88" if d["TENDENCIA"] == "ALTA" else "#ff4b4b" if d["TENDENCIA"] == "BAIXA" else "#ffff00"
        ct.markdown(f'<div class="card">TENDÊNCIA<br><span class="metric-value" style="color: {cor_t};">{d["TENDENCIA"]}</span></div>', unsafe_allow_html=True)

        if d["VIX"] > 22:
            st.warning(f"🚨 VOLATILIDADE ALTA: VIX em {d['VIX']}")

    time.sleep(2)
