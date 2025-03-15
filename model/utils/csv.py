import os
import pandas as pd
from config import config as cfg

def load_csv_context(directory_path):
    """
    Load all CSV files from a directory and return a list of DataFrames,
    one for each CSV file, with source_file as the first column in each.
    
    This function recursively searches for CSV files in the specified directory
    and its subdirectories. Each CSV file is read into a pandas DataFrame with
    a source_file column added at the beginning.
    
    Parameters:
    -----------
    directory_path : str
        Path to the directory containing CSV files to load
        
    Returns:
    --------
    list of pandas.DataFrame or None
        A list containing one DataFrame for each CSV file with 'source_file' as 
        the first column in each, or None if an error occurs.
    """
    dataframe_list = []
    
    try:
        # Walk through the directory and its subdirectories
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".csv"):
                    file_path = os.path.join(root, file)
                    try:
                        # Read the CSV file
                        df = pd.read_csv(file_path)
                        
                        # Add source file information as a column
                        relative_path = os.path.relpath(file_path, directory_path)
                        df['source_file'] = relative_path
                        
                        # Reordenar columnas para poner source_file al principio
                        cols = df.columns.tolist()
                        cols.remove('source_file')
                        cols = ['source_file'] + cols
                        df = df[cols]
                        
                        # Append to our list of dataframes
                        dataframe_list.append(df)
                        
                        print(f"Loaded {relative_path} ({len(df)} rows)")
                    except Exception as e:
                        relative_path = os.path.relpath(file_path, directory_path)
                        print(f"Error reading {relative_path}: {e}")
        
        if not dataframe_list:
            print("No CSV files were found or loaded.")
            return None
        
        # Print summary info
        total_rows = sum(len(df) for df in dataframe_list)
        print(f"Loaded {len(dataframe_list)} CSV files with a total of {total_rows} rows.")
            
        return dataframe_list
        
    except Exception as e:
        print(f"Error loading CSV files: {e}")
        return None