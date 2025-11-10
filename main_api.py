from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

from ingest_web import ingest_webpage
from app_test import search
from rag_answer import answer

from ingest_pdf import ingest_pdf
from ingest_text_file import ingest_text_file

app = FastAPI()


class IngestURLRequest(BaseModel):
    url: str


@app.post("/ingest_url")
async def ingest_url(data: IngestURLRequest):
    await ingest_webpage(data.url)
    return {"status": "ok", "message": f"✅ Ingested {data.url}"}


@app.get("/search")
async def search_api(q: str, k: int = 5):
    results = await search(q, k)
    return {"query": q, "results": results}


class AnswerRequest(BaseModel):
    question: str


@app.post("/answer")
async def answer_api(data: AnswerRequest):
    result = await answer(data.question)
    # return {"question": data.question, "answer": result}
    return result

class IngestFileRequest(BaseModel):
    path: str


@app.post("/ingest_file")
async def ingest_file(data: IngestFileRequest):
    if data.path.endswith(".pdf"):
        await ingest_pdf(data.path)
    elif data.path.endswith(".txt"):
        await ingest_text_file(data.path)
    else:
        return {"error": "Unsupported file type"}
    return {"status": "ok", "message": f"✅ Ingested {data.path}"}