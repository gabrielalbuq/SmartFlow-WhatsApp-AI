import os

from flask_sqlalchemy import query
from app.database.connection import init_db
from app.database.models import IAKnowledge
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sqlalchemy import text

class KnowledgeService:

    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",
            google_api_key=os.getenv("API_KEY")
        )

    def add_chunk(self, ia_id: int, chunk: str):
        """Salva um único chunk de texto com seu respectivo embedding no banco."""
        db = init_db()
        try:
            embedding = self.embeddings.embed_query(chunk)

            knowledge = IAKnowledge(
                ia_id=ia_id,
                content=chunk,
                embedding=embedding
            )

            db.add(knowledge)
            db.commit()
            
        except Exception :
            db.rollback()
            raise
        finally:
            db.close()

    def similarity_search(  #na vdd eh uma hybrid search 
        self,
        ia_id: int,
        query: str,
        k: int = 5
    ):
        
        query_embedding = self.embeddings.embed_query(query)

        db = init_db()

        try:

            sql = text("""
            WITH semantic_search AS (

                SELECT
                    id,
                    content,

                    1 - (
                        embedding <=> CAST(:embedding AS vector)
                    ) AS semantic_score

                FROM ia_knowledge

                WHERE ia_id = :ia_id

                ORDER BY embedding <=> CAST(:embedding AS vector)

                LIMIT 50
            ),

            keyword_search AS (

                SELECT
                    id,

                    ts_rank(
                        content_tsv,
                        plainto_tsquery(
                            'portuguese',
                            :query
                        )
                    ) AS keyword_score

                FROM ia_knowledge

                WHERE ia_id = :ia_id

                ORDER BY keyword_score DESC

                LIMIT 50
            )

            SELECT
                s.content,

                (
                    0.7 * s.semantic_score +
                    0.3 * COALESCE(
                        k.keyword_score,
                        0
                    )
                ) AS final_score

            FROM semantic_search s

            LEFT JOIN keyword_search k
                ON s.id = k.id

            ORDER BY final_score DESC

            LIMIT :k
            """)

            result = db.execute(
                sql,
                {
                    "embedding": query_embedding,
                    "query": query,
                    "ia_id": ia_id,
                    "k": k
                }
            )

            return [row.content for row in result]

        finally:
            db.close()   