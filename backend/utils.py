import unicodedata
import re
from .config import MATERIAS_ENEM

def limpar_texto(texto):
    """Remove acentos, converte para minúsculas e normaliza o texto"""
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto

def detectar_intencao(texto):
    """Detecta a intenção básica do usuário"""
    texto_limpo = limpar_texto(texto)
    
    # Intenção de sair
    if any(palavra in texto_limpo for palavra in ["sair", "tchau", "ate mais", "adeus", "encerrar", "finalizar"]):
        return "sair"
    
    # Intenção de saudação
    elif any(palavra in texto_limpo for palavra in ["ola", "oi", "bom dia", "boa tarde", "boa noite", "tudo bem"]):
        return "saudacao"
    
    # Intenção de ajuda
    elif any(palavra in texto_limpo for palavra in ["ajuda", "help", "como funciona", "o que voce faz"]):
        return "ajuda"
    
    # Intenção padrão (conversa/pergunta)
    return "conversa"

def validar_materia(texto):
    """Valida se o texto corresponde a uma das matérias do ENEM"""
    texto_limpo = limpar_texto(texto)
    
    # Mapeamento de variações para matérias padrão
    mapeamento = {
        "matematica": ["matematica", "math", "mates", "matematicas", "numeros"],
        "fisica": ["fisica", "physics", "fisicas", "fisico"],
        "quimica": ["quimica", "chemistry", "quimicas", "quimico"],
        "biologia": ["biologia", "biology", "bio", "biologicas", "biologico"]
    }
    
    # Verifica se o texto corresponde a alguma variação
    for materia, variacoes in mapeamento.items():
        if any(variacao in texto_limpo for variacao in variacoes):
            return materia
    
    return None
