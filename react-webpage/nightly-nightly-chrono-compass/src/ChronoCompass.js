import React from 'react';

function ChronoCompass({ events }) {
  const formatDateTime = (isoString) => {
    if (!isoString) return 'N/A';
    const date = new Date(isoString);
    return date.toLocaleString();
  };

  return (
    <div className="chrono-compass">
      {events.length === 0 ? (
        <p style={{ textAlign: 'center', color: '#a0a0a0' }}>No temporal events logged yet. Add one above!</p>
      ) : (
        <ul className="event-list">
          {events.map((event) => (
            <li key={event.id} className="event-item">
              <strong>{event.name}</strong>
              <span>Original: {formatDateTime(event.originalDate)}</span>
              <span className="shifted-date">Shifted: {formatDateTime(event.shiftedDate)}</span>
              <span className="echo-date">Echo: {formatDateTime(event.echoDate)}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default ChronoCompass;
