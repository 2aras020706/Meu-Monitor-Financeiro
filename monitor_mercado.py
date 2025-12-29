              import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import time

# Chave e Símbolos (Trocamos para ETFs que funcionam 100% na versão grátis)
API_KEY = "8ee68d10f659463ba3380b93902e6407"
SYMBOLS = ["VIXY", "QQQ", "SPY"] # VIX, Nasdaq e S&P500

st.set_page_config(page_title="Monitor de Fluxo", layout="wide")
st.title("📈 Monitor de Mercado em Tempo Real")

def get_data(symbol):
    # Adicionamos um pequeno delay para a API não bloquear
    time.sleep(1) 
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&outputsize=30&apikey={API_KEY}"
    try:
        r = requests.get(url).json()
        if "values" in r:
            df = pd.DataFrame(r['values'])
            df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].apply(pd.to_numeric)
            return df
        else:
            st.error(f"Erro no ativo {symbol}: {r.get('message', 'Sem resposta')}")
            return None
    except:
        return None

if st.button('🔄 Atualizar Painel'):
    st.rerun()

cols = st.columns(3)

for i, s in enumerate(SYMBOLS):
    with cols[i]:
        df = get_data(s)
        if df is not None:
            atual = df.iloc[0]
            # Cálculo de Pressão
            diff = (atual['high'] - atual['low'])
            pressure = ((atual['close'] - atual['low']) / diff * 100) if diff != 0 else 50
            
            nome_amigavel = {"VIXY": "VIX (Volatilidade)", "QQQ": "NASDAQ 100", "SPY": "S&P 500"}
            st.subheader(nome_amigavel[s])
            st.metric("Preço", f"${atual['close']:.2f}")
            
            st.write(f"Pressão de Compra: {pressure:.1f}%")
            st.progress(int(max(0, min(100, pressure))))
            
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close'])])
            fig.update_layout(xaxis_rangeslider_visible=False, height=300, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)
