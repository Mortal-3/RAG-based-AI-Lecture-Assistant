# RAG based AI Lecture Assistant

This project turns recorded lecture videos into a practical study tool. It extracts speech from videos, transcribes the audio into searchable text, and uses embeddings to help answer questions from your own lecture content.

## What this does

The project follows a simple flow:

1. `process_videos.py`
   - Converts files in `videos/` into MP3 audio files saved in `audios/`.
   - Uses the video filename to keep the tutorial number and title in the audio name.

2. `create_chunks.py`
   - Transcribes the audio with Whisper.
   - Splits the transcript into timestamped chunks.
   - Saves each lecture transcript as a JSON file in `jsons/`.

3. `read_chunks.py`
   - Loads the processed JSON files.
   - Creates embeddings for each transcript chunk using a local Ollama API.
   - Lets you ask a question and matches it to the most relevant lecture content.

## What you need

- Python 3.11 or newer
- `ffmpeg` available on your system `PATH`
- The `whisper` package
- `requests`, `tqdm`, `pandas`, `scikit-learn`, `numpy`
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
python -m pip install whisper requests tqdm pandas scikit-learn numpy
```

3. Start Ollama locally so the embedding endpoint works.

## How to use it

### 1. Convert videos to audio

Put your lecture videos in `videos/` and run:

```powershell
python process_videos.py
```

This creates MP3 files in `audios/`.

### 2. Convert audio into text chunks

Run:

```powershell
python create_chunks.py
```

This produces JSON files in `jsons/`.

### 3. Ask a question

Run:

```powershell
python read_chunks.py
```

Then type your question and the script will compare it with the transcript chunks.

## Notes

- `read_chunks.py` needs JSON files in `jsons/` and the Ollama endpoint running.
- `create_chunks.py` currently transcribes in Hindi (`language="hi"`).
- `process_videos.py` expects a certain video filename format to extract tutorial number and title.

## Why this is useful

This repo makes it easier to learn from lecture videos by turning them into content you can search with natural questions. It helps you quickly find the right part of the lecture without rewatching the entire video.

## Ideas for later

- Add a proper `requirements.txt` file.
- Build a nicer query interface that returns top answers.
- Support more video filename styles.
- Add better error handling for missing files and API problems.
