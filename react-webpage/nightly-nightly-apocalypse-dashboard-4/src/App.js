import React, { useState, useEffect } from 'react';
import './App.css';
import UtilityCard from './components/UtilityCard';

// Mock data for utilities and their statuses
const mockUtilities = [
  {
    name: "nightly-shelter-sentry-log",
    classifier: "python-utils",
    status: "Operational",
    readiness: 0.95
  },
  {
    name: "nightly-simulated-weather-forecast",
    classifier: "python-utils",
    status: "Stable",
    readiness: 0.88
  },
  {
    name: "nightly-survival-cache-checksum-veri",
    classifier: "data-scripts",
    status: "Nominal",
    readiness: 0.92
  },
  {
    name: "nightly-temporal-anomaly-detector",
    classifier: "monitoring-scripts",
    status: "Active",
    readiness: 0.75
  },
  {
    name: "nightly-wasteland-resource-tracker",
    classifier: "data-scripts",
    status: "Fluctuating",
    readiness: 0.60
  },
  {
    name: "nightly-whimsical-emoji-clock",
    classifier: "js-utils",
    status: "Charming",
    readiness: 0.99
  },
  {
    name: "nightly-whisperwind-cipher",
    classifier: "rust-utils",
    status: "Encrypted",
    readiness: 0.85
  },
  {
    name: "nightly-workflow-sanity-checker",
    classifier: "ci-cd-pipelines",
    status: "Vigilant",
    readiness: 0.90
  }
];

function App() {
  const [utilities, setUtilities] = useState([]);

  useEffect(() => {
    // In a real app, this would fetch data from an API.
    // For this standalone utility, we use mock data.
    setUtilities(mockUtilities);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Utility Status Dashboard</h1>
        <p>Monitoring the readiness of our finest post-apocalyptic tools!</p>
      </header>
      <main className="App-main">
        <div className="utility-grid">
          {utilities.map((util, index) => (
            <UtilityCard key={index} utility={util} />
          ))}
        </div>
      </main>
      <footer className="App-footer">
        <p>&copy; 2023 ApocalypsAI Collective. All rights reserved (for now).</p>
      </footer>
    </div>
  );
}

export default App;
