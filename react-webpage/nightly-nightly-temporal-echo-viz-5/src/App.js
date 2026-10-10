import React, { useState, useEffect } from 'react';
import './App.css';
import EchoTimeline from './components/EchoTimeline';
import mockEchoes from './data/mockEchoes'; // Mock rationale: Directly import mock data for deterministic, offline display and testing.

function App() {
  const [echoes, setEchoes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate fetching data, but use mock data directly
    const fetchEchoes = () => {
      return new Promise(resolve => {
        setTimeout(() => {
          resolve(mockEchoes);
        }, 500); // Simulate network delay
      });
    };

    fetchEchoes().then(data => {
      setEchoes(data);
      setLoading(false);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Visualizer</h1>
        <p>Unraveling the fabric of time, one echo at a time.</p>
      </header>
      <main className="App-main">
        {loading ? (
          <p>Calibrating temporal sensors...</p>
        ) : (
          <EchoTimeline echoes={echoes} />
        )}
      </main>
      <footer className="App-footer">
        <p>&copy; ApocalypsAI Nightly Integrator</p>
      </footer>
    </div>
  );
}

export default App;
