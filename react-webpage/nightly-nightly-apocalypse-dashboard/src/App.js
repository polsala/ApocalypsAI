import React, { useState, useEffect } from 'react';
import './App.css';

// Mock data generation functions
const generateResourceData = () => {
  const resources = ['Water', 'Food', 'Medicine', 'Fuel'];
  return resources.map(res => ({ name: res, value: Math.floor(Math.random() * 100) }));
};

const generateThreatLevel = () => {
  const levels = ['Low', 'Medium', 'High', 'Critical'];
  return levels[Math.floor(Math.random() * levels.length)];
};

const generateSafeZones = () => {
  const zones = [
    { name: 'Haven Alpha', population: Math.floor(Math.random() * 5000) },
    { name: 'Sanctuary Beta', population: Math.floor(Math.random() * 3000) },
    { name: 'Oasis Gamma', population: Math.floor(Math.random() * 7000) },
  ];
  return zones;
};

const generateVoidWhispers = () => {
  const whispers = [
    "The stars are aligning, or perhaps they are falling.",
    "Echoes of what was, whispers of what will be.",
    "The silence speaks volumes, if only you could hear.",
    "Beware the shadows, for they hold forgotten truths.",
    "The veil thins, revealing the cracks in reality."
  ];
  return whispers[Math.floor(Math.random() * whispers.length)];
};

function App() {
  const [resources, setResources] = useState([]);
  const [threatLevel, setThreatLevel] = useState('');
  const [safeZones, setSafeZones] = useState([]);
  const [voidWhispers, setVoidWhispers] = useState([]);

  useEffect(() => {
    const updateDashboard = () => {
      setResources(generateResourceData());
      setThreatLevel(generateThreatLevel());
      setSafeZones(generateSafeZones());
      setVoidWhispers(Array.from({ length: 5 }, () => generateVoidWhispers()));
    };

    updateDashboard(); // Initial data load
    const intervalId = setInterval(updateDashboard, 15000); // Update every 15 seconds

    return () => clearInterval(intervalId); // Cleanup on unmount
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Apocalypse Dashboard</h1>
        <p>Your real-time (simulated) status report from the end of days.</p>
      </header>
      <main>
        <section className="dashboard-section">
          <h2>Resource Availability</h2>
          <div className="resource-grid">
            {resources.map((res, index) => (
              <div key={index} className="resource-item">
                <h3>{res.name}</h3>
                <div className="progress-bar-container">
                  <div className="progress-bar" style={{ width: `${res.value}%` }}></div>
                </div>
                <p>{res.value}%</p>
              </div>
            ))}
          </div>
        </section>

        <section className="dashboard-section">
          <h2>Global Threat Level</h2>
          <p className={`threat-level ${threatLevel.toLowerCase()}`}>{threatLevel}</p>
        </section>

        <section className="dashboard-section">
          <h2>Safe Zone Status</h2>
          <div className="safe-zone-list">
            {safeZones.map((zone, index) => (
              <div key={index} className="safe-zone-item">
                <h3>{zone.name}</h3>
                <p>Population: {zone.population.toLocaleString()}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="dashboard-section">
          <h2>Whispers of the Void</h2>
          <div className="void-whispers-feed">
            {voidWhispers.map((whisper, index) => (
              <p key={index}>- {whisper}</p>
            ))}
          </div>
        </section>
      </main>
      <footer>
        <p>&copy; 2023 ApocalypsAI - Stay vigilant.</p>
      </footer>
    </div>
  );
}

export default App;
