import os
import math
import shutil
from fpdf import FPDF
from database import buscar_produto
import qrcode

# Constantes
PASTA_TEMP = "/tmp"
ORIGEM_LOGO = "LOGO.png"
DESTINO_LOGO = os.path.join(PASTA_TEMP, "LOGO.png")

# Garante que a logo seja copiada para a pasta temporária
if os.path.exists(ORIGEM_LOGO) and not os.path.exists(DESTINO_LOGO):
    shutil.copyfile(ORIGEM_LOGO, DESTINO_LOGO)


def gerar_qrcode(numero_serie, tamanho_caixa=10, borda=4):
    os.makedirs(PASTA_TEMP, exist_ok=True)
    caminho_arquivo = os.path.join(PASTA_TEMP, f"qrcode_{numero_serie}.png")

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=tamanho_caixa,
        border=borda
    )

    qr.add_data(numero_serie)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(caminho_arquivo)

    return caminho_arquivo


def gerar_etiqueta_pdf(produto, lista_series, tamanho='Pequena'):
    tamanho_map = {
        "Pequena": (70, 40),
        "Média": (80, 50),
        "Grande": (100, 70),
        "Dupla": (103, 30)
    }

    largura, altura = tamanho_map.get(tamanho, (70, 40))
    nome_produto = produto["nome"]
    codigo_produto = produto["codigo"]

    lista_series = [
        {"numero_serie": s} if isinstance(s, str) else s
        for s in lista_series
    ]

    total_series = len(lista_series)
    etiquetas_por_pagina = 5 if tamanho != 'Dupla' else 3
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

            if tamanho == 'Grande':
                y = 4
                logo_path = os.path.join(PASTA_TEMP, "LOGO.png")
                if os.path.exists(logo_path):
                    pdf.image(logo_path, x=5, y=y, w=20)
                y += 10

                pdf.set_xy(5, y)
                nome_linhas = [nome_produto[i:i+35] for i in range(0, len(nome_produto), 35)]
                for linha in nome_linhas:
                    pdf.cell(0, 5, linha, ln=True)
                    y += 5

                pdf.set_xy(5, y)
                pdf.cell(0, 5, f"Código: {codigo_produto}", ln=True)
                y += 5

                pdf.set_xy(5, y)
                pdf.cell(0, 5, f"Nº Série: {numero_serie}", ln=True)
                y += 7

                qr_path = gerar_qrcode(numero_serie)
                if os.path.exists(qr_path):
                    pdf.image(qr_path, x=10, y=y, w=30)

            elif tamanho == 'Dupla':
                margem_x_1 = 0
                margem_x_2 = 53
                y_inicial = 2
        
                for margem_x in [margem_x_1, margem_x_2]:
                    y = y_inicial
        
                    logo_path = os.path.join(PASTA_TEMP, "LOGO.png")
                    if os.path.exists(logo_path):
                        pdf.image(logo_path, x=margem_x + 2, y=y + 2, w=8)
                        y += 6
        
                    pdf.set_font("Arial", size=8)
                    pdf.set_xy(margem_x + 2, y)
                    pdf.cell(48, 4, f"Código: {codigo_produto}", ln=True)
                    y += 4
        
                    pdf.set_xy(margem_x + 2, y)
                    pdf.cell(48, 4, f"Nº Série: {numero_serie}", ln=True)
                    y += 5
        
                    pdf.set_font("Arial", size=8)
        
                    qr_path = gerar_qrcode(numero_serie)
                    if os.path.exists(qr_path):
                        qr_altura_max = altura - y - 2
                        qr_largura = 22
                        qr_x = margem_x + (50 - qr_largura) / 2
                        pdf.image(qr_path, x=qr_x, y=y, w=qr_largura, h=qr_altura_max)
        
            else:
                margem_x = 3
                y = 3
        
                logo_path = os.path.join(PASTA_TEMP, "LOGO.png")
                if os.path.exists(logo_path):
                    pdf.image(logo_path, x=margem_x, y=y, w=14)
        
                pdf.set_xy(margem_x + 16, y)
                nome_linhas = [nome_produto[i:i+22] for i in range(0, len(nome_produto), 22)]
                for linha in nome_linhas[:2]:
                    pdf.cell(0, 4, linha, ln=True)
        
                y += 12
                pdf.set_xy(margem_x, y)
                pdf.cell(0, 4, f"Código: {codigo_produto}", ln=True)
                y += 4
                pdf.set_xy(margem_x, y)
                pdf.cell(0, 4, f"Nº Série: {numero_serie}", ln=True)
                y += 6
        
                qr_path = gerar_qrcode(numero_serie)
                if os.path.exists(qr_path):
                    qr_largura = 24
                    qr_x = margem_x + (largura - 2 * margem_x - qr_largura) / 2
                    pdf.image(qr_path, x=qr_x, y=y, w=qr_largura)
        
            nome_arquivo = os.path.join(PASTA_TEMP, f"etiqueta_{numero_serie}.pdf")
            pdf.output(nome_arquivo)


    return arquivos_gerados


