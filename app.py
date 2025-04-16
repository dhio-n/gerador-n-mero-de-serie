
from fpdf import FPDF
import os
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image

def gerar_codigo_barras(numero_serie, caminho_imagem):
    codigo = Code128(numero_serie, writer=ImageWriter())
    codigo.save(caminho_imagem[:-4])  # salva sem a extensão .png duplicada

def gerar_etiqueta_pdf(produto, series, tamanho="Grande"):
    nome_produto = produto['nome']
    codigo_produto = produto['codigo']
    arquivos_pdf = []

    for i, numero_serie in enumerate(series):
        if tamanho == "Dupla 5x3":
            pdf = FPDF("P", "mm", (50, 30))
            pdf.add_page()
            pdf.set_auto_page_break(0)
            caminho_imagem = f"barcode_{numero_serie}.png"
            gerar_codigo_barras(numero_serie, caminho_imagem)
            for x_offset in [0, 25.5]:  # margem de 3mm entre etiquetas
                pdf.image("LOGO2.png", x=x_offset+1, y=1, w=8)
                pdf.set_font("Arial", size=6)
                pdf.set_xy(x_offset+1, 10)
                pdf.multi_cell(23, 3, f"{nome_produto}", border=0)
                pdf.set_xy(x_offset+1, 16)
                pdf.set_font("Arial", size=7)
                pdf.cell(23, 3, f"{codigo_produto} - {numero_serie}", ln=1)
                pdf.image(caminho_imagem, x=x_offset+1, y=19, w=22)
            os.remove(caminho_imagem)
            nome_arquivo = f"etiqueta_{numero_serie}_dupla.pdf"
        else:
            largura, altura = (70, 30) if tamanho == "Pequena" else (100, 50) if tamanho == "Média" else (100, 70)
            pdf = FPDF("P", "mm", (largura, altura))
            pdf.add_page()
            pdf.set_auto_page_break(0)
            caminho_imagem = f"barcode_{numero_serie}.png"
            gerar_codigo_barras(numero_serie, caminho_imagem)
            pdf.image("LOGO2.png", x=2, y=2, w=15)
            y_offset = 20 if tamanho == "Grande" else 16 if tamanho == "Média" else 14
            if tamanho == "Grande":
                pdf.set_font("Arial", size=10)
                pdf.set_xy(2, 15)
                pdf.multi_cell(0, 5, f"{nome_produto}", border=0)
            pdf.set_font("Arial", size=8)
            pdf.set_xy(2, y_offset)
            pdf.cell(0, 5, f"{codigo_produto} - {numero_serie}", ln=1)
            pdf.image(caminho_imagem, x=2, y=y_offset+6, w=largura - 4)
            os.remove(caminho_imagem)
            nome_arquivo = f"etiqueta_{numero_serie}.pdf"

        pdf.output(nome_arquivo)
        arquivos_pdf.append(nome_arquivo)

    return arquivos_pdf
