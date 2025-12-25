import React from 'react';
import EchoEvent from './EchoEvent';
import './Timeline.css';

function Timeline({ echoes }) {
  if (!echoes || echoes.length === 0) {
    return <p className="timeline-empty">No temporal echoes detected.</p>;
  }

  return (
    <div className="timeline-container">
      {echoes.map(echo => (
        <EchoEvent key={echo.id} event={echo} />
      ))}
    </div>
  );
}

export default Timeline;
