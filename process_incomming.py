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
URL = "http://localhost:11434/api/generate"
MODEL_NAME = "bge-m3"
JSON_FOLDER = "jsons"
# Create embedding for the user input Query or prompt
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



def inference(prompt):
    try:
        response = requests.post(
            URL,
            json={
                "model": "deepseek-r1:8b",
                "prompt": prompt,
                "stream": False
            },
            timeout=500
        )

        response.raise_for_status()
        data = response.json()

        return data["response"]

    except requests.exceptions.RequestException as e:
        print(e)
        return None




#Get the embeddings dataframe from the joblib file created  by read_chunks.py by joblib.dump(df, "embeddings.joblib"). Here df is the datafram pushed/dumped in the joblib file. The dataframe contains the embeddings of the chunks of text read from the json files in the jsons folder. The dataframe has columns: chunk_id, title, text, embedding. The embedding column contains the embeddings of the chunks of text.

df=joblib.load("embeddings.joblib")

# User Question (Take a input from user and create embedding for it)

incoming_query = input("\nPlease enter your question: ")
user_embedding = create_embedding(incoming_query) # Create embedding for user question

# if user_embedding is not None:
#     print("\nUser Question Embedding:")
#     print("Vector Size :", len(user_embedding))
#     print("First 5     :", user_embedding[:5])
# else:
#     print("\nFailed to create embedding for user question.")



# Find similarities of question embedding with other embeddings in the dataframe
# print (np.vstack(df["embedding"].values))
# print(np.vstack(df["embedding"]).shape)
similarities=cosine_similarity([user_embedding], np.vstack(df["embedding"].values)).flatten()
# print("\nSimilarities with each chunk:")
# print(similarities)
top_result=3
max_indices=similarities.argsort()[::-1][:top_result]
new_df = df.iloc[max_indices].copy()

new_df["similarity"] = similarities[max_indices]

# print(new_df[
#     [
#         "chunk_id",
#         "title",
#         "similarity",
#         "text"
#     ]
# ])

# Create a prompt for the llm
prompt=f'''Here are vidos chunks containing video number,video title ,start time secons,end time in seconds,the text at that  time:
{new_df[['chunk_id', 'title', 'similarity', 'text']].to_string(index=False)}
-------------------------------------------

"{incoming_query}"
User asked this question related  to the video chunks ,you have to answer the question based on the video chunks provided below and guide the user to the relevant chunk of the video.if user ask unreated questiion tehn tell him that  you can only answer the question related to the video chunks provided below and you cannot answer any other question.Tell him  thath you can only answer question related to the course video
'''

#Demo purpose for promt testing
# with open ("prompt.txt", "w", encoding="utf-8") as f:
#     f.write(prompt)

#Introspecting Top Result
# for index,item in new_df.iterrows():
#     print(f"\nChunk ID: {item['chunk_id']}")
#     print(f"Title: {item['title']}")


response=(inference(prompt))
print(response)
with open("response.txt", "w", encoding="utf-8") as f:
    f.write(response)

