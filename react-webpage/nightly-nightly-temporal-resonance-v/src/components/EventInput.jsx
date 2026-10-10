import React, { useState } from 'react';

function EventInput({ onAddEvent }) {
  const [eventName, setEventName] = useState('');
  const [eventDate, setEventDate] = useState('');
  const [resonanceStrength, setResonanceStrength] = useState('5');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!eventName || !eventDate) return;
    onAddEvent(eventName, eventDate, resonanceStrength);
    setEventName('');
    setEventDate('');
    setResonanceStrength('5'); // Reset to default
  };

  return (
    <div className="event-input-form">
      <h2>Add Temporal Event</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="eventName">Event Name:</label>
        <input
          id="eventName"
          type="text"
          value={eventName}
          onChange={(e) => setEventName(e.target.value)}
          placeholder="e.g., The Great Coffee Spill"
          required
        />

        <label htmlFor="eventDate">Event Date:</label>
        <input
          id="eventDate"
          type="datetime-local"
          value={eventDate}
          onChange={(e) => setEventDate(e.target.value)}
          required
        />

        <label htmlFor="resonanceStrength">Resonance Strength (1-10):</label>
        <select
          id="resonanceStrength"
          value={resonanceStrength}
          onChange={(e) => setResonanceStrength(e.target.value)}
        >
          {[...Array(10)].map((_, i) => (
            <option key={i + 1} value={i + 1}>
              {i + 1}
            </option>
          ))}
        </select>

        <button type="submit">Add Event</button>
      </form>
    </div>
  );
}

export default EventInput;
