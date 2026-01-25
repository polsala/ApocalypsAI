import React, { useState } from 'react';

function EchoInput({ onAddEvent }) {
  const [timestamp, setTimestamp] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (timestamp && message) {
      onAddEvent(timestamp, message);
      setTimestamp('');
      setMessage('');
    } else {
      alert('Please provide both a timestamp and a message.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Add Temporal Event</h2>
      <label htmlFor="timestamp">Timestamp:</label>
      <input
        type="datetime-local"
        id="timestamp"
        value={timestamp}
        onChange={(e) => setTimestamp(e.target.value)}
        required
      />
      <label htmlFor="message">Message:</label>
      <textarea
        id="message"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Enter event message..."
        rows="4"
        required
      ></textarea>
      <button type="submit">Add Event</button>
    </form>
  );
}

export default EchoInput;
