import streamlit as st
import pandas as pd
import random
import time
import plotly.express as px

# 1. Configurações Iniciais para evitar erros de ID e Layout
st.set_page_config(page_title="Terminal Financeiro Estável", layout="wide")

# CSS para alertas e cards (Mantendo o visual das suas fotos)
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    .card { background-color: #1a1a1a; border: 1px solid #333; border-radius: 10px; padding: 15px; text-align: center; color: white; }
    .vix-danger { background-color: #4a0000; border: 2px solid #ff0000; border-radius: 10px; padding: 15px; text-align: center; color: #ff0000; animation: pulse 1.5s infinite; }
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); } 70% { box-shadow: 0 0 0 15px rgba(255, 0, 0, 0); } 100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); } }
</style>
""", unsafe_allow_html=True)

# 2. Funções de Dados (Resolvendo o NameError)
def gerar_dados_ativo():
    # Criamos o dataframe dentro da função para que ele SEMPRE exista
    df = pd.DataFrame({
        "Data": pd.date_range(start="2023-01-01", periods=12, freq="H"),
        "Valor": [random.uniform(95, 105) for _ in range(12)]
    })
    pressao = random.randint(15, 90)
    return df, pressao

def tocar_alerta():
    st.components.v1.html("<script>var context = new (window.AudioContext || window.webkitAudioContext)(); var osc = context.createOscillator(); osc.type = 'sine'; osc.frequency.setValueAtTime(440, context.currentTime); osc.connect(context.destination); osc.start(); osc.stop(context.currentTime + 0.5);</script>", height=0)

# 3. Loop Principal (Usando placeholder para evitar que dados sumam)
placeholder = st.empty()

while True:
    with placeholder.container():
        st.title("📟 TERMINAL FINANCEIRO PRO")
        
        # Sorteio do VIX antes das colunas para controle do alerta
        vix_valor = round(random.uniform(18, 25), 2)
        
        col1, col2, col3 = st.columns(3)
        
        # --- ATIVO 1: SP500 ---
        df_sp, p_sp = gerar_dados_ativo()
        with col1:
            st.markdown(f'<div class="card"><h3>S&P 500</h3><h2 style="color:#00ff00">6893.72</h2></div>', unsafe_allow_html=True)
            fig_sp = px.line(df_sp, x="Data", y="Valor")
            fig_sp.update_traces(line_color="#00ff00").update_layout(height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_visible=False)
            # USANDO KEY ÚNICA para evitar o erro de DuplicateElementKey
            st.plotly_chart(fig_sp, use_container_width=True, key="graf_sp_estavel")
            st.write(f"**Pressão Individual: {p_sp}%**")
            st.progress(p_sp / 100)

        # --- ATIVO 2: NASDAQ ---
        df_nq, p_nq = gerar_dados_ativo()
        with col2:
            st.markdown(f'<div class="card"><h3>NASDAQ</h3><h2 style="color:#00ff00">25678.10</h2></div>', unsafe_allow_html=True)
            fig_nq = px.line(df_nq, x="Data", y="Valor")
            fig_nq.update_traces(line_color="#0088ff").update_layout(height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_visible=False)
            # KEY ÚNICA DIFERENTE
            st.plotly_chart(fig_nq, use_container_width=True, key="graf_nq_estavel")
            st.write(f"**Pressão Individual: {p_nq}%**")
            st.progress(p_nq / 100)

        # --- ATIVO 3: VIX E ALERTAS ---
        with col3:
            if vix_valor > 22:
                st.markdown(f'<div class="vix-danger"><h3>⚠️ VIX ALTO</h3><h2>{vix_valor}</h2><p>RISCO DE QUEDA</p></div>', unsafe_allow_html=True)
                tocar_alerta()
            else:
                st.markdown(f'<div class="card"><h3>VIX</h3><h2 style="color:#ffaa00">{vix_valor}</h2><p>ESTÁVEL</p></div>', unsafe_allow_html=True)

    time.sleep(2)
