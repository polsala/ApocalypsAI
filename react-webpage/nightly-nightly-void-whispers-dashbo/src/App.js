import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [anomalies, setAnomalies] = useState([]);
  const [metrics, setMetrics] = useState({});
  const [whispers, setWhispers] = useState([]);

  useEffect(() => {
    // Mock data initialization
    setAnomalies([
      { id: 1, type: 'Temporal Rift', severity: 'High', location: 'Sector 7' },
      { id: 2, type: 'Echo Chamber', severity: 'Medium', location: 'Zone 3' }
    ]);

    setMetrics({
      survivalRate: 92,
      resourceLevel: 78,
      stabilityIndex: 85
    });

    setWhispers([
      { id: 1, message: 'The void hums with forgotten echoes.', sentiment: 'neutral' },
      { id: 2, message: 'Time bends near the ancient ruins.', sentiment: 'caution' }
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>.Void Whispers Dashboard</h1>
      </header>
      <main>
        <section>
          <h2>Current Anomalies</h2>
          <ul>
            {anomalies.map(a => (
              <li key={a.id}>{a.type} ({a.severity}) at {a.location}</li>
            ))}
          </ul>
        </section>
        <section>
          <h2>Survival Metrics</h2>
          <p>Survival Rate: {metrics.survivalRate}%</p>
          <p>Resource Level: {metrics.resourceLevel}%</p>
          <p>Stability Index: {metrics.stabilityIndex}/100</p>
        </section>
        <section>
          <h2>Void Whispers</h2>
          <ul>
            {whispers.map(w => (
              <li key={w.id} className={w.sentiment}>{w.message}</li>
            ))}
          </ul>
        </section>
      </main>
    </div>
  );
}

export default App;