def reimprimir_etiqueta_individual(produto, numero_serie, tamanho='Pequena'):
    tamanho_map = {
        "Pequena": (70, 40),
        "Média": (80, 50),
        "Grande": (100, 70),
        "Dupla": (103, 30)
    }

    largura, altura = tamanho_map.get(tamanho, (70, 40))
    nome_produto = produto["nome"]
    codigo_produto = produto["codigo"]

    pdf = FPDF('P', 'mm', (largura, altura))
    pdf.set_auto_page_break(auto=False)
    pdf.set_font("Arial", size=8)
    pdf.add_page()

    if tamanho == 'Grande':
        y = 4
        logo_path = os.path.join(PASTA_TEMP, "LOGO.png")
        if os.path.exists(logo_path):
            pdf.image(logo_path, x=5, y=y, w=20)
        y += 10

        pdf.set_xy(5, y)
        nome_linhas = [nome_produto[i:i+35] for i in range(0, len(nome_produto), 35)]
        for linha in nome_linhas:
            pdf.cell(0, 5, linha, ln=True)
            y += 5

        pdf.set_xy(5, y)
        pdf.cell(0, 5, f"Código: {codigo_produto}", ln=True)
        y += 5

        pdf.set_xy(5, y)
        pdf.cell(0, 5, f"Nº Série: {numero_serie}", ln=True)
        y += 7

        qr_path = gerar_qrcode(numero_serie)
        if os.path.exists(qr_path):
            pdf.image(qr_path, x=10, y=y, w=30)

    elif tamanho == 'Dupla':
        margem_x_1 = 0
        margem_x_2 = 53
        y_inicial = 2

        for margem_x in [margem_x_1, margem_x_2]:
            y = y_inicial

            logo_path = os.path.join(PASTA_TEMP, "LOGO.png")
            if os.path.exists(logo_path):
                pdf.image(logo_path, x=margem_x + 2, y=y + 2, w=8)
                y += 6

            pdf.set_font("Arial", size=8)
            pdf.set_xy(margem_x + 2, y)
            pdf.cell(48, 4, f"Código: {codigo_produto}", ln=True)
            y += 4

            pdf.set_xy(margem_x + 2, y)
            pdf.cell(48, 4, f"Nº Série: {numero_serie}", ln=True)
            y += 5

            pdf.set_font("Arial", size=8)

            qr_path = gerar_qrcode(numero_serie)
            if os.path.exists(qr_path):
                qr_altura_max = altura - y - 2
                qr_largura = 22
                qr_x = margem_x + (50 - qr_largura) / 2
                pdf.image(qr_path, x=qr_x, y=y, w=qr_largura, h=qr_altura_max)

    else:
        margem_x = 3
        y = 3

        logo_path = os.path.join(PASTA_TEMP, "LOGO.png")
        if os.path.exists(logo_path):
            pdf.image(logo_path, x=margem_x, y=y, w=14)

        pdf.set_xy(margem_x + 16, y)
        nome_linhas = [nome_produto[i:i+22] for i in range(0, len(nome_produto), 22)]
        for linha in nome_linhas[:2]:
            pdf.cell(0, 4, linha, ln=True)

        y += 12
        pdf.set_xy(margem_x, y)
        pdf.cell(0, 4, f"Código: {codigo_produto}", ln=True)
        y += 4
        pdf.set_xy(margem_x, y)
        pdf.cell(0, 4, f"Nº Série: {numero_serie}", ln=True)
        y += 6

        qr_path = gerar_qrcode(numero_serie)
        if os.path.exists(qr_path):
            qr_largura = 24
            qr_x = margem_x + (largura - 2 * margem_x - qr_largura) / 2
            pdf.image(qr_path, x=qr_x, y=y, w=qr_largura)

    nome_arquivo = os.path.join(PASTA_TEMP, f"etiqueta_{numero_serie}.pdf")
    pdf.output(nome_arquivo)

    return nome_arquivo
