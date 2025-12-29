# 1. Crie o espaço vazio FORA do loop
placeholder = st.empty()

# 2. Inicie o loop de atualização
while True:
    with placeholder.container():
        # Gere seus dados aqui (exemplo)
        dados = gerar_dados_simulados() 
        
        # Crie as colunas para os cards
        col1, col2, col3 = st.columns(3)
        
        # Exemplo de preenchimento de um card
        with col1:
            st.markdown(f"""
                <div class="card">
                    <h3>WIN</h3>
                    <p>{dados['WIN']}</p>
                </div>
            """, unsafe_allow_html=True)
            
        # Repita para col2 e col3...

    # 3. O PASSO MAIS IMPORTANTE: O tempo de espera
    time.sleep(2)
