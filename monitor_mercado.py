import streamlit as st
import pandas as pd
import random
import time

# Configuração da página
st.set_page_config(page_title="Monitor Pro com Alerta Sonoro", layout="wide")

# --- DESIGN E ALERTAS (CSS) ---
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
</style>
""", unsafe_allow_html=True)

# Função para o Alerta Sonoro (HTML/JS)
def tocar_alerta():
    # Gera um som de "Beep" via Browser
    st.components.v1.html(
        """
        <script>
        var context = new (window.AudioContext || window.webkitAudioContext)();
        var osc = context.createOscillator();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(440, context.currentTime);
        osc.connect(context.destination);
        osc.start();
        osc.stop(context.currentTime + 0.5);
        </script>
        """,
        height=0,
    )

def gerar_dados():
    vix = round(random.uniform(16.0, 24.0), 2)
    sp500 = round(6896.12 + random.uniform(-10, 10), 2)
    nasdaq = round(25694.50 + random.uniform(-40, 40), 2)
    pressao = random.randint(10, 95)
    return {"SP500": sp500, "NASDAQ": nasdaq, "VIX": vix, "PRESSAO": pressao}

st.title("📟 MONITOR COM ALERTA SONORO")
st.info("Nota: Clique em qualquer lugar da página uma vez para o navegador permitir o som.")

placeholder = st.empty()

while True:
    with placeholder.container():
        d = gerar_dados()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="card"><h3>S&P 500 (ES)</h3><h2 style="color:#00ff00">{d["SP500"]}</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="card"><h3>NASDAQ (NQ)</h3><h2 style="color:#00ff00">{d["NASDAQ"]}</h2></div>', unsafe_allow_html=True)
        with col3:
            if d["VIX"] > 21:
                st.markdown(f'<div class="vix-danger"><h3>⚠️ VIX ALTO</h3><h2>{d["VIX"]}</h2></div>', unsafe_allow_html=True)
                tocar_alerta() # Dispara o som
            else:
                st.markdown(f'<div class="card"><h3>VIX</h3><h2 style="color:#ffaa00">{d["VIX"]}</h2></div>', unsafe_allow_html=True)

        # Medidor de Pressão
        st.write("")
        st.markdown(f"""
            <div class="card">
                <p><b>PRESSÃO ({d["PRESSAO"]}%)</b></p>
                <div style="background-color: #333; border-radius: 20px; height: 20px;">
                    <div style="background: linear-gradient(90deg, #ff4b4b {100-d["PRESSAO"]}%, #00ff00 {d["PRESSAO"]}%); 
                    width: 100%; height: 100%; border-radius: 20px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    time.sleep(2)
