import React, { useState } from 'react';
import './App.css';
import EchoVisualizer from './EchoVisualizer';
import { generateEchoData } from './EchoGenerator';

function App() {
  const [location, setLocation] = useState('');
  const [time, setTime] = useState('');
  const [echoData, setEchoData] = useState([]);

  const handleVisualize = () => {
    if (location && time) {
      const data = generateEchoData(location, time);
      setEchoData(data);
    } else {
      alert('Please enter both location and time.');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Visualizer</h1>
        <p>Perceive the ripples in spacetime.</p>
      </header>
      <main className="App-main">
        <div className="input-section">
          <label htmlFor="location-input">Location:</label>
          <input
            id="location-input"
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="e.g., Old Bridge Crossing"
          />
          <label htmlFor="time-input">Time:</label>
          <input
            id="time-input"
            type="datetime-local"
            value={time}
            onChange={(e) => setTime(e.target.value)}
          />
          <button onClick={handleVisualize}>Visualize Temporal Echoes</button>
        </div>
        <div className="visualization-section">
          {echoData.length > 0 ? (
            <EchoVisualizer data={echoData} />
          ) : (
            <p className="placeholder-text">Enter location and time to visualize echoes.</p>
          )}
        </div>
      </main>
      <footer className="App-footer">
        <p>&copy; 2077 ApocalypsAI Nightly Integrator</p>
      </footer>
    </div>
  );
}

export default App;
