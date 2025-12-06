from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
# Import the new factory functions
from agents.tools import get_vector_search_tool, get_plotting_tool
import pandas as pd

def get_data_analyst_agent(df: pd.DataFrame, api_key: str):
    """
    Creates and returns a LangChain Data Analyst Agent.
    This agent has access to:
    1. The pandas DataFrame (for quantitative analysis)
    2. A Vector Search tool (for qualitative retrieval)
    3. A Plotting tool (for visualization)
    """
    
    # Initialize LLM (using gpt-4o for robust reasoning)
    llm = ChatOpenAI(
        model_name="gpt-4o",
        temperature=0, # Ensure factual responses
        openai_api_key=api_key
    )
    
    # Define tools for the agent
    # We invoke the factory functions to get the configured tools
    tools = [
        get_vector_search_tool(api_key),
        get_plotting_tool(df)
    ]

    # The core prompt that defines the agent's personality and instructions
    prefix = """
    You are an expert Autonomous Data Analyst Agent. Your goal is to assist the user in understanding their dataset.
    You have access to the following tools:
    
    1.  **pandas_tool**: This is your primary tool for any quantitative question (e.g., "What is the average sales?", "Filter for region X"). The dataframe is available as `df`. You can write and execute python code to manipulate it.
    2.  **vector_search_tool**: Use this for qualitative questions that require understanding the context or descriptions within the data (e.g., "Find products related to 'eco-friendly'", "What are the key themes in the feedback?").
    3.  **plotting_tool**: Use this whenever the user asks for a visualization, chart, graph, or plot. You must generate valid python code using `matplotlib.pyplot` (as `plt`) or `seaborn` (as `sns`).
    
    **Important Instructions:**
    -   **Always** try to answer the user's question directly using the pandas dataframe first if it's a numerical query.
    -   If the query is ambiguous or qualitative, use the `vector_search_tool` to gain context.
    -   If the user asks for a plot, you **MUST** use the `plotting_tool`. The tool will automatically save the image to the 'plots' directory.
    -   After using the plotting tool, your final answer should be a summary of what the plot shows. You do NOT need to show the image yourself, the UI will handle it.
    -   Be concise and professional.
    -   If you cannot answer the question with the available tools, state that clearly.
    
    You should follow this thought process:
    1.  Understand the user's query.
    2.  Decide which tool is best suited for the task.
    3.  Formulate the input for the tool.
    4.  Execute the tool.
    5.  Synthesize the tool's output into a final answer.
    """

    # Create the Agent
    # We use the `create_pandas_dataframe_agent` as the base, as it's highly optimized for data tasks.
    # We pass our custom tools as `extra_tools` so the agent can decide when to use them.
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        agent_type=AgentType.OPENAI_FUNCTIONS, # Best for robust tool-calling with newer models
        verbose=True, # Set to True to see the agent's thought process in the terminal
        prefix=prefix,
        extra_tools=tools,
        allow_dangerous_code=True # Required for the plotting tool's exec() and pandas operations
    )
    
    return agent