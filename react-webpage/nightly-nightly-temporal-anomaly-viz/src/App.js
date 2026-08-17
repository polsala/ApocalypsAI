import React, { useState, useEffect } from 'react';
import AnomalyTimeline from './components/AnomalyTimeline';
import AnomalyCard from './components/AnomalyCard';
import anomaliesData from './data/anomalies.json';
import './App.css';

function App() {
  const [anomalies, setAnomalies] = useState([]);
  const [selectedAnomaly, setSelectedAnomaly] = useState(null);

  useEffect(() => {
    // Simulate fetching data
    setAnomalies(anomaliesData.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp)));
  }, []);

  const handleAnomalySelect = (anomaly) => {
    setSelectedAnomaly(anomaly);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Temporal Anomaly Visualizer</h1>
        <p>Gaze upon the fabric of time, for it is... wiggly.</p>
      </header>
      <main className="App-main">
        <div className="timeline-section">
          <h2>Detected Anomalies</h2>
          {anomalies.length > 0 ? (
            <AnomalyTimeline anomalies={anomalies} onSelectAnomaly={handleAnomalySelect} />
          ) : (
            <p>No temporal anomalies detected. All is calm... for now.</p>
          )}
        </div>
        <div className="details-section">
          <h2>Anomaly Details</h2>
          {selectedAnomaly ? (
            <AnomalyCard anomaly={selectedAnomaly} />
          ) : (
            <p>Select an anomaly from the timeline to view its intricate details.</p>
          )}
        </div>
      </main>
      <footer className="App-footer">
        <p>&copy; ApocalypsAI Integrator. Keeping time... mostly.</p>
      </footer>
    </div>
  );
}

export default App;
