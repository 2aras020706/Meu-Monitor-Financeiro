import streamlit as st
import pandas as pd
import random
import time
from collections import deque

# Configuração da página
st.set_page_config(page_title="Monitor Pro: S&P, NQ e VIX", layout="wide")

# Estilos CSS (Foco nos principais e alerta VIX)
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    .main-card {
        background-color: #1a1a1a;
        border: 2px solid #5a189a;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        color: white;
    }
    .secondary-card {
        background-color: #0e0e0e;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        color: #bbb;
    }
    .vix-alert {
        background-color: #4a0000;
        border: 2px solid #ff0000;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        color: #ff0000;
        font-weight: bold;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255, 0, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }
    }
</style>
""", unsafe_allow_html=True)

# Memória para o gráfico do S&P 500 (Principal)
if 'hist_sp' not in st.session_state:
    st.session_state.hist_sp = deque([5250.0] * 50, maxlen=50)

def atualizar_dados():
    vix = round(random.uniform(18.0, 26.0), 2)
    novo_sp = st.session_state.hist_sp[-1] + random.uniform(-5, 5)
    st.session_state.hist_sp.append(novo_sp)
    return {
        "SP500": round(novo_sp, 2),
        "NASDAQ": random.randint(18200, 18400),
        "VIX": vix,
        "WIN": random.randint(115000, 117000),
        "DOLAR": round(random.uniform(5.30, 5.40), 2)
    }

st.title("🚀 MONITOR DE ALTA PRIORIDADE")

placeholder = st.empty()

while True:
    with placeholder.container():
        d = atualizar_dados()
        
        # --- LINHA PRINCIPAL (S&P 500, NASDAQ, VIX) ---
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'<div class="main-card"><h3>S&P 500 (ES)</h3><h1 style="color:#00ff00">{d["SP500"]}</h1></div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="main-card"><h3>NASDAQ (NQ)</h3><h1 style="color:#00ff00">{d["NASDAQ"]}</h1></div>', unsafe_allow_html=True)
            
        with col3:
            if d["VIX"] > 22:
                st.markdown(f'<div class="vix-alert"><h3>⚠️ VIX ALTO</h3><h1>{d["VIX"]}</h1></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="main-card"><h3>VIX</h3><h1 style="color:#ffaa00">{d["VIX"]}</h1></div>', unsafe_allow_html=True)

        # --- GRÁFICO DE 5 MINUTOS (Focado no S&P 500) ---
        st.write("")
        st.subheader("Tendência S&P 500 (Últimos 5 Minutos)")
        st.area_chart(pd.DataFrame(list(st.session_state.hist_sp), columns=['Pontos']), color="#5a189a")

        # --- LINHA SECUNDÁRIA (Outros ativos) ---
        st.write("")
        c_a, c_b = st.columns(2)
        c_a.markdown(f'<div class="secondary-card"><b>WIN:</b> {d["WIN"]}</div>', unsafe_allow_html=True)
        c_b.markdown(f'<div class="secondary-card"><b>DÓLAR:</b> R$ {d["DOLAR"]}</div>', unsafe_allow_html=True)

    time.sleep(2)
