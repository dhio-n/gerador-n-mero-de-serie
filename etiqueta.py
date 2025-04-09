from fpdf import FPDF
import os
import math
from barcode import Code128
from barcode.writer import ImageWriter
from database import buscar_produto
import shutil

# Garante que a logo seja copiada para a pasta temporária (/tmp) ao rodar no Streamlit Cloud
PASTA_TEMP = "/tmp"
ORIGEM_LOGO = "LOGO.png"
DESTINO_LOGO = os.path.join(PASTA_TEMP, "LOGO.png")

# Copia a logo se ainda não estiver na pasta temporária
if os.path.exists(ORIGEM_LOGO) and not os.path.exists(DESTINO_LOGO):
    shutil.copyfile(ORIGEM_LOGO, DESTINO_LOGO)

def gerar_codigo_barras(numero_serie):
    caminho_base = os.path.join(PASTA_TEMP, f"barcode_{numero_serie}")
    barcode = Code128(numero_serie, writer=ImageWriter())
    barcode_path = barcode.save(caminho_base)
    return barcode_path

def gerar_etiqueta_pdf(produto, lista_series, tamanho='Grande'):
    tamanho_map = {
        "Pequena": (60, 40),
        "Média": (80, 50),
        "Grande": (100, 70)
    }

    largura, altura = tamanho_map.get(tamanho, (100, 70))
    nome_produto = produto["nome"]
    codigo_produto = produto["codigo"]

    total_series = len(lista_series)
    etiquetas_por_pagina = 5
    pdf_count = math.ceil(total_series / etiquetas_por_pagina)
    arquivos_gerados = []

    for i in range(pdf_count):
        pdf = FPDF('P', 'mm', (largura, altura))
        pdf.set_auto_page_break(auto=False)
        pdf.set_font("Arial", size=10)

        for j in range(etiquetas_por_pagina):
            index = i * etiquetas_por_pagina + j
            if index >= total_series:
                break

            numero_serie = lista_series[index]
            pdf.add_page()

            y = 4  # margem superior

            # Logo
            logo_path = os.path.join(PASTA_TEMP, "LOGO.png")
            if os.path.exists(logo_path):
                pdf.image(logo_path, x=5, y=y, w=20)
            y += 10  # espaço abaixo da logo

            # Nome do produto
            pdf.set_xy(5, y)
            nome_linhas = [nome_produto[i:i+35] for i in range(0, len(nome_produto), 35)]
            for linha in nome_linhas:
                pdf.cell(0, 5, linha, ln=True)
                y += 5

            # Código do produto
            pdf.set_xy(5, y)
            pdf.cell(0, 5, f"Código: {codigo_produto}", ln=True)
            y += 5

            # Número de série
            pdf.set_xy(5, y)
            pdf.cell(0, 5, f"Nº Série: {numero_serie}", ln=True)
            y += 7

            # Código de barras
            barcode_path = gerar_codigo_barras(numero_serie)
            if os.path.exists(barcode_path):
                pdf.image(barcode_path, x=10, y=y, w=80)

        nome_arquivo = os.path.join(PASTA_TEMP, f"etiquetas_lote_{i}.pdf")
        pdf.output(nome_arquivo)
        arquivos_gerados.append(nome_arquivo)

    return arquivos_gerados

def reimprimir_etiqueta_individual(codigo_produto, numero_serie, tamanho='Grande'):
    tamanho_map = {
        "Pequena": (60, 40),
        "Média": (80, 50),
        "Grande": (100, 70)
    }

    largura, altura = tamanho_map.get(tamanho, (100, 70))
    produto = buscar_produto(codigo_produto)

    if not produto:
        raise ValueError("Produto não encontrado.")

    nome_produto = produto["nome"]
    codigo_produto = produto["codigo"]

    pdf = FPDF('P', 'mm', (largura, altura))
    pdf.set_auto_page_break(auto=False)
    pdf.set_font("Arial", size=10)
    pdf.add_page()

    y = 4

    # Logo
    logo_path = os.path.join(PASTA_TEMP, "LOGO.png")
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=5, y=y, w=20)
    y += 10

    # Nome do produto
    pdf.set_xy(5, y)
    nome_linhas = [nome_produto[i:i+35] for i in range(0, len(nome_produto), 35)]
    for linha in nome_linhas:
        pdf.cell(0, 5, linha, ln=True)
        y += 5

    # Código
    pdf.set_xy(5, y)
    pdf.cell(0, 5, f"Código: {codigo_produto}", ln=True)
    y += 5

    # Nº de Série
    pdf.set_xy(5, y)
    pdf.cell(0, 5, f"Nº Série: {numero_serie}", ln=True)
    y += 7

    # Código de barras
    barcode_path = gerar_codigo_barras(numero_serie)
    if os.path.exists(barcode_path):
        pdf.image(barcode_path, x=10, y=y, w=80)

    nome_arquivo = os.path.join(PASTA_TEMP, f"etiqueta_{codigo_produto}_{numero_serie}.pdf")
    pdf.output(nome_arquivo)

    return nome_arquivo
