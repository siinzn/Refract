from sentence_transformers import SentenceTransformer

class Embedding:
    def __init__(self, column_name):
        self.column_name = column_name
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    
    def get_embedding(self, df):
        batch = df[self.column_name].tolist()
        return self.model.encode(batch, show_progress_bar=True,batch_size=64)
        
