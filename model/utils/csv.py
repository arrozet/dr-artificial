import os
import pandas as pd
from config import config as cfg

def load_csv_context(directory_path):
    """
    Load all CSV files from a directory and its subdirectories and convert them to a string context.
    This function recursively searches for CSV files in the specified directory and all its
    subdirectories. Each CSV file is read into a pandas DataFrame and then converted to a 
    string representation that is concatenated into a single context string.
    Parameters:
    -----------
    directory_path : str
        Path to the directory containing CSV files to load
    Returns:
    --------
    str or None
        A string containing the concatenated contents of all CSV files found, with each file
        prefaced by its path. Returns None if an error occurs during directory traversal.
    Notes:
    ------
    - Each CSV file's content is prefixed with "CSV Data Context from {file_path}:"
    - Errors reading individual files are caught and logged but don't stop processing
    - Uses pandas to read CSV files and the to_string() method for text representation
    """
    context = ""
    try:
        # Walk through the directory and its subdirectories
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".csv"):
                    file_path = os.path.join(root, file)
                    try:
                        # Read the CSV file
                        df = pd.read_csv(file_path)
                        # Convert to string representation and append to context
                        context += f"{cfg.CONTEXT_PREFIX} {file_path}: {df.to_string()}\n"
                    except Exception as e:
                        relative_path = os.path.relpath(file_path, directory_path)
                        print(f"Error reading {relative_path}: {e}")
        
        print(f"Loaded context from all CSV files in {directory_path} successfully.")
        return context
    except Exception as e:
        print(f"Error loading CSV files: {e}")
        return None