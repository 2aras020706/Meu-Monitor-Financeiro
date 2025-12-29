import streamlit as st
import pandas as pd
import random
import time
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Monitor Financeiro Pro", layout="wide")

# --- DESIGN CSS ---
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
    /* Estilo da barra de progresso customizada */
    .progress-container {
        background-color: #333;
        border-radius: 10px;
        height: 12px;
        width: 100%;
        margin-top: 10px;
    }
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease-in-out;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNÇÕES DE APOIO ---
def gerar_dados_ativos():
    """Gera dados de preço, volume e calcula a pressão baseada no volume"""
    # Simulando volumes (Compra e Venda)
    vol_compra = random.randint(100, 1000)
    vol_venda = random.randint(100, 1000)
    total_vol = vol_compra + vol_venda
    pressao = round((vol_compra / total_vol) * 100) # Porcentagem de força compradora
    
    # Gerando histórico para o gráfico
    df = pd.DataFrame({
        "Data": pd.date_range(start="2023-01-01", periods=12, freq="H"),
        "Valor": [random.uniform(100, 110) for _ in range(12)]
    })
    
    return {"pressao": pressao, "df": df, "vol": total_vol}

def criar_grafico(df, cor_linha):
    fig = px.line(df, x="Data", y="Valor")
    fig.update_traces(line_color=cor_linha, line_width=2)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        height=150,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    return fig

def barra_pressao(porcentagem):
    """Renderiza uma barra de pressão dinâmica (Vermelho para venda, Verde para compra)"""
    cor = "#00ff00" if porcentagem > 50 else "#ff4b4b"
    return f"""
    <div style="margin-top:15px;">
        <p style="margin:0; font-size:12px; color:#aaa;">PRESSÃO DE VOLUME: {porcentagem}%</p>
        <div class="progress-container">
            <div class="progress-bar" style="width: {porcentagem}%; background-color: {cor};"></div>
        </div>
    </div>
    """

# --- LOOP PRINCIPAL ---
placeholder = st.empty()

while True:
    with placeholder.container():
        st.title("📟 MONITOR DE PRESSÃO POR ATIVO")
        
        col1, col2, col3 = st.columns(3)
        
        # Ativo 1: SP500
        dados_sp = gerar_dados_ativos()
        with col1:
            st.markdown(f"""
                <div class="card">
                    <h3>S&P 500</h3>
                    <h2 style="color:#00ff00">{6893 + random.uniform(-5, 5):.2f}</h2>
                    {barra_pressao(dados_sp['pressao'])}
                </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(criar_grafico(dados_sp['df'], "#00ff00"), use_container_width=True, key="graf_sp")

        # Ativo 2: NASDAQ
        dados_nasdaq = gerar_dados_ativos()
        with col2:
            st.markdown(f"""
                <div class="card">
                    <h3>NASDAQ</h3>
                    <h2 style="color:#00ff00">{25678 + random.uniform(-20, 20):.2f}</h2>
                    {barra_pressao(dados_nasdaq['pressao'])}
                </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(criar_grafico(dados_nasdaq['df'], "#0088ff"), use_container_width=True, key="graf_nq")

        # Ativo 3: VIX (Volatilidade)
        vix_val = round(random.uniform(18, 25), 2)
        with col3:
            if vix_val > 22:
                st.markdown(f'<div class="vix-danger"><h3>⚠️ VIX ALTO</h3><h2>{vix_val}</h2></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="card"><h3>VIX</h3><h2 style="color:#ffaa00">{vix_val}</h2></div>', unsafe_allow_html=True)

    time.sleep(1)
