import React, { useState } from 'react';
import './App.css';
import EchoVisualizer from './components/EchoVisualizer';

function App() {
  const [temporalCoordinate, setTemporalCoordinate] = useState('');
  const [echoes, setEchoes] = useState([]);

  const generateSimulatedEchoes = (coordinate) => {
    // # Mock rationale: This utility simulates temporal echoes.
    // In a real scenario, this might call an API or a complex temporal
    // analysis engine. For a self-contained, whimsical utility,
    // a deterministic simulation is appropriate.
    const seed = coordinate.length > 0 ? coordinate.charCodeAt(0) : 0;
    const numEchoes = 3 + (seed % 3); // 3 to 5 echoes
    const newEchoes = [];
    for (let i = 0; i < numEchoes; i++) {
      const offset = (i * 50 + (seed * i) % 100) - 100; // Relative offset from coordinate
      const intensity = 0.3 + (seed + i) % 7 / 10; // 0.3 to 1.0
      const distortionTypes = ['Ripple', 'Warp', 'Flicker', 'Phase Shift'];
      const distortionType = distortionTypes[(seed + i) % distortionTypes.length];
      newEchoes.push({
        id: i,
        offset,
        intensity,
        distortionType,
        duration: 20 + (seed + i) % 30 // For visual length
      });
    }
    return newEchoes;
  };

  const handleGenerate = () => {
    const simulatedEchoes = generateSimulatedEchoes(temporalCoordinate);
    setEchoes(simulatedEchoes);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Visualizer</h1>
        <p>Unraveling the ripples of spacetime, whimsically.</p>
      </header>
      <main className="App-main">
        <div className="input-section">
          <label htmlFor="temporal-coordinate">Temporal Coordinate:</label>
          <input
            id="temporal-coordinate"
            type="text"
            value={temporalCoordinate}
            onChange={(e) => setTemporalCoordinate(e.target.value)}
            placeholder="e.g., 'The Great Silence', '2077-10-23'"
          />
          <button onClick={handleGenerate}>Generate Echoes</button>
        </div>
        <EchoVisualizer echoes={echoes} />
      </main>
    </div>
  );
}

export default App;
