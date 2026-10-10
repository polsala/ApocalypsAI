import React, { useState } from 'react';

const AnomalyForm = ({ onAddAnomaly }) => {
  const [description, setDescription] = useState('');
  const [timestamp, setTimestamp] = useState('');
  const [type, setType] = useState('Auditory Echo');
  const [energyLevel, setEnergyLevel] = useState(5);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!description || !timestamp) {
      alert('Description and Timestamp are required!');
      return;
    }

    const newAnomaly = {
      id: Date.now(), // Simple unique ID
      description,
      timestamp,
      type,
      energyLevel: parseInt(energyLevel, 10),
    };

    onAddAnomaly(newAnomaly);
    setDescription('');
    setTimestamp('');
    setType('Auditory Echo');
    setEnergyLevel(5);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Log New Anomaly</h2>
      <div>
        <label htmlFor="description">Description:</label>
        <input
          id="description"
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="e.g., Heard a faint Roman trumpet call"
          required
        />
      </div>
      <div>
        <label htmlFor="timestamp">Timestamp:</label>
        <input
          id="timestamp"
          type="datetime-local"
          value={timestamp}
          onChange={(e) => setTimestamp(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="type">Anomaly Type:</label>
        <select
          id="type"
          value={type}
          onChange={(e) => setType(e.target.value)}
        >
          <option value="Auditory Echo">Auditory Echo</option>
          <option value="Visual Glitch">Visual Glitch</option>
          <option value="Object Displacement">Object Displacement</option>
          <option value="Temporal Loop">Temporal Loop</option>
          <option value="Phantom Entity">Phantom Entity</option>
          <option value="Other">Other</option>
        </select>
      </div>
      <div>
        <label htmlFor="energyLevel">Temporal Energy Level (1-10):</label>
        <input
          id="energyLevel"
          type="number"
          min="1"
          max="10"
          value={energyLevel}
          onChange={(e) => setEnergyLevel(e.target.value)}
        />
      </div>
      <button type="submit">Add Anomaly</button>
    </form>
  );
};

export default AnomalyForm;
