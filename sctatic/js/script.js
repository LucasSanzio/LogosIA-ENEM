document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const resetBtn = document.getElementById('reset-btn');
    const exitBtn = document.getElementById('exit-btn');
    const materiaSelector = document.getElementById('materia-selector');
    const materiaBtns = document.querySelectorAll('.materia-btn');
    const materiaAtual = document.getElementById('materia-nome');
    
    // Configuração do Marked.js para renderização de Markdown
    marked.setOptions({
        breaks: true,        // Quebras de linha são convertidas em <br>
        gfm: true,           // GitHub Flavored Markdown
        headerIds: true,     // Adiciona IDs aos cabeçalhos
        mangle: false,       // Não codifica caracteres especiais nos IDs
        sanitize: false,     // Permite HTML dentro do markdown
        smartLists: true,    // Listas mais inteligentes
        smartypants: true,   // Tipografia mais bonita
        xhtml: false         // Não fecha tags vazias com />
    });
    
    // Mostra o seletor de matéria no início
    materiaSelector.classList.add('active');
    
    // Função para adicionar mensagem ao chat
    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        // Se for mensagem do bot, renderiza o Markdown
        if (!isUser) {
            messageContent.innerHTML = marked.parse(message);
        } else {
            messageContent.textContent = message;
        }
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Rola para a última mensagem
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Função para enviar mensagem ao servidor
    async function sendMessage(message, materia = null) {
        // Desabilita o botão de envio durante o processamento
        sendBtn.disabled = true;
        
        // Prepara os dados para envio
        const formData = new FormData();
        formData.append('message', message);
        if (materia) {
            formData.append('materia', materia);
        }
        
        try {
            // Envia a requisição para o servidor
            const response = await fetch('/chat', {
                method: 'POST',
                body: formData
            });
            
            // Processa a resposta
            const data = await response.json();
            
            // Adiciona a resposta ao chat com renderização Markdown
            addMessage(data.resposta);
            
            // Atualiza a matéria atual se disponível
            if (data.materia_atual) {
                materiaAtual.textContent = data.materia_atual.charAt(0).toUpperCase() + data.materia_atual.slice(1);
                // Esconde o seletor de matéria uma vez que a matéria foi definida
                materiaSelector.classList.remove('active');
                // Habilita o campo de entrada
                userInput.disabled = false;
                sendBtn.disabled = false;
            }
            
        } catch (error) {
            console.error('Erro ao enviar mensagem:', error);
            addMessage('Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.');
        } finally {
            // Reabilita o botão de envio
            sendBtn.disabled = false;
        }
    }
    
    // Evento de clique no botão de envio
    sendBtn.addEventListener('click', function() {
        const message = userInput.value.trim();
        
        if (message) {
            // Adiciona a mensagem do usuário ao chat
            addMessage(message, true);
            
            // Envia a mensagem para o servidor
            sendMessage(message);
            
            // Limpa o campo de entrada
            userInput.value = '';
        }
    });
    
    // Evento de pressionar Enter no campo de entrada
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendBtn.click();
        }
    });
    
    // Evento de clique nos botões de matéria
    materiaBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const materia = this.getAttribute('data-materia');
            
            // Adiciona a seleção de matéria ao chat
            addMessage(`Quero falar sobre ${this.textContent}`, true);
            
            // Envia a matéria selecionada para o servidor
            sendMessage('', materia);
        });
    });
    
    // Evento de clique no botão de reset
    resetBtn.addEventListener('click', async function() {
        try {
            // Envia requisição para resetar a conversa
            const response = await fetch('/reset', {
                method: 'POST'
            });
            
            // Processa a resposta
            const data = await response.json();
            
            // Limpa o chat
            chatMessages.innerHTML = '';
            
            // Adiciona mensagem de boas-vindas
            addMessage(data.boas_vindas);
            
            // Reseta a matéria atual
            materiaAtual.textContent = 'Não definida';
            
            // Mostra o seletor de matéria novamente
            materiaSelector.classList.add('active');
            
            // Habilita os controles
            userInput.disabled = false;
            sendBtn.disabled = false;
            exitBtn.disabled = false;
            
        } catch (error) {
            console.error('Erro ao resetar conversa:', error);
            addMessage('Desculpe, ocorreu um erro ao resetar a conversa. Por favor, recarregue a página.');
        }
    });
    
    // Evento de clique no botão de sair
    exitBtn.addEventListener('click', function() {
        // Adiciona a mensagem de saída do usuário
        addMessage('Encerrar conversa', true);
        
        // Envia comando de saída
        sendMessage('sair');
        
        // Desabilita a entrada após encerrar
        userInput.disabled = true;
        sendBtn.disabled = true;
        exitBtn.disabled = true;
        
        // Habilita apenas o botão de nova conversa
        resetBtn.disabled = false;
    });
    
    // Inicialmente, desabilita o campo de entrada até que uma matéria seja selecionada
    if (materiaAtual.textContent === 'Não definida') {
        userInput.disabled = true;
    }
});
