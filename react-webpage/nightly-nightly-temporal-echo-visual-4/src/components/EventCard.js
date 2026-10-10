import React, { useState } from 'react';
import '../styles/EventCard.css';

function EventCard({ event }) {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  const formatTimestamp = (timestamp) => {
    try {
      const date = new Date(timestamp);
      return date.toLocaleString();
    } catch (e) {
      return timestamp; // Return original if invalid
    }
  };

  return (
    <div className={`event-card ${isExpanded ? 'expanded' : ''}`}>
      <div className="event-header" onClick={toggleExpand}>
        <span className="event-timestamp">{formatTimestamp(event.timestamp)}</span>
        <span className="event-type">{event.type}</span>
        <span className="expand-toggle">{isExpanded ? '▲' : '▼'}</span>
      </div>
      {isExpanded && (
        <pre className="event-details">
          {JSON.stringify(event, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default EventCard;
