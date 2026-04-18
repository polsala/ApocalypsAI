import React from 'react';
import './EchoDisplay.css';

const EchoDisplay = ({ value, maxValue, label, color }) => {
  const percentage = (value / maxValue) * 100;

  return (
    <div className="echo-display-bar-container">
      <div
        className="echo-display-bar"
        style={{
          width: `${percentage}%`,
          backgroundColor: color || '#00FF00'
        }}
      ></div>
      <span className="echo-display-label">{label}</span>
    </div>
  );
};

export default EchoDisplay;
