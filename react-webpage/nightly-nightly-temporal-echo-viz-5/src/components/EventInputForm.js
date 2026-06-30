import React, { useState } from 'react';

function EventInputForm({ onGenerate }) {
  const [event, setEvent] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onGenerate(event);
  };

  return (
    <form className="event-input-form" onSubmit={handleSubmit}>
      <label htmlFor="eventNameInput">
        Describe a Temporal Event:
      </label>
      <input
        id="eventNameInput"
        type="text"
        value={event}
        onChange={(e) => setEvent(e.target.value)}
        placeholder="e.g., 'The Great Spore Bloom of '27'"
        aria-label="Temporal Event Name"
      />
      <button type="submit">Generate Echoes</button>
    </form>
  );
}

export default EventInputForm;
