import React, { useState } from 'react';

function GlitchForm({ onAddGlitch }) {
  const [description, setDescription] = useState('');
  const [type, setType] = useState('Object Displacement');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!description.trim()) return;
    onAddGlitch({ description, type });
    setDescription('');
    setType('Object Displacement');
  };

  return (
    <div className="glitch-form-container">
      <h2>Report a New Glitch</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="description">Description:</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="e.g., My coffee mug vanished from my desk and reappeared in the fridge!"
          rows="3"
          required
        ></textarea>

        <label htmlFor="type">Type of Glitch:</label>
        <select id="type" value={type} onChange={(e) => setType(e.target.value)}>
          <option value="Object Displacement">Object Displacement</option>
          <option value="Time Skip">Time Skip</option>
          <option value="Auditory Echo">Auditory Echo</option>
          <option value="Déjà Vu Loop">Déjà Vu Loop</option>
          <option value="Minor Reality Shift">Minor Reality Shift</option>
          <option value="Unexplained Phenomenon">Unexplained Phenomenon</option>
        </select>

        <button type="submit">Report Glitch</button>
      </form>
    </div>
  );
}

export default GlitchForm;
