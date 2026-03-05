import React from 'react';

const AlignmentDisplay = ({ influences }) => {
  return (
    <div style={{
      marginTop: '30px',
      padding: '20px',
      backgroundColor: '#2e2e4a',
      borderRadius: '8px',
      boxShadow: '0 4px 10px rgba(0, 0, 0, 0.3)',
      maxHeight: '200px',
      overflowY: 'auto'
    }}>
      <h3 style={{ color: '#FFD700', marginBottom: '15px' }}>Cosmic Influences Today:</h3>
      {
        influences.length > 0 ? (
          <ul>
            {influences.map((influence, index) => (
              <li key={index} style={{ marginBottom: '8px', lineHeight: '1.4' }}>
                <span role="img" aria-label="star">✨</span> {influence}
              </li>
            ))}
          </ul>
        ) : (
          <p>No significant alignments detected. A calm day awaits.</p>
        )
      }
    </div>
  );
};

export default AlignmentDisplay;
