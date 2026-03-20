import React, { useState, useEffect } from 'react';
import TemporalEchoDisplay from './TemporalEchoDisplay';
import './App.css';

function App() {
  const [echoData, setEchoData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate fetching data from an API or another utility
    const fetchEchoes = () => {
      // # Mock rationale: Simulates data fetching for temporal echoes without needing a real backend or complex data generation.
      const mockEchoes = [
        {
          id: 'echo-001',
          timestamp: '2024-07-20T10:00:00Z',
          magnitude: 0.75,
          type: 'Minor Ripple',
          description: 'A slight tremor in the fabric of time.'
        },
        {
          id: 'echo-002',
          timestamp: '2024-07-20T10:15:30Z',
          magnitude: 1.2,
          type: 'Temporal Glitch',
          description: 'A brief, localized distortion detected near Sector Gamma.'
        },
        {
          id: 'echo-003',
          timestamp: '2024-07-20T10:45:10Z',
          magnitude: 0.5,
          type: 'Echo Residue',
          description: 'Lingering energy from a past event.'
        },
        {
          id: 'echo-004',
          timestamp: '2024-07-20T11:05:00Z',
          magnitude: 2.1,
          type: 'Major Anomaly',
          description: 'Significant temporal displacement detected. Investigate!'
        }
      ];
      return new Promise(resolve => {
        setTimeout(() => {
          resolve(mockEchoes);
        }, 500); // Simulate network delay
      });
    };

    fetchEchoes().then(data => {
      setEchoData(data);
      setLoading(false);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Visualizer</h1>
        <p>Observing the ripples of spacetime.</p>
      </header>
      <main>
        {loading ? (
          <p>Loading temporal echoes...</p>
        ) : echoData.length > 0 ? (
          <TemporalEchoDisplay echoes={echoData} />
        ) : (
          <p>No temporal echoes detected at this time.</p>
        )}
      </main>
      <footer className="App-footer">
        <p>&copy; ApocalypsAI Nightly Integrator</p>
      </footer>
    </div>
  );
}

export default App;
