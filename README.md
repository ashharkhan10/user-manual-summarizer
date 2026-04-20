# 🚗 Automobile User Manual Summarizer

---

## 🖼️ Project Banner

[Screenshot]<img width="1915" height="877" alt="app_preview" src="https://github.com/user-attachments/assets/440c04d4-7ad2-404b-89ea-ab4a7a032bb4" />


---

## 🏷️ Badges

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-green)
![FAISS](https://img.shields.io/badge/FAISS-Vector_DB-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 📝 Short Description

> An AI powered web application that lets you upload 
> any automobile user manual PDF and instantly ask 
> questions about it in plain English. Get accurate 
> answers with page citations in multiple languages 
> without reading a single page of the manual!

---

## 📚 Table of Contents

- [About The Project](#about-the-project)
- [Features](#features)
- [Demo](#demo)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Known Issues](#known-issues)
- [Future Roadmap](#future-roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

---

## 💡 About The Project

Automobile user manuals are typically 200 to 500 pages 
long and contain highly technical information. Vehicle 
owners and service technicians often struggle to find 
specific information quickly. 

Imagine you just bought a new car and the check engine 
light comes on. Do you really want to search through 
400 pages to find what it means? 

**That is exactly the problem this project solves.**

This application uses a technique called 
**Retrieval Augmented Generation (RAG)** which works 
like having a super intelligent assistant who has read 
your entire car manual and can answer any question 
about it instantly.

### Why This Project?

```
❌ Without this project:
   → Open 400 page PDF
   → Press Ctrl+F and search
   → Read multiple pages
   → Still not sure of answer
   → Takes 10-15 minutes

✅ With this project:
   → Upload PDF once
   → Type your question
   → Get accurate answer in seconds
   → See exact page number
   → Done in 10 seconds
```

### Who Is This For?

| User | Use Case |
|---|---|
| Vehicle Owner | Quick answers about their car |
| Service Technician | Technical specs and procedures |
| Fleet Manager | Managing multiple vehicle manuals |
| Students | Learning about automobile systems |
---

## How It Works

The system uses a technique called **Retrieval Augmented 
Generation (RAG)**. Think of it like a super smart 
librarian who has read your entire car manual and can 
find any information instantly.

### Simple Explanation

```
Normal AI:
Question → AI guesses answer from training data
Problem  → AI might make up wrong information

This Project (RAG):
Question → Search manual → Find exact text → 
AI explains it → Accurate answer every time
```

### Two Main Processes

**Process 1 — When You Upload a Manual**
```
You upload PDF
      ↓
System reads every page
      ↓
Text split into small pieces (chunks)
      ↓
Each chunk converted to numbers (vectors)
      ↓
Numbers saved in search database (FAISS)
      ↓
Manual is ready to answer questions!
```

**Process 2 — When You Ask a Question**
```
You type a question
      ↓
Question converted to numbers
      ↓
System searches database for similar numbers
      ↓
Top 3 most relevant chunks found
      ↓
Chunks sent to Groq AI with your question
      ↓
AI generates answer using only those chunks
      ↓
Answer shown with page numbers
```

---

## System Architecture

```
┌──────────────────────────────────────────────┐
│           USER INTERFACE LAYER               │
│         Streamlit Web Application            │
│           localhost:8501                     │
└─────────────────┬────────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────────┐
│          APPLICATION LAYER                   │
│                                              │
│  ┌─────────────────┐  ┌──────────────────┐   │
│  │    INGESTION    │  │     QUERYING     │   │
│  │                 │  │                  │   │
│  │  Upload PDF     │  │  User Question   │   │
│  │  Extract Text   │  │  Embed Question  │   │
│  │  Split Chunks   │  │  Search FAISS    │   │
│  │  Embed Chunks   │  │  Get Chunks      │   │
│  │  Store FAISS    │  │  Send to LLM     │   │
│  └─────────────────┘  │  Return Answer   │   │
│                       └──────────────────┘   │
└─────────────────┬────────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────────┐
│              AI/ML LAYER                     │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │  Sentence Transformer                  │  │
│  │  BAAI/bge-small-en-v1.5               │  │
│  │  Converts text to 384 dim vectors     │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │  FAISS Vector Database                 │  │
│  │  Stores and searches document vectors  │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │  Groq API — LLaMA 3.3 70B              │  │
│  │  Generates answers in any language     │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

---

## Project Structure

```
Auto-manual-summarizer/
│
├── 📄 app.py
│       Main web application
│       Contains all features and UI
│       Upload, chat, compare, summarize
│
├── 📄 step1.py
│       Reads PDF file
│       Extracts text page by page
│       Saves to manual_text.txt
│
├── 📄 step2.py
│       Splits text into 500 char chunks
│       Saves page number with each chunk
│       Saves chunks to chunks.pkl
│
├── 📄 step3.py
│       Loads embedding model
│       Converts chunks to vectors
│       Saves to vectorstore.faiss
│
├── 📄 step4.py
│       Tests question answering
│       Used during development
│       Run to verify everything works
│
├── 📄 requirements.txt
│       All Python libraries needed
│       Run pip install -r requirements.txt
│
├── 📄 README.md
│       Project documentation
│       This file you are reading
│
├── 📄 .env
│       Contains API keys
│       NOT uploaded to GitHub
│       Must create manually
│
├── 📄 .gitignore
│       Lists files hidden from GitHub
│       Protects sensitive information
│
├── 📦 chunks.pkl
│       Processed text chunks
│       Generated automatically
│       NOT uploaded to GitHub
│
├── 📦 vectorstore.faiss
│       Vector search database
│       Generated automatically
│       NOT uploaded to GitHub
│
└── 📦 manual_text.txt
        Extracted PDF text
        Generated automatically
        NOT uploaded to GitHub
```

---

## Prerequisites

Before running this project make sure you have:

### 1. Python 3.10 or Higher
Check your Python version:
```
python --version
```
If not installed download from:
```
https://python.org
```

### 2. Git
Check if Git is installed:
```
git --version
```
If not installed download from:
```
https://git-scm.com
```

### 3. Free Groq API Key
This project uses Groq AI which is completely free.

Get your free key here:
```
https://console.groq.com
```

Steps:
- Sign up for free account
- Click API Keys on left side
- Click Create API Key
- Copy the key starting with gsk_

### 4. A Car Manual PDF
Download free automobile manuals from:
```
https://www.manualslib.com
```

### 5. VS Code (Recommended)
Best code editor for this project:
```
https://code.visualstudio.com
```

### Minimum System Requirements
| Component | Minimum | Recommended |
|---|---|---|
| RAM | 4GB | 8GB |
| Storage | 2GB free | 5GB free |
| Internet | Required | Required |
| OS | Windows 10 | Windows 11 |

---

## Installation

### Step 1 — Clone The Repository
Open terminal and type:
```
git clone https://github.com/ashharkhan10/user-manual-summarizer.git
```
Then go into the folder:
```
cd user-manual-summarizer
```

### Step 2 — Install All Libraries
```
pip install -r requirements.txt
```
This will take 3 to 5 minutes. Just wait for it to finish.

### Step 3 — Create Environment File
Create a file called `.env` in the project folder:
```
notepad .env
```
Add your Groq API key inside:
```
GROQ_API_KEY=your-groq-api-key-here
```
Save and close.

### Step 4 — Verify Installation
Check everything installed correctly:
```
python -c "import streamlit; import faiss; import fitz; print('All good!')"
```
You should see:
```
All good!
```

### Step 5 — Run The App
```
streamlit run app.py
```

### Step 6 — Open Browser
App will open automatically or go to:
```
http://localhost:8501
```

### Common Installation Errors

**Error: pip not found**
```
Solution: Use python -m pip install -r requirements.txt
```

**Error: No module named faiss**
```
Solution: pip install faiss-cpu
```

**Error: No module named fitz**
```
Solution: pip install pymupdf
```
---

## Usage

### Basic Usage — Ask a Question

**Step 1 — Open the app**
```
streamlit run app.py
```

**Step 2 — Upload your manual**
- Look at the left sidebar
- Click **Browse Files** button
- Select your car manual PDF
- Give it a name like `Toyota Camry`
- Click **Process Manual** button
- Wait for processing to finish

**Step 3 — Ask a question**
- Type your question in the chat box
- Press Enter
- Answer appears with page numbers

### Example Questions You Can Ask
```
✅ What type of engine oil should I use?
✅ What is the recommended tire pressure?
✅ How do I reset the maintenance light?
✅ What does the check engine light mean?
✅ How do I use the smart key system?
✅ What are the hybrid system features?
✅ How often should I change the oil?
✅ What is the fuel tank capacity?
```

---

### Advanced Usage — Multiple Manuals

**Step 1 — Upload first manual**
- Upload Toyota Camry manual
- Name it `Toyota Camry`
- Click Process Manual

**Step 2 — Upload second manual**
- Upload Honda Civic manual
- Name it `Honda Civic`
- Click Process Manual

**Step 3 — Switch between manuals**
- Use the dropdown in sidebar
- Select which manual to search
- Ask questions from each manual

---

### Advanced Usage — Compare Two Manuals

**Step 1 — Make sure two manuals are uploaded**

**Step 2 — Turn on compare mode**
- Find the toggle at top of page
- Turn on **Compare Two Manuals Mode**

**Step 3 — Select both manuals**
- Select first manual from left dropdown
- Select second manual from right dropdown

**Step 4 — Ask comparison question**
- Type your question
- Click **Compare Now**
- See both answers side by side
- AI summary of differences shown below

---

### Advanced Usage — Summarize a Topic

**Step 1 — Upload your manual**

**Step 2 — Find Summarize Topic in sidebar**
- Type any topic like `engine oil`
- Click **Summarize** button
- Get bullet point summary instantly

---

### Advanced Usage — Multiple Languages

**Step 1 — Find language dropdown at top**

**Step 2 — Select your language**
```
Available languages:
→ English
→ Hindi
→ Urdu
→ Arabic
→ French
→ Spanish
→ German
```

**Step 3 — Ask any question**
- Answer will come in selected language
- Page numbers still shown correctly

---

## API Reference

This project uses the following external APIs:

### Groq API
```
Provider  : Groq
Model     : llama-3.3-70b-versatile
Purpose   : Generating answers and summaries
Cost      : Free tier available
Rate Limit: 30 requests per minute on free tier
Docs      : https://console.groq.com/docs
```

How it is called in code:
```python
from groq import Groq

client = Groq(api_key="your-key-here")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": "You are a car manual assistant."
        },
        {
            "role": "user",
            "content": "Your question here"
        }
    ],
    max_tokens=300
)

answer = response.choices[0].message.content
```

---

### Hugging Face Model
```
Provider  : Hugging Face
Model     : BAAI/bge-small-en-v1.5
Purpose   : Converting text to vectors
Cost      : Completely free
Size      : 130MB downloaded automatically
Docs      : https://huggingface.co/BAAI/bge-small-en-v1.5
```

How it is called in code:
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

embeddings = model.encode(
    chunks,
    normalize_embeddings=True
)
```

---

### FAISS
```
Provider  : Facebook AI Research
Purpose   : Vector similarity search
Cost      : Completely free and open source
Type      : IndexFlatIP with normalized vectors
Docs      : https://faiss.ai
```

How it is called in code:
```python
import faiss

dimension = 384
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

scores, indices = index.search(query, k=3)
```

---

## Known Issues

| Issue | Status | Workaround |
|---|---|---|
| Scanned PDFs not supported | Open | Use text searchable PDFs only |
| Manuals lost on browser refresh | Open | Re-upload after refreshing |
| Groq rate limit on free tier | Open | Wait 1 minute and try again |
| Very large PDFs take long to process | Open | Wait for processing to complete |
| Non English manuals less accurate | Open | Use English manuals for best results |
| Answer quality varies by manual | Open | Try rephrasing your question |

### How To Report a New Issue
1. Go to GitHub repository
2. Click **Issues** tab
3. Click **New Issue**
4. Describe the problem clearly
5. Add screenshot if possible

---

## Future Roadmap

### Version 2.0 — Coming Soon
```
🎤 Voice Input
   Speak your question instead of typing
   Uses Web Speech API

📱 Mobile Responsive Design  
   Works perfectly on phones and tablets
   Touch friendly interface

🔍 OCR Support
   Process scanned PDF manuals
   Uses Tesseract OCR engine

📤 Export Chat History
   Download your questions and answers
   Export as PDF or Word document
```

### Version 3.0 — Planned
```
📧 Maintenance Reminder Emails
   Set reminders for oil changes
   Get email alerts automatically

📊 Maintenance Schedule Tracker
   Visual calendar of service intervals
   Track what has been done

⚠️ Warning Light Identifier
   Upload photo of dashboard
   AI identifies warning lights

🌐 Multi Language Manuals
   Process manuals in any language
   Better multilingual embeddings
```

### Version 4.0 — Future Vision
```
📱 Mobile App
   Native Android and iOS app
   Works offline

🔗 OBD Integration
   Connect to car diagnostic port
   Real time fault code reading

📍 Service Center Locator
   Find nearest service center
   Book appointments directly

🤝 Community Features
   Share questions and answers
   Build knowledge base together
```
