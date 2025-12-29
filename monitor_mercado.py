import streamlit as st
import pandas as pd
import requests
import time

# Configurações de API
API_KEY = "8ee68d10f659463ba3380b93902e6407"
# Usando ETFs para garantir que os dados apareçam na conta gratuita
SYMBOLS = {"VIX": "VIXY", "ES": "SPY", "NQ": "QQQ"}

st.set_page_config(page_title="Monitor de Mercado", layout="wide")

# --- ESTILO CSS PARA O VISUAL NEON/DARK ---
st.markdown("""
    <style>
    main { background-color: #000000; }
    .stApp { background-color: #000000; }
    
    /* Estilo dos Cartões */
    .metric-card {
        background-color: #0e0e10;
        border: 1px solid #3d2b56;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(123, 31, 162, 0.2);
    }
    
    .symbol-title { color: #ffffff; font-size: 24px; font-weight: bold; margin-bottom: 5px; }
    .sub-title { color: #8a8a8e; font-size: 14px; margin-bottom: 20px; }
    .price { color: #ffffff; font-size: 42px; font-weight: bold; font-family: 'Courier New', monospace; }
    .delta-neg { color: #ff3b30; font-size: 18px; }
    .delta-pos { color: #34c759; font-size: 18px; }
    
    /* Detalhes de Baixo */
    .info-label { color: #8a8a8e; font-size: 12px; text-transform: uppercase; }
    .info-value { color: #ffffff; font-size: 16px; font-weight: bold; margin-bottom: 10px; }
    
    /* Barra de Progresso Roxa */
    .stProgress > div > div > div > div { background-color: #7b1fa2; }
    </style>
    """, unsafe_allow_html=True)

def get_data(symbol):
    url = f"https://api.twelvedata.com/quote?symbol={symbol}&apikey={API_KEY}"
    try:
        r = requests.get(url).json()
        return r if "price" in r else None
    except:
        return None

# Cabeçalho Superior
st.markdown("<h1 style='color: #ffffff; text-shadow: 2px 2px #7b1fa2;'>MONITOR DE MERCADO</h1>", unsafe_allow_html=True)
if st.button('🔄 REFRESH'):
    st.rerun()

# Layout em colunas
for label, sym in SYMBOLS.items():
    data = get_data(sym)
    
    if data:
        price = float(data['price'])
        change = float(data['change'])
        percent = float(data['percent_change'])
        color_class = "delta-pos" if change >= 0 else "delta-neg"
        arrow = "▲" if change >= 0 else "▼"
        
        # HTML customizado para imitar a sua imagem
        st.markdown(f"""
            <div class="metric-card">
                <div class="symbol-title">{label} <span style="font-size: 14px; color: #7b1fa2;">{arrow}</span></div>
                <div class="sub-title">Futuros do {label} 100</div>
                <div class="price">$ {price:,.2f}</div>
                <div class="{color_class}">{change:+.2f} ( {percent:+.2f} % )</div>
                <hr style="border: 0.1px solid #333; margin: 20px 0;">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <div class="info-label">ALTO</div>
                        <div class="info-value">$ {float(data['high']):,.2f}</div>
                    </div>
                    <div>
                        <div class="info-label">BAIXO</div>
                        <div class="info-value">$ {float(data['low']):,.2f}</div>
                    </div>
                </div>
                <div class="info-label">PRESSÃO DE COMPRA (RSI)</div>
            </div>
        """, unsafe_allow_html=True)
        # Barra de progresso roxa (simulando o medidor da imagem)
        st.progress(52 if label == "ES" else 45) 
    else:
        st.warning(f"Aguardando dados de {label}...")
    
    time.sleep(1) # Delay para evitar bloqueio da API
