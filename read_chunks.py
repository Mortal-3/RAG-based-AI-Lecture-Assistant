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
df = pd.DataFrame(records)

print("\nDataFrame Preview")
print(df.head())

print("\nDataFrame Info")
print(df.info())

print("\nTotal Chunks:", len(df))

if len(df) > 0:
    first = df.iloc[0]

    print("\nFirst Record")
    print("-" * 40)
    print("Chunk ID    :", first["chunk_id"])
    print("Document ID :", first["document_id"])
    print("Title       :", first["title"])
    print("File Name   :", first["file_name"])
    print("Text        :", first["text"])
    print("Vector Size :", len(first["embedding"]))
    print("First 5     :", first["embedding"][:5])
else:
    print("\nNo embeddings were created.")

# User Question (Take a input from user and create embedding for it)
incoming_query = input("\nPlease enter your question: ")
user_embedding = create_embedding([incoming_query]) # Create embedding for user question

if user_embedding is not None:
    print("\nUser Question Embedding:")
    print("Vector Size :", len(user_embedding))
    print("First 5     :", user_embedding[:5])
else:
    print("\nFailed to create embedding for user question.")



#Find similarities of question embedding with other embeddings in the dataframe
# print (np.vstack(df["embedding"].values))
# print(np.vstack(df["embedding"]).shape)
similarities=cosine_similarity([user_embedding], np.vstack(df["embedding"].values)).flatten()
# print("\nSimilarities with each chunk:")
# print(similarities)
top_results=3
max_indx=similarities.argsort()[::-1][:top_results] # Getting top 3 most similar chunks 
print(max_indx)
new_df=df.iloc[max_indx]
print("\nTop 3 most similar chunks:")
print(new_df[[ "chunk_id","title","text"]])