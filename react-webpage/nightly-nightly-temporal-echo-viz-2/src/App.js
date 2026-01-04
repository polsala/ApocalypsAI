import React, { useState, useEffect } from 'react';
import TemporalGraph from './components/TemporalGraph';
import mockTemporalData from './data/mockTemporalData';
import './App.css'; // Component-specific styles

function App() {
  const [temporalData, setTemporalData] = useState([]);
  const [stabilityIndex, setStabilityIndex] = useState(100); // Start stable

  useEffect(() => {
    // Simulate fetching or generating new data over time
    const interval = setInterval(() => {
      const newDataPoint = {
        time: new Date().toLocaleTimeString(),
        distortion: Math.random() * 50 + 10, // 10-60
        echoIntensity: Math.random() * 40 + 5, // 5-45
      };

      setTemporalData(prevData => {
        const updatedData = [...prevData, newDataPoint];
        // Keep only the last 20 data points for a rolling window
        return updatedData.slice(-20);
      });

      // Calculate a whimsical stability index
      // Higher distortion/echo means lower stability
      const currentDistortion = newDataPoint.distortion;
      const currentEcho = newDataPoint.echoIntensity;
      const newStability = Math.max(0, 100 - (currentDistortion * 0.8 + currentEcho * 0.5));
      setStabilityIndex(newStability.toFixed(2));

    }, 3000); // Update every 3 seconds

    // Initialize with mock data
    setTemporalData(mockTemporalData);
    const initialStability = mockTemporalData.reduce((acc, curr) => {
      return acc + (100 - (curr.distortion * 0.8 + curr.echoIntensity * 0.5));
    }, 0) / mockTemporalData.length;
    setStabilityIndex(initialStability ? initialStability.toFixed(2) : 100);


    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Visualizer</h1>
        <p className="subtitle">Monitoring the Fabric of Spacetime</p>
      </header>
      <main className="App-main">
        <div className="dashboard-card">
          <h2>Current Temporal Status</h2>
          <div className="status-indicators">
            <div className="indicator">
              <span>Stability Index:</span>
              <span className={`value ${stabilityIndex < 50 ? 'critical' : stabilityIndex < 80 ? 'warning' : 'stable'}`}>
                {stabilityIndex}%
              </span>
            </div>
            <div className="indicator">
              <span>Last Distortion:</span>
              <span className="value">
                {temporalData.length > 0 ? temporalData[temporalData.length - 1].distortion.toFixed(2) : 'N/A'} units
              </span>
            </div>
            <div className="indicator">
              <span>Last Echo:</span>
              <span className="value">
                {temporalData.length > 0 ? temporalData[temporalData.length - 1].echoIntensity.toFixed(2) : 'N/A'} units
              </span>
            </div>
          </div>
        </div>
        <div className="dashboard-card graph-card">
          <h2>Temporal Anomaly Trends</h2>
          {temporalData.length > 0 ? (
            <TemporalGraph data={temporalData} />
          ) : (
            <p>Initializing temporal sensors...</p>
          )}
        </div>
      </main>
      <footer className="App-footer">
        <p>&copy; ApocalypsAI Nightly Integrator - Temporal Division</p>
      </footer>
    </div>
  );
}

export default App;
