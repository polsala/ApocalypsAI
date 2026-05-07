import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [agentStatus, setAgentStatus] = useState({});
  const [utilityCounts, setUtilityCounts] = useState({});
  const [workflowHealth, setWorkflowHealth] = useState('stable');
  const [resourceScarcity, setResourceScarcity] = useState(30);

  // Mock data fetching for demonstration
  useEffect(() => {
    const mockDataInterval = setInterval(() => {
      setAgentStatus({
        integrator: Math.random() > 0.1 ? 'active' : 'idle',
        builder: Math.random() > 0.2 ? 'active' : 'idle',
        guardian: Math.random() > 0.15 ? 'active' : 'idle',
      });
      setUtilityCounts({
        'python-utils': Math.floor(Math.random() * 500) + 100,
        'react-webpage': Math.floor(Math.random() * 50) + 10,
        'rust-utils': Math.floor(Math.random() * 200) + 50,
        'bash-utils': Math.floor(Math.random() * 300) + 75,
      });
      const healthStates = ['stable', 'warning', 'critical'];
      setWorkflowHealth(healthStates[Math.floor(Math.random() * healthStates.length)]);
      setResourceScarcity(Math.max(0, Math.min(100, resourceScarcity + (Math.random() - 0.5) * 10)));
    }, 5000);

    return () => clearInterval(mockDataInterval);
  }, [resourceScarcity]);

  const getWorkflowIndicatorClass = (health) => {
    switch (health) {
      case 'stable': return 'indicator-stable';
      case 'warning': return 'indicator-warning';
      case 'critical': return 'indicator-critical';
      default: return '';
    }
  };

  const getResourceMeterStyle = (scarcity) => ({
    width: `${scarcity}%`
  });

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Status Dashboard</h1>
      </header>
      <main className="dashboard-grid">
        <section className="card agent-status">
          <h2>Agent Status</h2>
          <ul>
            {Object.entries(agentStatus).map(([agent, status]) => (
              <li key={agent}>
                <strong>{agent.charAt(0).toUpperCase() + agent.slice(1)}</strong>: 
                <span className={`status-${status}`}>{status}</span>
              </li>
            ))}
          </ul>
        </section>

        <section className="card utility-counts">
          <h2>Utility Counts by Classifier</h2>
          <ul>
            {Object.entries(utilityCounts).map(([classifier, count]) => (
              <li key={classifier}>
                <strong>{classifier}</strong>: {count}
              </li>
            ))}
          </ul>
        </section>

        <section className="card workflow-health">
          <h2>Workflow Health</h2>
          <div className={`workflow-indicator ${getWorkflowIndicatorClass(workflowHealth)}`}>
            {workflowHealth.toUpperCase()}
          </div>
        </section>

        <section className="card resource-scarcity">
          <h2>Resource Scarcity Meter</h2>
          <div className="meter-container">
            <div className="meter-bar" style={getResourceMeterStyle(resourceScarcity)}>
              {Math.round(resourceScarcity)}%
            </div>
          </div>
          <p>Low scarcity is good, high scarcity means we're running low on vital resources!</p>
        </section>
      </main>
    </div>
  );
}

export default App;
