from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_classic.chains import ConversationChain
from langchain_core.prompts import PromptTemplate

# Importando os dois motores: OpenAI e Google Gemini
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

class IAresponse:
    def __init__(self, api_key:str, ia_model:str, system_prompt:str, resume_lead:str = ""):
        self.api_key = api_key
        self.ai_model = ia_model or "gpt-4o-mini"
        self.system_prompt = system_prompt
        self.resume_lead = resume_lead

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
        self.ai_model = self.ai_model.strip()
        self.api_key = self.api_key.strip()

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

    def generate_response(self, message_lead:str, history_message:list=[]) -> str:
        try:
            # Inicializa a memória e o prompt
            memory = ConversationBufferWindowMemory(k=20)
            review_template = PromptTemplate.from_template(self.prompt_template)

            conversation = ConversationChain(
                llm=self.chat,
                memory=memory,
                prompt=review_template,
                verbose=False
            )

            # iii) ALIMENTAR A MEMÓRIA COM O HISTÓRICO
            if history_message:
                for msg in history_message:
                    # Pula a mensagem atual se ela já foi salva no banco antes de chamar a IA
                    if msg.get("content") == message_lead and msg.get("role") == "user":
                        continue

                    if msg.get("role") == "user":
                        conversation.memory.chat_memory.add_user_message(msg.get("content") or "")
                    
                    elif msg.get("role") == "assistant":
                        conversation.memory.chat_memory.add_ai_message(msg.get("content") or "")

            print(f"Total de interações carregadas: {len(history_message)}")
            
            # iv) GERAR RESPOSTA
            resposta = conversation.predict(input=message_lead)
            print(f"Resposta da IA: {resposta}")
            
            return resposta

        except Exception as ex:
            print(f"Erro ao processar resposta: {ex}")
            return ""

    def generate_resume(self, history_message:list=[]) -> str:
        pass