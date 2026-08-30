import React, { useState } from 'react';
import './App.css';
import EchoMap from './EchoMap';
import { detectEcho } from './EchoDetector';

const GRID_SIZE = 10;

function App() {
  const [echoes, setEchoes] = useState([]);

  const handleMapClick = (x, y) => {
    const newEcho = detectEcho(x, y);
    // Check if an echo already exists at this exact spot (by id or coords)
    const existingEchoIndex = echoes.findIndex(e => e.id === newEcho.id);

    if (existingEchoIndex > -1) {
      // Update existing echo
      setEchoes(prevEchoes => {
        const updatedEchoes = [...prevEchoes];
        updatedEchoes[existingEchoIndex] = { ...newEcho, x, y };
        return updatedEchoes;
      });
    } else {
      // Add new echo
      setEchoes(prevEchoes => [...prevEchoes, { ...newEcho, x, y }]);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo-Location Visualizer</h1>
        <p>Click on the grid to ping for temporal anomalies.</p>
      </header>
      <main>
        <EchoMap gridSize={GRID_SIZE} echoes={echoes} onMapClick={handleMapClick} />
        <div className="legend">
          <h2>Legend</h2>
          <ul>
            <li><span className="legend-color temporal-rift"></span> Temporal Rift (High Strength)</li>
            <li><span className="legend-color echo-chamber"></span> Echo Chamber (Medium-High Strength)</li>
            <li><span className="legend-color time-warp"></span> Time Warp (Medium Strength)</li>
            <li><span className="legend-color stable-zone"></span> Stable Zone (Low Strength / Ambient)</li>
          </ul>
        </div>
      </main>
    </div>
  );
}

export default App;
