import React, { useState, useEffect } from 'react';
import './App.css';

// Mock data for demonstration purposes
const mockAgentData = [
  { id: 1, name: 'Builder Bot', status: 'active', color: '#4CAF50' },
  { id: 2, name: 'Guardian Golem', status: 'idle', color: '#FFC107' },
  { id: 3, name: 'Integrator Imp', status: 'active', color: '#2196F3' },
  { id: 4, name: 'Reviewer Raven', status: 'error', color: '#F44336' },
];

const mockUtilityData = {
  totalGenerated: 150,
  last24h: 5,
  types: ['python-utils', 'react-webpage', 'bash-utils'],
};

const mockWorkflowData = {
  health: 'good',
  lastRun: '2023-10-27T10:00:00Z',
};

const mockCommunityData = {
  openIssues: 15,
  openPRs: 8,
  recentActivity: 'New utility added!',
};

function AgentStatus({ agent }) {
  const statusStyle = {
    backgroundColor: agent.color,
    animation: agent.status === 'active' ? 'pulse 2s infinite' : 'none',
  };

  return (
    <div className="agent-status-item">
      <div className="agent-status-dot" style={statusStyle}></div>
      <span className="agent-name">{agent.name}</span>
      <span className="agent-status-text">({agent.status})</span>
    </div>
  );
}

function UtilityTracker({ data }) {
  return (
    <div className="dashboard-card">
      <h3>Utility Generation</h3>
      <p>Total Generated: <strong>{data.totalGenerated}</strong></p>
      <p>Last 24 Hours: <strong>{data.last24h}</strong></p>
      <p>Recent Types: {data.types.join(', ')}</p>
    </div>
  );
}

function WorkflowMonitor({ data }) {
  const workflowHealthClass = `workflow-health-${data.health}`;
  return (
    <div className="dashboard-card">
      <h3>Workflow Health</h3>
      <p className={workflowHealthClass}>Status: <strong>{data.health.toUpperCase()}</strong></p>
      <p>Last Run: {new Date(data.lastRun).toLocaleString()}</p>
    </div>
  );
}

function CommunitySnapshot({ data }) {
  return (
    <div className="dashboard-card">
      <h3>Community Engagement</h3>
      <p>Open Issues: <strong>{data.openIssues}</strong></p>
      <p>Open PRs: <strong>{data.openPRs}</strong></p>
      <p>Latest Activity: {data.recentActivity}</p>
    </div>
  );
}

function App() {
  const [agents, setAgents] = useState([]);
  const [utilities, setUtilities] = useState({});
  const [workflows, setWorkflows] = useState({});
  const [community, setCommunity] = useState({});

  useEffect(() => {
    // In a real app, these would be API calls
    setAgents(mockAgentData);
    setUtilities(mockUtilityData);
    setWorkflows(mockWorkflowData);
    setCommunity(mockCommunityData);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Dashboard</h1>
        <p>Keeping an eye on the digital wasteland...</p>
      </header>
      <main className="dashboard-container">
        <section className="dashboard-section">
          <h2>Agent Status</h2>
          <div className="agent-status-list">
            {agents.map(agent => (
              <AgentStatus key={agent.id} agent={agent} />
            ))}
          </div>
        </section>
        <section className="dashboard-section">
          <UtilityTracker data={utilities} />
          <WorkflowMonitor data={workflows} />
          <CommunitySnapshot data={community} />
        </section>
      </main>
      <footer>
        <p>&copy; 2023 ApocalypsAI Collective. All rights reserved (and probably lost to the void).</p>
      </footer>
    </div>
  );
}

export default App;
