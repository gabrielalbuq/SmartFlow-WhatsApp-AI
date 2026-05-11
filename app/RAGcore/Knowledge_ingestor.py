
from app.RAGcore.knowledge_service import KnowledgeService

class KnowledgeIngestor:

    def __init__(self):
        self.knowledge_service = KnowledgeService()

    def ingest_text(
        self,
        ia_id: int,
        text: str
    ):

        self.knowledge_service.add_text(
            ia_id=ia_id,
            text=text
        )

        print("Texto ingerido com sucesso.")
        
        
