import os
import fitz
from pathlib import Path

def extrair_texto_pdf(caminho_pdf):
    try:
        if not os.path.exists(caminho_pdf):
            return f"Erro: Arquivo {caminho_pdf} não encontrado."
        
        doc = fitz.open(caminho_pdf)
        texto = ""
        
        for pagina in doc:
            texto += pagina.get_text()
        
        doc.close()
        
        return texto
    except Exception as e:
        return f"Erro ao extrair texto do PDF {caminho_pdf}: {str(e)}"

def obter_caminho_pdf_por_materia(materia):
    arquivos_pdf = {
        "matematica": "matematica.pdf",
        "fisica": "fisica.pdf",
        "quimica": "quimica.pdf",
        "biologia": "biologia.pdf"
    }
    
    nome_arquivo = arquivos_pdf.get(materia)
    if not nome_arquivo:
        return None
    
    caminho_pdf = os.path.join("documents", materia, nome_arquivo)
    
    if not os.path.exists(caminho_pdf):
        print(f"AVISO: Arquivo PDF para a matéria {materia} não encontrado: {caminho_pdf}")
        return None
    
    return caminho_pdf
