import json
import asyncpg
import requests
from newspaper import Article
from sentence_transformers import SentenceTransformer

DSN = "postgresql://postgres:password@localhost:5432/semantic_db"
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def get_clean_text(url: str) -> str:
    article = Article(url)
    article.download()
    article.parse()
    return article.text


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


async def insert_chunk(conn, url, chunk, chunk_index):
    vec = model.encode(chunk, normalize_embeddings=True)
    embedding_str = "[" + ",".join(str(x) for x in vec) + "]"
    metadata = {"source": url, "chunk_index": chunk_index}
    metadata_json = json.dumps(metadata)

    await conn.execute("""
        INSERT INTO documents (title, content, source, metadata, embedding)
        VALUES ($1, $2, $3, $4::jsonb, $5::vector)
    """, "webpage", chunk, url, metadata_json, embedding_str)


async def ingest_webpage(url: str):
    text = get_clean_text(url)
    chunks = chunk_text(text)

    conn = await asyncpg.connect(DSN)
    for i, chunk in enumerate(chunks):
        await insert_chunk(conn, url, chunk, i)
    await conn.close()

    print(f"✅ Ingested {len(chunks)} chunks from {url}")
