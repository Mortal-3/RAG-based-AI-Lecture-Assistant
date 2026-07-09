# RAG based AI Lecture Assistant

This project turns recorded lecture videos into a practical study tool. It extracts speech from videos, transcribes the audio into searchable text, creates embeddings for transcript chunks, and lets you query your own lecture content.

## What this does

The project follows this workflow:

1. `process_videos.py`
   - Converts files in `videos/` into MP3 audio files in `audios/`.
   - Uses the video filename to preserve the tutorial number and title in the audio name.

2. `create_chunks.py`
   - Transcribes each MP3 audio file using Whisper.
   - Splits the transcript into timestamped chunks.
   - Saves each lecture transcript as a JSON file in `jsons/`.

3. `read_chunks.py`
   - Loads JSON transcript files from `jsons/`.
   - Creates embeddings for each transcript chunk using a local Ollama API.
   - Saves the embedding dataset to `embeddings.joblib`.

4. `process_incomming.py`
   - Loads `embeddings.joblib`.
   - Prompts for a user question.
   - Computes similarity between the question embedding and transcript chunks.
   - Prints the top matching chunks.

## What you need

- Python 3.11 or newer
- `ffmpeg` available on your system `PATH`
- `whisper` package
- `requests`, `tqdm`, `pandas`, `scikit-learn`, `numpy`, `joblib`
- A running Ollama embedding API at `http://localhost:11434/api/embed`

## Setup

1. Activate the project environment:

```powershell
& .\aienv\Scripts\Activate.ps1
```

2. Install required packages:

```powershell
python -m pip install -r requirements.txt
```

If you don’t have `requirements.txt`, use:

```powershell
python -m pip install whisper requests tqdm pandas scikit-learn numpy joblib
```

3. Start Ollama locally so the embedding endpoint works.

## File run order

Follow these steps in order:

1. `python process_videos.py`
   - Converts `videos/` files into `audios/` MP3s.

2. `python create_chunks.py`
   - Transcribes audio files and saves JSON transcripts in `jsons/`.

3. `python read_chunks.py`
   - Builds embeddings from the JSON transcript chunks and saves `embeddings.joblib`.

4. `python process_incomming.py`
   - Loads the embeddings file and asks for a query.
   - Returns the most similar transcript chunks for the question.

## Notes

- Do not run `read_chunks.py` before `create_chunks.py` unless you already have JSON files in `jsons/`.
- Do not run `process_incomming.py` before `read_chunks.py`, because it needs `embeddings.joblib`.
- `create_chunks.py` currently transcribes in Hindi (`language="hi"`).
- `process_videos.py` expects video filenames with a `#` tutorial number and ` | ` separator.
- `read_chunks.py` does not ask questions; it only creates embeddings.

## Why this is useful

This repo helps you learn from lecture videos by converting them into searchable text and embeddings. You can quickly find the right part of a lecture using natural language queries instead of rewatching the entire video.

## Ideas for later

- Add a proper `requirements.txt` file.
- Build a nicer query interface that returns top answers.
- Support more video filename styles.
- Add better error handling for missing files and API problems.
