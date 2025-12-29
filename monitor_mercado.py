import streamlit as st
import pandas as pd
import random
import time
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(page_title="Monitor Integrado Pro", layout="wide")

# 2. CSS para manter o visual escuro e os alertas
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    .card {
        background-color: #1a1a1a;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        color: white;
        margin-bottom: 5px;
    }
    .vix-danger {
        background-color: #4a0000;
        border: 2px solid #ff0000;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        color: #ff0000;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255, 0, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }
    }
</style>
""", unsafe_allow_html=True)

# 3. Funções de Suporte (Som e Dados)
def tocar_alerta():
    st.components.v1.html("<script>var context = new (window.AudioContext || window.webkitAudioContext)(); var osc = context.createOscillator(); osc.type = 'sine'; osc.frequency.setValueAtTime(440, context.currentTime); osc.connect(context.destination); osc.start(); osc.stop(context.currentTime + 0.5);</script>", height=0)

def gerar_dados_completos():
    # Gera dados para cada ativo separadamente para ser preciso
    def criar_df():
        return pd.DataFrame({
            "Data": pd.date_range(start="2023-01-01", periods=15, freq="H"),
            "Valor": [random.uniform(90, 110) for _ in range(15)]
        })
    
    return {
        "sp_preco": 6893.72 + random.uniform(-2, 2),
        "sp_pressao": random.randint(10, 95),
        "sp_df": criar_df(),
        "nq_preco": 25678.10 + random.uniform(-10, 10),
        "nq_pressao": random.randint(10, 95),
        "nq_df": criar_df(),
        "vix": round(random.uniform(17, 24), 2)
    }

# 4. Interface e Loop Infinito
st.title("📟 MONITOR FINANCEIRO TOTAL")
placeholder = st.empty()

while True:
    with placeholder.container():
        d = gerar_dados_completos()
        
        # Criando as 3 colunas para garantir que o VIX não suma
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'<div class="card"><h3>S&P 500</h3><h2 style="color:#00ff00">{d["sp_preco"]:.2f}</h2></div>', unsafe_allow_html=True)
            # Gráfico com chave única
            fig_sp = px.line(d["sp_df"], x="Data", y="Valor")
            fig_sp.update_traces(line_color="#00ff00").update_layout(height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_visible=False)
            st.plotly_chart(fig_sp, use_container_width=True, key="graf_sp_fixo")
            # Medidor de Pressão Individual
            st.write(f"Pressão: {d['sp_pressao']}%")
            st.progress(d["sp_pressao"] / 100)

        with col2:
            st.markdown(f'<div class="card"><h3>NASDAQ</h3><h2 style="color:#00ff00">{d["nq_preco"]:.2f}</h2></div>', unsafe_allow_html=True)
            # Gráfico com chave única
            fig_nq = px.line(d["nq_df"], x="Data", y="Valor")
            fig_nq.update_traces(line_color="#0088ff").update_layout(height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_visible=False)
            st.plotly_chart(fig_nq, use_container_width=True, key="graf_nq_fixo")
            # Medidor de Pressão Individual
            st.write(f"Pressão: {d['nq_pressao']}%")
            st.progress(d["nq_pressao"] / 100)

        with col3:
            # Lógica do VIX e Som integrada
            if d["vix"] > 21:
                st.markdown(f'<div class="vix-danger"><h3>⚠️ VIX ALTO</h3><h2>{d["vix"]}</h2><p>DISPARANDO ALERTA</p></div>', unsafe_allow_html=True)
                tocar_alerta()
            else:
                st.markdown(f'<div class="card"><h3>VIX</h3><h2 style="color:#ffaa00">{d["vix"]}</h2><p>NORMAL</p></div>', unsafe_allow_html=True)

    time.sleep(2)
