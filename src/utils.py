import glob
import os
import pandas as pd

def load_data():
    data_dir = '../data/' 
    file_extension = '*.csv'

    all_files = glob.glob(os.path.join(data_dir, file_extension))
    
    df = []
    
    for filename in all_files:
        df.append(pd.read_csv(filename))
    
    return df
