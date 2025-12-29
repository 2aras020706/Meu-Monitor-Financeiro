import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuração da página para ocupar a tela toda
st.set_page_config(layout="wide")

# --- FUNÇÃO PARA CRIAR O GRÁFICO ---
def criar_grafico(df, titulo):
    # Cálculo de Indicadores (Média Móvel de 9 e 20 períodos)
    df['MA9'] = df['close'].rolling(window=9).mean()
    df['MA20'] = df['close'].rolling(window=20).mean()

    fig = go.Figure()

    # Candlestick
    fig.add_trace(go.Candlestick(
        x=df.index, open=df['open'], high=df['high'],
        low=df['low'], close=df['close'], name='Preço'
    ))

    # Indicadores de Tendência
    fig.add_trace(go.Scatter(x=df.index, y=df['MA9'], name='MA9', line=dict(color='yellow', width=1)))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='MA20', line=dict(color='blue', width=1)))

    # Estilização para evitar que o gráfico "pule"
    fig.update_layout(
        title=titulo,
        xaxis_rangeslider_visible=False,
        height=300,
        margin=dict(l=20, r=20, t=30, b=20),
        uirevision='constant' # MANTÉM O ZOOM E POSIÇÃO FIXOS
    )
    return fig

# --- LAYOUT PRINCIPAL ---
st.title("📊 Terminal Financeiro Pro")

# Criamos 3 colunas para SP500, NASDAQ e VIX
col1, col2, col3 = st.columns(3)

# Usamos FRAGMENTOS para atualizar apenas os dados, sem piscar a tela
@st.fragment(run_every=1) # Atualiza a cada 1 segundo
def atualizar_painel():
    # Simulando a coleta de dados (Substitua pela sua API)
    # Exemplo: dados_sp500 = sua_api.get('SP500')
    
    with col1:
        st.metric("SP500", "6893.72", "+0.12%")
        # Gráfico logo abaixo do ativo
        st.plotly_chart(criar_grafico(df_exemplo, "S&P 500"), use_container_width=True)
        # Medidor de Pressão
        st.progress(80, text="Pressão de Compra: 80%")

    with col2:
        st.metric("NASDAQ", "25678.10", "-0.05%")
        st.plotly_chart(criar_grafico(df_exemplo, "NASDAQ"), use_container_width=True)
        st.progress(41, text="Pressão: 41%")

    with col3:
        st.metric("VIX", "18.45", "-2.30%")
        st.plotly_chart(criar_grafico(df_exemplo, "VIX"), use_container_width=True)
        st.progress(72, text="Pressão: 72%")

atualizar_painel()
