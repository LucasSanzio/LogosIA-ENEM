import os
from .config import (
    MATERIAS_ENEM, 
    MENSAGEM_BOAS_VINDAS, 
    MENSAGEM_DESPEDIDA,
    MENSAGEM_FALLBACK,
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
from .utils import limpar_texto, detectar_intencao, validar_materia
from .document_utils import extrair_texto_pdf, carregar_documentos_referencia, carregar_conteudo_pdf_por_materia
import google.generativeai as genai

class LogosIAChatbot:
    def __init__(self, api_key):
        # Configuração da API Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Estado das conversas
        self.conversas = {}
        
        # Carrega documentos de referência
        self.documentos = carregar_documentos_referencia()
        
        # Mapeamento de prompts por matéria
        self.prompts = {
            "matematica": PROMPT_MATEMATICA,
            "fisica": PROMPT_FISICA,
            "quimica": PROMPT_QUIMICA,
            "biologia": PROMPT_BIOLOGIA
        }
        
        # Mapeamento de mensagens após seleção de matéria
        self.mensagens_apos_selecao = {
            "matematica": MENSAGEM_APOS_MATEMATICA,
            "fisica": MENSAGEM_APOS_FISICA,
            "quimica": MENSAGEM_APOS_QUIMICA,
            "biologia": MENSAGEM_APOS_BIOLOGIA
        }
        
        print(f"Chatbot inicializado com documentos para as seguintes matérias: {list(self.documentos.keys())}")
    
    def iniciar_conversa(self, usuario_id):
        """Inicializa uma nova conversa para um usuário"""
        self.conversas[usuario_id] = {
            "materia_identificada": None,
            "historico": [],
            "aguardando_materia": True  # Sempre começa aguardando a matéria
        }
        return MENSAGEM_BOAS_VINDAS
    
    def processar_mensagem(self, usuario_id, mensagem):
        """Processa a mensagem do usuário e retorna uma resposta"""
        # Inicializa conversa se for novo usuário
        if usuario_id not in self.conversas:
            return self.iniciar_conversa(usuario_id)
        
        # Detecta intenção de saída
        intencao = detectar_intencao(mensagem)
        if intencao == "sair":
            return MENSAGEM_DESPEDIDA
        
        # Obtém o estado atual da conversa
        estado = self.conversas[usuario_id]
        
        # Se estamos aguardando que o usuário especifique a matéria
        if estado["aguardando_materia"]:
            materia = validar_materia(mensagem)
            if materia:
                estado["materia_identificada"] = materia
                estado["aguardando_materia"] = False
                return self.mensagens_apos_selecao.get(materia, f"Entendi que sua dúvida é sobre {materia.capitalize()}. Como posso ajudar?")
            else:
                return MENSAGEM_IDENTIFICACAO_MATERIA
        
        # Se já temos a matéria, gera resposta com base nela
        return self.gerar_resposta(usuario_id, mensagem)
    
    def processar_pdf(self, usuario_id, texto_pdf):
        """Processa o conteúdo de um PDF enviado pelo usuário"""
        # Inicializa conversa se for novo usuário
        if usuario_id not in self.conversas:
            return self.iniciar_conversa(usuario_id)
        
        # Obtém o estado atual da conversa
        estado = self.conversas[usuario_id]
        
        # Se ainda não temos uma matéria definida, solicita ao usuário
        if estado["aguardando_materia"]:
            return "Por favor, selecione uma matéria antes de enviar um documento PDF."
        
        # Obtém a matéria atual
        materia = estado["materia_identificada"]
        
        # Obtém o prompt fixo para a matéria
        prompt_base = self.prompts.get(materia, "")
        
        # Monta o prompt completo com o prompt fixo e o conteúdo do PDF
        prompt_completo = f"""
        {prompt_base}
        
        Documento PDF:
        {texto_pdf}
        
        Com base no documento acima, forneça uma explicação detalhada sobre o conteúdo, 
        destacando os conceitos principais e como eles se aplicam ao ENEM.
        """
        
        # Registra a interação no histórico
        estado["historico"].append({
            "usuario": "Enviou um documento PDF",
            "materia": materia
        })
        
        # Gera resposta usando a API Gemini
        try:
            response = self.model.generate_content(prompt_completo)
            resposta = response.text.strip()
            
            # Registra a resposta no histórico
            estado["historico"][-1]["resposta"] = resposta
            
            return resposta
        except Exception as e:
            # Em caso de erro, retorna uma mensagem amigável
            print(f"Erro ao processar PDF: {str(e)}")
            return "Desculpe, estou tendo dificuldades para processar o documento PDF. O arquivo pode ser muito grande ou estar em um formato que não consigo ler adequadamente."
    
    def gerar_resposta(self, usuario_id, mensagem):
        """Gera uma resposta usando a API Gemini com base na matéria identificada e prompt fixo"""
        estado = self.conversas[usuario_id]
        materia = estado["materia_identificada"]
        
        # Obtém o prompt fixo para a matéria
        prompt_base = self.prompts.get(materia, "")
        
        # Obtém documentos da matéria
        docs_materia = self.documentos.get(materia, {})
        
        # Constrói o contexto com os documentos de referência
        contexto_docs = ""
        for nome_doc, conteudo in docs_materia.items():
            # Limita o tamanho do contexto para não exceder limites da API
            if len(contexto_docs) + len(conteudo) < 500000:  # Limite arbitrário, ajuste conforme necessário
                contexto_docs += f"\n--- DOCUMENTO: {nome_doc} ---\n{conteudo}\n"
        
        # Monta o prompt completo com o prompt fixo, documentos e pergunta do usuário
        prompt_completo = f"""
        {prompt_base}
        
        {f'Documentos de referência para consulta:\n{contexto_docs}' if contexto_docs else ''}
        
        Pergunta do estudante:
        {mensagem}
        """
        
        # Registra a interação no histórico
        estado["historico"].append({
            "usuario": mensagem,
            "materia": materia
        })
        
        # Gera resposta usando a API Gemini
        try:
            response = self.model.generate_content(prompt_completo)
            resposta = response.text.strip()
            
            # Registra a resposta no histórico
            estado["historico"][-1]["resposta"] = resposta
            
            return resposta
        except Exception as e:
            # Em caso de erro, retorna uma mensagem amigável
            print(f"Erro ao gerar resposta: {str(e)}")
            return "Desculpe, estou tendo dificuldades para processar sua pergunta. Poderia reformulá-la ou tentar novamente mais tarde?"
    
    def definir_materia(self, usuario_id, materia):
        """Define explicitamente a matéria para o usuário"""
        materia_validada = validar_materia(materia)
        
        if materia_validada:
            if usuario_id not in self.conversas:
                self.iniciar_conversa(usuario_id)
            
            self.conversas[usuario_id]["materia_identificada"] = materia_validada
            self.conversas[usuario_id]["aguardando_materia"] = False
            return self.mensagens_apos_selecao.get(materia_validada, f"Entendi que sua dúvida é sobre {materia_validada.capitalize()}. Como posso ajudar?")
        else:
            return f"Desculpe, não trabalho com a matéria {materia}. Posso ajudar com Matemática, Física, Química ou Biologia para o ENEM."
    
    def resetar_conversa(self, usuario_id):
        """Reseta o estado da conversa para um usuário"""
        if usuario_id in self.conversas:
            del self.conversas[usuario_id]
        return self.iniciar_conversa(usuario_id)
    
    def obter_materia_atual(self, usuario_id):
        """Retorna a matéria atual da conversa"""
        if usuario_id in self.conversas:
            return self.conversas[usuario_id].get("materia_identificada")
        return None
