import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Localizador de Ferramentas",
    layout="centered"
)
st.title("Localizador de Ferramentas da Oficina")
conn = sqlite3.connect("ferramentas.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS ferramentas (
    item TEXT PRIMARY KEY,
    categoria TEXT,
    armario TEXT,
    prateleira TEXT,
    maquina TEXT
)
""")
conn.commit()
def carregar_dados():
    return pd.read_sql("SELECT * FROM ferramentas", conn)
def salvar_item(item, categoria, armario, prateleira, maquina):
    cursor.execute("""
        INSERT OR REPLACE INTO ferramentas
        (item, categoria, armario, prateleira, maquina)
        VALUES (?, ?, ?, ?, ?)
    """, (item, categoria, armario, prateleira, maquina))
    conn.commit()
def excluir_item(item):
    cursor.execute("DELETE FROM ferramentas WHERE item = ?", (item,))
    conn.commit()
df = carregar_dados()
if "logado" not in st.session_state:
    st.session_state.logado = False

if "role" not in st.session_state:
    st.session_state.role = None
def autenticar(usuario, senha):
    usuarios = {
        "admin": {"senha": "1234", "role": "admin"}
    }
    if usuario in usuarios and usuarios[usuario]["senha"] == senha:
        return usuarios[usuario]["role"]
    return None
st.sidebar.header("Acesso Administrativo")

if not st.session_state.logado:
    usuario = st.sidebar.text_input("Usuário")
    senha = st.sidebar.text_input("Senha", type="password")

    if st.sidebar.button("Entrar"):
        role = autenticar(usuario, senha)
        if role == "admin":
            st.session_state.logado = True
            st.session_state.role = role
            st.sidebar.success("Admin logado")
            st.rerun()
        else:
            st.sidebar.error("Acesso negado")
else:
    st.sidebar.success("Administrador logado")
    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.session_state.role = None
        st.rerun()
st.header("🔍 Buscar Ferramenta")
busca = st.selectbox("Selecione a ferramenta que você deseja", df["item"])
if busca:
    resultado = df[df["item"].str.contains(busca, case=False, na=False)]
    if not resultado.empty:
        st.dataframe(resultado, use_container_width=True)
    else:
        st.warning("Item não encontrado")
st.divider()
if st.session_state.logado and st.session_state.role == "admin":
    st.header("🛠️ Gerenciamento de Itens")
    with st.form("cadastro"):
        nome = st.text_input("Nome do Item")
        categoria = st.selectbox(
            "Categoria", ["Ferramenta", "Insumo", "Acessório"]
        )
        armario = st.text_input("Armário")
        prateleira = st.text_input("Prateleira")
        maquina = st.text_input("Máquina")

        salvar = st.form_submit_button("Salvar / Atualizar")

        if salvar and nome:
            salvar_item(nome, categoria, armario, prateleira, maquina)
            st.success("Item salvo com sucesso")
            st.rerun()
    st.divider()
    st.subheader("❌ Excluir Item")
    if not df.empty:
        item_excluir = st.selectbox("Selecione o item", df["item"])

        if st.button("Excluir"):
            excluir_item(item_excluir)
            st.success("Item excluído")
            st.rerun()
    else:
        st.info("Nenhum item cadastrado")

    st.divider()
    st.subheader("📋 Banco de Dados")
    st.dataframe(df, use_container_width=True)

