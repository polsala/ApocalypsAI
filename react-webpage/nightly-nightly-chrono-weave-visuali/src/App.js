/**
 * @file App.js
 * @description Main application component for the Nightly Chrono-Weave Visualizer.
 */

import React, { useState } from 'react';
import ChronoWeave from './ChronoWeave';

function App() {
  const [isRunning, setIsRunning] = useState(true);
  const [speed, setSpeed] = useState(50); // 0-100
  const [anomalyFrequency, setAnomalyFrequency] = useState(20); // 0-100

  return (
    <div className="App">
      <div className="controls">
        <button onClick={() => setIsRunning(!isRunning)}>
          {isRunning ? 'Stop Weave' : 'Start Weave'}
        </button>
        <label>
          Speed:
          <input
            type="range"
            min="0"
            max="100"
            value={speed}
            onChange={(e) => setSpeed(Number(e.target.value))}
          />
          <span>{speed}</span>
        </label>
        <label>
          Anomaly Frequency:
          <input
            type="range"
            min="0"
            max="100"
            value={anomalyFrequency}
            onChange={(e) => setAnomalyFrequency(Number(e.target.value))}
          />
          <span>{anomalyFrequency}</span>
        </label>
      </div>
      <ChronoWeave
        isRunning={isRunning}
        speed={speed}
        anomalyFrequency={anomalyFrequency}
      />
    </div>
  );
}

export default App;
