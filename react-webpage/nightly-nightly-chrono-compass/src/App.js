import React, { useState, useEffect } from 'react';
import './App.css';

// Mock function to simulate fetching temporal anomalies
export const fetchAnomalies = async () => {
  // Mock rationale: In a real scenario, this would be an API call to a backend
  // service that tracks temporal anomalies. For self-contained utility and
  // deterministic tests, we use static mock data.
  return new Promise(resolve => {
    setTimeout(() => {
      resolve([
        { id: 'TAD-001', type: 'Minor Drift', severity: 'Low', status: 'Unstable' },
        { id: 'TAD-002', type: 'Echo Cascade', severity: 'Medium', status: 'Stabilizing' },
        { id: 'TAD-003', type: 'Rift Tear', severity: 'High', status: 'Unstable' },
        { id: 'TAD-004', type: 'Temporal Ripple', severity: 'Low', status: 'Stabilized' },
        { id: 'TAD-005', type: 'Chronal Flux', severity: 'Medium', status: 'Unstable' },
      ]);
    }, 500); // Simulate network delay
  });
};

function App() {
  const [anomalies, setAnomalies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const getAnomalies = async () => {
      const data = await fetchAnomalies();
      setAnomalies(data);
      setLoading(false);
    };
    getAnomalies();
  }, []);

  const handleStabilizeAll = () => {
    // Mock rationale: In a real scenario, this would trigger an API call
    // to a temporal stabilization service. Here, we simulate the process
    // by updating the local state to 'Stabilizing' or 'Stabilized'.
    setAnomalies(prevAnomalies =>
      prevAnomalies.map(anomaly =>
        anomaly.status === 'Unstable'
          ? { ...anomaly, status: 'Stabilizing' }
          : anomaly
      )
    );
    setTimeout(() => {
      setAnomalies(prevAnomalies =>
        prevAnomalies.map(anomaly =>
          anomaly.status === 'Stabilizing'
            ? { ...anomaly, status: 'Stabilized' }
            : anomaly
        )
      );
    }, 1500); // Simulate stabilization time
  };

  const getStatusClass = (status) => {
    switch (status) {
      case 'Unstable': return 'status-unstable';
      case 'Stabilizing': return 'status-stabilizing';
      case 'Stabilized': return 'status-stabilized';
      default: return '';
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Chrono-Compass 🧭</h1>
        <p>Tracking Temporal Anomalies Across the ApocalypsAI Network</p>
      </header>
      <main className="App-main">
        {loading ? (
          <p>Calibrating temporal sensors...</p>
        ) : (
          <>
            <div className="anomaly-actions">
              <button onClick={handleStabilizeAll} disabled={anomalies.every(a => a.status === 'Stabilized')}>
                Initiate Global Stabilization
              </button>
            </div>
            <div className="anomaly-list">
              {anomalies.length === 0 ? (
                <p>No temporal anomalies detected. All clear!</p>
              ) : (
                anomalies.map(anomaly => (
                  <div key={anomaly.id} className="anomaly-card">
                    <h2>{anomaly.id} - {anomaly.type}</h2>
                    <p>Severity: <strong>{anomaly.severity}</strong></p>
                    <p>Status: <span className={getStatusClass(anomaly.status)}>{anomaly.status}</span></p>
                  </div>
                ))
              )}
            </div>
          </>
        )}
      </main>
      <footer className="App-footer">
        <p>&copy; ApocalypsAI Nightly Integrator</p>
      </footer>
    </div>
  );
}

export default App;
