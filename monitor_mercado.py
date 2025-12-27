import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime

# Configurações de API
API_KEY = "8ee68d10f659463ba3380b93902e6407"
SYMBOLS = ["VIX", "NQ=F", "ES=F"] 

st.set_page_config(page_title="Monitor de Fluxo", layout="wide")

def get_data(symbol):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&outputsize=30&apikey={API_KEY}"
    try:
        r = requests.get(url).json()
        if "values" in r:
            df = pd.DataFrame(r['values'])
            df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].apply(pd.to_numeric)
            return df
        return None
    except:
        return None

st.title("📊 Monitor em Tempo Real")

if st.button('🔄 Atualizar Agora'):
    st.rerun()

cols = st.columns(3)
for i, s in enumerate(SYMBOLS):
    with cols[i]:
        df = get_data(s)
        if df is not None:
            atual = df.iloc[0]
            # Cálculo de Pressão de Compra
            pressure = ((atual['close'] - atual['low']) / (atual['high'] - atual['low'] + 0.001)) * 100
            st.metric(s, f"{atual['close']:.2f}")
            st.write(f"Pressão: {pressure:.1f}%")
            st.progress(int(max(0, min(100, pressure))))
            
            # Gráfico
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close'])])
            fig.update_layout(xaxis_rangeslider_visible=False, height=200, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)

st.caption("Limite da API: Atualize a cada 1 minuto.")
