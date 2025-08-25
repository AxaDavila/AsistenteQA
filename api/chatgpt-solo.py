# ──────────────────────────────────────────────────────────────
# main.py  –  FastAPI “Senior QA” Assistant (ChatGPT‑solo)
# ──────────────────────────────────────────────────────────────
import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# ------------------------------------------------------------------
# 1️⃣  Cargar variables de entorno (.env)
# ------------------------------------------------------------------
load_dotenv()

USE_LLM = os.getenv("USE_LLM", "chatgpt").lower()
if USE_LLM != "chatgpt":
    raise RuntimeError("El proyecto está configurado exclusivamente para ChatGPT.")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY no encontrado en el entorno.")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # modelo por defecto

# ------------------------------------------------------------------
# 2️⃣  Instanciar la API de OpenAI
# ------------------------------------------------------------------
client = OpenAI(api_key=OPENAI_API_KEY)

# ------------------------------------------------------------------
# 3️⃣  FastAPI y esquemas
# ------------------------------------------------------------------
app = FastAPI(
    title="QA Assistant API – ChatGPT solo",
    version="1.0.0",
    description="Asistente que responde preguntas de QA usando únicamente ChatGPT."
)

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str

class TestWebRequest(BaseModel):
    url: str
    steps: list[str]

class TestWebResponse(BaseModel):
    report: str

# ------------------------------------------------------------------
# 4️⃣  Helpers
# ------------------------------------------------------------------
def generate_answer(question: str) -> str:
    """
    Llama a OpenAI y devuelve el texto generado.
    """
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": question}]
        )
    except Exception as exc:
        # Se propaga al handler de FastAPI que devuelve 500
        raise exc

    # La respuesta de OpenAI es un objeto con la estructura:
    # {"choices":[{"message":{"content":"…"}}], …}
    return response.choices[0].message.content.strip()

def run_web_test(url: str, steps: list[str]) -> str:
    """
    Simulación básica de una prueba de página web.
    Este bloque sirve solo como demo; para pruebas reales se debe usar Playwright/Playwright‑Python.
    """
    report_lines = [f"Testing {url}"]
    for i, step in enumerate(steps, 1):
        report_lines.append(f"  {i}. {step} → [SIMULADO] OK")
    return "\n".join(report_lines)

# ------------------------------------------------------------------
# 5️⃣  Endpoints FastAPI
# ------------------------------------------------------------------
@app.post("/ask", response_model=QuestionResponse)
async def ask(req: QuestionRequest):
    try:
        answer = generate_answer(req.question)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return {"answer": answer}

@app.post("/test-web", response_model=TestWebResponse)
def test_web(req: TestWebRequest):
    report = run_web_test(req.url, req.steps)
    return {"report": report}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "backend": "ChatGPT",
        "model": OPENAI_MODEL
    }

# ------------------------------------------------------------------
# 6️⃣  Si se ejecuta directamente, arrancamos Uvicorn
# ------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if os.getenv("ENVIRONMENT") == "dev" else False
    )
