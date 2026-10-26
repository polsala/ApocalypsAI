import React from 'react';

function EventDisplay({ events }) {
  return (
    <section className="event-display">
      <h2>Simulated Apocalyptic Events</h2>
      {events.length === 0 ? (
        <p>No current apocalyptic events detected. Enjoy the calm!</p>
      ) : (
        <ul>
          {events.map(event => (
            <li key={event.id}>
              <strong>{event.type}</strong> - {event.intensity || event.severity || event.location || 'Details unknown'}
              <br />
              <small>Occurred: {new Date(event.timestamp).toLocaleString()}</small>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default EventDisplay;
