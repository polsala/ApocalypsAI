import React from 'react';
import './AnomalyTimeline.css';

function AnomalyTimeline({ anomalies, onSelectAnomaly }) {
  return (
    <div className="anomaly-timeline">
      {anomalies.map((anomaly) => (
        <div
          key={anomaly.id}
          className={`anomaly-item severity-${anomaly.severity.toLowerCase().replace(' ', '-')}`}
          onClick={() => onSelectAnomaly(anomaly)}
          title={`Click for details on ${anomaly.type}`}
        >
          <span className="anomaly-timestamp">{new Date(anomaly.timestamp).toLocaleString()}</span>
          <span className="anomaly-type">{anomaly.type}</span>
          <span className="anomaly-severity">({anomaly.severity})</span>
        </div>
      ))}
    </div>
  );
}

export default AnomalyTimeline;
