import os
import math
import shutil
from fpdf import FPDF
from barcode import Code128
from barcode.writer import ImageWriter
from database import buscar_produto
import textwrap

# Constantes
PASTA_TEMP = "/tmp"
ORIGEM_LOGO = "LOGO.png"
DESTINO_LOGO = os.path.join(PASTA_TEMP, "LOGO.png")

# Garante que a logo seja copiada para a pasta temporária
if os.path.exists(ORIGEM_LOGO) and not os.path.exists(DESTINO_LOGO):
    shutil.copyfile(ORIGEM_LOGO, DESTINO_LOGO)







def gerar_codigo_barras(numero_serie, largura_mm=0.3):
    caminho_base = os.path.join(PASTA_TEMP, f"barcode_{numero_serie}")
    writer = ImageWriter()
    
    # Definindo opções de qualidade e legibilidade
    options = {
        "module_width": largura_mm,   # Largura da barra
        "module_height": 25.0,        # Altura da barra
        "quiet_zone": 6.5,            # Margem lateral
        "write_text": False,          # Oculta texto abaixo
        "dpi": 200,                   # Alta resolução
    }

    barcode = Code128(numero_serie, writer=writer)
    return barcode.save(caminho_base, options=options)



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
        pdf.set_font("Arial", size=8) # Fonte base para 'Dupla'

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

                barcode_path = gerar_codigo_barras(numero_serie)
                if os.path.exists(barcode_path):
                    pdf.image(barcode_path, x=10, y=y, w=80)

            elif tamanho == 'Dupla':
                margem_x_1 = 0
                margem_x_2 = 53  # 50mm + 3mm separação
                y_inicial = 2

                for margem_x in [margem_x_1, margem_x_2]:
                    y = y_inicial  # Resetar Y para cada etiqueta

                    #logo_path = os.path.join(PASTA_TEMP, "LOGO.png")
                    #if os.path.exists(logo_path):
                        #pdf.image(logo_path, x=margem_x + 2, y=y + 2, w=8) # Ajustando posição e tamanho da logo
                        #y += 6 # Menos espaço após a logo

                    pdf.set_font("Arial", size=6) # Diminuindo a fonte para código e série
                    pdf.set_xy(margem_x + 2, y)
                    pdf.cell(48, 4, f"Código: {codigo_produto}", ln=True) # Menor altura da célula
                    y += 4

                    pdf.set_xy(margem_x + 2, y)
                    pdf.cell(48, 4, f"Nº Série: {numero_serie}", ln=True) # Menor altura da célula
                    y += 5 # Menos espaço antes do código de barras

                    pdf.set_font("Arial", size=8) # Retorna para a fonte base para outros elementos (se houver no futuro)

                    barcode_path = gerar_codigo_barras(numero_serie)
                    if os.path.exists(barcode_path):
                        # Calculando a altura disponível e usando quase todo o espaço
                        barcode_altura_max = altura - y - 2 # Margem inferior de 2mm
                        barcode_largura = 48 # Largura razoável
                        barcode_x = margem_x + (50 - barcode_largura) / 2
                        pdf.image(barcode_path, x=barcode_x, y=y, w=barcode_largura, h=barcode_altura_max)

            else:
                margem_x = 3
                y = 3

                #logo_path = os.path.join(PASTA_TEMP, "LOGO.png")
                #if os.path.exists(logo_path):
                #    pdf.image(logo_path, x=margem_x, y=y, w=14)

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

                barcode_path = gerar_codigo_barras(numero_serie)
                if os.path.exists(barcode_path):
                    barcode_largura = 64
                    barcode_x = margem_x + (largura - 2 * margem_x - barcode_largura) / 2
                    pdf.image(barcode_path, x=barcode_x, y=y, w=barcode_largura)

        nome_arquivo = os.path.join(PASTA_TEMP, f"etiquetas_lote_{i}.pdf")
        pdf.output(nome_arquivo)
        arquivos_gerados.append(nome_arquivo)

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
    pdf.set_font("Arial", size=8) # Fonte base para 'Dupla'
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

        barcode_path = gerar_codigo_barras(numero_serie)
        if os.path.exists(barcode_path):
            pdf.image(barcode_path, x=10, y=y, w=80)

    elif tamanho == 'Dupla':
        margem_x_1 = 0
        margem_x_2 = 53  # 50mm + 3mm separação
        y_inicial = 2

        for margem_x in [margem_x_1, margem_x_2]:
            y = y_inicial  # Resetar Y para cada etiqueta

            logo_path = os.path.join(PASTA_TEMP, "LOGO.png")
            if os.path.exists(logo_path):
                pdf.image(logo_path, x=margem_x + 2, y=y + 2, w=8) # Ajustando posição e tamanho da logo
                y += 6 # Menos espaço após a logo

            pdf.set_font("Arial", size=6) # Diminuindo a fonte para código e série
            pdf.set_xy(margem_x + 2, y)
            pdf.cell(48, 4, f"Código: {codigo_produto}", ln=True) # Menor altura da célula
            y += 4

            pdf.set_xy(margem_x + 2, y)
            pdf.cell(48, 4, f"Nº Série: {numero_serie}", ln=True) # Menor altura da célula
            y += 5 # Menos espaço antes do código de barras

            pdf.set_font("Arial", size=8) # Retorna para a fonte base para outros elementos (se houver no futuro)

            barcode_path = gerar_codigo_barras(numero_serie)
            if os.path.exists(barcode_path):
                # Calculando a altura disponível e usando quase todo o espaço
                barcode_altura_max = altura - y - 2 # Margem inferior de 2mm
                barcode_largura = 48 # Largura razoável
                barcode_x = margem_x + (50 - barcode_largura) / 2
                pdf.image(barcode_path, x=barcode_x, y=y, w=barcode_largura, h=barcode_altura_max)

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

        barcode_path = gerar_codigo_barras(numero_serie)
        if os.path.exists(barcode_path):
            barcode_largura = 64
            barcode_x = margem_x + (largura - 2 * margem_x - barcode_largura) / 2
            pdf.image(barcode_path, x=barcode_x, y=y, w=barcode_largura)

    nome_arquivo = os.path.join(PASTA_TEMP, f"etiqueta_{numero_serie}.pdf")
    pdf.output(nome_arquivo)

    return nome_arquivo
