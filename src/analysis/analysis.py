from src.analysis.analyser import Analyser
from src.analysis.utils import root_dir, load_dataset

input_path = root_dir / "data" / "test" / "test_keywords.csv" #add your dataset path
output_path = root_dir / "data" / "test" / "test_entities.csv" #add desired path for your cleaned dataset to be saved
df = load_dataset(input_path)
print(len(df))

analyser = Analyser(source="test", column_name="text_clean")
#sentiment = analyser.sentiment_analysis(df)
#sentiment.to_csv(output_path, index=False)

#keyword = analyser.keyword_extraction(df)
#keyword.to_csv(output_path, index=False)

entities = analyser.named_entity(df)
entities.to_csv(output_path, index=False)