import React, { useState, useEffect } from 'react';
import './App.css';
import EchoMap from './components/EchoMap';
import EchoDisplay from './components/EchoDisplay';
import { mockEchoData } from './data/mockEchoData';

function App() {
  const [echoes, setEchoes] = useState([]);
  const [selectedEcho, setSelectedEcho] = useState(null);

  useEffect(() => {
    // In a real scenario, this would fetch data from an API.
    // For this utility, we use mock data.
    setEchoes(mockEchoData);
  }, []);

  const handleEchoSelect = (echo) => {
    setSelectedEcho(echo);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Visualization</h1>
        <p>Unveiling the whispers of the past, one shimmer at a time.</p>
      </header>
      <main className="App-main">
        <div className="map-container">
          <EchoMap echoes={echoes} onEchoSelect={handleEchoSelect} />
        </div>
        <div className="sidebar">
          <EchoDisplay selectedEcho={selectedEcho} />
        </div>
      </main>
    </div>
  );
}

export default App;
