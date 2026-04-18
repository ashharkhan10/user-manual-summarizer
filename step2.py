import pickle

# Read the text file we created
with open("manual_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Split into pieces manually - no library needed!
def split_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if len(chunk.strip()) > 30:
            chunks.append(chunk)
        start = end - overlap
    return chunks

chunks = split_text(text)

# Save the pieces
with open("chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print(f"Total pieces created: {len(chunks)}")
print("First piece:")
print(chunks[0])