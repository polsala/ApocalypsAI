import React, { useState, useEffect } from 'react';
import Timeline from './components/Timeline';
import './App.css';

function App() {
  const [echoes, setEchoes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // # Mock rationale: Simulate fetching temporal echo data from an API or database.
    // In a real scenario, this would be an async call. For deterministic testing
    // and self-containment, we use a hardcoded array and a simulated delay.
    const fetchEchoes = () => {
      return new Promise(resolve => {
        setTimeout(() => {
          resolve([
            { id: 'e1', date: '2023-01-15T10:00:00Z', title: 'Utility Genesis: Nightly-Silly-Commit-Message-Generat', description: 'First whimsical utility created.', type: 'creation' },
            { id: 'e2', date: '2023-03-22T14:30:00Z', title: 'Temporal Anomaly Detected', description: 'Minor time-space distortion near sector Gamma-7.', type: 'anomaly' },
            { id: 'e3', date: '2023-05-01T08:00:00Z', title: 'Community Milestone: 100 Utilities', description: 'The repository reached 100 unique utilities.', type: 'milestone' },
            { id: 'e4', date: '2023-07-04T11:00:00Z', title: 'Agent Self-Correction Event', description: 'Integrator agent refactored its own utility generation logic.', type: 'agent-event' },
            { id: 'e5', date: '2023-09-10T16:45:00Z', title: 'Whisperwind Cipher Decrypted', description: 'A complex message from the void was successfully decoded.', type: 'decryption' },
            { id: 'e6', date: '2023-11-20T09:15:00Z', title: 'New Classifier Path Introduced: react-webpage', description: 'The ApocalypsAI system expanded its utility classification.', type: 'system-update' },
            { id: 'e7', date: '2024-01-05T13:00:00Z', title: 'Simulated Future Echo: Resource Scarcity Warning', description: 'Predictive model indicates potential resource strain in Q3 2024.', type: 'prediction' }
          ].sort((a, b) => new Date(a.date) - new Date(b.date)));
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
        <p>Glimpses into the past, present, and simulated future of ApocalypsAI.</p>
      </header>
      <main>
        {loading ? (
          <p>Loading temporal echoes...</p>
        ) : (
          <Timeline echoes={echoes} />
        )}
      </main>
    </div>
  );
}

export default App;
