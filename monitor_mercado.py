import streamlit as st
import pandas as pd
import random
import time

# Configuração da página
st.set_page_config(page_title="Monitor de Mercado Simulado", layout="wide")

# --- DESIGN DOS CARDS ROXOS NEON (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .card {
        background-color: #0a0a0a;
        border: 2px solid #5a189a;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 30px;
        box-shadow: 0 0 20px rgba(90, 24, 154, 0.5);
    }
    .symbol { color: #ffffff; font-size: 28px; font-weight: bold; }
    .price { color: #ffffff; font-size: 55px; font-weight: bold; font-family: 'Courier New', monospace; letter-spacing: -2px; }
    .pos { color: #34c759; font-size: 22px; font-weight: bold; }
    .neg { color: #ff3b30; font-size: 22px; font-weight: bold; }
    .label { color: #444444; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-top: 15px; }
    .value { color: #ffffff; font-size: 18px; font-weight: bold; }
    .stProgress > div > div > div > div { background-color: #9d4edd; }
    </style>
    """, unsafe_allow_html=True)

# Título
st.markdown("<h1 style='color: white; border-left: 6px solid #5a189a; padding-left: 15px;'>MONITOR DE MERCADO (SIMULADO)</h1>", unsafe_allow_html=True)

# Função para simular preços
def gerar_dados_simulados():
    ativos = {
        "VIX": {"preco": 15.50, "desc": "Volatilidade"},
        "ES": {"preco": 5850.25, "desc": "S&P 500 Futuros"},
        "NQ": {"preco": 20110.75, "desc": "Nasdaq 100 Futuros"}
    }
    dados = []
    for sym, info in ativos.items():
        variacao = random.uniform(-0.02, 0.02)
        preco_atual = info["preco"] * (1 + variacao)
        mudanca = preco_atual - info["preco"]
        pct = variacao * 100
        dados.append({
            "label": sym,
            "preco": preco_atual,
            "change": mudanca,
            "pct": pct,
            "high": preco_atual * 1.005,
            "low": preco_atual * 0.995
        })
    return dados

# Botão de atualização
if st.button('🔄 ATUALIZAR PREÇOS AGORA'):
    st.rerun()

# Exibição dos Cards
for item in gerar_dados_simulados():
    c_class = "pos" if item["change"] >= 0 else "neg"
    arrow = "▲" if item["change"] >= 0 else "▼"
    
    st.markdown(f"""
        <div class="card">
            <div class="symbol">{item['label']} <span style="font-size: 16px; color: #5a189a;">{arrow}</span></div>
            <div class="price">$ {item['preco']:,.2f}</div>
            <div class="{c_class}">{item['change']:+.2f} ({item['pct']:+.2f}%)</div>
            <div style="display: flex; gap: 40px; margin-top: 20px; border-top: 1px solid #1a1a1a; padding-top: 15px;">
                <div><div class="label">Máxima</div><div class="value">$ {item['high']:,.2f}</div></div>
                <div><div class="label">Mínima</div><div class="value">$ {item['low']:,.2f}</div></div>
            </div>
            <div class="label" style="margin-top: 20px;">Pressão de Compra</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Barra de pressão aleatória para o visual
    pressao = random.randint(30, 85)
    st.progress(pressao)
