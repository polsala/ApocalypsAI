import React, { useState, useEffect } from 'react';
import AnomalyMap from './AnomalyMap';
import { getAnomalies, stabilizeAnomaly } from './AnomalyData';
import './App.css';

function App() {
  const [anomalies, setAnomalies] = useState([]);

  useEffect(() => {
    // In a real app, this would fetch data from an API
    setAnomalies(getAnomalies());
  }, []);

  const handleStabilize = (id) => {
    // Simulate stabilization
    stabilizeAnomaly(id);
    setAnomalies([...getAnomalies()]); // Re-fetch updated anomalies
    alert(`Anomaly ${id} has been stabilized!`);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Map</h1>
        <p>Visualizing Chronal Disturbances Across the Wasteland</p>
      </header>
      <main>
        <AnomalyMap anomalies={anomalies} onStabilize={handleStabilize} />
        <div className="anomaly-list">
          <h2>Anomaly Log</h2>
          {anomalies.length === 0 ? (
            <p>No anomalies detected. All clear... for now.</p>
          ) : (
            <ul>
              {anomalies.map(anomaly => (
                <li key={anomaly.id} className={anomaly.status.toLowerCase().replace(' ', '-')}>
                  <strong>{anomaly.type}</strong> at {anomaly.location} (Severity: {anomaly.severity}, Status: {anomaly.status})
                </li>
              ))}
            </ul>
          )}
        </div>
      </main>
      <footer>
        <p>&copy; 2077 ApocalypsAI Nightly Integrator</p>
      </footer>
    </div>
  );
}

export default App;
