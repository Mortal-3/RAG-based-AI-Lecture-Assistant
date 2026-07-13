import joblib
import numpy as np
import requests
from sklearn.metrics.pairwise import cosine_similarity

# ==========================================================
# Configuration
# ==========================================================

OLLAMA_HOST = "http://localhost:11434"

EMBED_MODEL = "bge-m3"
CHAT_MODEL = "deepseek-r1:8b"

EMBED_URL = f"{OLLAMA_HOST}/api/embed"
GENERATE_URL = f"{OLLAMA_HOST}/api/generate"

EMBEDDINGS_FILE = "embeddings.joblib"
TOP_K = 3


# ==========================================================
# Ollama API
# ==========================================================

def create_embedding(text: str, model: str = EMBED_MODEL):
    """Generate embedding for the given text."""

    try:
        response = requests.post(
            EMBED_URL,
            json={
                "model": model,
                "input": text
            },
            timeout=300
        )

        response.raise_for_status()
        data = response.json()

        return data["embeddings"][0]

    except (requests.exceptions.RequestException, KeyError) as e:
        print(f"Embedding Error: {e}")
        return None


def inference(prompt: str, model: str = CHAT_MODEL):
    """Generate response from the chat model."""

    try:
        response = requests.post(
            GENERATE_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=600
        )

        response.raise_for_status()
        data = response.json()

        return data["response"]

    except (requests.exceptions.RequestException, KeyError) as e:
        print(f"LLM Error: {e}")
        return None


# ==========================================================
# Retrieval
# ==========================================================

def load_embeddings():
    """Load precomputed embeddings."""

    return joblib.load(EMBEDDINGS_FILE)


def retrieve_chunks(query_embedding, embeddings_df, top_k=TOP_K):
    """Return the most similar chunks."""

    similarities = cosine_similarity(
        [query_embedding],
        np.vstack(embeddings_df["embedding"].values)
    ).flatten()

    top_indices = similarities.argsort()[::-1][:top_k]

    results = embeddings_df.iloc[top_indices].copy()
    results["similarity"] = similarities[top_indices]

    return results


# ==========================================================
# Prompt
# ==========================================================

def build_prompt(context_df, question):
    """Build the prompt for the LLM."""

    context = context_df[
        ["chunk_id", "title", "similarity", "text"]
    ].to_string(index=False)

    return f"""
You are a helpful course assistant.

Answer ONLY using the provided video chunks.

Instructions:
- Answer only from the context.
- Do not make up information.
- If the answer is not available, say:
  "I couldn't find that information in the provided course videos."
- Mention the relevant chunk_id and video title whenever possible.

Video Chunks:
{context}

----------------------------------------

User Question:
{question}
"""


# ==========================================================
# Main
# ==========================================================

def main():

    print("Loading embeddings...")
    embeddings_df = load_embeddings()

    query = input("\nAsk a question: ").strip()

    query_embedding = create_embedding(query)

    if query_embedding is None:
        return

    retrieved_chunks = retrieve_chunks(
        query_embedding,
        embeddings_df
    )

    prompt = build_prompt(
        retrieved_chunks,
        query
    )

    answer = inference(prompt)

    if answer:
        print("\n" + "=" * 60)
        print(answer)
        print("=" * 60)

        with open("response.txt", "w", encoding="utf-8") as file:
            file.write(answer)


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":
    main()