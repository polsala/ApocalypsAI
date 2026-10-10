import React from 'react';

const AnomalyGraph = ({ anomalies }) => {
  // For this exercise, we'll display anomalies as a simple sorted list.
  // In a full implementation, this would be an interactive graph visualization.

  const sortedAnomalies = [...anomalies].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

  return (
    <div>
      <h2>Observed Temporal Anomalies</h2>
      {sortedAnomalies.length === 0 ? (
        <p>No anomalies logged yet. Start by adding one!</p>
      ) : (
        <ul className="anomaly-list">
          {sortedAnomalies.map((anomaly) => (
            <li key={anomaly.id} className="anomaly-item">
              <p><strong>Description:</strong> {anomaly.description}</p>
              <p><strong>Timestamp:</strong> {new Date(anomaly.timestamp).toLocaleString()}</p>
              <p><strong>Type:</strong> {anomaly.type}</p>
              <p><strong>Energy Level:</strong> {anomaly.energyLevel}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default AnomalyGraph;
