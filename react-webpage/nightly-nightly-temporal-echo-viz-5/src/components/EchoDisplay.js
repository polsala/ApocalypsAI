import React from 'react';

function EchoDisplay({ echoes }) {
  if (!echoes || echoes.length === 0) {
    return <p>No echoes found. Try a different keyword!</p>;
  }

  return (
    <div style={{ marginTop: '20px' }}>
      <h2>Temporal Echoes:</h2>
      <ul style={{ listStyleType: 'none', padding: 0 }}>
        {echoes.map((echo, index) => (
          <li key={index} style={{
            backgroundColor: '#3a3f47',
            margin: '8px 0',
            padding: '10px',
            borderRadius: '5px',
            borderLeft: '3px solid #61dafb'
          }}>
            {echo}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default EchoDisplay;
