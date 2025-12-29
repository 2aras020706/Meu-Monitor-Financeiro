import streamlit as st
import pandas as pd
import random
import time
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(page_title="Terminal Pro - Multi-Ativos", layout="wide")

# CSS para estilo escuro, cards e alertas
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    .main-card {
        background-color: #1a1a1a;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
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

# Função para simular velas (Candlesticks)
def gerar_velas(preco_atual):
    dados = []
    tempo = datetime.now()
    for i in range(15):
        abertura = preco_atual + random.uniform(-3, 3)
        fechamento = abertura + random.uniform(-4, 4)
        dados.append({
            "Date": tempo - timedelta(minutes=5*i),
            "Open": abertura, "High": max(abertura, fechamento) + 1,
            "Low": min(abertura, fechamento) - 1, "Close": fechamento
        })
    return pd.DataFrame(dados)

# Função para criar o gráfico de velas
def criar_grafico(df):
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        increasing_line_color='#00ff00', decreasing_line_color='#ff4b4b'
    )])
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0), height=180,
        xaxis_rangeslider_visible=False, template="plotly_dark",
        xaxis_showticklabels=False, yaxis_showticklabels=False,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# Alerta Sonoro
def tocar_alerta():
    st.components.v1.html("<script>var c=new AudioContext();var o=c.createOscillator();o.connect(c.destination);o.start();o.stop(c.currentTime+0.2);</script>", height=0)

placeholder = st.empty()

# Inicialização de preços estáveis
if 'precos' not in st.session_state:
    st.session_state.precos = {"SP500": 6896.12, "NASDAQ": 25694.50, "VIX": 16.73}

while True:
    # Atualiza preços levemente
    st.session_state.precos["SP500"] += random.uniform(-1, 1)
    st.session_state.precos["NASDAQ"] += random.uniform(-5, 5)
    st.session_state.precos["VIX"] = round(random.uniform(15, 23), 2)

    with placeholder.container():
        cols = st.columns(3)
        ativos = ["SP500", "NASDAQ", "VIX"]
        
        for i, ativo in enumerate(ativos):
            with cols[i]:
                preco = round(st.session_state.precos[ativo], 2)
                pressao = random.randint(20, 80)
                
                # Card de Título e Preço
                estilo = "vix-danger" if ativo == "VIX" and preco > 21 else ""
                st.markdown(f'<div class="main-card {estilo}"><p style="color:#aaa;margin:0">{ativo}</p><h2>{preco}</h2></div>', unsafe_allow_html=True)
                
                # Gráfico de Velas
                st.plotly_chart(criar_grafico(gerar_velas(preco)), use_container_width=True, config={'displayModeBar': False})
                
                # Medidor de Pressão Individual
                st.markdown(f"""
                    <div style="background:#1a1a1a; padding:10px; border-radius:10px; text-align:center;">
                        <small style="color:white">PRESSÃO: {pressao}%</small>
                        <div style="background:#333; height:12px; border-radius:10px; margin-top:5px;">
                            <div style="background:linear-gradient(90deg, #ff4b4b {100-pressao}%, #00ff00 {pressao}%); width:100%; height:100%; border-radius:10px;"></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                if ativo == "VIX" and preco > 21:
                    tocar_alerta()

    time.sleep(2)
