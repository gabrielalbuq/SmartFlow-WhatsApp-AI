from langchain_core.tools import tool


def create_knowledge_tool(retriever):

    @tool("buscar_base_conhecimento")
    def buscar_base_conhecimento(query: str) -> str:
        """
        Use esta ferramenta quando precisar consultar informações específicas que não estão no seu conhecimento geral, como:

        - políticas da empresa
        - informações de documentos enviados
        - regras internas
        - dados específicos do negócio

        Não use para:
        - conversas gerais
        - cumprimentos
        - perguntas simples que não precisam de contexto externo
        """

        docs = retriever.invoke(query)

        if not docs:
            return "Nenhuma informação relevante encontrada na base de conhecimento."

        return "\n\n".join([doc.page_content for doc in docs])

    return buscar_base_conhecimento