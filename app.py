def tela_consultar_serie():
    st.subheader("Consulta de Números de Série")

    codigo = st.text_input("Código do Produto")
    data_inicio = st.date_input("Data Inicial")
    data_fim = st.date_input("Data Final")
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

            st.markdown(f"📄 Mostrando página **{pagina}** de **{total_paginas}**")

            for idx, serie in enumerate(series_pagina):
                numero_serie = serie["numero_serie"]
                data_geracao = serie["data_geracao"]
                unique_id = f"{codigo}_{numero_serie}_{idx}"

                col1, col2, col3 = st.columns([3, 1.5, 1.5])
                with col1:
                    st.write(f"📦 Nº Série: {numero_serie}\n\n🕒 Gerado em: {data_geracao}")

                with col2:
                    tamanho_individual = st.selectbox(
                        "Tamanho", ["Pequena", "Média", "Grande"], index=2, key=f"selectbox_{unique_id}"
                    )
                    if st.button("Reimprimir", key=f"reimprimir_{unique_id}"):
                        st.session_state.reimprimir_serie = (codigo, numero_serie, idx, tamanho_individual)

                with col3:
                    if (
                        st.session_state.reimprimir_serie 
                        and st.session_state.reimprimir_serie[:3] == (codigo, numero_serie, idx)
                    ):
                        produto = buscar_produto(codigo)
                        tamanho_individual = st.session_state.reimprimir_serie[3]
                        if produto:
                            caminho = gerar_etiqueta_pdf(produto, [numero_serie], tamanho_individual)[0]
                            with open(caminho, "rb") as file:
                                st.download_button(
                                    label="⬇️ Baixar",
                                    data=file,
                                    file_name=os.path.basename(caminho),
                                    mime="application/pdf",
                                    key=f"download_{unique_id}"
                                )
        else:
            st.warning("❌ Nenhum número de série encontrado para os critérios.")
