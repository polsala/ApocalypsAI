import React from 'react';

function GlitchItem({ glitch }) {
  return (
    <div className="glitch-item">
      <h3>{glitch.type}</h3>
      <p>{glitch.description}</p>
      <p className="timestamp">Reported: {glitch.timestamp}</p>
    </div>
  );
}

export default GlitchItem;
