import React, { useState } from 'react';
import './App.css';
import TemporalRippleChart from './TemporalRippleChart';

function App() {
  const [temporalEvents, setTemporalEvents] = useState([]);
  const [newEventDescription, setNewEventDescription] = useState('');
  const [newDistortionLevel, setNewDistortionLevel] = useState('Minor');

  const distortionLevels = ['Minor', 'Moderate', 'Severe', 'Cataclysmic'];

  const addRipple = () => {
    if (newEventDescription.trim() === '') return;

    const newEvent = {
      id: Date.now(), // Unique ID for the ripple
      description: newEventDescription.trim(),
      timestamp: Date.now(),
      distortionLevel: newDistortionLevel,
    };

    setTemporalEvents((prevEvents) => [...prevEvents, newEvent].sort((a, b) => a.timestamp - b.timestamp));
    setNewEventDescription('');
    setNewDistortionLevel('Minor');
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Ripple Viewer</h1>
        <p>Observe the fabric of spacetime</p>
      </header>
      <main>
        <div className="input-section">
          <input
            type="text"
            placeholder="Describe the temporal anomaly..."
            value={newEventDescription}
            onChange={(e) => setNewEventDescription(e.target.value)}
            aria-label="Temporal anomaly description"
          />
          <select
            value={newDistortionLevel}
            onChange={(e) => setNewDistortionLevel(e.target.value)}
            aria-label="Distortion level"
          >
            {distortionLevels.map((level) => (
              <option key={level} value={level}>
                {level}
              </option>
            ))}
          </select>
          <button onClick={addRipple}>Add Ripple</button>
        </div>
        <TemporalRippleChart events={temporalEvents} />
      </main>
    </div>
  );
}

export default App;
