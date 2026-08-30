import React from 'react';
import './App.css'; // Import App.css for styling

function AnomalyDetails({ anomaly }) {
  if (!anomaly) {
    return <div className="anomaly-details">Select an anomaly to view details.</div>;
  }

  return (
    <div className="anomaly-details">
      <h3>Anomaly: {anomaly.name}</h3>
      <p><strong>ID:</strong> {anomaly.id}</p>
      <p><strong>Severity:</strong> <span className={`severity-${anomaly.severity}`}>{anomaly.severity.toUpperCase()}</span></p>
      <p><strong>Resonance Frequency:</strong> {anomaly.resonanceFrequency}</p>
      <p><strong>Drift Magnitude:</strong> {anomaly.driftMagnitude}</p>
      <p><strong>Estimated Impact Radius:</strong> {anomaly.impactRadius}</p>
      <p><strong>Description:</strong> {anomaly.description}</p>
    </div>
  );
}

export default AnomalyDetails;
