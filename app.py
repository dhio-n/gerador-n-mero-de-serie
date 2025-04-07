import streamlit as st
from database import *
from serial_generator import gerar_numero_serie
from etiqueta import gerar_etiqueta
from datetime import datetime

criar_tabelas()

st.title("Gerador de Números de Série - Centro de Distribuição")

opcao = st.sidebar.selectbox("Escolha a operação:", ["Gerar Série", "Consultar Série", "Cadastrar Produto"])

if opcao == "Cadastrar Produto":
    st.subheader("Cadastro de Produto")
    codigo = st.text_input("Código do Produto")
    nome = st.text_input("Nome do Produto")
    descricao = st.text_area("Descrição")
    if st.button("Cadastrar"):
        cadastrar_produto(codigo, nome, descricao)
        st.success("Produto cadastrado com sucesso!")

elif opcao == "Gerar Série":
    st.subheader("Gerar Número de Série")
    codigo = st.text_input("Digite o Código do Produto")
    if st.button("Gerar Série"):
        produto = buscar_produto(codigo)
        if produto:
            numero_serie = gerar_numero_serie(codigo)
            data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            salvar_serie(codigo, numero_serie, data)
            tamanho = st.selectbox("Tamanho da etiqueta", ["Pequena", "Média", "Grande"])
            caminho_pdf = gerar_etiqueta_pdf(produto, numero_serie, tamanho)

            with open(caminho_pdf, "rb") as file:
                st.download_button( label="📥 Baixar Etiqueta em PDF", data=file,file_name=os.path.basename(caminho_pdf),mime="application/pdf")

            st.success(f"Número de série gerado: {numero_serie}")
        else:
            st.warning("Produto não encontrado. Cadastre-o primeiro.")

elif opcao == "Consultar Série":
    st.subheader("Consulta de Número de Série")
    codigo = st.text_input("Código do Produto para Consulta")
    if st.button("Consultar"):
        serie = consultar_serie(codigo)
        if serie:
            st.info(f"Número de série: {serie[0]} (Gerado em: {serie[1]})")
        else:
            st.warning("Nenhum número de série encontrado.")
