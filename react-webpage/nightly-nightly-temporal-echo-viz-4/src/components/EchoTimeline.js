import React from 'react';
import EchoCard from './EchoCard';

function EchoTimeline({ echoes }) {
  return (
    <div className="timeline-container">
      <h2>Temporal Echoes Detected</h2>
      {echoes.length === 0 ? (
        <p>No echoes match the current filters. The timeline is eerily quiet...</p>
      ) : (
        <div className="echo-list">
          {echoes.map((echo) => (
            <EchoCard key={echo.id} echo={echo} />
          ))}
        </div>
      )}
    </div>
  );
}

export default EchoTimeline;
