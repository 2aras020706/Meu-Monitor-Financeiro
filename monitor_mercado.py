import streamlit as st
import pandas as pd
import requests
import time

# Chave Twelve Data
API_KEY = "8ee68d10f659463ba3380b93902e6407"
# Usando ETFs para estabilidade total
SYMBOLS = {"VIX": "VIXY", "ES": "SPY", "NQ": "QQQ"}

st.set_page_config(page_title="Monitor de Mercado", layout="wide")

# --- DESIGN DOS CARDS ROXOS (IGUAL À SUA IMAGEM) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .card {
        background-color: #0a0a0a;
        border: 2px solid #5a189a;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 0 15px rgba(90, 24, 154, 0.4);
    }
    .symbol { color: #ffffff; font-size: 28px; font-weight: bold; }
    .price { color: #ffffff; font-size: 50px; font-weight: bold; font-family: 'monospace'; }
    .pos { color: #34c759; font-size: 20px; }
    .neg { color: #ff3b30; font-size: 20px; }
    .label { color: #444444; font-size: 12px; font-weight: bold; text-transform: uppercase; }
    .value { color: #ffffff; font-size: 18px; font-weight: bold; }
    .stProgress > div > div > div > div { background-color: #9d4edd; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='color: white;'>MONITOR DE MERCADO</h1>", unsafe_allow_html=True)

def get_data(symbol):
    # Pausa de 5 segundos para a API gratuita não bloquear
    time.sleep(5) 
    url = f"https://api.twelvedata.com/quote?symbol={symbol}&apikey={API_KEY}"
    try:
        r = requests.get(url).json()
        return r if "price" in r else None
    except:
        return None

# Botão de atualização
if st.button('🔄 ATUALIZAR AGORA'):
    st.rerun()

# Espaço onde os cards vão aparecer
for label, sym in SYMBOLS.items():
    data = get_data(sym)
    
    if data:
        p = float(data['price'])
        c = float(data['change'])
        pc = float(data['percent_change'])
        color = "pos" if c >= 0 else "neg"
        
        st.markdown(f"""
            <div class="card">
                <div class="symbol">{label}</div>
                <div class="price">$ {p:,.2f}</div>
                <div class="{color}">{c:+.2f} ({pc:+.2f}%)</div>
                <div style="display: flex; gap: 40px; margin-top: 20px; border-top: 1px solid #222; padding-top: 15px;">
                    <div><div class="label">MÁXIMA</div><div class="value">${float(data['high']):,.2f}</div></div>
                    <div><div class="label">MÍNIMA</div><div class="value">${float(data['low']):,.2f}</div></div>
                </div>
                <div class="label" style="margin-top: 15px;">Pressão de Compra</div>
            </div>
        """, unsafe_allow_html=True)
        # Barra de pressão simulada
        st.progress(65 if label == "NQ" else 48)
    else:
        st.warning(f"Aguardando sinal de {label}... A API gratuita libera 1 ativo a cada 10 segundos.")
