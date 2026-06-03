from langchain_core.tools import tool


def create_knowledge_tool(retriever):

    @tool("buscar_base_conhecimento")
    def buscar_base_conhecimento(query: str) -> str:
        """
        Use esta ferramenta SOMENTE quando precisar consultar
        informações específicas que podem existir na base de conhecimento.

        A base pode conter:
        - documentos enviados
        - políticas internas
        - informações empresariais
        - regras de negócio
        - produtos e serviços
        - informações privadas da empresa

        NÃO use esta ferramenta para:
        - cumprimentos
        - conversas casuais
        - respostas simples
        - opiniões gerais
        - perguntas que podem ser respondidas sem contexto externo

        Sempre prefira usar esta ferramenta para perguntas factuais,
        técnicas ou específicas da empresa.
        """

        try:

            docs = retriever.invoke(query)

            if not docs:
                return (
                    "Nenhuma informação relevante foi encontrada "
                    "na base de conhecimento."
                )

            context = []

            for i, doc in enumerate(docs, start=1):

                content = doc.page_content.strip()

                if not content:
                    continue

                context.append(
                    f"[Documento {i}]\n{content}"
                )

            if not context:
                return (
                    "Os documentos encontrados estavam vazios "
                    "ou inválidos."
                )

            return "\n\n".join(context)

        except Exception as ex:

            print(f"Erro na tool de conhecimento: {ex}")

            return (
                "Ocorreu um erro ao consultar "
                "a base de conhecimento."
            )

    return buscar_base_conhecimento


@tool("mandar_feedback")
def MandarFeedback(feedback: str) -> str :
        """"use essa ferramenta quando não souber a resposta do usuário ou quando faltarem informações para responder.
        O feedback deve ser claro e específico, indicando quais informações estão faltando ou o que o usuário não entendeu."""
        try:
            with open("feedback.txt", "a") as f:
                f.write(feedback + "\n")
        except Exception as ex:
            print(f"Erro ao salvar feedback: {ex}")
            return "Ocorreu um erro ao salvar seu feedback. Por favor, tente novamente mais tarde."
     
        return "Obrigado pelo seu feedback! Ele foi registrado com sucesso."