import React, { useState } from 'react';
import './App.css';
import EchoVisualizer from './components/EchoVisualizer';

function App() {
  const [inputText, setInputText] = useState('The quick brown fox jumps over the lazy dog.');
  const [distortionLevel, setDistortionLevel] = useState(0.5);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Visualizer</h1>
        <p>Observe the subtle distortions of temporal echoes on text.</p>
      </header>
      <main>
        <div className="input-section">
          <label htmlFor="text-input">Input Text:</label>
          <textarea
            id="text-input"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            rows="5"
            placeholder="Enter text to visualize temporal echoes..."
          />
        </div>
        <div className="slider-section">
          <label htmlFor="distortion-slider">Distortion Level: {distortionLevel.toFixed(2)}</label>
          <input
            id="distortion-slider"
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={distortionLevel}
            onChange={(e) => setDistortionLevel(parseFloat(e.target.value))}
          />
        </div>
        <div className="visualizer-section">
          <h2>Echoed Text:</h2>
          <EchoVisualizer text={inputText} distortionLevel={distortionLevel} />
        </div>
      </main>
      <footer>
        <p>&copy; ApocalypsAI Nightly Integrator</p>
      </footer>
    </div>
  );
}

export default App;
