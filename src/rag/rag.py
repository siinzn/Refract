from src.rag.generator import RAG

rag = RAG(query="what frustrates C++ developers about memory management", threshold=0.5)
result = rag.routing()
print(result)
rag.close()