import React from 'react';
import './TimelineVisualization.css';

function TimelineVisualization({ echoes }) {
  if (!echoes || echoes.length === 0) {
    return <p>No echoes to display. Enter a concept and generate some!</p>;
  }

  // Sort echoes by offset for proper timeline display
  const sortedEchoes = [...echoes].sort((a, b) => a.offset - b.offset);

  return (
    <div className="timeline-container" data-testid="timeline-container">
      <div className="timeline-line"></div>
      {sortedEchoes.map((echo) => (
        <div
          key={echo.id}
          className="timeline-event"
          style={{ left: `${echo.offset}%`, opacity: echo.strength / 100 }}
          title={echo.description}
        >
          <div className="event-dot"></div>
          <div className="event-label">
            <span className="event-term">{echo.term}</span>
            <span className="event-offset">({echo.offset} units)</span>
          </div>
        </div>
      ))}
    </div>
  );
}

export default TimelineVisualization;
