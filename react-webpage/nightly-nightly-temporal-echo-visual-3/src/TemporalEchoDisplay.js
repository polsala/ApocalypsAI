import React from 'react';
import './TemporalEchoDisplay.css';

function TemporalEchoDisplay({ echoes }) {
  return (
    <div className="echo-list-container">
      <h2>Detected Echoes</h2>
      <ul className="echo-list">
        {echoes.map(echo => (
          <li key={echo.id} className={`echo-item echo-type-${echo.type.replace(/\s/g, '-')}`}>
            <div className="echo-header">
              <span className="echo-timestamp">{new Date(echo.timestamp).toLocaleString()}</span>
              <span className="echo-type">{echo.type}</span>
            </div>
            <div className="echo-details">
              <p>Magnitude: <span className="echo-magnitude">{echo.magnitude.toFixed(2)}</span></p>
              <p className="echo-description">{echo.description}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TemporalEchoDisplay;
