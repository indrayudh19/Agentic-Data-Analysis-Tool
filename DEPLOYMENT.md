🚀 Deployment Guide: Hugging Face Spaces (Docker)

This guide explains how to host your Agentic Data Analyst for free using Hugging Face Spaces with the Docker SDK.

Step 1: Create the Space

Sign up or log in at huggingface.co.

Go to Spaces (top nav) -> Create new Space.

Space Name: agentic-data-analyst (or similar).

License: Apache 2.0.

Select the Space SDK: Choose Docker. (This is important! Do not select Streamlit, as we want to use our custom Dockerfile).

Space Hardware: Keep as CPU Basic (Free).

Click Create Space.

Step 2: Upload Files

You will be redirected to your Space's repository page. You need to upload your project files here.

Option A: Upload via Web Interface (Easiest)

Click Files tab -> Add file -> Upload files.

Drag and drop the following files/folders:

Dockerfile (The one we just updated)

requirements.txt

app.py

agents/ folder

ingestion/ folder

embedding/ folder

Commit the changes.

Option B: Upload via Git

Clone the empty space:

git clone [https://huggingface.co/spaces/YOUR_USERNAME/agentic-data-analyst](https://huggingface.co/spaces/YOUR_USERNAME/agentic-data-analyst)


Copy your project files into that folder.

Push:

git add .
git commit -m "Initial commit"
git push


Step 3: Deployment

Hugging Face will detect the Dockerfile and automatically start building your container.

Click the App tab to see the build logs.

The "Building" status will change to "Running" in a few minutes.

Once running, you will see your Streamlit interface!

⚠️ Essential Use Tips

API Key: The app still requires the user to paste their OpenAI API key in the sidebar. This is secure; the key is not saved on the server.

Persistence: Hugging Face Spaces (Free) will restart if inactive. This means the data/ and plots/ folders will be wiped. This aligns with your goal of a "fresh start" for every session.