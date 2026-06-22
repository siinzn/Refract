from src.rag.generator import RAG

rag = RAG(query="after effects", threshold=0.6)
result = rag.routing()
print(result)
rag.close()