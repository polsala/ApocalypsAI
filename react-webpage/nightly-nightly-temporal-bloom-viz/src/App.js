import React, { useState } from 'react';
import TemporalBloomCanvas from './components/TemporalBloomCanvas';
import './App.css';

function App() {
  const [frequency, setFrequency] = useState(0.01);
  const [intensity, setIntensity] = useState(0.5);
  const [decay, setDecay] = useState(0.95);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Temporal Bloom Visualizer</h1>
      </header>
      <div className="controls">
        <label>
          Resonance Frequency: {frequency.toFixed(3)}
          <input
            type="range"
            min="0.001"
            max="0.05"
            step="0.001"
            value={frequency}
            onChange={(e) => setFrequency(parseFloat(e.target.value))}
          />
        </label>
        <label>
          Bloom Intensity: {intensity.toFixed(2)}
          <input
            type="range"
            min="0.1"
            max="1.0"
            step="0.01"
            value={intensity}
            onChange={(e) => setIntensity(parseFloat(e.target.value))}
          />
        </label>
        <label>
          Decay Rate: {decay.toFixed(2)}
          <input
            type="range"
            min="0.8" 
            max="0.99"
            step="0.01"
            value={decay}
            onChange={(e) => setDecay(parseFloat(e.target.value))}
          />
        </label>
      </div>
      <TemporalBloomCanvas
        frequency={frequency}
        intensity={intensity}
        decay={decay}
      />
    </div>
  );
}

export default App;
