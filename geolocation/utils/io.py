import pandas as pd

def load_csv_generic(filepath):

    df = pd.read_csv(filepath, comment = '#')

    return df
