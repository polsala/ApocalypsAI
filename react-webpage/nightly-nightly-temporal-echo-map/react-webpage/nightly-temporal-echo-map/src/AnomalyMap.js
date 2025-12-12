import React from 'react';
import './AnomalyMap.css';

const AnomalyMap = ({ anomalies, onStabilize }) => {
  return (
    <div className="anomaly-map-container">
      {anomalies.map(anomaly => (
        <div
          key={anomaly.id}
          className={`anomaly-marker ${anomaly.status.toLowerCase().replace(' ', '-')}`}
          style={{
            left: `${(anomaly.coordinates.lng + 180) / 3.6}vw`, // Simple mapping to a 0-100% range
            top: `${(anomaly.coordinates.lat + 90) / 1.8}vh`, // Simple mapping to a 0-100% range
          }}
          title={`${anomaly.type}: ${anomaly.location} (${anomaly.status})`}
        >
          <span className="anomaly-icon" role="img" aria-label={anomaly.type}>
            {anomaly.type === 'Temporal Ripple' && '🌊'}
            {anomaly.type === 'Echo Cascade' && '🔊'}
            {anomaly.type === 'Chronal Drift' && '⏳'}
            {anomaly.type === 'Void Whisper' && '🌌'}
            {anomaly.type === 'Temporal Loop' && '🔄'}
            {anomaly.status === 'Stabilized' && '✅'}
          </span>
          <div className="anomaly-details">
            <h3>{anomaly.type}</h3>
            <p><strong>Location:</strong> {anomaly.location}</p>
            <p><strong>Severity:</strong> {anomaly.severity}</p>
            <p><strong>Status:</strong> {anomaly.status}</p>
            <p>{anomaly.description}</p>
            {anomaly.status !== 'Stabilized' && (
              <button onClick={() => onStabilize(anomaly.id)}>Stabilize</button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default AnomalyMap;
