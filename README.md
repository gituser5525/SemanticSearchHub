```markdown
# **SemanticSearchHub**

**Local, Private, Offline RAG System with Vector Search + Phi-3**

A production-grade Retrieval-Augmented Generation (RAG) system built from scratch.

---

## 🧱 **Tech Stack**

| Component | Technology |
|----------|------------|
| Vector Database | PostgreSQL + pgvector |
| Embeddings (Offline) | `sentence-transformers/all-MiniLM-L6-v2` |
| Local LLM | Phi-3 (via Ollama) |
| Backend API | FastAPI |
| UI | Streamlit (chat-style) |
| Async DB Access | asyncpg |
| Supported Inputs | PDF, Text files, Web URLs |

This system allows you to ingest documents, perform semantic search, and **chat with your data completely offline** — **no OpenAI / API keys required**.

---

## 🔍 **Features**

- Store and index embeddings using **pgvector**
- **Semantic search** using cosine similarity
- Fully **local embeddings inference** (no external calls)
- **Local LLM answer generation** via Phi-3 (Ollama)
- **RAG pipeline** → Generated answers grounded in retrieved source text
- **Source citations included**
- Clean, chat-style **Streamlit UI**
- **Upload PDF, Text, or Web URLs** directly from interface

---

## 📂 **Project Structure**

```

SemanticSearchHub/
│
├── app_test.py               # Core semantic search + embeddings logic
├── main_api.py               # FastAPI backend
├── ui.py                     # Streamlit chat UI
│
├── ingest_web.py             # Ingest and chunk websites
├── ingest_pdf.py             # Ingest and chunk PDFs
├── ingest_text_file.py       # Ingest and chunk text files
│
├── rag_answer.py             # Retrieve + answer (RAG logic with Phi-3)
├── docker-compose.yml        # PostgreSQL + pgvector setup
│
├── documents/                # Uploaded/processed documents
├── .env                      # Optional environment configuration
└── venv/                     # Python virtual environment

````

---

## 🛠 **Prerequisites**

| Requirement | Version / Notes |
|------------|-----------------|
| Python | 3.10+ recommended |
| Docker | Latest |
| Ollama | Required for running Phi-3 locally |
| PostgreSQL + pgvector | Installed via `docker-compose` |

---

## 🚀 **Setup Instructions**

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd SemanticSearchHub
````

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
```

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start PostgreSQL + pgvector

```bash
docker compose up -d
```

Verify DB is running.

### 5. Install Ollama & Pull Phi-3

Download Ollama → [https://ollama.com/download](https://ollama.com/download)
Then pull the model:

```bash
ollama pull phi3
```

Test:

```bash
ollama run phi3 "Hello!"
```

### 6. Start Backend API (FastAPI)

```bash
uvicorn main_api:app --reload
```

### 7. Launch UI (Streamlit)

```bash
streamlit run ui.py
```

Visit UI:

```
http://localhost:8501
```

---

## 🧠 **Usage**

### Upload Documents

* Go to **Upload Documents** tab
* Upload PDF / TXT / Web URL
* Click **Process & Ingest**

### Chat with Your Knowledge Base

* Go to **Ask a Question** tab
* Ask:

  * `who founded apple?`
  * `explain chapter 3 of my document`

### Answers Include:

* Retrieved context text
* Source / chunk references
* LLM reasoning grounded in retrieved evidence

---

## 📚 **Example Queries**

| Query                              | Expected Response                        |
| ---------------------------------- | ---------------------------------------- |
| `who founded apple?`               | Steve Jobs, Steve Wozniak, Mike Markkula |
| `explain this PDF section`         | Summary grounded in document             |
| `list product categories of apple` | iPhone, Mac, iPad, Watch, etc.           |

---

## 🏗 **Architecture Overview**

```
User
  ↓
Streamlit (UI)
  ↓
FastAPI Backend
  ↓
pgvector Database (Semantic Search)
  ↓
Retrieve Top-K Relevant Chunks
  ↓
Phi-3 (Local LLM)
  ↓
Answer + Sources Returned to UI

```
