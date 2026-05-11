from app.RAGcore.Knowledge_ingestor import KnowledgeIngestor

ingestor = KnowledgeIngestor()

texto = """
a empresa possui 35667 funcionários e foi criada em 1990.
"""

ingestor.ingest_text(
    ia_id=3,
    text=texto
)