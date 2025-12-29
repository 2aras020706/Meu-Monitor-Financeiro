import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# 1. Configuração de Layout
st.set_page_config(layout="wide", page_title="Terminal Financeiro")

# --- FUNÇÃO PARA GERAR O GRÁFICO COM INDICADORES ---
def criar_grafico(df, titulo):
    # Cálculo de Indicadores (Ex: Médias Móveis de 9 e 20 períodos)
    df['MA9'] = df['close'].rolling(window=9).mean()
    df['MA20'] = df['close'].rolling(window=20).mean()

    fig = go.Figure()

    # Adiciona as Velas (Candlesticks)
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['open'], high=df['high'],
        low=df['low'], close=df['close'],
        name='Preço'
    ))

    # Indicador 1: Média Móvel Rápida (Amarela)
    fig.add_trace(go.Scatter(x=df.index, y=df['MA9'], line=dict(color='#FFD700', width=1.5), name='MA9'))
    
    # Indicador 2: Média Móvel Lenta (Azul)
    fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], line=dict(color='#00BFFF', width=1.5), name='MA20'))

    # Configurações para o gráfico ficar estável como no seu vídeo
    fig.update_layout(
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        height=350,
        margin=dict(l=10, r=10, t=40, b=10),
        uirevision='constant', # ISSO impede o gráfico de "pular" na atualização
        showlegend=False
    )
    return fig

# --- LÓGICA DE ATUALIZAÇÃO (FRAGMENTO) ---
@st.fragment(run_every=1) # Atualiza a cada 1 segundo sem recarregar a página
def atualizar_painel():
    # AQUI: Substitua pela sua função que puxa os dados reais
    # Exemplo: df_sp = buscar_dados("SP500")
    
    # Criando dados fictícios para o exemplo não dar erro de NameError
    chart_data = pd.DataFrame({
        'open': np.random.randn(50).cumsum() + 100,
        'high': np.random.randn(50).cumsum() + 105,
        'low': np.random.randn(50).cumsum() + 95,
        'close': np.random.randn(50).cumsum() + 100,
    }, index=pd.date_range(start=datetime.now(), periods=50, freq='min'))

    # Criar 3 colunas para os ativos
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("SP500", "6893.72", "0.12%")
        # O gráfico fica abaixo do valor
        st.plotly_chart(criar_grafico(chart_data, "SP500"), use_container_width=True, config={'displayModeBar': False})
        st.progress(80, text="Pressão: 80%")

    with col2:
        st.metric("NASDAQ", "25678.10", "-0.05%")
        st.plotly_chart(criar_grafico(chart_data, "NASDAQ"), use_container_width=True, config={'displayModeBar': False})
        st.progress(41, text="Pressão: 41%")

    with col3:
        st.metric("VIX", "18.45", "-2.30%")
        st.plotly_chart(criar_grafico(chart_data, "VIX"), use_container_width=True, config={'displayModeBar': False})
        st.progress(72, text="Pressão: 72%")

# Executa o painel
st.header("📈 Terminal Financeiro Pro")
atualizar_painel()
