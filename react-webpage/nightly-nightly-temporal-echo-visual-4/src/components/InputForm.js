import React, { useState } from 'react';
import '../styles/InputForm.css';

function InputForm({ onLoadEvents, error }) {
  const [jsonInput, setJsonInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onLoadEvents(jsonInput);
  };

  return (
    <form className="input-form" onSubmit={handleSubmit}>
      <label htmlFor="event-json">Paste Event JSON Data:</label>
      <textarea
        id="event-json"
        value={jsonInput}
        onChange={(e) => setJsonInput(e.target.value)}
        placeholder='[
  { "id": "e1", "timestamp": "2024-01-01T10:00:00Z", "type": "SensorRead", "value": 25.5 },
  { "id": "e2", "timestamp": "2024-01-01T10:05:00Z", "type": "SystemAlert", "message": "Temp high" }
]'
        rows="10"
      ></textarea>
      {error && <p className="error-message">{error}</p>}
      <button type="submit">Load Events</button>
    </form>
  );
}

export default InputForm;
