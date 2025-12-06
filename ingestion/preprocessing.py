import pandas as pd
import numpy as np

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and preprocesses the DataFrame:
    1. Removes duplicates.
    2. Infers and converts data types (Date, Numeric).
    3. Handles missing values (simple strategies).
    """
    # 1. Remove exact duplicates
    df = df.drop_duplicates()
    
    # 2. Smart Type Inference
    for col in df.columns:
        # Attempt to convert to datetime
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_datetime(df[col])
            except (ValueError, TypeError):
                # If it fails, check if it's numeric but stored as string
                try:
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    pass # Keep as object (string)

    # 3. Handle Missing Values
    # Strategy: 
    # - Numeric: Fill with mean
    # - Categorical: Fill with 'Unknown'
    # - DateTime: Fill with forward fill or drop (here we drop rows with missing dates for safety)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    datetime_cols = df.select_dtypes(include=['datetime64']).columns

    # Fill numeric NaNs with mean
    if not numeric_cols.empty:
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    
    # Fill categorical NaNs with "Unknown"
    if not categorical_cols.empty:
        df[categorical_cols] = df[categorical_cols].fillna("Unknown")
        
    # Drop rows where datetime is missing (dates are usually critical for trends)
    if not datetime_cols.empty:
        df = df.dropna(subset=datetime_cols)

    return df