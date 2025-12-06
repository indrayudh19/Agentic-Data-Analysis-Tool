import pandas as pd
import os

def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads a dataset from a given file path (CSV or Excel).
    
    Args:
        file_path (str): Path to the file.
        
    Returns:
        pd.DataFrame: Loaded DataFrame.
        
    Raises:
        FileNotFoundError: If file doesn't exist.
        ValueError: If file format is not supported.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_ext == '.csv':
            df = pd.read_csv(file_path)
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
            
        return df
        
    except Exception as e:
        raise Exception(f"Error loading data: {str(e)}")