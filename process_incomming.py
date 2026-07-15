import joblib
import numpy as np
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity

from config import api_key

# ==========================================================
# Configuration
# ==========================================================

client = OpenAI(api_key=api_key)

EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-5"

EMBEDDINGS_FILE = "embeddings.joblib"
TOP_K = 3


# ==========================================================
# OpenAI API
# ==========================================================

def create_embedding(text: str, model: str = EMBED_MODEL):
    """Generate an embedding using OpenAI."""

    try:
        response = client.embeddings.create(
            model=model,
            input=text,
        )

        return response.data[0].embedding

    except Exception as e:
        print(f"Embedding Error: {e}")
        return None


def inference(prompt: str, model: str = CHAT_MODEL):
    """Generate a response using OpenAI."""

    try:
        response = client.responses.create(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": "You are a helpful course assistant.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return response.output_text

    except Exception as e:
        print(f"OpenAI Error: {e}")
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
        np.vstack(embeddings_df["embedding"].values),
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
- Answer only from the provided context.
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
        embeddings_df,
    )

    prompt = build_prompt(
        retrieved_chunks,
        query,
    )

    answer = inference(prompt)

    print("\nAnswer:\n")
    print(answer)

    with open("response.txt", "w", encoding="utf-8") as file:
        file.write(answer or "")

    print("\nResponse saved to response.txt")


if __name__ == "__main__":
    main()