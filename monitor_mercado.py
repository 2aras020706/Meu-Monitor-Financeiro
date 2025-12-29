import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# Configuração da página para ocupar a tela toda
st.set_page_config(layout="wide", page_title="Monitor de Trading")

# --- FUNÇÃO PARA GERAR DADOS DE EXEMPLO ---
def get_market_data():
    # Simulando um histórico de 50 velas
    if 'df' not in st.session_state:
        dates = pd.date_range(end=datetime.now(), periods=50, freq='1min')
        st.session_state.df = pd.DataFrame({
            'time': dates,
            'open': np.random.uniform(25600, 25700, 50),
            'high': np.random.uniform(25700, 25750, 50),
            'low': np.random.uniform(25550, 25600, 50),
            'close': np.random.uniform(25600, 25700, 50)
        })
    
    # Simula a variação da "Vela Atual" (a última linha)
    last_idx = st.session_state.df.index[-1]
    current_close = st.session_state.df.loc[last_idx, 'close']
    variation = np.random.uniform(-5, 5)
    
    st.session_state.df.loc[last_idx, 'close'] = current_close + variation
    # Atualiza máxima/mínima da vela atual
    if current_close > st.session_state.df.loc[last_idx, 'high']:
        st.session_state.df.loc[last_idx, 'high'] = current_close
    if current_close < st.session_state.df.loc[last_idx, 'low']:
        st.session_state.df.loc[last_idx, 'low'] = current_close
        
    return st.session_state.df

# --- COMPONENTE DO GRÁFICO (O SEGREDO) ---
@st.fragment(run_every=1) # Atualiza apenas esta função a cada 1 segundo
def render_live_chart():
    df = get_market_data()
    
    fig = go.Figure(data=[go.Candlestick(
        x=df['time'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        increasing_line_color='#26a69a', decreasing_line_color='#ef5350'
    )])

    fig.update_layout(
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=500,
        # O uirevision impede que o gráfico "resete" o zoom/posição ao atualizar
        uirevision='constant', 
        yaxis=dict(
            side="right",
            fixedrange=False # Permite que o usuário mova o gráfico se quiser
        )
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- INTERFACE PRINCIPAL ---
st.title("📊 Terminal Financeiro")

col1, col2, col3 = st.columns(3)
col1.metric("SP500", "6893.72", "+0.12%")
col2.metric("NASDAQ", "25678.10", "-0.05%")
col3.metric("VIX", "18.45", "-2.30%")

# Chamada do fragmento
render_live_chart()
