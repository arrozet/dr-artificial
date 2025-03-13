import os
import pandas as pd

def load_csv_context(directory_path):
    """Load all CSV files from the given directory and its subdirectories, and convert them to a string context"""
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
                        context += f"CSV Data Context from {file_path}:\n{df.to_string()}\n\n"
                    except Exception as e:
                        relative_path = os.path.relpath(file_path, directory_path)
                        print(f"Error reading {relative_path}: {e}")
        
        print(f"Loaded context from all CSV files in {directory_path} successfully.")
        return context
    except Exception as e:
        print(f"Error loading CSV files: {e}")
        return None