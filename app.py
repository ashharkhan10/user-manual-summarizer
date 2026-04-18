from dotenv import load_dotenv
import os
load_dotenv()

import streamlit as st
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from groq import Groq

st.set_page_config(page_title="Car Manual Assistant", page_icon="🚗")
st.title("🚗 Ask Your Car Manual")
st.write("Ask any question about your Toyota Camry!")

@st.cache_resource
def load_everything():
    st.write("Loading... please wait...")
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    index = faiss.read_index("vectorstore.faiss")
    with open("chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    return model, index, chunks

model, index, chunks = load_everything()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_question(question):
    query = model.encode([question], normalize_embeddings=True)
    query = np.array(query).astype("float32")
    scores, indices = index.search(query, k=3)
    relevant_pieces = [chunks[i] for i in indices[0]]
    context = "\n\n".join(relevant_pieces)
    context = context[:2000]
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Answer questions using only the car manual text provided."
            },
            {
                "role": "user",
                "content": f"Car manual text:\n{context}\n\nQuestion: {question}"
            }
        ]
    )
    return response.choices[0].message.content

if "chat" not in st.session_state:
    st.session_state.chat = []

for message in st.session_state.chat:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Type your question here...")

if question:
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        with st.spinner("Searching manual..."):
            answer = ask_question(question)
        st.write(answer)
    st.session_state.chat.append({"role": "user", "content": question})
    st.session_state.chat.append({"role": "assistant", "content": answer})