from src.preprocessing.utils import root_dir, load_dataset
from src.preprocessing.cleaner import Cleaner

input_path = root_dir / "data" / "test" / "preprocessor_test.csv" #add your dataset path
output_path = root_dir / "data" / "test" / "test_cleaned.csv" #add desired path for your cleaned dataset to be saved
df = load_dataset(input_path)
print(len(df))

my_cleaner = Cleaner(source="test", column_name="text", min_words=8)
cleaned_df = my_cleaner.run(df)
print(len(cleaned_df))
cleaned_df.to_csv(output_path, index=False)
