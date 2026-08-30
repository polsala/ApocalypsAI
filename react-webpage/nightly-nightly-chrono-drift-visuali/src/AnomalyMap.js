import React from 'react';
import './App.css'; // Import App.css for styling

function AnomalyMap({ anomalies, onSelectAnomaly }) {
  return (
    <div className="map-container">
      {anomalies.map((anomaly) => (
        <div
          key={anomaly.id}
          className={`anomaly-marker severity-${anomaly.severity}`}
          style={{ left: anomaly.location.x, top: anomaly.location.y }}
          onClick={() => onSelectAnomaly(anomaly)}
          title={anomaly.name}
        >
          {/* Optional: display first letter of ID or severity */}
          {anomaly.id.split('-')[1]}
        </div>
      ))}
    </div>
  );
}

export default AnomalyMap;
