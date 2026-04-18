from dotenv import load_dotenv
import os
load_dotenv()

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from groq import Groq

# Put your Groq API key here
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
index = faiss.read_index("vectorstore.faiss")
with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

def ask_question(question):
    query = model.encode([question], normalize_embeddings=True)
    query = np.array(query).astype("float32")
    scores, indices = index.search(query, k=5)
    relevant_pieces = [chunks[i] for i in indices[0]]
    context = "\n\n".join(relevant_pieces)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Answer questions using only the car manual text provided."},
            {"role": "user", "content": f"Car manual text:\n{context}\n\nQuestion: {question}"}
        ]
    )
    return response.choices[0].message.content

print(ask_question("What type of engine oil should I use?"))