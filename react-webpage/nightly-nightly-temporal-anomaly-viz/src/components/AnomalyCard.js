import React, { useState } from 'react';

const AnomalyCard = ({ anomaly }) => {
  const [isStabilized, setIsStabilized] = useState(false);

  const handleStabilize = () => {
    // In a real application, this would trigger an API call
    // to a backend service to attempt stabilization.
    // For this utility, it's a simulated action.
    console.log(`Attempting to stabilize anomaly ${anomaly.id}...`);
    setIsStabilized(true);
  };

  const severityClass = `severity-${anomaly.severity.toLowerCase()}`;
  const cardClass = `anomaly-card ${severityClass} ${isStabilized ? 'stabilized' : ''}`;

  return (
    <div className={cardClass}>
      <h3 className={anomaly.severity === 'Critical' ? 'glitch-text' : ''}>Anomaly ID: {anomaly.id}</h3>
      <p><strong>Type:</strong> {anomaly.type}</p>
      <p><strong>Severity:</strong> {anomaly.severity}</p>
      <p><strong>Timestamp:</strong> {new Date(anomaly.timestamp).toLocaleString()}</p>
      <button onClick={handleStabilize} disabled={isStabilized}>
        {isStabilized ? 'Stabilized' : 'Stabilize Anomaly'}
      </button>
    </div>
  );
};

export default AnomalyCard;
