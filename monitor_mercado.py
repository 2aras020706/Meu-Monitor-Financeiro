import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Definição da Função (deve vir antes de ser chamada)
def criar_grafico(df):
    # Exemplo simples de gráfico usando Plotly
    fig = px.line(df, x='Data', y='Valor', title="Variação do Ativo")
    return fig

# 2. Criação dos Dados (O que está faltando no seu erro)
# Certifique-se de que o nome 'df_exemplo' seja exatamente igual ao da linha 51
data = {
    'Data': pd.date_range(start='2023-01-01', periods=10),
    'Valor': [10, 12, 11, 15, 14, 18, 17, 20, 19, 22]
}
df_exemplo = pd.DataFrame(data)

# 3. Layout do Streamlit
col1, col2 = st.columns(2)

with col1:
    st.metric("SP500", "6893.72", "+1.2%")
    
    # Linha 51: Agora o df_exemplo já existe acima!
    st.plotly_chart(criar_grafico(df_exemplo))
    
    # Medidor de Pressão
    st.progress(80, text="Pressão")
