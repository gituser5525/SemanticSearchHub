import fitz  # PyMuPDF
import json
import asyncpg
from sentence_transformers import SentenceTransformer

DSN = "postgresql://postgres:password@localhost:5432/semantic_db"
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
        text += "\n\n"
    return text


def chunk_text(text, chunk_size=400, overlap=60):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap
    return chunks


async def insert_chunk(conn, source, chunk, index):
    vec = model.encode(chunk, normalize_embeddings=True)
    emb = "[" + ",".join(str(x) for x in vec) + "]"

    metadata = json.dumps({"source": source, "chunk_index": index})

    await conn.execute("""
        INSERT INTO documents (title, content, source, metadata, embedding)
        VALUES ($1, $2, $3, $4::jsonb, $5::vector)
    """, source, chunk, source, metadata, emb)


async def ingest_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)

    conn = await asyncpg.connect(DSN)
    for i, chunk in enumerate(chunks):
        await insert_chunk(conn, pdf_path, chunk, i)
    await conn.close()

    print(f"✅ Ingested {len(chunks)} chunks from {pdf_path}")
