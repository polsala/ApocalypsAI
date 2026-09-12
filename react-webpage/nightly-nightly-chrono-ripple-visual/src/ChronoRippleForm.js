import React, { useState, useEffect } from 'react';

function ChronoRippleForm({ onVisualize, initialDetails }) {
  const [date, setDate] = useState(initialDetails.date);
  const [description, setDescription] = useState(initialDetails.description);
  const [magnitude, setMagnitude] = useState(initialDetails.magnitude);

  useEffect(() => {
    // Update local state if initialDetails change (e.g., from parent reset)
    setDate(initialDetails.date);
    setDescription(initialDetails.description);
    setMagnitude(initialDetails.magnitude);
  }, [initialDetails]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onVisualize({ date, description, magnitude });
  };

  return (
    <form onSubmit={handleSubmit} className="chrono-form">
      <div className="form-group">
        <label htmlFor="eventDate">Event Date:</label>
        <input
          type="date"
          id="eventDate"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="eventDescription">Description:</label>
        <input
          type="text"
          id="eventDescription"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="e.g., The Great Chrono-Shift"
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="eventMagnitude">Magnitude: {magnitude}</label>
        <input
          type="range"
          id="eventMagnitude"
          min="1"
          max="10"
          value={magnitude}
          onChange={(e) => setMagnitude(parseInt(e.target.value))}
        />
      </div>
      <button type="submit">Visualize Ripples</button>
    </form>
  );
}

export default ChronoRippleForm;
