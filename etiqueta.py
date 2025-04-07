from fpdf import FPDF
import os

def gerar_etiqueta_pdf(produto, numero_serie, tamanho='Pequena'):
    tamanho_map = {
        "Pequena": (60, 40),
        "Média": (80, 50),
        "Grande": (100, 60)
    }

    largura, altura = tamanho_map.get(tamanho, (80, 50))

    pdf = FPDF('P', 'mm', (largura, altura))
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    pdf.cell(0, 10, f"Produto: {produto[2]}", ln=True)
    pdf.cell(0, 10, f"Código: {produto[1]}", ln=True)
    pdf.cell(0, 10, f"Nº Série: {numero_serie}", ln=True)

    nome_arquivo = f"etiqueta_{numero_serie}.pdf"
    caminho = os.path.join("data", nome_arquivo)
    pdf.output(caminho)
    return caminho
