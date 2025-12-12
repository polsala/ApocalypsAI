import React, { useState } from 'react';
import './App.css';
import TemporalMoodRing from './TemporalMoodRing';

function App() {
  const [anomalySeverity, setAnomalySeverity] = useState(0.5); // Initial neutral mood

  const scanForAnomalies = () => {
    // Simulate fetching a new anomaly severity score between 0 and 1
    const newSeverity = Math.random();
    setAnomalySeverity(newSeverity);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Anomaly Mood Ring</h1>
        <TemporalMoodRing severity={anomalySeverity} />
        <button className="scan-button" onClick={scanForAnomalies}>
          Scan for Anomalies
        </button>
        <p className="lore-text">
          Gaze into the orb to discern the current temporal vibrations.
        </p>
      </header>
    </div>
  );
}

export default App;
