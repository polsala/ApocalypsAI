import React, { useState, useEffect } from 'react';
import AnomalyDashboard from './components/AnomalyDashboard';
import mockTemporalData from './api/mockTemporalData'; // Mock rationale: Using local mock data for offline functionality and deterministic testing.
import './App.css';

function App() {
  const [anomalies, setAnomalies] = useState([]);

  useEffect(() => {
    // In a real scenario, this would fetch data from an API.
    // For this utility, we use mock data.
    setAnomalies(mockTemporalData);
  }, []);

  const handleStabilize = (id) => {
    setAnomalies((prevAnomalies) =>
      prevAnomalies.map((anomaly) =>
        anomaly.id === id ? { ...anomaly, status: 'stabilized' } : anomaly
      )
    );
  };

  const activeAnomalies = anomalies.filter(a => a.status === 'active');
  const stabilizedAnomalies = anomalies.filter(a => a.status === 'stabilized');

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Temporal Ripple Viewer</h1>
        <p>Monitoring the fabric of space-time for anomalies.</p>
      </header>
      <main>
        <AnomalyDashboard
          title="Active Temporal Ripples"
          anomalies={activeAnomalies}
          onStabilize={handleStabilize}
        />
        <AnomalyDashboard
          title="Stabilized Anomalies"
          anomalies={stabilizedAnomalies}
          onStabilize={handleStabilize} // Still allow re-stabilizing if needed, or disable button
          readOnly={true}
        />
      </main>
    </div>
  );
}

export default App;
