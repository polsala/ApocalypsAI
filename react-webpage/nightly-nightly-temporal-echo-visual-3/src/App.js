import React, { useState, useEffect } from 'react';
import mockEchoData from './data/mockEchoData';
import './App.css';

function App() {
  const [echoes, setEchoes] = useState([]);

  useEffect(() => {
    // # Mock rationale: Simulates fetching temporal echo data from an API.
    // In a real application, this would be an async call (e.g., fetch('/api/echoes')).
    // Using setTimeout to mimic network latency for demonstration.
    const fetchEchoes = () => {
      return new Promise(resolve => {
        setTimeout(() => {
          resolve(mockEchoData);
        }, 500); // Simulate 500ms network delay
      });
    };

    fetchEchoes().then(data => {
      setEchoes(data);
    });
  }, []);

  const getEchoIcon = (type) => {
    switch (type) {
      case 'Whisper': return '👻';
      case 'Ripple': return '🌊';
      case 'Glitch': return '👾';
      case 'Paradox': return '🌀';
      default: return '❓';
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Visualizer</h1>
        <p>Monitoring the fabric of spacetime for anomalies.</p>
      </header>
      <main className="echo-list-container">
        {echoes.length === 0 ? (
          <p>Scanning for temporal echoes...</p>
        ) : (
          <div className="echo-grid">
            {echoes.map(echo => (
              <div key={echo.id} className={`echo-card echo-type-${echo.type.toLowerCase()}`}>
                <div className="echo-icon">{getEchoIcon(echo.type)}</div>
                <div className="echo-details">
                  <h3>{echo.type} Echo at {echo.location}</h3>
                  <p><strong>Time:</strong> {new Date(echo.timestamp).toLocaleString()}</p>
                  <p><strong>Magnitude:</strong> {echo.magnitude.toFixed(1)}</p>
                  <p>{echo.description}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
      <footer className="App-footer">
        <p>&copy; 2024 ApocalypsAI Nightly Integrator</p>
      </footer>
    </div>
  );
}

export default App;
