# RAG based AI Lecture Assistant

This project turns lecture videos into a searchable assistant with a Flask backend and React frontend.
It extracts audio from lecture videos, transcribes the speech into text, creates embeddings for each segment, and lets you ask questions about the material.

## Project structure

- `backend/` — Flask API for processing videos, creating transcript chunks, generating embeddings, and answering queries.
- `frontend/` — React app built with Vite for a browser interface.
- `videos/` — Source lecture videos.
- `audios/` — Converted MP3 audio files.
- `jsons/` — Transcript chunk files.
- `aienv/` — Python virtual environment for backend dependencies.

## What this app does

1. Converts lecture videos into MP3 audio.
2. Transcribes audio into timestamped text chunks.
3. Builds semantic embeddings for the transcript chunks.
4. Lets you ask a question and returns the lecture snippets that match best.

## Requirements

- Python 3.11+
- `ffmpeg` installed and available on `PATH`
- Local Ollama embedding API running at `http://localhost:11434/api/embed`
- Node.js and npm or yarn for the frontend

## Backend setup

1. Activate the Python environment:

```powershell
& .\aienv\Scripts\Activate.ps1
```

2. Install backend dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Start the Flask backend:

```powershell
python backend/app.py
```

The backend listens at `http://localhost:5051`.

## Frontend setup

1. Open a new terminal and change into the frontend folder:

```powershell
cd frontend
```

2. Install frontend dependencies:

```powershell
npm install
```

3. Start the React app:

```powershell
npm run dev
```

The frontend runs at `http://localhost:5173`.

## Docker setup

### Build and run everything with Docker Compose

```powershell
docker compose up --build
```

This starts the backend at `http://localhost:5051` and the frontend at `http://localhost:4173`.

### Notes for Docker

- The backend container mounts `videos/`, `audios/`, and `jsons/` from the host.
- The Flask backend is configured to use `http://host.docker.internal:11434/api/embed` for Ollama.

## Using the app

- Click **Convert Videos** to turn files in `videos/` into audio.
- Click **Create Transcript Chunks** to transcribe that audio and save JSON files.
- Enter a question and click **Search Lectures** to find the most relevant transcript snippets.

## Notes

- The backend uses Whisper for transcription and Ollama for generating embeddings.
- The new Flask API exposes the same functionality as the original scripts through endpoints.
- The frontend is a simple React interface built with Vite.

## Future improvements

- Add richer query results with better context.
- Support more video filename formats.
- Improve frontend error handling and UX.
- Add a shared `requirements.txt` for both backend and frontend dependencies.
