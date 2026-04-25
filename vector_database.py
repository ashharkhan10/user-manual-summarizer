from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

texts = [c["text"] for c in chunks]

print(f"Loaded {len(chunks)} chunks")
print("Converting to numbers...")

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
embeddings = model.encode(
    texts,
    normalize_embeddings=True,
    show_progress_bar=True
)
embeddings = np.array(embeddings).astype("float32")

dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

faiss.write_index(index, "vectorstore.faiss")
with open("chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("Done! Database saved.")