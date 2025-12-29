import streamlit as st
import pandas as pd
import time
import random

# 1. Configuração da página
st.set_page_config(page_title="Monitor de Mercado Simulado", layout="wide")

# 2. CSS (Mantenha o seu CSS original aqui)
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    .card {
        background-color: #1a1a1a;
        border: 2px solid #5a189a;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 0 20px rgba(90, 24, 154, 0.5);
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("MONITOR DE MERCADO")

# 3. Função para simular dados
def gerar_dados_simulados():
    ativos = ["WIN (Mini Ibovespa)", "ESI (S&P 500)", "NQI (Nasdaq 100)"]
    dados = []
    for ativo in ativos:
        preco = random.uniform(100000, 130000) if "WIN" in ativo else random.uniform(4000, 18000)
        variacao = random.uniform(-1.5, 1.5)
        dados.append({"Ativo": ativo, "Preço": preco, "Variação": variacao})
    return dados

# 4. O segredo para não travar: Placeholder
# Criamos um único lugar na tela que será limpo e atualizado
placeholder = st.empty()

# Loop de atualização
while True:
    with placeholder.container():
        dados_atuais = gerar_dados_simulados()
        
        # Criamos colunas para os cards ficarem lado a lado (opcional)
        cols = st.columns(3)
        
        for i, item in enumerate(dados_atuais):
            cor_var = "#00ff00" if item['Variação'] >= 0 else "#ff0000"
            seta = "▲" if item['Variação'] >= 0 else "▼"
            
            with cols[i]:
                st.markdown(f"""
                <div class="card">
                    <h2 style='margin:0;'>{item['Ativo']}</h2>
                    <h1 style='margin:10px 0;'>{item['Preço']:,.2f}</h1>
                    <p style='color:{cor_var}; font-size:20px; font-weight:bold;'>
                        {seta} {item['Variação']:.2f}%
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    # Pausa antes da próxima atualização
    time.sleep(2)
