import React, { useState } from 'react';
import './App.css';
import TemporalInput from './components/TemporalInput';
import EchoVisualizer from './components/EchoVisualizer';

// Simple string hash function (DJB2)
const hashString = (str) => {
  let hash = 5381;
  let i = str.length;
  while (i) {
    hash = (hash * 33) ^ str.charCodeAt(--i);
  }
  return hash >>> 0; // Ensure positive 32-bit integer
};

// Simple Linear Congruential Generator (LCG)
const createPseudoRandomGenerator = (seed) => {
  let currentSeed = seed;
  const a = 1103515245;
  const c = 12345;
  const m = Math.pow(2, 31); // Modulus

  return () => {
    currentSeed = (a * currentSeed + c) % m;
    return currentSeed / m; // Number between 0 and 1
  };
};

const generateEchoData = (coordinate) => {
  if (!coordinate) return [];
  const seed = hashString(coordinate);
  const prng = createPseudoRandomGenerator(seed);
  const echoCount = 10; // Number of echo segments
  const data = [];
  for (let i = 0; i < echoCount; i++) {
    data.push(Math.floor(prng() * 100) / 100); // Two decimal places for strength
  }
  return data;
};

function App() {
  const [temporalCoordinate, setTemporalCoordinate] = useState('');
  const [echoData, setEchoData] = useState([]);

  const handleCoordinateSubmit = (coordinate) => {
    setTemporalCoordinate(coordinate);
    setEchoData(generateEchoData(coordinate));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Visualizer</h1>
        <p>Unveil the ripples of time with a single coordinate.</p>
      </header>
      <main>
        <TemporalInput onCoordinateSubmit={handleCoordinateSubmit} />
        {echoData.length > 0 && (
          <div className="echo-display">
            <h2>Echoes from: "{temporalCoordinate}"</h2>
            <EchoVisualizer echoData={echoData} />
          </div>
        )}
        {echoData.length === 0 && temporalCoordinate && (
          <p className="no-echo">No echoes detected for empty coordinate. Please enter a value.</p>
        )}
      </main>
    </div>
  );
}

export default App;
