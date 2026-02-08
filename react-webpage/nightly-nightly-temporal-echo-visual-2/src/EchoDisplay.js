import React from 'react';
import './App.css'; // Using App.css for general styles and animations

function EchoDisplay({ text, style, delay }) {
  return (
    <div
      className="echo-item"
      style={{
        ...style,
        animationDelay: `${delay}s`,
      }}
    >
      {text}
    </div>
  );
}

export default EchoDisplay;
