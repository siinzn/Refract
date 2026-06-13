from src.analysis.analyser import Analyser
from src.utils import root_dir, load_dataset

"""
#this is for yt comments
input_path = root_dir / "data" / "processed" / "comments_cleaned.csv" #add your dataset path
output_path = root_dir / "data" / "processed" / "comments_enriched.csv" #add desired path for your cleaned dataset to be saved
"""


input_path = root_dir / "data" / "processed" / "stackoverflow_cleaned.csv" #add your dataset path
output_path = root_dir / "data" / "processed" / "stackoverflow_enriched.csv" #add desired path for your cleaned dataset to be saved
df = load_dataset(input_path)
print(len(df))

#analyser = Analyser(source="youtube", column_name="text_clean")
analyser = Analyser(source="stackoverflow", column_name="text_clean")

result = analyser.run(df)
result.to_csv(output_path, index=False)
