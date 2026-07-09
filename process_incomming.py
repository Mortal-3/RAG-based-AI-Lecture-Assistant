import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
# from read_chunks import create_embedding
import joblib
import requests


# -----------------------------
# Configuration
# -----------------------------
OLLAMA_URL = "http://localhost:11434/api/embed"
MODEL_NAME = "bge-m3"
JSON_FOLDER = "jsons"
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







df=joblib.load("embeddings.joblib")

# User Question (Take a input from user and create embedding for it)

incoming_query = input("\nPlease enter your question: ")
user_embedding = create_embedding(incoming_query) # Create embedding for user question

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
top_result=3
max_indices=similarities.argsort()[::-1][:top_result]
new_df = df.iloc[max_indices].copy()

new_df["similarity"] = similarities[max_indices]

print(new_df[
    [
        "chunk_id",
        "title",
        "similarity",
        "text"
    ]
])