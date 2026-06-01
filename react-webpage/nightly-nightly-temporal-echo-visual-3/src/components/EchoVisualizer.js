import React from 'react';
import './EchoVisualizer.css';

function EchoVisualizer({ echoData }) {
  return (
    <div className="echo-visualizer">
      {echoData.map((strength, index) => (
        <div
          key={index}
          className="echo-bar"
          style={{ height: `${strength * 100}%`, opacity: strength + 0.1 }}
          title={`Echo Strength: ${strength.toFixed(2)}`}
          aria-label={`Echo bar ${index + 1} with strength ${strength.toFixed(2)}`}
        ></div>
      ))}
    </div>
  );
}

export default EchoVisualizer;
