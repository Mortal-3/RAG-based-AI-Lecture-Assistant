# RAG Project

This project converts tutorial videos into searchable text embeddings so a user can ask questions and retrieve relevant content from the processed data.

## Project Overview

The repository contains three main steps:

1. `process_videos.py`
   - Converts video files from `videos/` into MP3 audio files stored in `audios/`.
   - Filenames are normalized using tutorial number and title extracted from the source video filename.

2. `create_chunks.py`
   - Uses OpenAI Whisper (`whisper` Python package) to transcribe audio files from `audios/`.
   - Breaks transcripts into timestamped chunks and saves the results as JSON files in `jsons/`.
   - Each JSON file contains segment metadata and the full transcribed text.

3. `read_chunks.py`
   - Loads chunk JSON files from `jsons/`.
   - Creates vector embeddings for each transcript chunk using a local Ollama embedding API endpoint and the `bge-m3` model.
   - Builds a pandas DataFrame of chunk metadata and embeddings.
   - Takes a user question, creates an embedding for it, and computes cosine similarity against the chunk embeddings.

## Requirements

- Python 3.11+ (project uses the provided `aienv/` virtual environment)
- `ffmpeg` installed and available on `PATH`
- `whisper` Python package
- `requests`, `tqdm`, `pandas`, `scikit-learn`, `numpy`
- Local Ollama embedding API running at `http://localhost:11434/api/embed`

## Recommended Setup

1. Activate the Python virtual environment:

```powershell
& .\aienv\Scripts\Activate.ps1
```

2. Install Python dependencies if not already installed:

```powershell
python -m pip install -r requirements.txt
```

If a `requirements.txt` file is not present, install directly:

```powershell
python -m pip install whisper requests tqdm pandas scikit-learn numpy
```

3. Install and run Ollama locally so the embedding endpoint is available.

## Usage

### Step 1: Convert videos to audio

Place your source video files in `videos/`, then run:

```powershell
python process_videos.py
```

This will create MP3 files in `audios/`.

### Step 2: Transcribe audio into JSON chunks

Run:

```powershell
python create_chunks.py
```

This writes transcription JSON files into `jsons/`.

### Step 3: Generate embeddings and query

Run:

```powershell
python read_chunks.py
```

Then enter your question when prompted. The script will compute similarity scores between your question and each transcript chunk.

## Notes

- `read_chunks.py` expects JSON files under `jsons/` and the Ollama embedding endpoint to be running.
- Transcription is currently configured for Hindi (`language="hi"`) in `create_chunks.py`.
- `process_videos.py` relies on specific filename formats in `videos/` to parse tutorial numbers and titles.

## Project Purpose

This repository is designed to take user input in the form of a question and produce relevant output by searching across processed tutorial data. The workflow converts media into text, generates vector embeddings, and ranks content by semantic similarity.

## Future Improvements

- Add a `requirements.txt` for easier dependency installation.
- Add a query ranking or retrieval interface that returns the most relevant transcript chunks.
- Improve filename parsing and metadata handling for broader video naming formats.
- Add error handling for missing audio files, API failures, and empty transcripts.
