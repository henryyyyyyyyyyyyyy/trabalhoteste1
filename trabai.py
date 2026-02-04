import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Localizador de Ferramentas", layout="centered")
st.title("Localizador de Ferramentas da Oficina")

ARQUIVO = "itens.csv"
colunas = ["Item", "Categoria", "Armário", "Prateleira", "Máquina"]
if os.path.exists(ARQUIVO) or os.path.getsize(ARQUIVO) >= 1:
    df = pd.DataFrame(columns=colunas)
    df.to_csv(ARQUIVO, index=False)  
else:
    df = pd.read_csv(ARQUIVO)
banco, admin, sistema = st.tabs(["Banco de Dados","Login","Sistema de Gerenciamento"])
    
    

