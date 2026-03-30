import React, { useState } from 'react';

const ActivityLogger = ({ onLog, activities }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onLog(input);
      setInput('');
    }
  };

  return (
    <div className="activity-logger">
      <h2>Daily Activities</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Log today's activity..."
        />
        <button type="submit">Add</button>
      </form>
      <ul>
        {activities.map((activity, index) => (
          <li key={index}>{activity}</li>
        ))}
      </ul>
    </div>
  );
};

export default ActivityLogger;
