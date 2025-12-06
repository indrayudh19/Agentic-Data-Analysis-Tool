import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def build_vector_store(documents, api_key):
    """
    Takes a list of Documents, embeds them using OpenAI, 
    and saves a FAISS index to disk.
    """
    if not documents:
        raise ValueError("No documents to index.")

    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    
    # Create VectorStore
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    # Save to disk
    save_path = "faiss_index"
    vectorstore.save_local(save_path)
    
    return True

def load_vector_store(api_key):
    """
    Loads an existing FAISS index.
    """
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    try:
        vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        return vectorstore
    except Exception as e:
        return None