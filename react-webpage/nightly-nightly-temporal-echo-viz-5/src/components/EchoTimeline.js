import React from 'react';
import './EchoTimeline.css';

const EchoTimeline = ({ echoes }) => {
  // Sort echoes by timestamp for chronological display
  const sortedEchoes = [...echoes].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

  const getTypeColor = (type) => {
    switch (type) {
      case 'Major Anomaly': return '#ff6b6b'; // Red
      case 'Echo Signature': return '#ffe66d'; // Yellow
      case 'Minor Drift': return '#6bff6b'; // Green
      case 'Temporal Ripple': return '#6bbaff'; // Blue
      default: return '#cccccc'; // Grey
    }
  };

  return (
    <div className="echo-timeline-container">
      <h2>Temporal Event Log</h2>
      <div className="timeline-track">
        {sortedEchoes.map((echo) => (
          <div
            key={echo.id}
            className="timeline-event"
            style={{ borderColor: getTypeColor(echo.type) }}
            title={`Magnitude: ${echo.magnitude}`}
          >
            <div className="event-header">
              <span className="event-type" style={{ backgroundColor: getTypeColor(echo.type) }}>{echo.type}</span>
              <span className="event-timestamp">{new Date(echo.timestamp).toLocaleString()}</span>
            </div>
            <p className="event-description">{echo.description}</p>
          </div>
        ))}
      </div>
      {sortedEchoes.length === 0 && <p>No temporal echoes detected. All clear... for now.</p>}
    </div>
  );
};

export default EchoTimeline;
