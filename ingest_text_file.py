import json
import asyncpg
from sentence_transformers import SentenceTransformer

DSN = "postgresql://postgres:password@localhost:5432/semantic_db"
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


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


async def ingest_text_file(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_text(text)

    conn = await asyncpg.connect(DSN)
    for i, chunk in enumerate(chunks):
        vec = model.encode(chunk, normalize_embeddings=True)
        emb = "[" + ",".join(str(x) for x in vec) + "]"
        meta = json.dumps({"source": path, "chunk_index": i})
        await conn.execute("""
            INSERT INTO documents (title, content, source, metadata, embedding)
            VALUES ($1, $2, $3, $4::jsonb, $5::vector)
        """, path, chunk, path, meta, emb)
    await conn.close()

    print(f"✅ Ingested {len(chunks)} chunks from {path}")
