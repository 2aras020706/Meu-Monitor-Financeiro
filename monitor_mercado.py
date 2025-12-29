import streamlit as st
import pandas as pd
import random
import time
from collections import deque

# Configuração da página
st.set_page_config(page_title="Monitor de Mercado Pro", layout="wide")

# Estilos CSS (Incluindo o novo alerta VIX)
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    .card {
        background-color: #1a1a1a;
        border: 2px solid #5a189a;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        color: white;
    }
    .vix-alert {
        background-color: #ff0000;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        animation: blinker 1.5s linear infinite;
    }
    @keyframes blinker { 50% { opacity: 0.2; } }
</style>
""", unsafe_allow_html=True)

# Inicializa o histórico para o gráfico de 5 min (armazenando 150 pontos para ~2s cada)
if 'historico_win' not in st.session_state:
    st.session_state.historico_win = deque([115000] * 50, maxlen=150)

def gerar_dados():
    vix = round(random.uniform(10.0, 30.0), 2)
    win = st.session_state.historico_win[-1] + random.randint(-50, 50)
    st.session_state.historico_win.append(win)
    return {"WIN": win, "VIX": vix, "Dolar": round(random.uniform(5.10, 5.40), 2)}

st.title("📊 MONITOR DE MERCADO COM ALERTA VIX")

placeholder = st.empty()

while True:
    with placeholder.container():
        dados = gerar_dados()
        
        # Primeira Linha: Cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="card"><h3>WIN</h3><h2>{dados["WIN"]}</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="card"><h3>DÓLAR</h3><h2>R$ {dados["Dolar"]}</h2></div>', unsafe_allow_html=True)
        with col3:
            # Alerta VIX Diferenciado se estiver alto (> 20)
            if dados["VIX"] > 22:
                st.markdown(f'<div class="vix-alert">⚠️ VIX ALTO: {dados["VIX"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="card"><h3>VIX</h3><h2>{dados["VIX"]}</h2></div>', unsafe_allow_html=True)

        st.markdown("---")
        
        # Segunda Linha: Gráfico de 5 Minutos (Simulado)
        st.subheader("Tendência WIN (Últimos minutos)")
        chart_data = pd.DataFrame(list(st.session_state.historico_win), columns=['Preço Ibovespa'])
        st.area_chart(chart_data, color="#5a189a")

    time.sleep(2)
