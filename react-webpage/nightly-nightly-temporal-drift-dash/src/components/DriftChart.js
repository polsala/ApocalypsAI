import React from 'react';

const DriftChart = ({ data }) => {
  if (!data || data.length === 0) {
    return <p>No temporal drifts detected. All clear... for now.</p>;
  }

  const getSeverityClass = (severity) => {
    switch (severity.toLowerCase()) {
      case 'low': return 'severity-low';
      case 'medium': return 'severity-medium';
      case 'high': return 'severity-high';
      default: return '';
    }
  };

  return (
    <div className="drift-list">
      <h2>Detected Temporal Anomalies</h2>
      {data.map((drift) => (
        <div key={drift.id} className={`drift-item ${getSeverityClass(drift.severity)}`}>
          <span className="drift-item-timestamp">{new Date(drift.timestamp).toLocaleString()}</span>
          <span className="drift-item-description">{drift.description}</span>
          <span className="drift-item-severity">{drift.severity.toUpperCase()}</span>
        </div>
      ))}
    </div>
  );
};

export default DriftChart;
