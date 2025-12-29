import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# Função para simular dados de volume e calcular pressão
def calcular_metricas_ativo():
    # Simulação de volume: compra vs venda
    vol_compra = np.random.randint(100, 1000)
    vol_venda = np.random.randint(100, 1000)
    total_vol = vol_compra + vol_venda
    pressao = int((vol_compra / total_vol) * 100)
    
    # Dados para o gráfico histórico
    df = pd.DataFrame({
        "Data": pd.date_range(start="2023-01-01", periods=20, freq="H"),
        "Valor": np.random.randn(20).cumsum() + 100
    })
    return pressao, df

def renderizar_ativo(nome, preco, cor, chave):
    pressao, df_exemplo = calcular_metricas_ativo() # Define a variável localmente para evitar NameError
    
    with st.container():
        st.metric(nome, preco, f"{np.random.uniform(-1, 1):.2f}%")
        
        # Gráfico Plotly customizado
        fig = px.line(df_exemplo, x="Data", y="Valor")
        fig.update_traces(line_color=cor)
        fig.update_layout(height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_visible=False)
        
        # Uso de chave única para evitar DuplicateElementId
        st.plotly_chart(fig, use_container_width=True, key=f"chart_{chave}")
        
        # Medidor de Pressão de Volume Individual
        cor_pressao = "green" if pressao > 50 else "red"
        st.markdown(f"**PRESSÃO DE VOLUME: {pressao}%**")
        st.progress(pressao / 100)

# Layout Principal
st.set_page_config(layout="wide")
placeholder = st.empty()

while True:
    with placeholder.container():
        col1, col2 = st.columns(2)
        
        with col1:
            renderizar_ativo("SP500", "6893.72", "#00FF00", "sp500")
            
        with col2:
            renderizar_ativo("NASDAQ", "25678.10", "#0088FF", "nasdaq")
            
    time.sleep(2)
