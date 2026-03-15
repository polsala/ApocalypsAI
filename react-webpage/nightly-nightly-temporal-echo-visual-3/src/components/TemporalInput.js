import React, { useState } from 'react';
import './TemporalInput.css';

function TemporalInput({ onCoordinateSubmit }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onCoordinateSubmit(input);
  };

  return (
    <form className="temporal-input-form" onSubmit={handleSubmit}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter a temporal coordinate (e.g., '2024-07-20', 'ancient ruins')"
        aria-label="Temporal Coordinate Input"
      />
      <button type="submit">Visualize Echoes</button>
    </form>
  );
}

export default TemporalInput;
