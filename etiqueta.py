from fpdf import FPDF
import os
import math
from barcode import Code128
from barcode.writer import ImageWriter
from database import buscar_produto
import shutil

def gerar_etiqueta_pdf(produto, lista_series, tamanho='Pequena'):
    tamanho_map = {
        "Pequena": (70, 40),  # largura x altura
        "Média": (80, 50),
        "Grande": (100, 70)
    }

    largura, altura = tamanho_map.get(tamanho, (70, 40))
    nome_produto = produto["nome"]
    codigo_produto = produto["codigo"]

    lista_series = [
        {"numero_serie": s} if isinstance(s, str) else s
        for s in lista_series
    ]

    total_series = len(lista_series)
    etiquetas_por_pagina = 5
    pdf_count = math.ceil(total_series / etiquetas_por_pagina)
    arquivos_gerados = []

    for i in range(pdf_count):
        pdf = FPDF('P', 'mm', (largura, altura))
        pdf.set_auto_page_break(auto=False)
        pdf.set_font("Arial", size=8)

        for j in range(etiquetas_por_pagina):
            index = i * etiquetas_por_pagina + j
            if index >= total_series:
                break

            numero_serie = lista_series[index]["numero_serie"]
            pdf.add_page()

            margem_x = 3
            y = 3

            # Logo
            logo_path = os.path.join(PASTA_TEMP, "LOGO.png")
            if os.path.exists(logo_path):
                pdf.image(logo_path, x=margem_x, y=y, w=14)

            # Nome do produto ao lado da logo
            pdf.set_xy(margem_x + 16, y)
            nome_linhas = [nome_produto[i:i+22] for i in range(0, len(nome_produto), 22)]
            for linha in nome_linhas[:2]:
                pdf.cell(0, 4, linha, ln=True)

            y += 12

            # Código do produto
            pdf.set_xy(margem_x, y)
            pdf.cell(0, 4, f"Código: {codigo_produto}", ln=True)
            y += 4

            # Nº Série
            pdf.set_xy(margem_x, y)
            pdf.cell(0, 4, f"Nº Série: {numero_serie}", ln=True)
            y += 6

            # Código de barras
            barcode_path = gerar_codigo_barras(numero_serie)
            if os.path.exists(barcode_path):
                pdf.image(barcode_path, x=10, y=y, w=50)

        nome_arquivo = os.path.join(PASTA_TEMP, f"etiquetas_lote_{i}.pdf")
        pdf.output(nome_arquivo)
        arquivos_gerados.append(nome_arquivo)

    return arquivos_gerados
