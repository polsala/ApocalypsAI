import React, { useState } from 'react';
import './TaskInput.css';

function TaskInput({ onAddTask }) {
  const [name, setName] = useState('');
  const [duration, setDuration] = useState('');
  const [charge, setCharge] = useState('Neutral');

  const handleSubmit = (e) => {
    e.preventDefault();
    onAddTask(name, duration, charge);
    setName('');
    setDuration('');
    setCharge('Neutral');
  };

  return (
    <form onSubmit={handleSubmit} className="task-input-form">
      <input
        type="text"
        placeholder="Task Name (e.g., Scavenge for parts)"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        type="number"
        placeholder="Duration (minutes)"
        value={duration}
        onChange={(e) => setDuration(e.target.value)}
        min="1"
        required
      />
      <select value={charge} onChange={(e) => setCharge(e.target.value)}>
        <option value="Positive">Positive</option>
        <option value="Neutral">Neutral</option>
        <option value="Negative">Negative</option>
      </select>
      <button type="submit">Add Task</button>
    </form>
  );
}

export default TaskInput;
