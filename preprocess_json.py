# Converting text to vector (Embegginh  via BGE-m3 model) using the local API endpoint install ollama  1st.
# Install: requests, tqdm
# pip install tqdm requests

import os
import json
import requests
import pandas as pd
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib

# -----------------------------
# Configuration
# -----------------------------
OLLAMA_URL = "http://localhost:11434/api/embed"
MODEL_NAME = "bge-m3"
JSON_FOLDER = "jsons"

# -----------------------------
# Create embedding
# -----------------------------
def create_embedding(text):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "input": text
            },
            timeout=500
        )

        response.raise_for_status()

        data = response.json()

        if "embeddings" not in data:
            print("Unexpected response:")
            print(data)
            return None

        return data["embeddings"][0]

    except requests.exceptions.RequestException as e:
        print(f"\nRequest Error:\n{e}")
        return None


# -----------------------------
# Check JSON folder
# -----------------------------
if not os.path.exists(JSON_FOLDER):
    raise FileNotFoundError(
        f"Folder '{JSON_FOLDER}' does not exist."
    )

json_files = [
    f for f in os.listdir(JSON_FOLDER)
    if f.endswith(".json")
]

if len(json_files) == 0:
    raise FileNotFoundError(
        f"No JSON files found inside '{JSON_FOLDER}'."
    )

# -----------------------------
# Process Files
# -----------------------------
records = []
chunk_id = 0

for filename in tqdm(json_files, desc="Processing JSON files"):

    filepath = os.path.join(JSON_FOLDER, filename)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = json.load(f)

    except Exception as e:
        print(f"\nCould not read {filename}")
        print(e)
        continue

    chunks = content.get("chunks", [])

    for chunk in tqdm(
        chunks,
        desc=f"Embedding {filename}",
        leave=False
    ):

        text = chunk.get("text", "").strip()

        if not text:
            continue

        embedding = create_embedding(text)

        if embedding is None:
            continue

        records.append(
            {
                "chunk_id": chunk_id,
                "document_id": content.get("document_id"),
                "title": content.get("title"),
                "file_name": filename,
                "text": text,
                "embedding": embedding
            }
        )

        chunk_id += 1

# -----------------------------
# Create DataFrame
# -----------------------------
df = pd.DataFrame.from_records(records)

# save thsi data frame
joblib.dump(df, "embeddings.joblib")

print("\nDataFrame Preview")
print(df.head())

print("\nDataFrame Info")
print(df.info())

print("\nTotal Chunks:", len(df))

# if len(df) > 0:
#     first = df.iloc[0]

#     print("\nFirst Record")
#     print("-" * 40)
#     print("Chunk ID    :", first["chunk_id"])
#     print("Document ID :", first["document_id"])
#     print("Title       :", first["title"])
#     print("File Name   :", first["file_name"])
#     print("Text        :", first["text"])
#     print("Vector Size :", len(first["embedding"]))
#     print("First 5     :", first["embedding"][:5])
# else:
#     print("\nNo embeddings were created.")

