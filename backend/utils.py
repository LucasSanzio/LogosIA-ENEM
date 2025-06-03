import unicodedata

def limpar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto

def detectar_intencao(texto):
    texto_limpo = limpar_texto(texto)
    
    if any(palavra in texto_limpo for palavra in ["sair", "tchau", "ate mais", "adeus", "encerrar", "finalizar"]):
        return "sair"
    
    elif any(palavra in texto_limpo for palavra in ["ola", "oi", "bom dia", "boa tarde", "boa noite", "tudo bem"]):
        return "saudacao"
    
    elif any(palavra in texto_limpo for palavra in ["ajuda", "help", "como funciona", "o que voce faz"]):
        return "ajuda"
    
    return "conversa"

def validar_materia(texto):
    texto_limpo = limpar_texto(texto)
    
    mapeamento = {
        "matematica": ["matematica", "math", "mates", "matematicas", "numeros"],
        "fisica": ["fisica", "physics", "fisicas", "fisico"],
        "quimica": ["quimica", "chemistry", "quimicas", "quimico"],
        "biologia": ["biologia", "biology", "bio", "biologicas", "biologico"]
    }
    
    for materia, variacoes in mapeamento.items():
        if any(variacao in texto_limpo for variacao in variacoes):
            return materia
    
    return None
