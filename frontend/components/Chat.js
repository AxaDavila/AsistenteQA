import { useState } from 'react';
import axios from 'axios';

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    if (!input.trim()) return;
    const newMsg = { role: 'user', text: input };
    setMessages((prev) => [...prev, newMsg]);

    try {
      // const { data } = await axios.post(
      //   '/api/chat',
      //   { question: input },
      //   { headers: { 'Content-Type': 'application/json' } }
      // );
      const { data } = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/ask`,   // 👉   ¡directo al backend!
        { question },
        { headers: { 'Content-Type': 'application/json' } }
      );
      setMessages((prev) => [...prev, { role: 'assistant', text: data.answer }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', text: 'Error interno: ' + err.message },
      ]);
    }
    setInput('');
  };

  return (
    <div>
      <div
        style={{
          border: '1px solid #444',
          borderRadius: 8,
          padding: 10,
          minHeight: 300,
          overflowY: 'auto',
          marginBottom: 10,
        }}
      >
        {messages.map((msg, i) => (
          <div key={i} style={{ marginBottom: 8 }}>
            <strong>{msg.role === 'user' ? 'Tú' : 'Asistente'}:</strong>{' '}
            {msg.text}
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', gap: 8 }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Escribe tu pregunta..."
          style={{ flex: 1, padding: 8 }}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
        />
        <button onClick={sendMessage} style={{ padding: '8px 12px' }}>
          Enviar
        </button>
      </div>
    </div>
  );
}
