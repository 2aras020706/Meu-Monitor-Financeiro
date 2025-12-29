import streamlit as st
import pandas as pd
import random
import time
import plotly.express as px

# 1. Configuração da Página (Sempre a primeira coisa)
st.set_page_config(page_title="Monitor Pro", layout="wide")

# 2. Estilização CSS
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    .card {
        background-color: #1a1a1a;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# 3. Função para gerar dados INDIVIDUAIS (Resolve o NameError)
def gerar_dados_ativo():
    # Simula volume para calcular a pressão
    vol_compra = random.randint(100, 1000)
    vol_venda = random.randint(100, 1000)
    pressao = int((vol_compra / (vol_compra + vol_venda)) * 100)
    
    # Cria o DataFrame aqui dentro (Resolve: name 'df_exemplo' is not defined)
    df = pd.DataFrame({
        "Data": pd.date_range(start="2023-01-01", periods=15, freq="H"),
        "Valor": [random.uniform(90, 110) for _ in range(15)]
    })
    return pressao, df

# 4. Função do Gráfico
def criar_grafico(df, cor):
    fig = px.line(df, x="Data", y="Valor")
    fig.update_traces(line_color=cor)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color="white", margin=dict(l=0, r=0, t=0, b=0), height=150,
        xaxis_visible=False, yaxis_visible=False
    )
    return fig

# --- ESTRUTURA DO MONITOR ---
st.title("📟 TERMINAL FINANCEIRO PRO")
placeholder = st.empty()

while True:
    with placeholder.container():
        col1, col2 = st.columns(2)
        
        # ATIVO 1: S&P 500
        pressao_sp, df_sp = gerar_dados_ativo() # Dados exclusivos para SP
        with col1:
            st.markdown(f'<div class="card"><h3>S&P 500</h3><h2>6893.72</h2></div>', unsafe_allow_html=True)
            # Use chaves únicas (key) para não dar DuplicateElementId
            st.plotly_chart(criar_grafico(df_sp, "#00ff00"), use_container_width=True, key="graf_sp500")
            st.write(f"PRESSÃO DE VOLUME: {pressao_sp}%")
            st.progress(pressao_sp / 100)

        # ATIVO 2: NASDAQ
        pressao_nq, df_nq = gerar_dados_ativo() # Dados exclusivos para NASDAQ
        with col2:
            st.markdown(f'<div class="card"><h3>NASDAQ</h3><h2>25678.10</h2></div>', unsafe_allow_html=True)
            st.plotly_chart(criar_grafico(df_nq, "#0088ff"), use_container_width=True, key="graf_nasdaq")
            st.write(f"PRESSÃO DE VOLUME: {pressao_nq}%")
            st.progress(pressao_nq / 100)

    time.sleep(2)
