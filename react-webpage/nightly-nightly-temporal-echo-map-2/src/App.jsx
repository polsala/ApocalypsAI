import React, { useState } from 'react';
import AnomalyMap from './components/AnomalyMap';
import mockAnomalies from './data/mockAnomalies';

const GRID_SIZE = 10; // 10x10 grid

function App() {
  const [anomalies, setAnomalies] = useState(mockAnomalies);
  const [nextId, setNextId] = useState(mockAnomalies.length + 1);

  const simulateNewAnomaly = () => {
    const newAnomaly = {
      id: `anomaly-${nextId}`,
      x: Math.floor(Math.random() * GRID_SIZE),
      y: Math.floor(Math.random() * GRID_SIZE),
      intensity: Math.random() * 100, // 0-100
      type: 'minor-echo',
    };
    setAnomalies((prevAnomalies) => [...prevAnomalies, newAnomaly]);
    setNextId((prevId) => prevId + 1);
  };

  return (
    <div style={{ fontFamily: 'monospace', textAlign: 'center', padding: '20px' }}>
      <h1>Nightly Temporal Echo Map</h1>
      <p>Visualizing chronal instabilities across the grid.</p>
      <button 
        onClick={simulateNewAnomaly} 
        style={{ 
          padding: '10px 20px', 
          fontSize: '16px', 
          cursor: 'pointer', 
          marginBottom: '20px',
          backgroundColor: '#4CAF50',
          color: 'white',
          border: 'none',
          borderRadius: '5px'
        }}
      >
        Simulate New Anomaly
      </button>
      <AnomalyMap anomalies={anomalies} gridSize={GRID_SIZE} />
    </div>
  );
}

export default App;
