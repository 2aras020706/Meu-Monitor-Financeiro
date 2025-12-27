import streamlit as st
import pandas as pd
import requests
import time

# Configurações de API - Chave Twelve Data
API_KEY = "8ee68d10f659463ba3380b93902e6407"
# Símbolos otimizados para estabilidade na conta gratuita
SYMBOLS = {"VIX": "VIXY", "ES": "SPY", "NQ": "QQQ"}

st.set_page_config(page_title="Monitor de Mercado", layout="wide")

# --- DESIGN PROFISSIONAL DARK/PURPLE (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .card {
        background-color: #0a0a0a;
        border: 2px solid #5a189a;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(90, 24, 154, 0.3);
    }
    .symbol-label { color: #ffffff; font-size: 28px; font-weight: bold; }
    .price-large { color: #ffffff; font-size: 55px; font-weight: bold; font-family: 'Courier New', monospace; letter-spacing: -2px; }
    .pos { color: #34c759; font-size: 22px; font-weight: bold; }
    .neg { color: #ff3b30; font-size: 22px; font-weight: bold; }
    .m-label { color: #444444; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-top: 15px; }
    .m-value { color: #ffffff; font-size: 18px; font-weight: bold; }
    .stProgress > div > div > div > div { background-color: #9d4edd; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def get_data(symbol):
    # Pausa de 4 segundos para garantir que a API gratuita não bloqueie o acesso
    time.sleep(4)
    url = f"https://api.twelvedata.com/quote?symbol={symbol}&apikey={API_KEY}"
    try:
        r = requests.get(url).json()
        return r if "price" in r else None
    except:
        return None

st.markdown("<h1 style='color: white; border-left: 6px solid #5a189a; padding-left: 15px;'>MONITOR DE MERCADO</h1>", unsafe_allow_html=True)

if st.button('🔄 ATUALIZAR AGORA'):
    st.rerun()

# Espaço para os cards aparecerem
container = st.container()

with container:
    for label, sym in SYMBOLS.items():
        data = get_data(sym)
        
        if data:
            price = float(data['price'])
            change = float(data['change'])
            p_change = float(data['percent_change'])
            high = float(data['high'])
            low = float(data['low'])
            c_class = "pos" if change >= 0 else "neg"
            arrow = "▲" if change >= 0 else "▼"
            
            st.markdown(f"""
                <div class="card">
                    <div class="symbol-label">{label} <span style="font-size: 16px; color: #5a189a;">{arrow}</span></div>
                    <div class="price-large">$ {price:,.2f}</div>
                    <div class="{c_class}">{change:+.2f} ({p_change:+.2f}%)</div>
                    <div style="display: flex; gap: 40px; margin-top: 20px; border-top: 1px solid #1a1a1a; padding-top: 15px;">
                        <div><div class="m-label">Máxima</div><div class="m-value">$ {high:,.2f}</div></div>
                        <div><div class="m-label">Mínima</div><div class="m-value">$ {low:,.2f}</div></div>
                    </div>
                    <div class="m-label">Pressão de Compra</div>
                </div>
            """, unsafe_allow_html=True)
            pressure = ((price - low) / (high - low) * 100) if high != low else 50
            st.progress(int(max(0, min(100, pressure))))
        else:
            st.info(f"Conectando ao sinal de {label}... Aguarde alguns segundos.")
