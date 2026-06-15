from src.utils import load_dataset, root_dir
from src.embeddings.embedding import Embedding
from src.vector_db.weaviate import Weaviate

dataset_path = root_dir / "data" / "processed" / "merged_dataset.csv" #add your dataset path
df = load_dataset(dataset_path)
print(len(df))

#collection_name = "RefractTest"
collection_name = "Refract"
batch_size = 10
embedding  = Embedding(column_name="text_clean")
weaviate = Weaviate()
#test_df = df.head(20)

print("starting embedding")
#get embedding for the dataframe
vector1 = embedding.get_embedding(df)
print("embedding done")

#create collection
weaviate.create_collection(collection_name)
print("Created Collection: ", collection_name)
#load data to collection using both dataframe and embeddings that ran earlier
weaviate.load_data_to_collection(name=collection_name, batch_size=batch_size, df=df, embeddings=vector1)
print("loaded data into collection")
#check vector db size
weaviate.check_count()
#well idk if i should leave a comment here for below line.....its very complicated code :((((((
weaviate.close()
print("weaviate closed")

