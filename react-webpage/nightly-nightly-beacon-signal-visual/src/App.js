import React, { useState, useCallback } from 'react';
import SignalVisualizer from './SignalVisualizer';
import './App.css';

function App() {
  const [signalText, setSignalText] = useState('');

  const generateSignalData = useCallback((text) => {
    if (!text) {
      return null;
    }
    // Simple deterministic hash for visualization parameters
    const seed = text.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);

    const numRings = (seed % 5) + 3; // 3 to 7 rings
    const hueStart = seed % 360;
    const hueEnd = (seed * 2) % 360;
    const rotationSpeed = (seed % 3) + 1; // 1 to 3 units/sec
    const flickerIntensity = (seed % 5) / 10 + 0.1; // 0.1 to 0.5
    const ringThickness = (seed % 3) + 1; // 1 to 3 pixels

    return {
      numRings,
      hueStart,
      hueEnd,
      rotationSpeed,
      flickerIntensity,
      ringThickness
    };
  }, []);

  const signalData = generateSignalData(signalText);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Beacon Signal Visualizer</h1>
        <p>Enter your beacon signal below:</p>
        <input
          type="text"
          value={signalText}
          onChange={(e) => setSignalText(e.target.value)}
          placeholder="Type your signal here..."
          className="signal-input"
          aria-label="Beacon Signal Input"
        />
      </header>
      <main className="App-main">
        {signalData ? (
          <SignalVisualizer data={signalData} />
        ) : (
          <p className="placeholder-text">Your signal will appear here...</p>
        )}
      </main>
    </div>
  );
}

export default App;
