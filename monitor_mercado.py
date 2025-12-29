import streamlit as st
import pandas as pd
import time
import random

# ... (seu CSS e configurações iniciais)

# Criando os espaços vazios onde os dados vão aparecer
placeholder = st.empty()

while True:
    with placeholder.container():
        # Aqui você gera os dados (ou chama sua função gerar_dados_simulados)
        dados = {
            "Ativo": ["WIN", "ESI", "NQI"],
            "Preço": [random.randint(100, 200) for _ in range(3)]
        }
        df = pd.DataFrame(dados)
        
        # Exibindo os dados de forma estilizada
        for index, row in df.iterrows():
            st.markdown(f"""
            <div class="card">
                <h3>{row['Ativo']}</h3>
                <p>Preço: {row['Preço']}</p>
            </div>
            """, unsafe_allow_html=True)
            
    time.sleep(2) # Pausa de 2 segundos antes da próxima atualização
