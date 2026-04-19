import pickle

def split_text_with_pages(pages_text, chunk_size=500, overlap=50):
    chunks = []
    for page_num, text in pages_text:
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            if len(chunk.strip()) > 30:
                chunks.append({
                    "text": chunk,
                    "page": page_num
                })
            start = end - overlap
    return chunks

if __name__ == "__main__":
    with open("pages_text.pkl", "rb") as f:
        pages_text = pickle.load(f)
    
    chunks = split_text_with_pages(pages_text)
    
    with open("chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)
    
    print(f"Total chunks created: {len(chunks)}")