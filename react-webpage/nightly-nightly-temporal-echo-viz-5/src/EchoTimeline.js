import React, { useState } from 'react';
import './EchoTimeline.css';

const EchoTimeline = ({ echoes }) => {
  const [selectedEcho, setSelectedEcho] = useState(null);

  // Sort echoes by timestamp for chronological display
  const sortedEchoes = [...echoes].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

  const handleEchoClick = (echo) => {
    setSelectedEcho(selectedEcho?.id === echo.id ? null : echo);
  };

  const formatTimestamp = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleString(); // Format to local date and time
  };

  return (
    <div className="echo-timeline-container">
      <h2>Temporal Echoes Detected</h2>
      <div className="timeline-track">
        {sortedEchoes.map((echo) => (
          <div
            key={echo.id}
            className={`echo-point ${echo.type.toLowerCase().replace(/\s/g, '-')}`}
            style={{ left: `${Math.random() * 90 + 5}%` }} // Whimsical: random horizontal position for visual spread
            onClick={() => handleEchoClick(echo)}
            title={`${echo.type} at ${formatTimestamp(echo.timestamp)}`}
          >
            <span className="echo-marker"></span>
            <span className="echo-label">{echo.type}</span>
          </div>
        ))}
      </div>
      {selectedEcho && (
        <div className="echo-detail-panel">
          <h3>Echo Details: {selectedEcho.type}</h3>
          <p><strong>Timestamp:</strong> {formatTimestamp(selectedEcho.timestamp)}</p>
          <p><strong>Magnitude:</strong> {selectedEcho.magnitude.toFixed(2)}</p>
          <p><strong>Description:</strong> {selectedEcho.description}</p>
          <button onClick={() => setSelectedEcho(null)}>Close</button>
        </div>
      )}
      {sortedEchoes.length === 0 && <p>No echoes to display on the timeline.</p>}
    </div>
  );
};

export default EchoTimeline;
