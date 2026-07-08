import json
import os
import re
import subprocess
from pathlib import Path

import numpy as np
import requests
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent.parent
VIDEO_DIR = BASE_DIR / "videos"
AUDIO_DIR = BASE_DIR / "audios"
JSON_DIR = BASE_DIR / "jsons"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/embed")
MODEL_NAME = os.getenv("EMBED_MODEL", "bge-m3")
CHUNK_STATE = {
    "records": None,
    "vector_matrix": None,
    "loaded": False,
}

VIDEO_EXTENSIONS = {"mp4", "mkv", "mov", "webm", "flv", "avi"}


def sanitize_filename(value: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9\-_ ]+", "", value)
    return safe.strip().replace(" ", "_")


def process_videos():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    if not VIDEO_DIR.exists():
        raise FileNotFoundError(f"Video folder not found: {VIDEO_DIR}")

    processed = []
    for file_path in sorted(VIDEO_DIR.iterdir()):
        if not file_path.is_file() or file_path.suffix.lower().lstrip(".") not in VIDEO_EXTENSIONS:
            continue

        base_name = file_path.name
        tutorial_number = None
        team_title = None

        if "#" in base_name:
            try:
                tutorial_number = base_name.split(" [")[0].split("#")[1]
            except Exception:
                tutorial_number = None

        if " | " in base_name:
            team_title = base_name.split(" | ")[0]

        if tutorial_number is None:
            tutorial_number = file_path.stem
        if team_title is None:
            team_title = file_path.stem

        output_name = f"{sanitize_filename(tutorial_number)}_{sanitize_filename(team_title)}.mp3"
        output_path = AUDIO_DIR / output_name

        subprocess.run([
            "ffmpeg",
            "-y",
            "-i",
            str(file_path),
            str(output_path),
        ], check=True)

        processed.append(str(output_path.name))

    return {"processed_files": processed}


def create_chunks():
    try:
        import whisper
    except ImportError as exc:
        raise ImportError("The whisper package is required to transcribe audio. Install it first.") from exc

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    JSON_DIR.mkdir(parents=True, exist_ok=True)

    if not any(AUDIO_DIR.glob("*.mp3")):
        raise FileNotFoundError(f"No MP3 audio files found in {AUDIO_DIR}")

    model = whisper.load_model("large-v2")
    saved_files = []

    for audio_path in sorted(AUDIO_DIR.glob("*.mp3")):
        segments = []
        base_name = audio_path.stem
        number, title = base_name.split("_", 1) if "_" in base_name else (base_name, base_name)

        result = model.transcribe(
            audio=str(audio_path),
            language="hi",
            task="transcribe",
            word_timestamps=False,
        )

        for segment in result.get("segments", []):
            segments.append(
                {
                    "number": number,
                    "title": title,
                    "start": segment.get("start"),
                    "end": segment.get("end"),
                    "text": segment.get("text", "").strip(),
                }
            )

        json_data = {
            "document_id": number,
            "title": title,
            "chunks": segments,
            "text": result.get("text", "").strip(),
        }

        output_path = JSON_DIR / f"{audio_path.name}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        saved_files.append(output_path.name)

    CHUNK_STATE["loaded"] = False
    return {"saved_files": saved_files}


def create_embedding(text: str):
    if not text:
        return None

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "input": text,
        },
        timeout=180,
    )
    response.raise_for_status()
    data = response.json()

    embeddings = data.get("embeddings")
    if not embeddings:
        raise ValueError("Embedding response missing embeddings")

    return embeddings[0]


def load_json_records():
    if not JSON_DIR.exists():
        raise FileNotFoundError(f"JSON folder not found: {JSON_DIR}")

    records = []
    json_files = sorted(JSON_DIR.glob("*.json"))
    if not json_files:
        raise FileNotFoundError(f"No JSON files found in {JSON_DIR}")

    for json_path in json_files:
        with open(json_path, "r", encoding="utf-8") as f:
            content = json.load(f)

        for chunk in content.get("chunks", []):
            text = chunk.get("text", "").strip()
            if not text:
                continue

            records.append(
                {
                    "chunk_id": len(records),
                    "document_id": content.get("document_id"),
                    "title": content.get("title"),
                    "file_name": json_path.name,
                    "text": text,
                }
            )

    return records


def build_embeddings():
    records = load_json_records()
    if not records:
        raise ValueError("No transcript chunks available to embed")

    embeddings = []
    for record in records:
        embedding = create_embedding(record["text"])
        if embedding is None:
            continue
        record["embedding"] = embedding
        embeddings.append(embedding)

    if not embeddings:
        raise ValueError("No embeddings could be created")

    CHUNK_STATE["records"] = records
    CHUNK_STATE["vector_matrix"] = np.vstack(embeddings)
    CHUNK_STATE["loaded"] = True
    return {"count": len(records)}


def query_text(question: str, top_k: int = 5):
    if not question:
        raise ValueError("Question cannot be empty")

    if not CHUNK_STATE["loaded"]:
        build_embeddings()

    user_embedding = create_embedding(question)
    if user_embedding is None:
        raise ValueError("Failed to create an embedding for the question")

    matrix = CHUNK_STATE["vector_matrix"]
    if matrix is None or matrix.shape[0] == 0:
        raise ValueError("No embeddings are loaded for search")

    scores = cosine_similarity([user_embedding], matrix).flatten()
    results = []

    for index in np.argsort(scores)[::-1][:top_k]:
        record = CHUNK_STATE["records"][index].copy()
        record["score"] = float(scores[index])
        results.append(record)

    return {"question": question, "results": results}


def get_status():
    return {
        "video_folder": str(VIDEO_DIR),
        "audio_folder": str(AUDIO_DIR),
        "json_folder": str(JSON_DIR),
        "ollama_url": OLLAMA_URL,
        "model": MODEL_NAME,
        "loaded": CHUNK_STATE["loaded"],
    }
