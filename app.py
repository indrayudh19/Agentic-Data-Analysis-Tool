import streamlit as st
import pandas as pd
import os
import sys
import shutil
import matplotlib.pyplot as plt

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ingestion.data_ingestion import load_data
from ingestion.preprocessing import preprocess_data
from embedding.embedding_service import create_row_documents, generate_global_context
from embedding.vectorstore import build_vector_store
from agents.data_analyst_agent import get_data_analyst_agent

# --- Page Config ---
st.set_page_config(page_title="Agentic Data Analyst", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# --- HARD RESET LOGIC ---
if "startup_processed" not in st.session_state:
    cleanup_paths = ["data", "faiss_index", "plots"] # Added plots to cleanup
    for path in cleanup_paths:
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                print(f"🧹 Cleanup: Removed {path}")
            except Exception as e:
                print(f"⚠️ Error cleaning {path}: {e}")
    
    # Create necessary folders
    os.makedirs("data", exist_ok=True)
    os.makedirs("plots", exist_ok=True) # Ensure plots folder exists
    
    st.session_state.startup_processed = True

# --- Session State Initialization ---
if "messages" not in st.session_state: st.session_state.messages = []
if "df" not in st.session_state: st.session_state.df = None
if "openai_api_key" not in st.session_state: st.session_state.openai_api_key = ""
if "processed_file" not in st.session_state: st.session_state.processed_file = None
if "agent" not in st.session_state: st.session_state.agent = None

def reset_pipeline():
    """Helper to wipe data when a NEW file is uploaded."""
    cleanup_paths = ["data", "faiss_index", "plots"]
    for path in cleanup_paths:
        if os.path.exists(path): shutil.rmtree(path)
    os.makedirs("data", exist_ok=True)
    os.makedirs("plots", exist_ok=True)
    st.session_state.df = None
    st.session_state.messages = []
    st.session_state.processed_file = None
    st.session_state.agent = None

# --- Sidebar ---
with st.sidebar:
    st.header("🔑 Configuration")
    api_key_input = st.text_input("OpenAI API Key", type="password", value=st.session_state.openai_api_key, help="Required for Agent functionality.")
    if api_key_input: st.session_state.openai_api_key = api_key_input

    st.divider()
    st.header("📂 Data Source")
    uploaded_file = st.file_uploader("Upload Dataset", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        is_new_file = st.session_state.processed_file != uploaded_file.name
        if is_new_file and st.session_state.openai_api_key:
            try:
                reset_pipeline()
                st.toast("System Reset: New analysis started.", icon="🧹")
                file_path = os.path.join("data", uploaded_file.name)
                with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())
                st.session_state.processed_file = uploaded_file.name

                # --- PIPELINE START ---
                with st.status("🚀 Processing Data Pipeline...", expanded=True) as status:
                    status.write("📥 Loading data...")
                    raw_df = load_data(file_path)
                    status.write("🧹 Cleaning & Preprocessing...")
                    clean_df = preprocess_data(raw_df)
                    st.session_state.df = clean_df
                    status.write("🌍 Generating Global Context...")
                    generate_global_context(clean_df)
                    status.write("🧠 Building Knowledge Base...")
                    documents = create_row_documents(clean_df)
                    build_vector_store(documents, st.session_state.openai_api_key)
                    
                    # --- AGENT INITIALIZATION ---
                    status.write("🤖 Initializing AI Agent...")
                    st.session_state.agent = get_data_analyst_agent(st.session_state.df, st.session_state.openai_api_key)
                    
                    status.update(label="✅ System Ready! AI Agent is Online.", state="complete", expanded=False)
                st.success(f"Processed: {uploaded_file.name}")
            except Exception as e:
                st.error(f"Pipeline Error: {e}")
                st.session_state.processed_file = None
        elif not st.session_state.openai_api_key:
            st.warning("⚠️ Please enter your OpenAI API Key above.")
    else:
        if st.session_state.processed_file is not None:
            reset_pipeline()
            st.rerun()
    
    st.divider()
    st.markdown("### System Status")
    st.caption(f"🟢 Ingestion: {'Active' if st.session_state.df is not None else 'Idle'}")
    st.caption(f"🟢 Vector DB: {'Active' if os.path.exists('faiss_index') else 'Not Built'}")
    st.caption(f"🟢 Agent: {'Ready' if st.session_state.agent is not None else 'Idle'}")

# --- Main Interface ---
st.title("🤖 Autonomous Agentic Data Analyst")

# Layout
tab1, tab2 = st.tabs(["📊 Data Overview", "💬 Chat with Analyst"])

# --- Tab 1: Data Overview ---
with tab1:
    if st.session_state.df is not None:
        st.subheader("Dataset Preview (Cleaned)")
        st.dataframe(st.session_state.df.head(10), use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Global Context Summary")
            if os.path.exists("data/context.json"):
                import json
                with open("data/context.json", "r") as f: st.json(json.load(f), expanded=False)
        with col2:
            st.subheader("Column Types")
            st.write(st.session_state.df.dtypes.astype(str))
    else:
        st.info("Please upload a dataset and provide an API key to begin.")

# --- Tab 2: Chat Interface ---
with tab2:
    st.subheader("Chat with your Data")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # If a plot path was associated with this message, display it
            if "plot_path" in message:
                st.image(message["plot_path"])

    # Chat Input
    if prompt := st.chat_input("Ask a question (e.g., 'Plot sales by region', 'What are the main trends?')..."):
        if st.session_state.agent is None:
            st.error("⚠️ Agent is not ready. Please upload data and provide an API key first.")
        else:
            # User message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Assistant Response
            with st.chat_message("assistant"):
                with st.spinner("Thinking... 🤖"):
                    try:
                        # 1. Snapshot existing plots
                        existing_plots = set(os.listdir("plots")) if os.path.exists("plots") else set()
                        
                        # 2. Run Agent
                        response = st.session_state.agent.invoke({"input": prompt})
                        output_text = response["output"]
                        
                        # 3. Detect new plots
                        current_plots = set(os.listdir("plots")) if os.path.exists("plots") else set()
                        new_plots = list(current_plots - existing_plots)
                        
                        # Prepare message package
                        message_package = {"role": "assistant", "content": output_text}
                        
                        st.markdown(output_text)
                        
                        # If a new plot was created, attach it to the message and display it
                        if new_plots:
                            # We take the first new plot found (assumes one plot per turn usually)
                            # Sorting ensures deterministic behavior if multiple are created
                            latest_plot = sorted(new_plots)[-1] 
                            plot_path = os.path.join("plots", latest_plot)
                            
                            message_package["plot_path"] = plot_path
                            st.image(plot_path, caption="Generated Plot")
                        
                        st.session_state.messages.append(message_package)
                        
                    except Exception as e:
                        error_msg = f"Generation Error: {e}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})