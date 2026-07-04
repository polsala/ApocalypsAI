import React, { useState, useEffect } from 'react';
import './App.css';
import EchoTimeline from './EchoTimeline';
import sampleEchoes from './data/sample-echoes.json'; // Local data for simplicity

function App() {
  const [echoes, setEchoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // In a real application, this would be an API call.
    // For this utility, we load local sample data.
    try {
      setEchoes(sampleEchoes);
      setLoading(false);
    } catch (e) {
      setError("Failed to load temporal echoes.");
      setLoading(false);
    }
  }, []);

  if (loading) {
    return <div className="App">Loading temporal echoes...</div>;
  }

  if (error) {
    return <div className="App error">{error}</div>;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Temporal Echo Visualizer</h1>
        <p>Observing the ripples in spacetime.</p>
      </header>
      <main>
        {echoes.length > 0 ? (
          <EchoTimeline echoes={echoes} />
        ) : (
          <p>No temporal echoes detected. All clear... for now.</p>
        )}
      </main>
      <footer className="App-footer">
        <p>&copy; ApocalypsAI Integrator Agent</p>
      </footer>
    </div>
  );
}

export default App;
