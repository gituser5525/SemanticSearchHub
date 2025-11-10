import json
import os
import asyncpg
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer

# load_dotenv()  # Load OPENAI_API_KEY from .env
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DSN = "postgresql://postgres:password@localhost:5432/semantic_db"


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

async def get_embedding(text: str):
    # response = client.embeddings.create(
    #     model="text-embedding-3-small",
    #     input=text,
    # )
    # return response.data[0].embedding
    vec = model.encode(text, normalize_embeddings=True)  # normalize → helps cosine similarity
    return vec.tolist()


async def insert_document(title, content):
    embedding = await get_embedding(content)
    # ✅ Convert embedding list → pgvector string format
    embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"
    metadata = {}
    metadata_json = json.dumps(metadata)
    conn = await asyncpg.connect(DSN)
    await conn.execute("""
        INSERT INTO documents (title, content, source, metadata, embedding)
        VALUES ($1, $2, $3, $4::jsonb, $5::vector)
    """, title, content, "manual", metadata_json, embedding_str)
    await conn.close()
    print("✅ Document inserted.")


# async def search(query, k=3):
#     q_embedding = await get_embedding(query)

#     # ✅ Convert to pgvector format
#     q_embedding_str = "[" + ",".join(str(x) for x in q_embedding) + "]"

#     conn = await asyncpg.connect(DSN)
#     rows = await conn.fetch("""
#         SELECT title, content, embedding <#> $1::vector AS score
#         FROM documents
#         ORDER BY embedding <#> $1::vector
#         LIMIT $2;
#     """, q_embedding_str, k)
#     await conn.close()

#     print("🔍 Search results:")
#     for r in rows:
#         print(f"- {r['title']} (score={round(r['score'], 4)})")
#         print(f"  {r['content'][:120]}...")
#         print()

async def search(query, k=3):
    q_embedding = await get_embedding(query)
    q_embedding_str = "[" + ",".join(str(x) for x in q_embedding) + "]"

    conn = await asyncpg.connect(DSN)
    rows = await conn.fetch("""
        SELECT title, content, metadata, embedding <#> $1::vector AS score
        FROM documents
        ORDER BY embedding <#> $1::vector
        LIMIT $2;
    """, q_embedding_str, k)
    await conn.close()

    # Convert rows to a list of dicts for easier use
    results = []
    for r in rows:
        results.append({
            "title": r["title"],
            "content": r["content"],
            "metadata": r["metadata"],
            "score": float(r["score"]),
        })

    # Still print results to the console for debugging
    print("🔍 Search results:")
    for r in results:
        print(f"- {r['title']} (score={round(r['score'], 4)})")
        print(f"  {r['content'][:120]}...\n")

    return results


