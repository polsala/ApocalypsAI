import React, { useState, useEffect } from 'react';
import './App.css';

// Mock data for demonstration purposes
const mockAgentStatus = [
  { id: 1, name: 'Integrator', status: 'active', lastRun: '2023-10-27T10:00:00Z' },
  { id: 2, name: 'Builder', status: 'idle', lastRun: '2023-10-26T23:59:59Z' },
  { id: 3, name: 'Guardian', status: 'active', lastRun: '2023-10-27T09:30:00Z' },
  { id: 4, name: 'Reviewer', status: 'error', lastRun: '2023-10-27T08:00:00Z' },
];

const mockUtilityStats = {
  generatedToday: 15,
  successRate: 92,
  recentTypes: ['python-utils', 'rust-utils', 'react-webpage'],
};

const mockWorkflowHealth = [
  { name: 'gen_openrouter.yml', status: 'success', duration: '5m 30s' },
  { name: 'gen_groq.yml', status: 'success', duration: '4m 15s' },
  { name: 'nightly_self_heal.yml', status: 'warning', duration: '10m 00s' },
  { name: 'deploy-pages.yml', status: 'failed', duration: '2m 00s' },
];

function App() {
  const [agents, setAgents] = useState([]);
  const [utilities, setUtilities] = useState({});
  const [workflows, setWorkflows] = useState([]);

  useEffect(() => {
    // In a real app, this would fetch data from an API
    setAgents(mockAgentStatus);
    setUtilities(mockUtilityStats);
    setWorkflows(mockWorkflowHealth);
  }, []);

  const getStatusClass = (status) => {
    switch (status.toLowerCase()) {
      case 'active': return 'status-active';
      case 'idle': return 'status-idle';
      case 'error': return 'status-error';
      case 'success': return 'status-success';
      case 'warning': return 'status-warning';
      case 'failed': return 'status-failed';
      default: return 'status-unknown';
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Status Dashboard</h1>
        <p>Navigating the digital wasteland, one utility at a time.</p>
      </header>
      <main>
        <section className="dashboard-section">
          <h2>Agent Status</h2>
          <div className="card-container">
            {agents.map(agent => (
              <div key={agent.id} className={`card agent-card ${getStatusClass(agent.status)}`}>
                <h3>{agent.name}</h3>
                <p>Status: <span className="status-badge">{agent.status.toUpperCase()}</span></p>
                <p>Last Run: {new Date(agent.lastRun).toLocaleString()}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="dashboard-section">
          <h2>Utility Generation</h2>
          <div className="card utility-stats-card">
            <h3>Generated Today</h3>
            <p className="large-number">{utilities.generatedToday}</p>
            <h3>Success Rate</h3>
            <p className="large-number">{utilities.successRate}%</p>
            <h3>Recent Types</h3>
            <ul>
              {utilities.recentTypes?.map((type, index) => <li key={index}>{type}</li>)}
            </ul>
          </div>
        </section>

        <section className="dashboard-section">
          <h2>Workflow Health</h2>
          <div className="card-container">
            {workflows.map((workflow, index) => (
              <div key={index} className={`card workflow-card ${getStatusClass(workflow.status)}`}>
                <h3>{workflow.name}</h3>
                <p>Status: <span className="status-badge">{workflow.status.toUpperCase()}</span></p>
                <p>Duration: {workflow.duration}</p>
              </div>
            ))}
          </div>
        </section>
      </main>
      <footer>
        <p>&copy; 2023 ApocalypsAI. All rights reserved (mostly).</p>
      </footer>
    </div>
  );
}

export default App;
