// frontend/pages/api/chat.js
// --------------------------
// Proxy simple que re‑envía /api/chat/... a /ask del backend
// (para Next.js 13+ con soporte de app router).

import { use } from 'next';
 // NO importa tipos aquí, ya que es un fichero .js

export default async function handler(req, res) {
  // 1️⃣  Dirección base del FastAPI
  const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://backend:8000';

  // 2️⃣  Conviértelo a la ruta real del backend
  const targetPath = req.url.replace(/^\/api\/chat/, '');

  // 3️⃣  Construye la petición al backend
  const fetchOptions = {
    method: req.method,
    // Elimina “host” para que el backend no lo confunda
    headers: { ...req.headers, host: undefined },
    body: !['GET', 'HEAD'].includes(req.method)
      ? JSON.stringify(req.body)
      : undefined,
  };

  try {
    const resp = await fetch(`${apiBase}${targetPath}`, fetchOptions);

    const contentType = resp.headers.get('content-type') || '';
    const payload = contentType.includes('application/json')
      ? await resp.json()
      : await resp.text();

    res.status(resp.status).json(payload);
  } catch (err) {
    res.status(500).json({
      error: 'Error proxy',
      details: err.message, // opcional, útil en debug
    });
  }
}
