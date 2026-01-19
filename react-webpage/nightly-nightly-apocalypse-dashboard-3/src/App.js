import React, { useState, useEffect } from 'react';
import './App.css';

// Mock data generation functions (replace with actual API calls if needed)
const generateRandomResource = () => Math.floor(Math.random() * 100) + 1;
const generateThreatLevel = () => Math.floor(Math.random() * 5) + 1;
const generateSurvivorCount = () => Math.floor(Math.random() * 10000) + 100;
const generateTemporalAnomaly = () => Math.floor(Math.random() * 10) + 1;

function App() {
  const [resources, setResources] = useState({ beans: 0, water: 0 });
  const [threatLevel, setThreatLevel] = useState(0);
  const [survivors, setSurvivors] = useState(0);
  const [temporalAnomaly, setTemporalAnomaly] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setResources({
        beans: generateRandomResource(),
        water: generateRandomResource()
      });
      setThreatLevel(generateThreatLevel());
      setSurvivors(generateSurvivorCount());
      setTemporalAnomaly(generateTemporalAnomaly());
    }, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Apocalypse Dashboard</h1>
      </header>
      <main>
        <section className="dashboard-section">
          <h2>Resource Status</h2>
          <p>Canned Beans: {resources.beans}%</p>
          <p>Clean Water: {resources.water}%</p>
        </section>
        <section className="dashboard-section">
          <h2>Threat Level</h2>
          <p>Current Threat: {threatLevel}/5 (Critical)</p>
        </section>
        <section className="dashboard-section">
          <h2>Survivor Count</h2>
          <p>Brave Souls Remaining: {survivors}</p>
        </section>
        <section className="dashboard-section">
          <h2>Temporal Stability</h2>
          <p>Anomaly Gauge: {temporalAnomaly}/10 (Unstable)</p>
        </section>
      </main>
    </div>
  );
}

export default App;
