import React from 'react';
import './EchoVisualizer.css';

function EchoVisualizer({ echoes }) {
  if (echoes.length === 0) {
    return <p className="no-echoes">No echoes found matching your criteria.</p>;
  }

  return (
    <div className="echo-list">
      {echoes.map(echo => (
        <div key={echo.id} className="echo-card">
          <div className="echo-header">
            <span className="echo-category">{echo.category}</span>
            <span className="echo-timestamp">{new Date(echo.timestamp).toLocaleString()}</span>
          </div>
          <p className="echo-description">{echo.description}</p>
        </div>
      ))}
    </div>
  );
}

export default EchoVisualizer;
