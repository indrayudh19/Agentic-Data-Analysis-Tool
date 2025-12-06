import os
import sys
from pyngrok import ngrok, conf
import subprocess
import time

# --- Configuration ---
# REPLACE THIS WITH YOUR ACTUAL NGROK AUTH TOKEN
NGROK_AUTH_TOKEN = "YOUR_NGROK_AUTH_TOKEN_HERE" 

def start_app():
    print("🚀 Starting Agentic Data Analyst System...")

    # 1. Authenticate with ngrok
    if NGROK_AUTH_TOKEN == "YOUR_NGROK_AUTH_TOKEN_HERE":
        print("❌ Error: Please update the NGROK_AUTH_TOKEN in launch.py")
        sys.exit(1)
    
    # Set the token
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)

    # 2. Cleanup: Kill any existing ngrok processes
    # This fixes the "ERR_NGROK_334" or "address already in use" errors
    print("🔄 Cleaning up old ngrok sessions...")
    ngrok.kill()
    time.sleep(2)  # Give the system a moment to release ports/locks

    # 3. Open a tunnel to the Streamlit port (Default 8501)
    try:
        # We explicitly bind to localhost:8501
        public_url = ngrok.connect(8501).public_url
        print(f"✅ Ngrok Tunnel Established: {public_url}")
        print("   (Click the link above to access the UI remotely)")
    except Exception as e:
        print(f"❌ Error connecting ngrok: {e}")
        print("💡 Tip: If you see 'already online', try waiting 1 minute or manually killing ngrok tasks.")
        sys.exit(1)

    # 4. Run the Streamlit App
    print("📋 Launching Streamlit UI...")
    try:
        # This runs `streamlit run app.py` as a subprocess
        # Added specific flags to ensure port alignment
        process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Keep the script running to keep the tunnel open
        try:
            while True:
                # Read output to keep the buffer from filling up (optional)
                output = process.stdout.readline()
                if output:
                    print(f"   [Streamlit] {output.strip()}")
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            process.terminate()
            ngrok.kill() # Final cleanup

    except FileNotFoundError:
        print("❌ Error: Streamlit not found. Did you run 'pip install -r requirements.txt'?")

if __name__ == "__main__":
    start_app()