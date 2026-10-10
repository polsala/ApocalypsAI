import React from 'react';

function EventList({ events }) {
  return (
    <div className="event-list-container">
      <h2>Temporal Echoes</h2>
      {events.length === 0 ? (
        <p>No temporal echoes detected yet. Add an event!</p>
      ) : (
        <ul className="event-list">
          {events.map((event) => (
            <li key={event.id}>
              <span className="event-name">{event.name}</span>
              <span className="event-date">{new Date(event.date).toLocaleString()}</span>
              <span className="event-resonance">Resonance: {event.resonance}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default EventList;
