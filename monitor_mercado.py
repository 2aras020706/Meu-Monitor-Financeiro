 import streamlit as st
import pandas as pd
import requests
import time

# Configurações de API
API_KEY = "8ee68d10f659463ba3380b93902e6407"
# Usando ativos que sempre funcionam na API gratuita
SYMBOLS = {"VIX": "VIXY", "ES": "SPY", "NQ": "QQQ"}

st.set_page_config(page_title="Monitor de Mercado", layout="wide")

# --- DESIGN PROFISSIONAL (CSS) ---
st.markdown("""
    <style>
    /* Fundo total preto */
    .stApp { background-color: #000000; }
    
    /* Estilo dos Cards Neon */
    .card {
        background-color: #0a0a0a;
        border: 2px solid #5a189a;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        font-family: 'Inter', sans-serif;
    }
    
    .symbol { color: #ffffff; font-size: 28px; font-weight: bold; }
    .description { color: #666666; font-size: 14px; margin-bottom: 15px; }
    .price { color: #ffffff; font-size: 50px; font-weight: bold; letter-spacing: -1px; }
    
    .delta-pos { color: #34c759; font-size: 20px; font-weight: bold; }
    .delta-neg { color: #ff3b30; font-size: 20px; font-weight: bold; }
    
    .label { color: #444444; font-size: 12px; font-weight: bold; text-transform: uppercase; margin-top: 15px; }
    .value { color: #ffffff; font-size: 18px; font-weight: bold; }
    
    /* Barra de progresso customizada (roxo neon) */
    .stProgress > div > div > div > div { background-color: #9d4edd; }
    
    /* Esconder menus do streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def get_data(symbol):
    url = f"https://api.twelvedata.com/quote?symbol={symbol}&apikey={API_KEY}"
    try:
        r = requests.get(url).json()
        return r if "price" in r else None
    except:
        return None

# Título do Painel
st.markdown("<h1 style='color: white; font-size: 30px; border-left: 5px solid #9d4edd; padding-left: 15px;'>MONITOR DE MERCADO</h1>", unsafe_allow_html=True)

# Botão de atualização
if st.button('🔄 ATUALIZAR DADOS'):
    st.rerun()

# Criar os Cards para cada ativo
for label, sym in SYMBOLS.items():
    data = get_data(sym)
    
    if data:
        price = float(data['price'])
        change = float(data['change'])
        percent = float(data['percent_change'])
        high = float(data['high'])
        low = float(data['low'])
        
        color_class = "delta-pos" if change >= 0 else "delta-neg"
        arrow = "↑" if change >= 0 else "↓"
        desc = {"VIX": "Índice de Volatilidade", "ES": "S&P 500 Futuros (SPY)", "NQ": "Nasdaq 100 Futuros (QQQ)"}

        # HTML do Card
        st.markdown(f"""
            <div class="card">
                <div class="symbol">{label} <span style="font-size: 18px; color: #9d4edd;">{arrow}</span></div>
                <div class="description">{desc[label]}</div>
                <div class="price">$ {price:,.2f}</div>
                <div class="{color_class}">{change:+.2f} ({percent:+.2f}%)</div>
                
                <div style="display: flex; gap: 40px; margin-top: 20px; border-top: 1px solid #222; padding-top: 15px;">
                    <div>
                        <div class="label">Máxima (High)</div>
                        <div class="value">$ {high:,.2f}</div>
                    </div>
                    <div>
                        <div class="label">Mínima (Low)</div>
                        <div class="value">$ {low:,.2f}</div>
                    </div>
                </div>
                
                <div class="label" style="margin-top: 20px;">Indicador de Pressão de Compra</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Simula o indicador RSI/Pressão com a barra do Streamlit
        # (Aqui usamos o percentual de fechamento em relação ao range do dia)
        pressure = ((price - low) / (high - low) * 100) if high != low else 50
        st.progress(int(max(0, min(100, pressure))))
        st.markdown("<br>", unsafe_allow_html=True)
    
    time.sleep(1) # Delay para respeitar o limite da API gratuita
