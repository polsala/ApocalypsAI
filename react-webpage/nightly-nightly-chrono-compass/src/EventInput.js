import React, { useState } from 'react';

function EventInput({ onAddEvent }) {
  const [eventName, setEventName] = useState('');
  const [eventDateTime, setEventDateTime] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (eventName.trim() && eventDateTime) {
      onAddEvent(eventName, eventDateTime);
      setEventName('');
      setEventDateTime('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="event-form">
      <label>
        Event Name:
        <input
          type="text"
          value={eventName}
          onChange={(e) => setEventName(e.target.value)}
          placeholder="e.g., Found the last can of beans"
          required
        />
      </label>
      <label>
        Original Date & Time:
        <input
          type="datetime-local"
          value={eventDateTime}
          onChange={(e) => setEventDateTime(e.target.value)}
          required
        />
      </label>
      <button type="submit">Add Event to Chrono-Compass</button>
    </form>
  );
}

export default EventInput;
