import React, { useState } from 'react';
import './App.css';
import { mockEchoes } from './data/mockEchoes';
import EchoDisplay from './components/EchoDisplay';

function App() {
  const [selectedEcho, setSelectedEcho] = useState(null);

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Temporal Echo Visualizer</h1>
        <p>Exploring the ripples in spacetime...</p>
      </header>
      <main className="App-main">
        <div className="echo-grid">
          {mockEchoes.map(echo => (
            <EchoDisplay
              key={echo.id}
              echo={echo}
              onSelect={setSelectedEcho}
              isSelected={selectedEcho && selectedEcho.id === echo.id}
            />
          ))}
        </div>
        <div className="echo-details">
          {selectedEcho ? (
            <div className="details-card">
              <h2>Echo Details</h2>
              <p><strong>ID:</strong> {selectedEcho.id}</p>
              <p><strong>Timestamp:</strong> {new Date(selectedEcho.timestamp).toLocaleString()}</p>
              <p><strong>Location:</strong> {selectedEcho.location}</p>
              <p><strong>Severity:</strong> <span className={`severity-${selectedEcho.severity.toLowerCase()}`}>{selectedEcho.severity}</span></p>
              <p><strong>Type:</strong> {selectedEcho.type}</p>
              <p><strong>Description:</strong> {selectedEcho.description}</p>
            </div>
          ) : (
            <p>Select an echo from the grid to see its details.</p>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
