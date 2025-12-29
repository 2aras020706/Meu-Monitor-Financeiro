import streamlit as st
import pandas as pd
import random
import time
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(page_title="Terminal Financeiro Pro", layout="wide")

# 2. CSS para Design, Alertas e Barras de Pressão
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
        margin-bottom: 10px;
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
        transition: width 0.5s ease;
    }
</style>
""", unsafe_allow_html=True)

# 3. Funções de Suporte
def tocar_alerta():
    """Gera o beep sonoro via JavaScript"""
    st.components.v1.html("""
        <script>
        var context = new (window.AudioContext || window.webkitAudioContext)();
        var osc = context.createOscillator();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(440, context.currentTime);
        osc.connect(context.destination);
        osc.start();
        osc.stop(context.currentTime + 0.5);
        </script>
        """, height=0)

def gerar_dados_ativo():
    """Gera dados individuais para cada gráfico e medidor"""
    pressao = random.randint(10, 95)
    df = pd.DataFrame({
        "Data": pd.date_range(start="2023-01-01", periods=15, freq="H"),
        "Valor": [random.uniform(90, 110) for _ in range(15)]
    })
    return pressao, df

def criar_grafico(df, cor):
    fig = px.line(df, x="Data", y="Valor")
    fig.update_traces(line_color=cor, line_width=2)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False, margin=dict(l=0, r=0, t=0, b=0), height=120,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    return fig

def render_pressao(porcentagem):
    cor = "#00ff00" if porcentagem > 50 else "#ff4b4b"
    return f"""
    <div style="margin-top:10px;">
        <p style="margin:0; font-size:11px; color:#aaa; text-align:left;">PRESSÃO DE VOLUME: {porcentagem}%</p>
        <div class="progress-container">
            <div class="progress-bar" style="width: {porcentagem}%; background-color: {cor};"></div>
        </div>
    </div>
    """

# 4. Interface e Loop
st.title("📟 TERMINAL FINANCEIRO PRO")
st.info("Clique na tela uma vez para habilitar o áudio dos alertas.")

placeholder = st.empty()

while True:
    with placeholder.container():
        # Gerar valores globais
        vix_atual = round(random.uniform(17, 24), 2)
        
        # Layout de 3 colunas (S&P, NASDAQ, VIX)
        col1, col2, col3 = st.columns(3)
        
        # --- COLUNA 1: S&P 500 ---
        p_sp, df_sp = gerar_dados_ativo()
        with col1:
            st.markdown(f'<div class="card"><h3>S&P 500</h3><h2 style="color:#00ff00">6893.72</h2>{render_pressao(p_sp)}</div>', unsafe_allow_html=True)
            st.plotly_chart(criar_grafico(df_sp, "#00ff00"), use_container_width=True, key="chart_sp")
            
        # --- COLUNA 2: NASDAQ ---
        p_nq, df_nq = gerar_dados_ativo()
        with col2:
            st.markdown(f'<div class="card"><h3>NASDAQ</h3><h2 style="color:#00ff00">25678.10</h2>{render_pressao(p_nq)}</div>', unsafe_allow_html=True)
            st.plotly_chart(criar_grafico(df_nq, "#0088ff"), use_container_width=True, key="chart_nq")
            
        # --- COLUNA 3: VIX E ALERTAS ---
        with col3:
            if vix_atual > 21:
                st.markdown(f'<div class="vix-danger"><h3>⚠️ VIX ALTO</h3><h2>{vix_atual}</h2><p>RISCO ELEVADO</p></div>', unsafe_allow_html=True)
                tocar_alerta()
            else:
                st.markdown(f'<div class="card"><h3>VIX (VOLATILIDADE)</h3><h2 style="color:#ffaa00">{vix_atual}</h2><p>MERCADO ESTÁVEL</p></div>', unsafe_allow_html=True)

    time.sleep(2)
