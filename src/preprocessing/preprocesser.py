from src.preprocessing.utils import root_dir, load_dataset
from src.preprocessing.cleaner import Cleaner
import pandas as pd

input_path = root_dir / "data" / "test" / "preprocessor_test.csv"
df = load_dataset(input_path)

my_cleaner = Cleaner(source="youtube", column_name="text", min_words=5)
my_cleaner.run(df)