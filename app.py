import streamlit as st
from database import *
from serial_generator import gerar_numero_serie
from etiqueta import gerar_etiqueta_pdf
from datetime import datetime, time
import os

criar_tabelas()

st.set_page_config(page_title="Gerador de Números de Série", layout="centered")

st.title("Gerador de Números de Série - Centro de Distribuição")

opcao = st.sidebar.selectbox("Escolha a operação:", ["Gerar Série", "Consultar Série", "Cadastrar Produto"])

# Inicializa o estado de reimpressão
if "reimprimir_serie" not in st.session_state:
    st.session_state.reimprimir_serie = None

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
    quantidade = st.number_input("Quantidade de Números de Série", min_value=1, step=1, value=1)
    tamanho = "Grande"

    if st.button("Gerar Série"):
        produto = buscar_produto(codigo)
        if produto:
            series_geradas = []
            for _ in range(quantidade):
                numero_serie = gerar_numero_serie(codigo)
                data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                salvar_serie(codigo, numero_serie, data)
                series_geradas.append(numero_serie)

            arquivos = gerar_etiqueta_pdf(produto, series_geradas, tamanho)
            for arquivo in arquivos:
                with open(arquivo, "rb") as file:
                    st.download_button(
                        label=f"📥 Baixar {os.path.basename(arquivo)}",
                        data=file,
                        file_name=os.path.basename(arquivo),
                        mime="application/pdf"
                    )

            st.success(f"{quantidade} número(s) de série gerado(s) com sucesso!")
        else:
            st.warning("Produto não encontrado. Cadastre-o primeiro.")

elif opcao == "Consultar Série":
    st.subheader("Consulta de Números de Série")

    if "reimprimir_serie" not in st.session_state:
        st.session_state.reimprimir_serie = None

    codigo = st.text_input("Código do Produto")
    data_inicio = st.date_input("Data Inicial", value=None)
    data_fim = st.date_input("Data Final", value=None)
    numero_serie_input = st.text_input("Buscar por Número de Série")
    pagina = st.number_input("Página", min_value=1, step=1, value=1)

    if st.button("Consultar") or codigo:
        filtros = {}
        if data_inicio:
            filtros['data_inicio'] = datetime.combine(data_inicio, time.min).strftime("%Y-%m-%d %H:%M:%S")
        if data_fim:
            filtros['data_fim'] = datetime.combine(data_fim, time.max).strftime("%Y-%m-%d %H:%M:%S")
        if numero_serie_input:
            filtros['numero_serie'] = numero_serie_input

        todas_series = consultar_series(codigo_produto=codigo, **filtros)

        if todas_series:
            total_paginas = (len(todas_series) + 49) // 50
            inicio = (pagina - 1) * 50
            fim = inicio + 50
            series_pagina = todas_series[inicio:fim]

            st.markdown(f"Mostrando página {pagina} de {total_paginas}")

            for numero_serie, data_geracao in series_pagina:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"📦 Nº Série: {numero_serie} - Gerado em: {data_geracao}")
                with col2:
                    if st.button("Reimprimir", key=f"reimprimir_{numero_serie}"):
                        st.session_state.reimprimir_serie = (codigo, numero_serie)
                with col3:
                    if st.session_state.reimprimir_serie == (codigo, numero_serie):
                        produto = buscar_produto(codigo)
                        if produto:
                            caminho = gerar_etiqueta_pdf(produto, [numero_serie])[0]
                            with open(caminho, "rb") as file:
                                st.download_button(
                                    label="⬇️ Baixar",
                                    data=file,
                                    file_name=os.path.basename(caminho),
                                    mime="application/pdf",
                                    key=f"download_{numero_serie}"
                                )
        else:
            st.warning("Nenhum número de série encontrado para os critérios.")
