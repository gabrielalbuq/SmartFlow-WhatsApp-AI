# app/service/vector_store.py

import os
from pathlib import Path
from typing import List, Optional

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from dotenv import load_dotenv
load_dotenv()
BASE_DIR = Path(__file__).resolve().parents[2]
VECTOR_DB_DIR = BASE_DIR / "vector_db"


class VectorStoreService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model="models/embedding-001",
            api_key=os.getenv("API_KEY")
        )

    def get_vectorstore(self, bot_id: int | str) -> Chroma:
        """
        Carrega ou cria a collection vetorial de um bot específico.
        """
        persist_dir = VECTOR_DB_DIR / str(bot_id)

        return Chroma(
        persist_directory=str(persist_dir),
        embedding_function=self.embeddings
        )

    def get_retriever(self, bot_id: int | str, k: int = 4):
        """
        Retorna um retriever para o bot.
        """
        vectorstore = self.get_vectorstore(bot_id)

        return vectorstore.as_retriever(
            search_kwargs={"k": k}
        )

    def add_text(
        self,
        bot_id: int | str,
        text: str,
        document_name: Optional[str] = None,
    ):
        """
        Quebra um texto em chunks e salva no banco vetorial do bot.
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

        chunks = splitter.split_text(text)

        documents: List[Document] = [
            Document(
                page_content=chunk,
                metadata={
                    "bot_id": str(bot_id),
                    "document_name": document_name or "unknown",
                    "chunk_index": i,
                },
            )
            for i, chunk in enumerate(chunks)
        ]

        vectorstore = self.get_vectorstore(bot_id)
        vectorstore.add_documents(documents)

        return {
            "bot_id": bot_id,
            "document_name": document_name,
            "chunks_created": len(documents),
        }

    def similarity_search(
        self,
        bot_id: int | str,
        query: str,
        k: int = 4,
    ):
        """
        Busca manualmente documentos parecidos.
        Útil para testes.
        """
        vectorstore = self.get_vectorstore(bot_id)

        return vectorstore.similarity_search(query, k=k)
    
    
    
    #retriever = vectorstore.as_retriever()