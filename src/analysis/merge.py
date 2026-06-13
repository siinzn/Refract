import pandas as pd
from src.utils import root_dir, load_dataset

youtube = root_dir / "data" / "processed" / "comments_enriched.csv" 
stackoverflow = root_dir / "data" / "processed" / "stackoverflow_enriched.csv"

df_youtube = load_dataset(youtube)
df_stackoverflow = load_dataset(stackoverflow)

output_path = root_dir / "data" / "processed" / "merged_dataset.csv" 
result = pd.concat([df_youtube, df_stackoverflow], ignore_index=True)
print(len(result))
result.to_csv(output_path, index=False)
