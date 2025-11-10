import requests
from app_test import search


def call_llm(prompt: str):
    resp = requests.post("http://localhost:11434/api/generate", json={
        "model": "phi3",
        "prompt": prompt,
        "stream": False
    })
    return resp.json()["response"]


async def answer(query):
    rows = await search(query, k=4)

    # Build a combined context **with chunk IDs**
    context_parts = []
    for i, row in enumerate(rows):
        context_parts.append(f"[CHUNK {i}] {row['content']}")
    context = "\n\n".join(context_parts)

    prompt = f"""
You are a helpful and factual assistant.
Use only the information inside <context>.
If the answer is not in the context, reply exactly: "I don't know."

<context>
{context}
</context>

Question: {query}

Answer:
"""

    answer_text = call_llm(prompt)

    # Return both answer and which chunks were used
    sources = [f"CHUNK {i}" for i in range(len(rows))]
    return {"answer": answer_text.strip(), "sources": sources, "chunks": rows}
