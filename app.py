import streamlit as st
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from groq import Groq
import fitz
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Car Manual Assistant",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Car Manual Assistant")
st.write("Upload your car manual and ask any question!")

@st.cache_resource
def load_model():
    return SentenceTransformer("BAAI/bge-small-en-v1.5")

model = load_model()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def process_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    chunks = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        start = 0
        while start < len(text):
            end = start + 500
            chunk = text[start:end]
            if len(chunk.strip()) > 30:
                chunks.append({
                    "text": chunk,
                    "page": page_num + 1
                })
            start = end - 50
    return chunks

def build_index(chunks):
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False
    )
    embeddings = np.array(embeddings).astype("float32")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    return index

def ask_question(question, index, chunks):
    try:
        query = model.encode(
            [question],
            normalize_embeddings=True
        )
        query = np.array(query).astype("float32")
        scores, indices = index.search(query, k=3)
        
        relevant_chunks = [chunks[i] for i in indices[0]]
        context = "\n\n".join([c["text"] for c in relevant_chunks])
        context = context[:1500]
        
        # Get page numbers
        pages = list(set([c["page"] for c in relevant_chunks]))
        pages.sort()
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Answer questions using only the car manual text. Be clear and simple."
                },
                {
                    "role": "user",
                    "content": f"Manual text:\n{context}\n\nQuestion: {question}"
                }
            ],
            max_tokens=300
        )
        
        answer = response.choices[0].message.content
        return answer, pages
        
    except Exception as e:
        return f"Error: {str(e)}", []

# ─── SIDEBAR ───────────────────────────────────────────
with st.sidebar:
    st.header("📄 Upload Manual")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="Upload your car manual PDF"
    )
    
    if uploaded_file is not None:
        if st.button("🔄 Process Manual", type="primary"):
            with st.spinner("Processing your manual... please wait..."):
                
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Process the PDF
                chunks = process_pdf(tmp_path)
                index = build_index(chunks)
                
                # Save to session
                st.session_state.chunks = chunks
                st.session_state.index = index
                st.session_state.manual_name = uploaded_file.name
                st.session_state.chat = []
                
                # Cleanup temp file
                os.unlink(tmp_path)
                
                st.success(
                    f"Done! Processed {len(chunks)} sections"
                )
    
    # Show current manual
    if "manual_name" in st.session_state:
        st.divider()
        st.success(f"📖 Active: {st.session_state.manual_name}")
    
    # Clear chat button
    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat = []
        st.rerun()

# ─── MAIN CHAT AREA ────────────────────────────────────
if "index" not in st.session_state:
    st.info(
        "👈 Please upload a car manual PDF from the sidebar to get started!"
    )
else:
    if "chat" not in st.session_state:
        st.session_state.chat = []
    
    # Show chat history
    for message in st.session_state.chat:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message.get("pages"):
                pages_str = ", ".join(
                    [str(p) for p in message["pages"]]
                )
                st.caption(f"📍 Found on page(s): {pages_str}")
    
    # Question input
    question = st.chat_input(
        "Ask anything about your car manual..."
    )
    
    if question:
        # Show user question
        with st.chat_message("user"):
            st.write(question)
        
        # Get and show answer
        with st.chat_message("assistant"):
            with st.spinner("Searching manual..."):
                answer, pages = ask_question(
                    question,
                    st.session_state.index,
                    st.session_state.chunks
                )
            st.write(answer)
            if pages:
                pages_str = ", ".join([str(p) for p in pages])
                st.caption(f"📍 Found on page(s): {pages_str}")
        
        # Save to history
        st.session_state.chat.append({
            "role": "user",
            "content": question
        })
        st.session_state.chat.append({
            "role": "assistant",
            "content": answer,
            "pages": pages
        })