import streamlit as st
import pandas as pd
import random
import time
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. Configuração da página
st.set_page_config(page_title="Terminal Pro - Multi-Ativos", layout="wide")

# 2. CSS para manter o estilo escuro e os alertas
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    .main-card {
        background-color: #1a1a1a;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        margin-bottom: 10px;
    }
    .vix-danger {
        background-color: #4a0000;
        border: 2px solid #ff0000;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 0, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }
    }
</style>
""", unsafe_allow_html=True)

# 3. Função para gerar dados de velas (OHLC) simulados
def gerar_velas(preco_atual, pontos=20):
    dados = []
    tempo_atual = datetime.now()
    for i in range(pontos):
        abertura = preco_atual + random.uniform(-5, 5)
        fechamento = abertura + random.uniform(-4, 4)
        maxima = max(abertura, fechamento) + random.uniform(0, 3)
        minima = min(abertura, fechamento) - random.uniform(0, 3)
        dados.append({
            "Date": tempo_atual - timedelta(minutes=5*i),
            "Open": abertura, "High": maxima, "Low": minima, "Close": fechamento
        })
    return pd.DataFrame(dados)

# 4. Função para criar o gráfico de velas compacto
def criar_grafico_velas(df):
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        increasing_line_color='#00ff00', decreasing_line_color='#ff4b4b'
    )])
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=150,
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        xaxis_showticklabels=False,
        yaxis_showticklabels=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# 5. Função de Alerta Sonoro
def tocar_alerta():
    st.components.v1.html("<script>var c=new AudioContext();var o=c.createOscillator();o.connect(c.destination);o.start();o.stop(c.currentTime+0.2);</script>", height=0)

# --- LOOP PRINCIPAL ---
placeholder = st.empty()

while True:
    # Simulando dados baseados na sua imagem
    dados = {
        "SP500": {"val": round(6897.69 + random.uniform(-2, 2), 2), "pres": random.randint(30, 80)},
        "NASDAQ": {"val": round(25694.50 + random.uniform(-10, 10), 2), "pres": random.randint(20, 90)},
        "VIX": {"val": round(16.73 + random.uniform(-1, 5), 2), "pres": random.randint(10, 50)}
    }

    with placeholder.container():
        cols = st.columns(3)
        
        for i, (ativo, info) in enumerate(dados.items()):
            with cols[i]:
                # Estilo dinâmico para o VIX
                estilo_vix = "vix-danger" if ativo == "VIX" and info['val'] > 21 else ""
                
                # Card de Preço
                st.markdown(f"""
                <div class="main-card {estilo_vix}">
                    <p style="color:#aaa; margin:0;">{ativo} FUTURO</p>
                    <h2 style="color:#00ff00; margin:0;">{info['val']}</h2>
                </div>
                """, unsafe_allow_html=True)
                
                # Gráfico de Velas
                df_velas = gerar_velas(info['val'])
                st.plotly_chart(criar_grafico_velas(df_velas), use_container_width=True, config={'displayModeBar': False})
                
                # Medidor de Pressão Individual
                st.markdown(f"""
                <div style="background-color:#1a1a1a; padding:5px; border-radius:5px; text-align:center;">
                    <small style="color:white;">PRESSÃO: {info['pres']}%</small>
                    <div style="background:#333; height:8px; border-radius:10px; margin-top:5px;">
                        <div style="background:linear-gradient(90deg, #ff4b4b {100-info['pres']}%, #00ff00 {info['pres']}%); 
                        width:100%; height:100%; border-radius:10px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if ativo == "VIX" and info['val'] > 21:
                    tocar_alerta()

    time.sleep(2)
