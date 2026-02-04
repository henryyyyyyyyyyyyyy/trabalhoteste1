import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Localizador de Ferramentas",
    layout="centered"
)

st.title("Localizador de Ferramentas da Oficina")

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(
        columns=["Item", "Categoria", "Armário", "Prateleira", "Máquina"]
    )

if "logado" not in st.session_state:
    st.session_state.logado = False

if "role" not in st.session_state:
    st.session_state.role = None

df = st.session_state.df

def autenticar(usuario, senha):
    usuarios = {
        "admin": {"senha": "1234", "role": "admin"},
        "user": {"senha": "abcd", "role": "user"}
    }
    if usuario in usuarios and usuarios[usuario]["senha"] == senha:
        return usuarios[usuario]["role"]
    return None

banco, admin, sistema = st.tabs(
    ["Banco de Dados", "Login", "Sistema de Gerenciamento"]
)

with admin:
    st.header("Área Administrativa")

    if not st.session_state.logado:
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            role = autenticar(usuario, senha)
            if role == "admin":
                st.session_state.logado = True
                st.session_state.role = role
                st.success("Login realizado")
                st.rerun()
            else:
                st.error("Acesso negado")
    else:
        st.success("Administrador logado")

        if st.button("Sair"):
            st.session_state.logado = False
            st.session_state.role = None
            st.rerun()

with sistema:
    if st.session_state.logado:
        st.header("Cadastrar Item")

        with st.form("cadastro"):
            nome = st.text_input("Nome do Item")
            categoria = st.selectbox(
                "Categoria",
                ["Ferramenta", "Insumo", "Acessório"]
            )
            armario = st.text_input("Armário")
            prateleira = st.text_input("Prateleira")
            maquina = st.text_input("Máquina")

            salvar = st.form_submit_button("Salvar")

            if salvar and nome and armario and prateleira:
                novo = {
                    "Item": nome,
                    "Categoria": categoria,
                    "Armário": armario,
                    "Prateleira": prateleira,
                    "Máquina": maquina
                }
                st.session_state.df = pd.concat(
                    [df, pd.DataFrame([novo])],
                    ignore_index=True
                )
                st.success("Item cadastrado")

        st.divider()

        busca = st.text_input("Buscar item")

        if busca:
            r = df[df["Item"].str.contains(busca, case=False, na=False)]
            if not r.empty:
                for _, i in r.iterrows():
                    st.markdown(
                        f"**Item:** {i['Item']}  \n"
                        f"**Categoria:** {i['Categoria']}  \n"
                        f"**Armário:** {i['Armário']}  \n"
                        f"**Prateleira:** {i['Prateleira']}  \n"
                        f"**Máquina:** {i['Máquina']}"
                    )
            else:
                st.error("Item não encontrado")
    else:
        st.warning("Faça login para acessar")

with banco:
    st.dataframe(df, use_container_width=True)
