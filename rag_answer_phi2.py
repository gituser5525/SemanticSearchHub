# import subprocess
# import asyncio
# from app_test import search

# LLAMA_PATH = r"C:\llama\llama-cli.exe"
# MODEL_PATH = r"C:\llama\models\phi-2.Q4_K_M.gguf"


# async def answer(query):
#     # 1) Get relevant chunks from DB
#     rows = await search(query, k=4)

#     context = "\n\n".join([r['content'] for r in rows])

#     # 2) Construct prompt
#     prompt = f"""
# You are a helpful AI assistant. Use ONLY the context below to answer.

# Context:
# {context}

# Question: {query}

# If the answer is not in the context, say "I don't know."
# Answer:
# """.strip()

#     # 3) Call local LLM using llama.cpp
#     process = subprocess.Popen(
#         [LLAMA_PATH, "-m", MODEL_PATH, "-p", prompt, "-n", "200"],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT,
#         text=True,
#     )

#     output = []
#     for line in process.stdout:
#         output.append(line)

#     return "".join(output)