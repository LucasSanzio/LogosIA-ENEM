import os
import fitz
from pathlib import Path

def extrair_texto_pdf(caminho_pdf):
    """Extrai texto de um arquivo PDF usando PyMuPDF (fitz)"""
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(caminho_pdf):
            return f"Erro: Arquivo {caminho_pdf} não encontrado."
        
        # Abre o documento PDF com fitz (PyMuPDF)
        doc = fitz.open(caminho_pdf)
        texto = ""
        
        # Extrai o texto de cada página
        for pagina in doc:
            texto += pagina.get_text()
        
        return texto
    except Exception as e:
        return f"Erro ao extrair texto do PDF {caminho_pdf}: {str(e)}"

def selecionar_pdf_por_materia(materia):
    """Seleciona o arquivo PDF correto com base na matéria escolhida pelo usuário"""
    # Mapeia as matérias para os nomes de arquivos correspondentes
    mapeamento_arquivos = {
        "matematica": "matematica.pdf",
        "fisica": "fisica.pdf",
        "quimica": "quimica.pdf",
        "biologia": "biologia.pdf"
    }
    
    # Verifica se a matéria está no mapeamento
    if materia not in mapeamento_arquivos:
        return None
    
    # Constrói o caminho completo para o arquivo PDF
    caminho_pdf = os.path.join("documents", mapeamento_arquivos[materia])
    
    # Verifica se o arquivo existe
    if not os.path.exists(caminho_pdf):
        print(f"ERRO: Arquivo PDF para a matéria {materia} não encontrado: {caminho_pdf}")
        return None
    
    return caminho_pdf

def carregar_conteudo_pdf_por_materia(materia):
    """Carrega o conteúdo do PDF correspondente à matéria selecionada"""
    caminho_pdf = selecionar_pdf_por_materia(materia)
    
    if not caminho_pdf:
        return f"Erro: Não foi possível encontrar o arquivo PDF para a matéria {materia}"
    
    try:
        texto = extrair_texto_pdf(caminho_pdf)
        print("="*50)
        print(f"Documento caregado com sucesso para {materia} ({len(texto)} caracteres)")
        print("Conteúdo do PDF lido com sucesso:")
        print(texto[:30])  # Mostra os primeiros 30 caracteres
        return texto
    except Exception as e:
        print(f"ERRO ao extrair texto do PDF para {materia}: {str(e)}")
        return f"Erro: Falha ao processar o arquivo PDF para {materia}: {str(e)}"

def carregar_documentos_referencia():
    """Carrega todos os documentos de referência das matérias disponíveis"""
    materias = ["matematica", "fisica", "quimica", "biologia"]
    documentos = {}
    
    for materia in materias:
        texto = carregar_conteudo_pdf_por_materia(materia)
        
        # Verifica se o texto extraído contém uma mensagem de erro
        if isinstance(texto, str) and (texto.startswith("Erro:") or texto.startswith("ERRO:")):
            print(f"FALHA ao carregar documento para {materia}: {texto}")
            documentos[materia] = {}
        else:
            documentos[materia] = {materia: texto}
    
    return documentos
