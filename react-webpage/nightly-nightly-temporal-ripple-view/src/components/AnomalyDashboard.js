import React from 'react';
import RippleDisplay from './RippleDisplay';
import './AnomalyDashboard.css';

function AnomalyDashboard({ title, anomalies, onStabilize, readOnly = false }) {
  return (
    <section className="anomaly-dashboard">
      <h2>{title} ({anomalies.length})</h2>
      {anomalies.length === 0 ? (
        <p>No {title.toLowerCase()} detected at this moment. All clear!</p>
      ) : (
        <div className="ripple-grid">
          {anomalies.map((anomaly) => (
            <RippleDisplay
              key={anomaly.id}
              anomaly={anomaly}
              onStabilize={onStabilize}
              readOnly={readOnly}
            />
          ))}
        </div>
      )}
    </section>
  );
}

export default AnomalyDashboard;
