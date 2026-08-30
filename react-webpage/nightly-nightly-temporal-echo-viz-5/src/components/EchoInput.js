import React, { useState } from 'react';

function EchoInput({ onSearch }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(input);
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter a keyword (e.g., apocalypse, future, hope)"
        style={{
          padding: '10px',
          marginRight: '10px',
          borderRadius: '5px',
          border: '1px solid #61dafb',
          backgroundColor: '#333',
          color: '#f0f0f0',
          width: '300px'
        }}
      />
      <button
        type="submit"
        style={{
          padding: '10px 15px',
          borderRadius: '5px',
          border: 'none',
          backgroundColor: '#61dafb',
          color: '#282c34',
          cursor: 'pointer'
        }}
      >
        Find Echoes
      </button>
    </form>
  );
}

export default EchoInput;
