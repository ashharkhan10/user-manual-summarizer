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
from datetime import datetime

load_dotenv()

st.set_page_config(
    page_title="Car Manual Assistant",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Car Manual Assistant")

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

def summarize_topic(topic, index, chunks):
    try:
        query = model.encode(
            [topic],
            normalize_embeddings=True
        )
        query = np.array(query).astype("float32")
        scores, indices = index.search(query, k=5)
        relevant_chunks = [chunks[i] for i in indices[0]]
        context = "\n\n".join([c["text"] for c in relevant_chunks])
        context = context[:2000]
        pages = list(set([c["page"] for c in relevant_chunks]))
        pages.sort()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """You are a car manual expert. 
                    Summarize the given manual text in a clear 
                    structured way using bullet points."""
                },
                {
                    "role": "user",
                    "content": f"""Summarize this topic from 
                    the car manual: {topic}
                    
                    Manual text:
                    {context}
                    
                    Provide a clear summary with bullet points."""
                }
            ],
            max_tokens=500
        )
        summary = response.choices[0].message.content
        return summary, pages
    except Exception as e:
        return f"Error: {str(e)}", []

# Initialize session state
if "manuals" not in st.session_state:
    st.session_state.manuals = {}
if "chat" not in st.session_state:
    st.session_state.chat = []
if "history" not in st.session_state:
    st.session_state.history = []
if "selected_manual" not in st.session_state:
    st.session_state.selected_manual = None

# ─── SIDEBAR ────────────────────────────────────────────
with st.sidebar:
    st.header("📄 Upload Manual")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="Upload your car manual PDF"
    )

    if uploaded_file is not None:
        manual_name = st.text_input(
            "Give this manual a name",
            value=uploaded_file.name.replace(".pdf", ""),
            help="Example: Toyota Camry 2023"
        )

        if st.button("🔄 Process Manual", type="primary"):
            with st.spinner("Processing manual... please wait..."):
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name

                chunks = process_pdf(tmp_path)
                index = build_index(chunks)
                os.unlink(tmp_path)

                st.session_state.manuals[manual_name] = {
                    "chunks": chunks,
                    "index": index,
                    "uploaded_at": datetime.now().strftime(
                        "%d-%m-%Y %H:%M"
                    )
                }
                st.session_state.selected_manual = manual_name
                st.session_state.chat = []
                st.success(f"Done! {len(chunks)} sections processed")

    # Dropdown to select manual
    if st.session_state.manuals:
        st.divider()
        st.header("📚 Select Manual")
        manual_names = list(st.session_state.manuals.keys())
        selected = st.selectbox(
            "Choose which manual to search",
            manual_names,
            index=manual_names.index(
                st.session_state.selected_manual
            ) if st.session_state.selected_manual in manual_names else 0
        )

        if selected != st.session_state.selected_manual:
            st.session_state.selected_manual = selected
            st.session_state.chat = []
            st.rerun()

        # Show all uploaded manuals
        st.divider()
        st.header("📖 Uploaded Manuals")
        for name, data in st.session_state.manuals.items():
            if name == st.session_state.selected_manual:
                st.success(f"▶ {name}")
            else:
                st.info(f"  {name}")
            st.caption(f"Uploaded: {data['uploaded_at']}")

    st.divider()

    # Summarize section
    st.header("📋 Summarize Topic")
    topic_input = st.text_input(
        "Enter topic to summarize",
        placeholder="Example: engine oil, brakes, tyres"
    )

    if st.button("✨ Summarize", use_container_width=True):
        if not st.session_state.manuals:
            st.warning("Please upload a manual first!")
        elif not topic_input:
            st.warning("Please enter a topic!")
        else:
            with st.spinner("Summarizing..."):
                manual = st.session_state.manuals[
                    st.session_state.selected_manual
                ]
                summary, pages = summarize_topic(
                    topic_input,
                    manual["index"],
                    manual["chunks"]
                )
                st.session_state.chat.append({
                    "role": "assistant",
                    "content": f"📋 **Summary of '{topic_input}':**\n\n{summary}",
                    "pages": pages,
                    "type": "summary"
                })
                st.rerun()

    st.divider()

    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat = []
        st.rerun()

# ─── MAIN AREA ───────────────────────────────────────────
if not st.session_state.manuals:
    st.info(
        "👈 Upload a car manual PDF from the sidebar to get started!"
    )
else:
    # Two columns — chat and history
    col1, col2 = st.columns([2, 1])

    # Chat column
    with col1:
        st.subheader(
            f"💬 Chat — {st.session_state.selected_manual}"
        )

        # Show chat messages
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
            manual = st.session_state.manuals[
                st.session_state.selected_manual
            ]

            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):
                with st.spinner("Searching manual..."):
                    answer, pages = ask_question(
                        question,
                        manual["index"],
                        manual["chunks"]
                    )
                st.write(answer)
                if pages:
                    pages_str = ", ".join([str(p) for p in pages])
                    st.caption(f"📍 Found on page(s): {pages_str}")

            # Save to chat
            st.session_state.chat.append({
                "role": "user",
                "content": question
            })
            st.session_state.chat.append({
                "role": "assistant",
                "content": answer,
                "pages": pages
            })

            # Save to history
            st.session_state.history.append({
                "question": question,
                "answer": answer,
                "pages": pages,
                "manual": st.session_state.selected_manual,
                "time": datetime.now().strftime("%H:%M")
            })

    # History column
    with col2:
        st.subheader("🕐 Search History")

        if not st.session_state.history:
            st.info("Your search history will appear here!")
        else:
            # Clear history button
            if st.button("🗑️ Clear History"):
                st.session_state.history = []
                st.rerun()

            # Show history newest first
            for item in reversed(st.session_state.history):
                with st.expander(
                    f"🕐 {item['time']} — {item['question'][:40]}..."
                ):
                    st.caption(f"📖 Manual: {item['manual']}")
                    st.write(f"**Q:** {item['question']}")
                    st.write(f"**A:** {item['answer']}")
                    if item['pages']:
                        pages_str = ", ".join(
                            [str(p) for p in item['pages']]
                        )
                        st.caption(f"📍 Pages: {pages_str}")