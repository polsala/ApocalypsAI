import React from 'react';
import './App.css'; // Using App.css for general styling

function FactionEcho({ factionName, originalMessage, echoMessage }) {
  return (
    <div className="faction-echo-card">
      <h3>{factionName}</h3>
      <p><strong>Original:</strong> {originalMessage}</p>
      <p><strong>Echo:</strong> <em>"{echoMessage}"</em></p>
    </div>
  );
}

export default FactionEcho;
