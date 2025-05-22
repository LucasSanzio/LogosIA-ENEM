# Chatbot Educacional para ENEM - Logos IA

Este é um chatbot especializado em auxiliar estudantes na preparação para o ENEM, oferecendo suporte nas matérias de Matemática, Física, Química e Biologia.

## Requisitos do Sistema

- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)
- Acesso à internet para comunicação com a API Gemini

## Instalação

Siga os passos abaixo para instalar e configurar o chatbot:

1. **Clone o repositório ou extraia os arquivos**

2. **Crie um ambiente virtual Python (recomendado)**
   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual**
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```
   - No macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```
   
   Se o arquivo requirements.txt não estiver disponível, instale as dependências manualmente:
   ```bash
   pip install google-generativeai flask pymupdf
   ```

5. **Estrutura de arquivos PDF**
   
   Certifique-se de que os arquivos PDF das matérias estejam na pasta `documents` com os seguintes nomes:
   - `matematica.pdf`
   - `fisica.pdf`
   - `quimica.pdf`
   - `biologia.pdf`

## Configuração da API

1. O sistema utiliza a API Gemini da Google. A chave API já está configurada no arquivo `config.py`.

2. Caso deseje utilizar sua própria chave API:
   - Obtenha uma chave API em [Google AI Studio](https://makersuite.google.com/)
   - Substitua a chave no arquivo `backend/config.py`

## Inicialização do Sistema

1. **Certifique-se de que o ambiente virtual está ativado**

2. **Execute o aplicativo**
   ```bash
   python app.py
   ```

3. **Acesse o chatbot**
   - Abra seu navegador e acesse: `http://localhost:5000`

## Como Usar o Chatbot

### Iniciando uma Conversa

1. Ao iniciar o chatbot, você será recebido com uma mensagem de boas-vindas.

2. **Seleção de Matéria**: 
   - O primeiro passo é informar qual matéria você deseja estudar.
   - Digite o nome da matéria: Matemática, Física, Química ou Biologia.
   - Exemplo: "Quero estudar Física" ou simplesmente "Física".

3. **Fazendo Perguntas**:
   - Após selecionar a matéria, você pode fazer perguntas específicas sobre o conteúdo.
   - Seja claro e específico em suas perguntas para obter melhores respostas.
   - Exemplo: "Explique o movimento uniformemente variado" ou "Como resolver equações do segundo grau?"

### Recursos Adicionais

1. **Mudança de Matéria**:
   - Para mudar de matéria durante a conversa, digite "Mudar matéria" ou "Trocar matéria".
   - Em seguida, informe a nova matéria desejada.

2. **Encerrar Conversa**:
   - Para encerrar a conversa, digite "Sair", "Encerrar" ou "Tchau".

3. **Reiniciar Conversa**:
   - Para reiniciar a conversa, digite "Reiniciar" ou "Recomeçar".

## Dicas para Melhores Resultados

1. **Seja Específico**: Perguntas específicas recebem respostas mais precisas.
   - Exemplo bom: "Explique a primeira lei de Newton e suas aplicações"
   - Exemplo ruim: "Me fale sobre física"

2. **Uma Pergunta por Vez**: Faça uma pergunta de cada vez para obter respostas mais completas.

3. **Peça Exemplos**: Se precisar de exemplos práticos, solicite explicitamente.
   - Exemplo: "Pode me dar um exemplo resolvido de derivada?"

4. **Solicite Esclarecimentos**: Se a resposta não for clara, peça mais detalhes.
   - Exemplo: "Pode explicar isso de forma mais simples?" ou "Não entendi a parte sobre..., pode detalhar?"

## Solução de Problemas

1. **Erro de Conexão com a API**:
   - Verifique sua conexão com a internet
   - Confirme se a chave API no arquivo config.py está correta

2. **PDFs não Encontrados**:
   - Verifique se os arquivos PDF estão na pasta `documents` com os nomes corretos
   - Certifique-se de que os arquivos não estão corrompidos

3. **Erro ao Iniciar o Aplicativo**:
   - Verifique se todas as dependências foram instaladas corretamente
   - Confirme se está usando uma versão compatível do Python

## Contato e Suporte

Para suporte técnico ou dúvidas sobre o funcionamento do chatbot, entre em contato com a equipe de desenvolvimento.

---

Desenvolvido por Logos IA - Assistente Educacional para o ENEM
