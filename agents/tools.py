import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import os
import uuid
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import json

# --- Factory Function for Vector Search Tool ---
def get_vector_search_tool(api_key: str):
    """
    Creates a tool with the API key pre-bound.
    """
    
    @tool
    def vector_search_tool(query: str) -> str:
        """
        Useful for answering qualitative questions about the dataset, such as finding similar items, 
        identifying trends based on descriptions, or understanding context. 
        Input should be a natural language query.
        """
        try:
            # Lazy import to avoid circular dependencies
            from embedding.vectorstore import load_vector_store

            # Load the Vector DB
            vectorstore = load_vector_store(api_key)
            if vectorstore is None:
                return "Error: Vector store not found. Please ensure data is indexed."

            # Perform similarity search (Top 5 results)
            docs = vectorstore.similarity_search(query, k=5)
            
            # Load Global Context for better answer synthesis
            try:
                with open("data/context.json", "r") as f:
                    global_context = json.load(f)
            except FileNotFoundError:
                global_context = "No global context available."

            # Use an LLM to synthesize the retrieved documents into a coherent answer
            llm = ChatOpenAI(model_name="gpt-4o", temperature=0, openai_api_key=api_key)
            
            # Prompt for synthesis
            template = """
            You are a data analyst assistant. Answer the user's query based ONLY on the provided context.
            
            Global Dataset Context: {global_context}
            
            Retrieved relevant rows from the dataset:
            {context}
            
            User Query: {query}
            
            Provide a concise and accurate answer based on the information above. If the answer is not in the context, say so.
            """
            prompt = ChatPromptTemplate.from_template(template)
            output_parser = StrOutputParser()
            
            chain = prompt | llm | output_parser
            
            # Format retrieved docs as a single string
            context_str = "\n\n".join([f"Row {i+1}: {doc.page_content}" for i, doc in enumerate(docs)])
            
            response = chain.invoke({
                "global_context": global_context,
                "context": context_str,
                "query": query
            })
            
            return response
            
        except Exception as e:
            return f"Error during vector search: {str(e)}"
    
    return vector_search_tool

# --- Factory Function for Plotting Tool ---
def get_plotting_tool(df: pd.DataFrame):
    """
    Creates a tool with the DataFrame pre-bound.
    Saves plots to the 'plots' directory.
    """
    
    @tool
    def plotting_tool(command: str) -> str:
        """
        Useful for generating plots and charts. The input should be a Python command 
        that uses matplotlib (plt) or seaborn (sns) to create a plot based on the dataframe 'df'. 
        E.g., "sns.barplot(data=df, x='Category', y='Sales'); plt.title('Sales by Category')"
        
        This tool executes the code and SAVES the plot to a file in the 'plots/' directory.
        It returns the path of the saved file.
        """
        try:
            # Ensure plots directory exists
            if not os.path.exists("plots"):
                os.makedirs("plots")
                
            # Create a new figure to avoid conflicts
            plt.figure(figsize=(10, 6))
            
            # Execute the plotting command
            # We use the outer scope 'df' here which is captured by the closure
            exec(command, {'plt': plt, 'sns': sns, 'df': df, 'pd': pd})
            
            # Generate unique filename
            filename = f"plots/plot_{uuid.uuid4()}.png"
            
            # Save plot to file
            plt.savefig(filename)
            plt.close() # Close the figure to free memory
            
            return f"Plot generated and saved to {filename}"
            
        except Exception as e:
            return f"Error generating plot: {str(e)}"

    return plotting_tool