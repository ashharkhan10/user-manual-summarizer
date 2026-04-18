from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Load our text pieces
with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

print(f"Loaded {len(chunks)} pieces")
print("Converting to numbers... this will take 2-3 minutes, please wait...")

# Load the AI model
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# Convert every piece to numbers
embeddings = model.encode(
    chunks,
    normalize_embeddings=True,
    show_progress_bar=True
)
embeddings = np.array(embeddings).astype("float32")

# Save in searchable database
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

faiss.write_index(index, "vectorstore.faiss")
with open("chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("Done! Database saved successfully!")