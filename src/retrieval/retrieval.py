import weaviate
from weaviate.classes import query
from weaviate.classes.query import MetadataQuery, HybridFusion
from src.embeddings.embedding import Embedding

class Retrieval:
    def __init__(self, query_text):
        self.query_text = query_text
        self.client = weaviate.connect_to_local()
        self.embedding = Embedding()
        self.collection = self.client.collections.use("Refract")
        self.vector_ = self.embedding.query_embedding(query_text)

    def semantic_retrieval(self, k=5, threshold=0.5):
        """
        im a little lost here, im guessing the above for the vector but i think i might need a loop
        i may be wrong since we can look up through the embeddings, but my doubt is embeddings
        isnt saved anywhere so thats bugging me.  
        was talking ab this - self.embedding.query_embedding(query_text)
        UPDATE - so the above vector is to vectorize the query text not the data LMAO. im so dumb
        """
        response = self.collection.query.near_vector(
            near_vector=self.vector_,
            limit=k,
            certainty=threshold,
            return_metadata=query.MetadataQuery(certainty=True),
        )
        return [(obj.properties, obj.metadata.certainty) for obj in response.objects]
    
    def hybrid_retrieval(self, alpha=0.5, limit=3):
        response = self.collection.query.hybrid(
            query=self.query_text,
            vector=self.vector_,
            alpha=alpha, #means how to distribute semantic and BM25 Keyword Search 0.5 means 50%-50%
            return_metadata=MetadataQuery(score=True, explain_score=True),
            fusion_type=HybridFusion.RELATIVE_SCORE, #tbh idk what this does, it normalize score from both list
            limit=limit
        )
        return [(obj.properties, obj.metadata.score) for obj in response.objects]

    def close(self):
        self.client.close()

"""
tests
retrieval = Retrieval("C++")
semantic_result = retrieval.semantic_retrieval()
print(semantic_result)
hybrid_result = retrieval.hybrid_retrieval()
print(hybrid_result)
retrieval.close()
"""  