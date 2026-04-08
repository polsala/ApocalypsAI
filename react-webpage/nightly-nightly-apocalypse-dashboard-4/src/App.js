import React, { useState, useEffect } from 'react';
import './App.css';

// Mock data for utilities and agent activity
const mockUtilities = [
  { id: 1, name: 'nightly-survival-snack-sorter', classifier: 'python-utils', summary: 'Sorts survival snacks based on shelf-life.' },
  { id: 2, name: 'nightly-temporal-drift-detector', classifier: 'rust-utils', summary: 'Detects temporal drift in the spacetime continuum.' },
  { id: 3, name: 'nightly-wasteland-resource-tracker', classifier: 'bash-utils', summary: 'Tracks essential resources in the wasteland.' },
  { id: 4, name: 'nightly-whimsical-emoji-clock', classifier: 'js-utils', summary: 'A clock that displays time using whimsical emojis.' },
  { id: 5, name: 'nightly-whisperwind-cipher', classifier: 'cli-apps', summary: 'A command-line tool for encrypting whisperwind messages.' },
];

const mockAgentActivity = [
  { id: 101, agent: 'Integrator', action: 'Generated new utility: nightly-apocalypse-dashboard', timestamp: '2023-10-27T10:00:00Z' },
  { id: 102, agent: 'Builder', action: 'Created a new issue for "Temporal Anomaly Stabilizer"', timestamp: '2023-10-27T10:05:00Z' },
  { id: 103, agent: 'Guardian', action: 'Triage complete for "Suspicious Commit Message"', timestamp: '2023-10-27T10:10:00Z' },
  { id: 104, agent: 'Integrator', action: 'Refactored nightly-silly-username-generator', timestamp: '2023-10-27T10:15:00Z' },
];

const mockTemporalAnomalies = [
  { id: 201, type: 'Minor Flux', severity: 'Low', status: 'Stable', time: '2023-10-27T09:55:00Z' },
  { id: 202, type: 'Echo Chamber', severity: 'Medium', status: 'Monitoring', time: '2023-10-27T10:02:00Z' },
];

function App() {
  const [utilities, setUtilities] = useState([]);
  const [agentActivity, setAgentActivity] = useState([]);
  const [temporalAnomalies, setTemporalAnomalies] = useState([]);

  useEffect(() => {
    // Simulate fetching data
    setUtilities(mockUtilities);
    setAgentActivity(mockAgentActivity);
    setTemporalAnomalies(mockTemporalAnomalies);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Command Center</h1>
        <p>Your whimsical overview of the digital apocalypse.</p>
      </header>
      <main>
        <section className="dashboard-section">
          <h2>Recently Generated Utilities</h2>
          <ul className="utility-list">
            {utilities.map(util => (
              <li key={util.id} className="utility-item">
                <h3>{util.name}</h3>
                <p><strong>Classifier:</strong> {util.classifier}</p>
                <p>{util.summary}</p>
              </li>
            ))}
          </ul>
        </section>

        <section className="dashboard-section">
          <h2>Agent Activity Feed</h2>
          <ul className="activity-list">
            {agentActivity.map(activity => (
              <li key={activity.id} className="activity-item">
                <span className="agent-name">[{activity.agent}]</span> {activity.action}
                <span className="timestamp"> - {new Date(activity.timestamp).toLocaleTimeString()}</span>
              </li>
            ))}
          </ul>
        </section>

        <section className="dashboard-section">
          <h2>Temporal Anomaly Watch</h2>
          <div className="anomaly-grid">
            {temporalAnomalies.map(anomaly => (
              <div key={anomaly.id} className={`anomaly-card ${anomaly.status.toLowerCase()}`}>
                <h3>{anomaly.type}</h3>
                <p><strong>Severity:</strong> {anomaly.severity}</p>
                <p><strong>Status:</strong> {anomaly.status}</p>
                <p><em>{new Date(anomaly.time).toLocaleString()}</em></p>
              </div>
            ))}
          </div>
        </section>
      </main>
      <footer>
        <p>&copy; 2023 ApocalypsAI - Keeping the digital world whimsically intact.</p>
      </footer>
    </div>
  );
}

export default App;
