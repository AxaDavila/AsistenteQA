import { useState } from 'react';
import Chat from '../components/Chat';

export default function Home() {
  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: 20 }}>
      <h1>Asistente Senior QA</h1>
      <p>Hazme cualquier pregunta sobre pruebas de software, DevOps o seguridad web.</p>
      <Chat />
    </div>
  );
}
