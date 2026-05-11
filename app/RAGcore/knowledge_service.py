from app.database.connection import init_db
from app.database.models import IAKnowledge

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sqlalchemy import text
import os


class KnowledgeService:

    def __init__(self):

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",
            google_api_key=os.getenv("API_KEY")
        )

    def add_text(self, ia_id: int, text: str):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = splitter.split_text(text)

        db = init_db()

        try:

            for chunk in chunks:

                embedding = self.embeddings.embed_query(chunk)

                knowledge = IAKnowledge(
                    ia_id=ia_id,
                    content=chunk,
                    embedding=embedding
                )

                db.add(knowledge)

            db.commit()

        finally:
            db.close()
    def similarity_search(
        self,
        ia_id: int,
        query: str,
        k: int = 1
    ):

        query_embedding = self.embeddings.embed_query(query)

        db = init_db()

        try:

            sql = text("""
                SELECT
            content,
            embedding <=> CAST(:embedding AS vector) AS distance
                FROM ia_knowledge
                WHERE ia_id = :ia_id
                ORDER BY embedding <=> CAST(:embedding AS vector)
                LIMIT :k
            """)

            result = db.execute(
                sql,
                {
                    "embedding": query_embedding,
                    "ia_id": ia_id,
                    "k": k
                }
            )

            return [row.content for row in result]

        finally:
            db.close()