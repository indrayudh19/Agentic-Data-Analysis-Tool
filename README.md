🤖 Agentic Data Analyst

A fully autonomous AI-powered data analysis system built with LangChain, OpenAI, FAISS, and Streamlit.

This project delivers an AI Data Analyst capable of ingesting raw datasets, cleaning them, embedding them for semantic understanding, and performing quantitative + qualitative analysis autonomously through agentic loops.
It also features a modern Streamlit dashboard for seamless user interaction.

🚀 Key Features
📂 Automated Ingestion & Cleaning

Supports CSV (.csv) and Excel (.xlsx) file uploads

Automatically:

Handles missing values

Detects date columns

Fixes inconsistent data types

Prepares the dataset for analysis within seconds

🧠 Hybrid Intelligence: RAG + Pandas
✔️ Qualitative Analysis (Semantic Understanding)

Powered by FAISS Vector Search, the system can:

Understand unstructured questions

Detect patterns

Identify semantic themes (e.g., "What are the common issues reported by customers?")

✔️ Quantitative Analysis (Code Execution)

A dedicated LangChain Pandas Agent executes Python operations such as:

Mean/median calculations

Grouping, filtering, aggregations

Trend analysis

Numerical comparisons

📊 Autonomous Visualization

The agent decides when a plot is necessary

Automatically generates:

Line charts

Bar charts

Scatter plots

Distribution charts

Uses Matplotlib + Seaborn

Displays plots directly inside the Streamlit chat interface

🧹 Session Management

Every dataset upload triggers a Hard Reset

Ensures:

No cross-contamination

Clean memory

Fresh vector index

All temporary files stored locally and wiped on reset

🛠️ Tech Stack

Framework: Streamlit
LLM Orchestration: LangChain, langchain-experimental
Vector Database: FAISS
Models: OpenAI GPT-4o (Chat + Embeddings)
Data Processing: Pandas, OpenPyXL
Visualization: Matplotlib, Seaborn

🏗️ Architecture

The system follows a multi-layer Agentic Loop:

1️⃣ Ingestion Layer

Loads and preprocesses raw data

Cleans NaN values and inconsistent types

Generates a Global Context JSON summarizing the dataset

2️⃣ Embedding Layer

Converts every row into a semantic text summary

Embeds using OpenAI embeddings

Stores vectors in a local FAISS index

3️⃣ Agent Core

The main agent receives user questions and decides which tool to use:

Tool	Purpose
pandas_tool	For calculations, metrics, and code execution
vector_search_tool	For semantic lookup using FAISS
plotting_tool	For automatic chart generation

The agent executes tools, receives observations, and builds a final natural language answer.

📦 Installation
1. Clone the repository
git clone https://github.com/yourusername/agentic-data-analyst.git
cd agentic-data-analyst

2. Create a virtual environment (Recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

🖥️ Usage
Start the App
streamlit run app.py

Configure API Key

The UI will open in your browser

Paste your OpenAI API key in the sidebar

Upload Data

Upload a .csv or .xlsx file

The system:

Cleans it

Generates embeddings

Builds vector index

Status is shown via a progress bar

Start Chatting

Examples:

“Show me the trend of Sales over time.”
→ Triggers plotting tool

“Which category has the highest returns?”
→ RAG + Pandas

“Give me a complete summary of the dataset.”
→ Global context reasoning

📂 Project Structure
├── agents/
│   ├── data_analyst_agent.py      # Main LangChain Agent
│   └── tools.py                   # Custom tools (Vector Search, Plotting)
│
├── embedding/
│   ├── embedding_service.py       # Row summaries & global context
│   └── vectorstore.py             # FAISS index management
│
├── ingestion/
│   ├── data_ingestion.py          # File loading logic
│   └── preprocessing.py           # Dataset cleaning logic
│
├── app.py                         # Streamlit UI
├── requirements.txt               # Dependencies
└── README.md                      # Documentation

⚠️ Important Notes
🔐 Data Privacy

Your OpenAI API key is never stored

All user data remains local

Temporary files inside data/ and plots/ are automatically deleted on reset

💰 Model Costs

The system uses OpenAI models for:

Row embeddings (one-time per upload)

Chat responses (on every question)

Ensure your OpenAI account has sufficient credits.
