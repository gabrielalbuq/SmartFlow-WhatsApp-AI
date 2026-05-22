"""from app.RAGcore.Knowledge_ingestor import KnowledgeIngestor

ingestor = KnowledgeIngestor()

texto = '
   a empresa possui 35667 funcionários e foi criada em 1990.
'

ingestor.ingest_text(
    ia_id=3,
    text=texto
)"""


from app.RAGcore.Knowledge_ingestor import KnowledgeIngestor


ingestor = KnowledgeIngestor()


caminho_do_arquivo = "dados_alimentacao_ia3.txt"

print("Iniciando a ingestão do arquivo TXT...")
ingestor.ingest_txt(
    ia_id=3,
    file_path=caminho_do_arquivo
)
print("Processo finalizado!")