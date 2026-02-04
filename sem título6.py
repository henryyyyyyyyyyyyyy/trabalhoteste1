import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Localizador de Ferramentas", layout="centered")
st.title("Localizador de Ferramentas da Oficina")

ARQUIVO = "itens.csv"
colunas = ["Item", "Categoria", "Armário", "Prateleira", "Máquina"]
if not os.path.exists(ARQUIVO) or os.path.getsize(ARQUIVO) == 0:
    df = pd.DataFrame(columns=colunas)
    df.to_csv(ARQUIVO, index=False)
else:
    df = pd.read_csv(ARQUIVO)
banco, admin,sistema = st.tabs(["Banco de Dados","Login","Sistema de Gerenciamento"])
with admin:
    if "logado" not in st.session_state:
        st.session_state.logado = False

    if "role" not in st.session_state:
        st.session_state.role = None
    def autenticar(usuario, senha):
        usuarios = {
            "admin": {"senha": "1234", "role": "admin"},
            "user": {"senha": "abcd", "role": "user"}
        }

        if usuario in usuarios and usuarios[usuario]["senha"] == senha:
            return usuarios[usuario]["role"]
        return None
    st.header("Área Administrativa")

    if not st.session_state.logado:
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            log = autenticar(usuario, senha)

            if log == "admin":
                st.session_state.logado = True
                st.session_state.role = log
                st.success("Login realizado")
                st.rerun()
            else:
                st.error("Acesso negado")

    else:
        st.success(f"Admin logado ({st.session_state.role})")

        if st.button("Sair"):
            st.session_state.logado = False
            st.session_state.role = None
            st.rerun()
with sistema:
    if st.session_state.logado == True:
        st.header("Cadastrar Item")
        with st.form("form_cadastro"):
            nome = st.text_input("Nome do Item")
            categoria = st.selectbox("Categoria", ["Ferramenta", "Insumo", "Acessório"])
            armario = st.text_input("Armário")
            prateleira = st.text_input("Prateleira")
            maquina = st.text_input("Máquina associada")
   
            salvar = st.form_submit_button("Salvar Item")
   
            if salvar:
                if nome and armario and prateleira:
                    novo_item = {
                        "Item": nome,
                        "Categoria": categoria,
                        "Armário": armario,
                        "Prateleira": prateleira,
                        "Máquina": maquina
                    }
   
                    df = pd.concat([df, pd.DataFrame([novo_item])], ignore_index=True)
                    df.to_csv(ARQUIVO, index=False)
                    st.success("Item cadastrado com sucesso!")
                else:
                    st.warning("Preencha Nome, Armário e Prateleira.")
   
        st.divider()
        st.header("Buscar Item")
        busca = st.text_input("Digite o nome do item")
   
        if busca:
            resultado = df[df["Item"].str.contains(busca, case=False, na=False)]
   
            if not resultado.empty:
                st.success("Item encontrado!")
                for _, item in resultado.iterrows():
                    st.markdown(f"""
                    **Item:** {item['Item']}  
                    **Categoria:** {item['Categoria']}  
                    **Armário:** {item['Armário']}  
                    **Prateleira:** {item['Prateleira']}  
                    **Máquina:** {item['Máquina']}
                    """)
            else:
                st.error("Item não encontrado.")
   
        st.divider()
   
        st.header("Alterar Item")
        nome_alt = st.text_input("Nome do item para alterar")
   
        if nome_alt:
            resultado = df[df["Item"].str.lower() == nome_alt.lower()]
   
            if not resultado.empty:
                st.success("Item encontrado! (edição pode ser adicionada aqui depois)")
            else:
                st.error("Item não encontrado.")
    else:
        st.warning('Login não efetuado!!')
with banco:
    st.header("Banco de Dados Completo")
    st.dataframe(df, use_container_width=True)  

st.divider()