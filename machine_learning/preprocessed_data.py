import os
import pandas as pd

def importing_preprocessed_data():
    csv_path = os.path.abspath('../preprocessed_dataset.csv')
    preprocessed_data = pd.read_csv(csv_path)
    return preprocessed_data