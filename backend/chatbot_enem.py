from .config import (
    MENSAGEM_BOAS_VINDAS,
    MENSAGEM_DESPEDIDA,
    MENSAGEM_IDENTIFICACAO_MATERIA,
    PROMPT_MATEMATICA,
    PROMPT_FISICA,
    PROMPT_QUIMICA,
    PROMPT_BIOLOGIA,
    MENSAGEM_APOS_MATEMATICA,
    MENSAGEM_APOS_FISICA,
    MENSAGEM_APOS_QUIMICA,
    MENSAGEM_APOS_BIOLOGIA
)
from .utils import detectar_intencao, validar_materia
from .document_utils import extrair_texto_pdf, obter_caminho_pdf_por_materia
import google.generativeai as genai

class LogosIAChatbot:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        self.conversas = {}
        
        self.prompts = {
            "matematica": PROMPT_MATEMATICA,
            "fisica": PROMPT_FISICA,
            "quimica": PROMPT_QUIMICA,
            "biologia": PROMPT_BIOLOGIA
        }
        
        self.mensagens_apos_selecao = {
            "matematica": MENSAGEM_APOS_MATEMATICA,
            "fisica": MENSAGEM_APOS_FISICA,
            "quimica": MENSAGEM_APOS_QUIMICA,
            "biologia": MENSAGEM_APOS_BIOLOGIA
        }
        
        print(f"Chatbot inicializado com suporte para as matérias: matematica, fisica, quimica, biologia")
    
    def iniciar_conversa(self, usuario_id):
        self.conversas[usuario_id] = {
            "materia_identificada": None,
            "historico": [],
            "aguardando_materia": True,
            "texto_pdf": None 
        }
        return MENSAGEM_BOAS_VINDAS
    
    def _carregar_texto_pdf(self, materia):

        caminho_pdf = obter_caminho_pdf_por_materia(materia)
        
        if not caminho_pdf:
            print(f"PDF não encontrado para a matéria {materia}")
            return ""
        
        texto_pdf = extrair_texto_pdf(caminho_pdf)
        if texto_pdf.startswith("Erro:"):
            print(f"Erro ao extrair texto do PDF para {materia}: {texto_pdf}")
            return ""
        
        print(f"Texto extraído do PDF para {materia}: {len(texto_pdf)} caracteres")
        
        if len(texto_pdf) > 500000:
            texto_pdf = texto_pdf[:500000]
            print(f"Texto do PDF truncado para 500000 caracteres")
            
        return texto_pdf
    
    def processar_mensagem(self, usuario_id, mensagem):
        if usuario_id not in self.conversas:
            return self.iniciar_conversa(usuario_id)
        
        intencao = detectar_intencao(mensagem)
        if intencao == "sair":
            return MENSAGEM_DESPEDIDA
        
        estado = self.conversas[usuario_id]
        
        if estado["aguardando_materia"]:
            materia = validar_materia(mensagem)
            if materia:
                estado["materia_identificada"] = materia
                estado["aguardando_materia"] = False

                estado["texto_pdf"] = self._carregar_texto_pdf(materia)
                
                return self.mensagens_apos_selecao.get(materia, f"Entendi que sua dúvida é sobre {materia.capitalize()}. Como posso ajudar?")
            else:
                return MENSAGEM_IDENTIFICACAO_MATERIA
        
        return self.gerar_resposta(usuario_id, mensagem)
    
    def gerar_resposta(self, usuario_id, mensagem):
        estado = self.conversas[usuario_id]
        materia = estado["materia_identificada"]
        
        prompt_base = self.prompts.get(materia, "")

        contexto_docs = estado.get("texto_pdf", "")
        
        prompt_completo = f"""
        {prompt_base}
        
        {f'Documento de referência para consulta:\n{contexto_docs}' if contexto_docs else ''}
        
        Pergunta do estudante:
        {mensagem}
        """
        
        estado["historico"].append({
            "usuario": mensagem,
            "materia": materia
        })
        
        try:
            response = self.model.generate_content(prompt_completo)
            resposta = response.text.strip()
            
            estado["historico"][-1]["resposta"] = resposta
            
            return resposta
        except Exception as e:
            print(f"Erro ao gerar resposta: {str(e)}")
            return "Desculpe, estou tendo dificuldades para processar sua pergunta. Poderia reformulá-la ou tentar novamente mais tarde?"
    
    def definir_materia(self, usuario_id, materia):
        materia_validada = validar_materia(materia)
        
        if materia_validada:
            if usuario_id not in self.conversas:
                self.iniciar_conversa(usuario_id)

            self.conversas[usuario_id]["materia_identificada"] = materia_validada
            self.conversas[usuario_id]["aguardando_materia"] = False

            self.conversas[usuario_id]["texto_pdf"] = self._carregar_texto_pdf(materia_validada)
            
            return self.mensagens_apos_selecao.get(materia_validada, f"Entendi que sua dúvida é sobre {materia_validada.capitalize()}. Como posso ajudar?")
        else:
            return f"Desculpe, não trabalho com a matéria {materia}. Posso ajudar com Matemática, Física, Química ou Biologia para o ENEM."
    
    def resetar_conversa(self, usuario_id):
        if usuario_id in self.conversas:
            del self.conversas[usuario_id]
        return self.iniciar_conversa(usuario_id)
    
    def obter_materia_atual(self, usuario_id):
        if usuario_id in self.conversas:
            return self.conversas[usuario_id].get("materia_identificada")
        return None
