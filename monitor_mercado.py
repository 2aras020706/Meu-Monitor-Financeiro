import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from datetime import datetime

# 1. Configuração de Layout
st.set_page_config(page_title="Terminal Pro", layout="wide")

# 2. Inicialização da Memória (Se não existir, cria)
if 'historico_sp' not in st.session_state:
    st.session_state.historico_sp = pd.DataFrame(columns=['Data', 'Valor'])
if 'historico_nq' not in st.session_state:
    st.session_state.historico_nq = pd.DataFrame(columns=['Data', 'Valor'])

# 3. Função para Atualizar Dados sem perder os anteriores
def atualizar_dados(ticker):
    novo_valor = 6893.72 + np.random.uniform(-5, 5) if ticker == "SP" else 25678.10 + np.random.uniform(-10, 10)
    nova_linha = pd.DataFrame({'Data': [datetime.now()], 'Valor': [novo_valor]})
    
    if ticker == "SP":
        st.session_state.historico_sp = pd.concat([st.session_state.historico_sp, nova_linha]).tail(20)
        return st.session_state.historico_sp, np.random.randint(10, 90)
    else:
        st.session_state.historico_nq = pd.concat([st.session_state.historico_nq, nova_linha]).tail(20)
        return st.session_state.historico_nq, np.random.randint(10, 90)

# 4. Interface
st.title("📟 MONITOR COM MEMÓRIA DE DADOS")
placeholder = st.empty()

while True:
    with placeholder.container():
        col1, col2, col3 = st.columns(3)
        
        # Ativo 1: S&P 500
        df_sp, pressao_sp = atualizar_dados("SP")
        with col1:
            st.metric("S&P 500", f"{df_sp['Valor'].iloc[-1]:.2f}")
            fig_sp = px.line(df_sp, x='Data', y='Valor', title="Pressão SP")
            st.plotly_chart(fig_sp, use_container_width=True, key="graf_sp") # Key evita erro de ID
            st.progress(pressao_sp / 100, text=f"Pressão: {pressao_sp}%")

        # Ativo 2: NASDAQ
        df_nq, pressao_nq = atualizar_dados("NQ")
        with col2:
            st.metric("NASDAQ", f"{df_nq['Valor'].iloc[-1]:.2f}")
            fig_nq = px.line(df_nq, x='Data', y='Valor', title="Pressão NQ")
            st.plotly_chart(fig_nq, use_container_width=True, key="graf_nq")
            st.progress(pressao_nq / 100, text=f"Pressão: {pressao_nq}%")

        # Ativo 3: VIX e Som
        vix = np.random.uniform(18, 25)
        with col3:
            if vix > 22:
                st.error(f"⚠️ VIX ALTO: {vix:.2f}")
                # Código de som aqui
            else:
                st.success(f"VIX ESTÁVEL: {vix:.2f}")

    time.sleep(2)
