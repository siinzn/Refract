from src.preprocessing.utils import root_dir, load_dataset
from src.preprocessing.cleaner import Cleaner

input_path = root_dir / "data" / "raw" / "stackoverflow.csv" #add your dataset path
output_path = root_dir / "data" / "processed" / "stackoverflow_cleaned.csv" #add desired path for your cleaned dataset to be saved
df = load_dataset(input_path)
print(len(df))

"""
Source can be set according to the dataset, this is for clarity later. Column Name is the name of the column in the
dataset that needs to be cleaned or pre processed. Minimum words can be changed according to the dataset to exclude 
data that are below the minimum word count
"""
my_cleaner = Cleaner(source="stackoverflow", column_name="body", min_words=15) 
cleaned_df = my_cleaner.run(df)
print(len(cleaned_df))
cleaned_df.to_csv(output_path, index=False)
