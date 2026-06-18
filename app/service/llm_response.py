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
            template_base += f"\n\nResumo de todas as interaÃ§Ãµes que teve com este lead: {self.resume_lead}"
        
        template_base += """
        
        REGRA RIGOROSA DE COMPORTAMENTO:
        Analise o 'HistÃ³rico da conversa' abaixo. Se o histÃ³rico NÃƒO estiver vazio (ou seja, se jÃ¡ existir uma conversa em andamento), VOCÃŠ ESTÃ ESTRITAMENTE PROIBIDO de usar saudaÃ§Ãµes (como "OlÃ¡", "Oi", "Bom dia", "Tudo bem?") e PROIBIDO de se apresentar novamente. VÃ¡ direto ao ponto e responda Ã  nova pergunta do UsuÃ¡rio como se fosse uma conversa contÃ­nua no WhatsApp.
        """

        # O LangChain precisa das variÃ¡veis {history} e {input} no final
        template_base += "\n\nHistÃ³rico da conversa:\n{history}\n\nUsuÃ¡rio: {input}\nAssistente:"
        self.prompt_template = template_base

        # ii) MOTOR AGNÃ“STICO (A "Chave Mestra")
        # Limpeza de seguranÃ§a (tira espaÃ§os vazios que possam vir do banco)
        self.api_key = self.api_key.strip()
        self.ai_model = self._normalize_model(self.ai_model, self.api_key)
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

    def _normalize_model(self, ia_model: str, api_key: str = "") -> str:
        model = (ia_model or "").strip()
        model_lower = model.lower()
        api_key = (api_key or "").strip()

        if api_key.startswith("AQ.") and "gemini" not in model_lower:
            return "gemini-2.5-flash-lite"

        if api_key.startswith("sk-") and "gemini" in model_lower:
            return "gpt-4o-mini"

        if model_lower in {"gemini", "google", "google gemini"}:
            return "gemini-2.5-flash-lite"

        if model_lower in {"openai", "chatgpt", "gpt"}:
            return "gpt-4o-mini"

        return model or "gpt-4o-mini"
#bot_id: int colocar no futuro para o rag
    def generate_response(self, message_lead: str, history_message: list = [], bot_id = None) -> str:
        try:
            system_prompt = self.prompt_template

            if bot_id:
                try:
                    retriever = KnowledgeRetriever(bot_id)
                    docs = retriever.invoke(message_lead)
                    context_parts = []

                    for i, doc in enumerate(docs, start=1):
                        content = (doc.page_content or "").strip()
                        if content:
                            context_parts.append(f"[Documento {i}]\n{content}")

                    if context_parts:
                        knowledge_context = "\n\nBASE DE CONHECIMENTO DA IA:\n"
                        knowledge_context += "\n\n".join(context_parts)
                        knowledge_context += """

INSTRUCAO RAG:
Use a BASE DE CONHECIMENTO DA IA acima como fonte principal para responder.
Se a pergunta estiver relacionada a esse conteudo, responda com base nele.
Se a resposta nao estiver explicitamente na base, diga que nao encontrou a informacao na base de conhecimento.
"""
                        system_prompt += knowledge_context
                        print(f"[RAG] Contexto carregado: {len(context_parts)} documentos")
                    else:
                        print("[RAG] Nenhum contexto encontrado para esta IA")

                except Exception as rag_error:
                    print(f"[RAG] Erro ao buscar conhecimento: {rag_error}")

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

            print(f"Total de interacoes carregadas: {len(history_message)}")

            messages.append(("user", message_lead))

            response = self.chat.invoke(messages)
            resposta = response.content

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
            VocÃª Ã© um assistente especializado em resumir conversas com leads. Seu objetivo Ã© identificar, extrair e armazenar de forma clara todos os pontos-chave e informaÃ§Ãµes importantes discutidas durante a conversa. Ao elaborar o resumo, siga estas diretrizes:

            1. **IdentificaÃ§Ã£o dos Pontos-Chave:** Extraia os tÃ³picos principais da conversa, incluindo necessidades, interesses, objeÃ§Ãµes e prÃ³ximos passos do lead.
            2. **OrganizaÃ§Ã£o das InformaÃ§Ãµes:** Estruture o resumo de maneira clara e organizada, facilitando a visualizaÃ§Ã£o dos dados mais relevantes.
            3. **Foco nas InformaÃ§Ãµes Relevantes:** Certifique-se de que nenhuma informaÃ§Ã£o importante seja omitida. Dados como informaÃ§Ãµes de contato, dÃºvidas especÃ­ficas e requisitos do lead devem ser destacados.
            4. **Clareza e ConcisÃ£o:** O resumo deve ser conciso, mas detalhado o suficiente para fornecer um panorama completo da conversa.
            5. **Privacidade e SeguranÃ§a:** Garanta que todas as informaÃ§Ãµes sensÃ­veis sejam tratadas com a devida confidencialidade.

            Utilize este prompt para transformar a conversa em um resumo que possibilite um acompanhamento eficaz e estratÃ©gico do lead.

            HistÃ³rico da conversa:
            {history}
            UsuÃ¡rio: {input}
            """

            # i) Utiliza o motor agnÃ³stico jÃ¡ configurado no __init__ (self.chat) - Ele jÃ¡ sabe se Ã© Gemini ou OpenAI
            memory = ConversationBufferWindowMemory(k=60)
            review_template = PromptTemplate.from_template(system_prompt)
            
            # ii) Passa o self.chat para a chain
            conversation = ConversationChain(
                llm=self.chat,
                memory=memory,
                prompt=review_template
            )

            # Alimenta a memÃ³ria com cada mensagem do histÃ³rico
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

            print(f"Total de {len(history_message)} interaÃ§Ãµes")   
            resposta = conversation.predict(input=message)
            print(f"Resposta da IA   : {resposta}")
            
            return resposta
        except Exception as ex:
            print(f"âŒ Erro ao processar resposta: {ex}")
            return None




