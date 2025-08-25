# backend/Dockerfile
FROM python:3.12-slim AS builder

# 1. Instala compiladores y headers requeridos por pydantic‑core y websockets
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Copia el lock y los paquetes que vamos a instalar
WORKDIR /app
COPY requirements.txt .

# 3. Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia el resto de la app
COPY . .

# 5. Expone y arranca el servidor
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
