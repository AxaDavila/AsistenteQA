# QA Assistant – Asistente virtual de pruebas de software

Un **FastAPI** con especificación OpenAPI que actúa como un asistente de QA, capaz de:
- Responder preguntas sobre pruebas, DevOps y seguridad con ChatGPT o Llama‑OSS 20B.
- Simular pruebas de páginas web con pasos definidos.

## Instalación

```bash
git clone https://github.com/tu_usuario/qa-assistant.git
cd qa-assistant
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

1️⃣ Descarga el modelo correcto con token de Ollama

Crea una cuenta HuggingFace → Settings → Access Tokens → New Token → scope read. Copia el token (ej. hf_XYZ...).
Descarga el fichero de forma autenticada:
Opción A – curl
export HF_TOKEN="hf_XYZ..."          # ← el token que acabas de crear

curl -H "Authorization: Bearer $HF_TOKEN" \
     -L -o ./ollama/models/llama2.3b.bin \
     https://huggingface.co/TheBloke/Llama-2-3b/resolve/main/Llama-2-3b.ggmlv3.q5_0.bin

Opción B – huggingface-cli
pip install -U huggingface-hub
huggingface-cli download TheBloke/Llama-2-3b \
     --local-dir ./ollama/models --force
# el archivo se colocará con el

##  Próximos pasos (road‑map)

|       Tarea           |         Descripción                    |  |
|-----------------------|----------------------------------------------------------------| |
| Integrar Playwright   | Reemplazar la simulación de `run_web_test` con pruebas reales. | |
| Caching de respuestas | Usar Redis para almacenar respuestas frecuentes.               | |
| Seguridad             | Añadir autenticación JWT, límites de tasa.                     | |
| CI/CD                 | GitHub Actions que prueben y desplieguen a Heroku o Azure.     | |
| UI front‑end          | React/Next.js que consuma la API y muestre un chat.            | |

---
