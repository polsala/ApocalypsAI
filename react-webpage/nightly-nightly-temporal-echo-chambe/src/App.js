import React, { useState, useEffect } from 'react';
import AnomalyForm from './components/AnomalyForm';
import AnomalyGraph from './components/AnomalyGraph';
import { loadAnomalies, saveAnomalies } from './data/localStorageService';
import './App.css'; // Import global styles

function App() {
  const [anomalies, setAnomalies] = useState([]);

  // Load anomalies from local storage on initial render
  useEffect(() => {
    setAnomalies(loadAnomalies());
  }, []);

  // Save anomalies to local storage whenever they change
  useEffect(() => {
    saveAnomalies(anomalies);
  }, [anomalies]);

  const handleAddAnomaly = (newAnomaly) => {
    setAnomalies((prevAnomalies) => [...prevAnomalies, newAnomaly]);
  };

  return (
    <div className="App">
      <h1>Temporal Echo Chamber Visualizer</h1>
      <AnomalyForm onAddAnomaly={handleAddAnomaly} />
      <AnomalyGraph anomalies={anomalies} />
    </div>
  );
}

export default App;
