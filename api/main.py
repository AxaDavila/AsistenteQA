from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv
import httpx
import json

load_dotenv()

app = FastAPI()

# === Configuración del modelo ===
USE_LLM = os.getenv("USE_LLM", "ollama")  # Por defecto usar Ollama
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")  # URL del contenedor Ollama

# Configurar OpenAI solo si es necesario y si existe la API key
if USE_LLM == "chatgpt" and OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
    MODEL = "gpt-4"
elif USE_LLM == "chatgpt" and not OPENAI_API_KEY:
    print("⚠️  OPENAI_API_KEY no encontrada, cambiando a Ollama")
    USE_LLM = "ollama"

# === Schemas ===
class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str

class TestWebRequest(BaseModel):
    url: str
    steps: list[str]

class TestWebResponse(BaseModel):
    report: str

# === Helpers ===
# main.py – fragmento de generate_answer
async def generate_answer(question: str) -> str:
    # -----  ChatGPT primero  -------------------------------------------------
    if USE_LLM == "chatgpt":
        try:
            resp = client.chat.completions.create(
                model="gpt-4",                      # gpt-4, gpt‑4o‑mini, …
                messages=[{"role": "user", "content": question}]
            )
            return resp.choices[0].message.content.strip()
        except Exception as exc:                     # 404, key error, …​
            print("[WARN] Falta acceso a ChatGPT:", exc)
            # ← fallamos: cambiamos la lógica y seguimos a Ollama

    # -----  Ollama  ----------------------------------------------------------
    payload = {
        "model": "gpt-oss:20b",            # por ej. "gpt-oss:20b"
        "prompt": question,
        "stream": False,
        "temperature": 0.7,
        "top_p": 0.9,
    }
    async with httpx.AsyncClient() as c:
        resp = await c.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=60.0)
        resp.raise_for_status()
        return resp.json().get("response",
                                "Error: respuesta vacía de Ollama")

    if USE_LLM == "chatgpt":
        # OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}]
        )
        return response.choices[0].message.content.strip()
    else:
        # Ollama
        try:
            async with httpx.AsyncClient() as client_http:
                response = await client_http.post(
                    f"{OLLAMA_URL}/api/generate",
                    json={
                        "model": "gpt-oss:20b",  # o el modelo que tengas en Ollama
                        "prompt": question,
                        "stream": False
                    },
                    timeout=60.0
                )
                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "Error: respuesta vacía de Ollama")
                else:
                    return f"Error: Ollama respondió con código {response.status_code}"
        except Exception as e:
            return f"Error conectando con Ollama: {str(e)}"

def run_web_test(url: str, steps: list[str]) -> str:
    report_lines = [f"Testing {url}"]
    for i, step in enumerate(steps, 1):
        report_lines.append(f"  {i}. {step} -> [SIMULADO] OK")
    return "\n".join(report_lines)

# === Endpoints ===
@app.post("/ask", response_model=QuestionResponse)
async def ask(req: QuestionRequest):
    try:
        ans = await generate_answer(req.question)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return {"answer": ans}

@app.post("/test-web", response_model=TestWebResponse)
def test_web(req: TestWebRequest):
    report = run_web_test(req.url, req.steps)
    return {"report": report}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "llm_provider": USE_LLM,
        "ollama_url": OLLAMA_URL if USE_LLM == "ollama" else None
    }