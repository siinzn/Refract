import weaviate
from weaviate.classes.config import Configure, Property, DataType, VectorDistances
import ast
import math
import pandas as pd

class Weaviate:
    def __init__(self):
        self.client = weaviate.connect_to_local()
        self.properties = []

    """
    I have done the below to avoid longggg calls of Property which was a pain to read and 
    to write, so this saves me tone of time and headache. There is a better way to do this 
    using a tuple and a loop - maybe later i will do that
    """
    @staticmethod
    def build_property(name: str, type: DataType, desc: str, idxsearch: bool):
        return Property(name=name,data_type=type,description=desc,index_filterable=True,
            index_searchable=idxsearch,vectorize_property_name=False,skip_vectorization=True)
        
    def get_properties(self):
        self.properties = [
            self.build_property("index_id", DataType.INT, "Index ID", False),
            self.build_property("text_clean", DataType.TEXT, "Cleaned Text", True),
            self.build_property("source", DataType.TEXT, "Text Source", True),
            self.build_property("sentiment_label", DataType.TEXT, "Sentiment Label", True),
            self.build_property("sentiment_score", DataType.NUMBER, "Sentiment Score", False),
            self.build_property("topic_label", DataType.TEXT, "Topic Label", True),
            self.build_property("keyword", DataType.TEXT_ARRAY, "Keywords", True),
            self.build_property("entities", DataType.TEXT_ARRAY, "Named Entities", True),
            self.build_property("author", DataType.TEXT, "Author", True),
            self.build_property("like_count", DataType.INT, "Like Count", False)
        ]
        return self.properties

    def create_collection(self, name):
        if self.client.collections.exists(name):
            self.client.collections.delete(name)
        
        """
        So what we are doing is essentially Vector DB it has two parts - embedding(done earlier) 
        and indexing. In indexing we need to make sort of like a schema for our vector db. That
        is collection. The collections.create has vector_config which is saying how to store and search for the vectors. Vectors.self_provided is saying im providing the vector. inside that
        we specify the search algorithm as HNSW. HNSW is a graph based algorithm with O(log n) search which is pretty fast. VectorDistances.COSINE specifies how are vectors going to
        be measured. IDK much about COSINE but its related to angle ig LMAOO. i just know that my embedding model sentence-transformers was trained with COSINE SIMILARITY. 
        ef=128,ef_construction=128,max_connections=64 these are default values from what i know. 
        ef -> how many neigbouring vector to check before give result
        ef_construction -? same as ef but for while index building 
        max_connection -> some sort of link between each HNSW im not 100% ab it. But for all these higher the value, more accurate but slower, the values below are the most
        optimal because it sits in the middle ground
        """

        collection = self.client.collections.create(
            name,
            vector_config=Configure.Vectors.self_provided(
                vector_index_config=Configure.VectorIndex.hnsw(
                    distance_metric=VectorDistances.COSINE,
                    ef=128,
                    ef_construction=128,
                    max_connections=64
                ),
            ),
            properties=self.get_properties(),
            #below is BM25 which is a keyword search algo, it works based on scoring system
            # k1 -> if a term has higher freq in multiple docs, score goes up
            # b -> idont get it but, its how much document length normalization matters
            inverted_index_config=Configure.inverted_index(
                bm25_k1=1.2,
                bm25_b=0.75
            )
        )

    """
    okay so we made our collection(or schema above), now we define how we insert data into it. its pretty simple in theory. we do it in batches in case if it fails previous
    data will be stored. rest is pretty self explanatory. sentiment_score, author, like_count may have empty fields due to merged dataset. so we check if it is NaN and handle
    it accordingly. keyword and entities are list stored as strings, so i converted them to actual lists using ast.literal_eval(claude asked me to use this). 
    """
    def load_data_to_collection(self, name, batch_size, df, embeddings):
        collection = self.client.collections.use(name)
        with collection.batch.fixed_size(batch_size=batch_size) as batch: #insert data in chunks which makes it easier for cpu
            for i, row in df.iterrows():
                vector_ = embeddings[i]
                object_ = {
                    "index_id" : i,
                    "text_clean" : row['text_clean'],
                    "source": row['source'],
                    "sentiment_label" : row['sentiment_label'],
                    "sentiment_score" : None if math.isnan(row['sentiment_score']) else row['sentiment_score'],
                    "topic_label": row['topic_label'],
                    "keyword": ast.literal_eval(row['keyword']),
                    "entities" : ast.literal_eval(row['entities']),
                    "author": None if pd.isna(row['author']) or row['author'] == "" else row['author'],
                    "like_count": None if math.isnan(row['like_count']) else row['like_count']
                }
                batch.add_object(properties=object_, vector=vector_)

    #not important but i wanted to know the size of the collection we made
    def check_count(self):
        collection = self.client.collections.use("Refract")
        result = collection.aggregate.over_all(total_count=True)
        print(result.total_count)
        
    def close(self):
        self.client.close()
    
            

