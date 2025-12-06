import pandas as pd
import json
import os
from langchain_core.documents import Document

def generate_global_context(df: pd.DataFrame) -> str:
    """
    Analyzes the entire dataframe to generate a Global Context JSON.
    This helps the Agent understand the 'Big Picture' before looking at specific rows.
    """
    context = {
        "columns": list(df.columns),
        "shape": df.shape,
        "missing_values": df.isnull().sum().to_dict(),
        "data_types": df.dtypes.astype(str).to_dict(),
        "numerical_stats": df.describe().to_dict() if not df.select_dtypes(include='number').empty else {},
        "categorical_samples": {col: df[col].unique().tolist()[:5] for col in df.select_dtypes(include='object').columns}
    }
    
    # Save to file
    with open("data/context.json", "w") as f:
        json.dump(context, f, indent=4)
        
    return "data/context.json"

def create_row_documents(df: pd.DataFrame):
    """
    Converts each DataFrame row into a LangChain Document.
    The 'page_content' is a rich narrative description of the row.
    The 'metadata' holds the original raw values for retrieval.
    """
    documents = []
    
    # We pre-calculate some stats to add qualitative context (e.g., "High" vs "Low")
    num_cols = df.select_dtypes(include='number').columns
    means = df[num_cols].mean()
    
    for index, row in df.iterrows():
        # 1. Build Narrative Description (The "Content" for the LLM)
        description_parts = []
        for col in df.columns:
            val = row[col]
            
            # Qualitative enrichment for numbers
            qualifier = ""
            if col in num_cols:
                if val > means[col]:
                    qualifier = "(Above Average)"
                elif val < means[col]:
                    qualifier = "(Below Average)"
            
            description_parts.append(f"{col}: {val} {qualifier}")
            
        page_content = " | ".join(description_parts)
        
        # 2. Store Metadata (The "Source of Truth")
        # We convert the row to a dict and ensure all values are JSON serializable
        metadata = row.to_dict()
        metadata["row_index"] = index
        
        doc = Document(page_content=page_content, metadata=metadata)
        documents.append(doc)
        
    return documents