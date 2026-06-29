import pandas as pd
from src.utils import root_dir, load_dataset
from src.preprocessing.cleaner import Cleaner
from src.analysis.analyser import Analyser
from src.embeddings.embedding import Embedding
from src.vector_db.weaviate import Weaviate

"""
This is the pipeline which you can run either with the dataset in data/raw or u can replace with your own
"""

# paths
RAW_YT = root_dir / "data" / "raw" / "comments_final.csv"
RAW_SO = root_dir / "data" / "raw" / "stackoverflow.csv"
CLEAN_YT = root_dir / "data" / "processed" / "comments_cleaned.csv"
CLEAN_SO = root_dir / "data" / "processed" / "stackoverflow_cleaned.csv"
ENRICHED_YT = root_dir / "data" / "processed" / "comments_enriched.csv"
ENRICHED_SO = root_dir / "data" / "processed" / "stackoverflow_enriched.csv"
MERGED = root_dir / "data" / "processed" / "merged_dataset.csv"


print("Preprocessing")
yt_cleaner = Cleaner(source="youtube", column_name="text", min_words=8)
clean_yt = yt_cleaner.run(load_dataset(RAW_YT))
clean_yt.to_csv(CLEAN_YT, index=False)
print(f"YouTube cleaned: {len(clean_yt)} rows")

so_cleaner = Cleaner(source="stackoverflow", column_name="body", min_words=15)
clean_so = so_cleaner.run(load_dataset(RAW_SO))
clean_so.to_csv(CLEAN_SO, index=False)
print(f"Stack Overflow cleaned: {len(clean_so)} rows")


print("Analysis")
yt_analyser = Analyser(source="youtube", column_name="text_clean")
enriched_yt = yt_analyser.run(load_dataset(CLEAN_YT))
enriched_yt.to_csv(ENRICHED_YT, index=False)
print(f"YouTube enriched: {len(enriched_yt)} rows")

so_analyser = Analyser(source="stackoverflow", column_name="text_clean")
enriched_so = so_analyser.run(load_dataset(CLEAN_SO))
enriched_so.to_csv(ENRICHED_SO, index=False)
print(f"Stack Overflow enriched: {len(enriched_so)} rows")


print("Merging")
merged = pd.concat([load_dataset(ENRICHED_YT), load_dataset(ENRICHED_SO)], ignore_index=True)
merged.to_csv(MERGED, index=False)
print(f"Merged: {len(merged)} rows")


print("Embedding and Indexing")
df_merged = load_dataset(MERGED)
embedder = Embedding(column_name="text_clean")
vectors = embedder.get_embedding(df_merged)

db = Weaviate()
db.create_collection("Refract")
db.load_data_to_collection(name="Refract", batch_size=100, df=df_merged, embeddings=vectors)
db.close()
print("Pipeline complete. Weaviate indexed and ready.")



