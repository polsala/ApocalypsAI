import React, { useState } from 'react';
import AnomalyMap from './AnomalyMap';
import AnomalyDetails from './AnomalyDetails';
import mockAnomalies from './data/mockAnomalies';
import './App.css';

function App() {
  const [selectedAnomaly, setSelectedAnomaly] = useState(null);

  const handleSelectAnomaly = (anomaly) => {
    setSelectedAnomaly(anomaly);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Chrono-Drift Visualizer</h1>
        <p>Tracking temporal anomalies across the wasteland.</p>
      </header>
      <AnomalyMap anomalies={mockAnomalies} onSelectAnomaly={handleSelectAnomaly} />
      <AnomalyDetails anomaly={selectedAnomaly} />
    </div>
  );
}

export default App;
