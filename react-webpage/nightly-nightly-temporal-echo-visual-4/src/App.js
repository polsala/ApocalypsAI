import React, { useState, useEffect } from 'react';
import EchoTimeline from './components/EchoTimeline';
import mockEchoes from './data/mockEchoes';
import './App.css';

function App() {
  const [echoes, setEchoes] = useState([]);
  const [selectedEcho, setSelectedEcho] = useState(null);

  useEffect(() => {
    // In a real scenario, this would fetch from an API.
    // For this utility, we load mock data directly.
    setEchoes(mockEchoes);
  }, []);

  const handleSelectEcho = (echo) => {
    setSelectedEcho(echo);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Temporal Echo Visualizer</h1>
      </header>
      <main>
        <section className="timeline-section">
          <h2>Temporal Echo Timeline</h2>
          <EchoTimeline echoes={echoes} onSelectEcho={handleSelectEcho} />
        </section>
        <section className="details-section">
          <h2>Selected Echo Details</h2>
          {selectedEcho ? (
            <div className="echo-details-card">
              <h3>{selectedEcho.type}</h3>
              <p><strong>Timestamp:</strong> {new Date(selectedEcho.timestamp).toLocaleString()}</p>
              <p><strong>Magnitude:</strong> {selectedEcho.magnitude}</p>
              <p><strong>Location:</strong> {selectedEcho.location}</p>
              <p><strong>Description:</strong> {selectedEcho.description}</p>
            </div>
          ) : (
            <p>Select an echo from the timeline to view its details.</p>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
