
🤖 #Agentic Data Analyst

A fully autonomous data analysis system powered by LangChain, OpenAI, and FAISS.

This project implements an AI Data Analyst that can ingest raw datasets (CSV/Excel), understand them contextually using Vector Search (RAG), and perform complex quantitative analysis and visualization capabilities on command. It features a modern Streamlit interface for seamless interaction.

🚀 Key Features

📂 Automated Ingestion & Cleaning:

Supports .csv and .xlsx uploads.

Automatically handles missing values, detects date columns, and cleans data types before analysis.

🧠 Hybrid Intelligence (RAG + Pandas):

Qualitative Analysis: Uses FAISS vector search to understand text descriptions, categorical trends, and "unstructured" queries (e.g., "What are the common themes in feedback?").

Quantitative Analysis: A specialized LangChain Pandas Agent executes Python code to calculate exact metrics (e.g., "What is the average sales for Region X?").

📊 Autonomous Visualization:

The agent can decide when to generate a plot.

Uses Matplotlib/Seaborn to create charts and automatically displays them in the chat interface.

🧹 Session Management:

Built-in "Hard Reset" ensures no cross-contamination between analysis sessions. Every file upload triggers a fresh environment cleanup.

🛠️ Tech Stack

Framework: Streamlit

LLM Orchestration: LangChain & langchain-experimental

Vector Database: FAISS (Facebook AI Similarity Search)

Model: OpenAI gpt-4o (Embeddings & Chat)

Data Processing: Pandas, OpenPyXL

Visualization: Matplotlib, Seaborn

🏗️ Architecture

The system follows a multi-step Agentic Loop:

Ingestion Layer:

Raw data is loaded and preprocessed (NaN filling, type casting).

A Global Context JSON is generated (summary stats, column types) to give the LLM a "bird's eye view".

Embedding Layer:

Each row is converted into a rich text summary (e.g., "Sales: 500 (Above Average) | Region: West").

These summaries are embedded using OpenAI embeddings and stored in a local FAISS index.

Agent Core:

The Main Agent receives a user query.

It evaluates which tool to use:

pandas_tool: For math/code execution.

vector_search_tool: For semantic search/context retrieval.

plotting_tool: For generating visual charts.

The agent executes the tool, observes the output, and synthesizes a final natural language response.

📦 Installation

Clone the repository:

git clone [https://github.com/yourusername/agentic-data-analyst.git](https://github.com/yourusername/agentic-data-analyst.git)
cd agentic-data-analyst


Create a virtual environment (Recommended):

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


🖥️ Usage

Run the application:

streamlit run app.py


Configure API Key:

The app will launch in your browser.

In the Sidebar, paste your OpenAI API Key. (This is required for the Agent and Embeddings).

Upload Data:

Upload any CSV or Excel file.

The system will automatically clean, ingest, and build the vector index (watch the progress bar!).

Chat:

Ask questions like:

"Show me the trend of Sales over time." (Triggers Plotting Tool)

"Which region has the most complaints?" (Triggers Vector Search/Pandas)

"Give me a summary of the dataset." (Triggers Global Context)

📂 Project Structure

├── agents/
│   ├── data_analyst_agent.py  # Main LangChain Agent definition
│   └── tools.py               # Custom tools (Vector Search, Plotting)
├── embedding/
│   ├── embedding_service.py   # Row serialization & Global Context generation
│   └── vectorstore.py         # FAISS index creation & loading
├── ingestion/
│   ├── data_ingestion.py      # File loading logic
│   └── preprocessing.py       # Data cleaning logic
├── app.py                     # Main Streamlit UI application
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation


⚠️ Notes

Data Privacy: Your API key is not stored persistently. All data (uploads, vector indices, plots) is stored locally in the data/ and plots/ folders and is wiped automatically whenever you restart the app or upload a new file.

Model Cost: This system makes calls to OpenAI for both Embeddings (one-time per file) and Chat (per query). Ensure your account has sufficient credits.
