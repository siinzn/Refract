import pandas as pd
from pathlib import Path

def load_dataset(filepath: str):
    df = pd.read_csv(filepath)
    return df

script_dir = Path(__file__).parent
root_dir = script_dir.parent.parent


#think later how to make this global
