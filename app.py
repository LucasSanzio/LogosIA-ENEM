import os
from flask import Flask, render_template, request, jsonify, session
from backend.chatbot_enem import LogosIAChatbot
from backend.config import MENSAGEM_BOAS_VINDAS, GEMINI_API_KEY

app = Flask(__name__)
app.secret_key = os.urandom(24)

chatbot = LogosIAChatbot(GEMINI_API_KEY)

@app.route("/")
def index():
    if 'user_id' not in session:
        session['user_id'] = os.urandom(16).hex()
    user_id = session.get('user_id')
    mensagem_inicial = chatbot.iniciar_conversa(user_id)
    
    return render_template("index.html", mensagem_boas_vindas=mensagem_inicial)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("message", "")
    user_id = session.get('user_id', os.urandom(16).hex())

    materia_explicita = request.form.get("materia", None)
    
    if materia_explicita:
        resposta = chatbot.definir_materia(user_id, materia_explicita)
    else:
        resposta = chatbot.processar_mensagem(user_id, user_input)
    
    return jsonify({
        "resposta": resposta,
        "materia_atual": chatbot.obter_materia_atual(user_id)
    })

@app.route("/reset", methods=["POST"])
def reset_chat():
    user_id = session.get('user_id', os.urandom(16).hex())
    mensagem_inicial = chatbot.resetar_conversa(user_id)
    return jsonify({
        "status": "ok", 
        "mensagem": "Conversa reiniciada",
        "boas_vindas": mensagem_inicial
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
