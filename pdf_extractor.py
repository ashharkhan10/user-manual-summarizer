import fitz
import pickle
import os

def extract_pages(pdf_path):
    doc = fitz.open(pdf_path)
    pages_text = []
    full_text = ""
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        pages_text.append((page_num + 1, text))
        full_text += text
    
    return pages_text, full_text

if __name__ == "__main__":
    # Find PDF in folder
    pdf_file = None
    for f in os.listdir("."):
        if f.endswith(".pdf"):
            pdf_file = f
            break
    
    if not pdf_file:
        print("No PDF found in folder!")
    else:
        print(f"Reading: {pdf_file}")
        pages_text, full_text = extract_pages(pdf_file)
        
        with open("pages_text.pkl", "wb") as f:
            pickle.dump(pages_text, f)
        
        with open("manual_text.txt", "w", encoding="utf-8") as f:
            f.write(full_text)
        
        print(f"Done! Extracted {len(pages_text)} pages")