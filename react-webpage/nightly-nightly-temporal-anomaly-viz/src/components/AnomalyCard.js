import React from 'react';
import './AnomalyCard.css';

function AnomalyCard({ anomaly }) {
  if (!anomaly) {
    return <p>No anomaly selected.</p>;
  }

  const handleStabilize = () => {
    alert(`Attempting to stabilize the ${anomaly.type} at ${new Date(anomaly.timestamp).toLocaleString()}... \n\n(Spoiler: It's mostly for show. Time is a fickle mistress.)`);
  };

  return (
    <div className="anomaly-card">
      <h3>{anomaly.type}</h3>
      <p><strong>Detected:</strong> {new Date(anomaly.timestamp).toLocaleString()}</p>
      <p><strong>Location:</strong> {anomaly.location}</p>
      <p><strong>Severity:</strong> <span className={`severity-text severity-${anomaly.severity.toLowerCase().replace(' ', '-')}`}>{anomaly.severity}</span></p>
      <p><strong>Potential Impact:</strong> {anomaly.impact}</p>
      <p><strong>Description:</strong> {anomaly.description}</p>
      <button onClick={handleStabilize} className="stabilize-button">Attempt Stabilization</button>
    </div>
  );
}

export default AnomalyCard;
