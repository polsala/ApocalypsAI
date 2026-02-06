import React, { useState } from 'react';
import './App.css';

const echoes = [
  { id: 1, name: 'Whispering Winds', date: '2024-01-15', description: 'A faint echo of voices carried by the wind.' },
  { id: 2, name: 'Shattered Clocktower', date: '2024-03-22', description: 'Time fractures near the ruins of the old clocktower.' },
  { id: 3, name: 'Void Bloom', date: '2024-05-30', description: 'A mysterious bloom that distorts nearby echoes.' },
];

function App() {
  const [selectedEcho, setSelectedEcho] = useState(null);
  const [isSimulating, setIsSimulating] = useState(false);

  const handleEchoClick = (echo) => {
    setSelectedEcho(echo);
  };

  const simulateEcho = () => {
    setIsSimulating(true);
    setTimeout(() => setIsSimulating(false), 2000);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Explorer</h1>
        <button onClick={simulateEcho} disabled={isSimulating}>
          {isSimulating ? 'Simulating...' : 'Simulate Echo Propagation'}
        </button>
      </header>
      <div className="timeline">
        {echoes.map(echo => (
          <div 
            key={echo.id} 
            className={`echo-event ${selectedEcho?.id === echo.id ? 'selected' : ''}`}
            onClick={() => handleEchoClick(echo)}
          >
            <div className="echo-date">{echo.date}</div>
            <div className="echo-name">{echo.name}</div>
          </div>
        ))}
      </div>
      {selectedEcho && (
        <div className="echo-detail">
          <h2>{selectedEcho.name}</h2>
          <p><strong>Date:</strong> {selectedEcho.date}</p>
          <p>{selectedEcho.description}</p>
        </div>
      )}
      {isSimulating && (
        <div className="simulation-overlay">
          <div className="pulse-circle"></div>
          <p>Echo propagation in progress...</p>
        </div>
      )}
    </div>
  );
}

export default App;
