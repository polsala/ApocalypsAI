import React from 'react';

function EchoDisplay({ echo }) {
  const { type, content, intensity, color } = echo;

  const style = {
    borderColor: color,
    boxShadow: `0 0 ${intensity * 2}px ${color}`,
    opacity: 0.8 + (intensity * 0.04) // More intense echoes are slightly more opaque
  };

  return (
    <div className="echo-card" style={style}>
      <h3 className="echo-type">{type}</h3>
      <p className="echo-content">{content}</p>
      <p className="echo-intensity">Intensity: {intensity}/10</p>
    </div>
  );
}

export default EchoDisplay;
