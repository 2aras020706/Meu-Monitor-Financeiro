import streamlit as st
import pandas as pd
import plotly.graph_objects as go

@st.fragment(run_every=1) # Atualiza a cada 1 segundo
def renderizar_grafico_tempo_real():
    # 1. Obter os dados (apenas o necessário)
    df = buscar_dados_recentes() 

    # 2. Criar a figura
    fig = go.Figure(data=[go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])

    # 3. FIXAR O LAYOUT (Crucial para não "pular")
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        # Mantém a escala do eixo Y consistente
        yaxis=dict(autorange=True, fixedrange=False), 
        # Evita animações bruscas que fazem a vela 'sumir' e voltar
        uirevision='constant' 
    )

    st.plotly_chart(fig, use_container_width=True)
