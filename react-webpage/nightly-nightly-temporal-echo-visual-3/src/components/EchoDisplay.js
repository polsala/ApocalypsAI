import React from 'react';
import './EchoDisplay.css';

const EchoDisplay = ({ echo, onSelect, isSelected }) => {
  const getEchoSymbol = (type) => {
    switch (type) {
      case 'Temporal Ripple': return '〰️';
      case 'Echo Loop': return '🌀';
      case 'Reality Glitch': return '⚡';
      case 'Chronal Shift': return '⏳';
      default: return '✨';
    }
  };

  return (
    <div
      className={`echo-item ${isSelected ? 'selected' : ''} severity-${echo.severity.toLowerCase()}`}
      onClick={() => onSelect(echo)}
      title={echo.description}
    >
      <span className="echo-symbol">{getEchoSymbol(echo.type)}</span>
      <span className="echo-id">{echo.id.substring(0, 4)}...</span>
    </div>
  );
};

export default EchoDisplay;
