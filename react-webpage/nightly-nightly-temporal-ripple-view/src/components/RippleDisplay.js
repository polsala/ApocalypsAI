import React from 'react';
import './RippleDisplay.css';

function RippleDisplay({ anomaly, onStabilize, readOnly }) {
  const { id, type, severity, timestamp, status } = anomaly;
  const severityClass = `severity-${severity}`;
  const statusClass = `status-${status}`;

  const handleStabilizeClick = () => {
    if (!readOnly && status === 'active') {
      onStabilize(id);
    }
  };

  return (
    <div className={`ripple-card ${severityClass} ${statusClass}`}>
      <h3>{type} Anomaly</h3>
      <p><strong>ID:</strong> {id}</p>
      <p><strong>Severity:</strong> {severity} / 5</p>
      <p><strong>Detected:</strong> {new Date(timestamp).toLocaleString()}</p>
      <p><strong>Status:</strong> {status}</p>
      {!readOnly && status === 'active' && (
        <button onClick={handleStabilizeClick} className="stabilize-button">
          Stabilize Ripple
        </button>
      )}
      {readOnly && status === 'stabilized' && (
        <span className="stabilized-indicator">Stabilized</span>
      )}
    </div>
  );
}

export default RippleDisplay;
