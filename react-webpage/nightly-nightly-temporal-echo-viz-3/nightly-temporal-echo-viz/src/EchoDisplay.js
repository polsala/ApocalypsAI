import React from 'react';
import './App.css'; // For styling

function EchoDisplay({ type, text, level }) {
  const className = `echo-card level-${level}`;
  return (
    <div className={className}>
      <h3>{type}</h3>
      <p>{text}</p>
    </div>
  );
}

export default EchoDisplay;
