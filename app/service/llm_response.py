from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_classic.chains import ConversationChain
from langchain_core.prompts import PromptTemplate

# Importando os dois motores: OpenAI e Google Gemini
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from app.RAGcore.retriver import KnowledgeRetriever
from app.service.tools import create_knowledge_tool
from langchain.agents import create_agent
from app.service.tools import create_feedback_tool



class IAresponse:
    def __init__(self, api_key:str, ia_model:str, system_prompt:str, resume_lead:str = "",bot_id = None):
        self.api_key = api_key
        self.ai_model = ia_model or "gpt-4o-mini"
        self.system_prompt = system_prompt
        self.resume_lead = resume_lead
        self.bot_id = bot_id
        self.last_error = ""

        # i) MONTANDO O PROMPT
        template_base = self.system_prompt
        if self.resume_lead:
            print("Resumo localizado!")
            template_base += f"\n\nResumo de todas as interações que teve com este lead: {self.resume_lead}"
        
        template_base += """
        
        REGRA RIGOROSA DE COMPORTAMENTO:
        Analise o 'Histórico da conversa' abaixo. Se o histórico NÃO estiver vazio (ou seja, se já existir uma conversa em andamento), VOCÊ ESTÁ ESTRITAMENTE PROIBIDO de usar saudações (como "Olá", "Oi", "Bom dia", "Tudo bem?") e PROIBIDO de se apresentar novamente. Vá direto ao ponto e responda à nova pergunta do Usuário como se fosse uma conversa contínua no WhatsApp.
        """

        # O LangChain precisa das variáveis {history} e {input} no final
        template_base += "\n\nHistórico da conversa:\n{history}\n\nUsuário: {input}\nAssistente:"
        self.prompt_template = template_base

        # ii) MOTOR AGNÓSTICO (A "Chave Mestra")
        # Limpeza de segurança (tira espaços vazios que possam vir do banco)
        self.ai_model = self._normalize_model(self.ai_model)
        self.api_key = self.api_key.strip()
        ##### llm = get_llm(nome do provider)  ### pode se usado
        if "gemini" in self.ai_model.lower():
            print(f"Conectando ao modelo do Google: {self.ai_model}")
            self.chat = ChatGoogleGenerativeAI(
                model=self.ai_model, 
                google_api_key=self.api_key, 
                temperature=0.7
            )
        else:
            self.chat = ChatOpenAI(
                model=self.ai_model, 
                api_key=self.api_key, 
                temperature=0.2
            )

    def _normalize_model(self, ia_model: str) -> str:
        model = (ia_model or "").strip()
        model_lower = model.lower()

        if model_lower in {"gemini", "google", "google gemini"}:
            return "gemini-2.5-flash-lite"

        if model_lower in {"openai", "chatgpt", "gpt"}:
            return "gpt-4o-mini"

        return model or "gpt-4o-mini"
#bot_id: int colocar no futuro para o rag
    def generate_response(self, message_lead: str, history_message: list = [], bot_id = None) -> str:
        try:
            #retriever = vector_service.get_retriever(bot_id=bot_id)
            #knowledge_tool = create_knowledge_tool(retriever)
            tools = []
            if bot_id:
                
                 retriever = KnowledgeRetriever(bot_id)
                 knowledge_tool = create_knowledge_tool(retriever)
                 feedback_tool = create_feedback_tool(bot_id)
                 tools.append(knowledge_tool)
                 tools.append(feedback_tool)
                 
                 
            agent = create_agent(
                model=self.chat,
                tools=tools,
                
            )
            system_prompt = self.prompt_template

            messages = [
                ("system", system_prompt)
            ]
            if history_message:
                for msg in history_message:

                    if msg.get("content") == message_lead and msg.get("role") == "user":
                        continue

                    if msg.get("role") == "user":
                        messages.append(("user", msg.get("content") or ""))

                    elif msg.get("role") == "assistant":
                        messages.append(("assistant", msg.get("content") or ""))

            print(f"Total de interações carregadas: {len(history_message)}")

            
            messages.append(("user", message_lead))

            
            response = agent.invoke({
                "messages": messages
            })

            resposta = response["messages"][-1].content

            print(f"Resposta da IA: {resposta}")

            return resposta

            

        except Exception as ex:
            self.last_error = str(ex)
            print(f"Erro ao processar resposta: {self.last_error}")
            return ""

    def generate_resume(self, history_message:list=[]) -> str:
        try:
            message = "Gere um resumo detalhado dessa conversa"
            system_prompt = """
            Você é um assistente especializado em resumir conversas com leads. Seu objetivo é identificar, extrair e armazenar de forma clara todos os pontos-chave e informações importantes discutidas durante a conversa. Ao elaborar o resumo, siga estas diretrizes:

            1. **Identificação dos Pontos-Chave:** Extraia os tópicos principais da conversa, incluindo necessidades, interesses, objeções e próximos passos do lead.
            2. **Organização das Informações:** Estruture o resumo de maneira clara e organizada, facilitando a visualização dos dados mais relevantes.
            3. **Foco nas Informações Relevantes:** Certifique-se de que nenhuma informação importante seja omitida. Dados como informações de contato, dúvidas específicas e requisitos do lead devem ser destacados.
            4. **Clareza e Concisão:** O resumo deve ser conciso, mas detalhado o suficiente para fornecer um panorama completo da conversa.
            5. **Privacidade e Segurança:** Garanta que todas as informações sensíveis sejam tratadas com a devida confidencialidade.

            Utilize este prompt para transformar a conversa em um resumo que possibilite um acompanhamento eficaz e estratégico do lead.

            Histórico da conversa:
            {history}
            Usuário: {input}
            """

            # i) Utiliza o motor agnóstico já configurado no __init__ (self.chat) - Ele já sabe se é Gemini ou OpenAI
            memory = ConversationBufferWindowMemory(k=60)
            review_template = PromptTemplate.from_template(system_prompt)
            
            # ii) Passa o self.chat para a chain
            conversation = ConversationChain(
                llm=self.chat,
                memory=memory,
                prompt=review_template
            )

            # Alimenta a memória com cada mensagem do histórico
            if not history_message:
                conversation.memory.chat_memory.add_user_message(message)
            else:
                for msg in history_message:

                    #Adicionando memoria do User
                    if msg["role"] == "user":
                        conversation.memory.chat_memory.add_user_message(msg.get("content") or "")
                    
                    #Adicionando memoria da IA
                    elif msg["role"] == "assistant":
                        conversation.memory.chat_memory.add_ai_message(msg.get("content") or "")

            print(f"Total de {len(history_message)} interações")   
            resposta = conversation.predict(input=message)
            print(f"Resposta da IA   : {resposta}")
            
            return resposta
        except Exception as ex:
            print(f"❌ Erro ao processar resposta: {ex}")
            return None
