import React from 'react';

function EchoDisplay({ echoes }) {
  if (echoes.length === 0) {
    return (
      <div className="echo-display">
        <h2>Temporal Echoes</h2>
        <p>Enter an event above to see its echoes across the timelines.</p>
      </div>
    );
  }

  return (
    <div className="echo-display">
      <h2>Temporal Echoes</h2>
      <ul className="echo-list">
        {echoes.map((echo) => (
          <li key={echo.id} className="echo-item">
            <h3>Echo from {echo.timeOffset}</h3>
            <p>Intensity: <span className="intensity">{echo.intensity}</span></p>
            <p>{echo.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default EchoDisplay;
