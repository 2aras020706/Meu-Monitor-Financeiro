import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# 1. Configuração (Deve ser a primeira linha)
st.set_page_config(layout="wide")

# 2. CSS para o visual e alertas (Mantendo seu estilo)
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: white; }
    .card { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 20px; text-align: center; }
    .vix-alert { background-color: #490e0e; border: 2px solid #f85149; border-radius: 10px; padding: 20px; text-align: center; animation: pulse 1.5s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# 3. Funções que geram os dados NA HORA para evitar NameError
def obter_dados_frescos():
    """Gera todos os dados necessários em um único dicionário"""
    return {
        "sp_preco": 6893.72 + np.random.uniform(-5, 5),
        "nq_preco": 25678.10 + np.random.uniform(-20, 20),
        "vix": round(np.random.uniform(15, 25), 2),
        "pressao_sp": np.random.randint(20, 90),
        "pressao_nq": np.random.randint(20, 90),
        "df": pd.DataFrame({
            "Tempo": pd.date_range(start="now", periods=10, freq="min"),
            "Valor": np.random.randn(10).cumsum() + 100
        })
    }

def som_alerta():
    st.components.v1.html("<script>var c=new AudioContext();var o=c.createOscillator();o.connect(c.destination);o.start();o.stop(c.currentTime+0.3);</script>", height=0)

# 4. Loop Principal
st.title("📟 Terminal de Monitoramento Financeiro")
placeholder = st.empty() # Espaço que será limpo e atualizado

while True:
    # Capturamos os dados primeiro. Agora 'dados' existe com certeza.
    dados = obter_dados_frescos()
    
    with placeholder.container():
        col1, col2, col3 = st.columns(3)

        # ATIVO 1: SP500
        with col1:
            st.markdown(f'<div class="card"><h3>S&P 500</h3><h2>{dados["sp_preco"]:.2f}</h2></div>', unsafe_allow_html=True)
            # Criamos o gráfico usando os dados que acabamos de gerar
            fig1 = px.line(dados["df"], x="Tempo", y="Valor", template="plotly_dark")
            fig1.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_visible=False)
            st.plotly_chart(fig1, use_container_width=True, key="grafico_sp") # KEY ÚNICA
            st.write(f"Pressão Compra: {dados['pressao_sp']}%")
            st.progress(dados['pressao_sp'] / 100)

        # ATIVO 2: NASDAQ
        with col2:
            st.markdown(f'<div class="card"><h3>NASDAQ</h3><h2>{dados["nq_preco"]:.2f}</h2></div>', unsafe_allow_html=True)
            fig2 = px.line(dados["df"], x="Tempo", y="Valor", template="plotly_dark")
            fig2.update_traces(line_color="#0088ff")
            fig2.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_visible=False)
            st.plotly_chart(fig2, use_container_width=True, key="grafico_nq") # KEY ÚNICA
            st.write(f"Pressão Compra: {dados['pressao_nq']}%")
            st.progress(dados['pressao_nq'] / 100)

        # VIX E ALERTAS
        with col3:
            if dados["vix"] > 22:
                st.markdown(f'<div class="vix-alert"><h3>⚠️ VIX ALTO</h3><h2>{dados["vix"]}</h2></div>', unsafe_allow_html=True)
                som_alerta()
            else:
                st.markdown(f'<div class="card"><h3>VIX</h3><h2>{dados["vix"]}</h2><p>Estável</p></div>', unsafe_allow_html=True)

    time.sleep(1) # Atualiza a cada 1 segundo
