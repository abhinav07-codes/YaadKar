# YaadKar

YaadKar is a Chrome extension that summarizes the currently open YouTube video by sending its URL to a FastAPI backend powered by LangChain and Groq.

## What is included

- Chrome extension popup with a single action button
- FastAPI backend with modular services, models, routing, and prompts
- YouTube transcript extraction and validation
- Structured study output with summary, key points, revision notes, and interview questions
- Basic tests for the URL parsing helper

## Backend setup

1. Open a terminal in the project root.
2. Create and activate a Python 3.11 virtual environment.
3. Install dependencies:
   ```bash
   .\.venv311\Scripts\python.exe -m pip install -r backend/requirements.txt pytest
   ```
4. Add your Groq API key to backend/.env.
5. Start the API:
   ```bash
   .\.venv311\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
   ```
6. Verify it is running:
   ```bash
   curl http://127.0.0.1:8000/health
   ```

## Extension setup

1. Open Chrome and navigate to chrome://extensions.
2. Enable Developer mode.
3. Load the unpacked extension from the extension folder in this repository.
4. Open a YouTube video and click the YaadKar extension popup.
5. Press Generate Notes.

## Notes

-- The extension expects the FastAPI backend to be running on http://127.0.0.1:8000.
- The backend requires a valid transcript to exist for the requested video.
- If Groq is not configured, the API returns a clear error message instead of crashing.
