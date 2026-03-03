import React from 'react';
import './App.css'; // Re-using App.css for echo-item styles

const EchoVisualizer = ({ echoes }) => {
  if (!echoes || echoes.length === 0) {
    return null;
  }

  return (
    <div className="echo-container">
      {echoes.map((echo, index) => (
        <div
          key={index}
          className="echo-item"
          style={{ animationDelay: `${index * 0.1}s` }} // Staggered animation
        >
          {echo}
        </div>
      ))}
    </div>
  );
};

export default EchoVisualizer;
