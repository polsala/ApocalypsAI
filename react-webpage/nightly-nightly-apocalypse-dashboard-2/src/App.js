import React, { useState, useEffect } from 'react';
import './App.css';

// Mock data for demonstration
const mockAgentActivity = [
  { id: 1, agent: 'Generator', action: 'Minted utility', timestamp: '2023-10-27T10:00:00Z' },
  { id: 2, agent: 'Integrator', action: 'Added new utility', timestamp: '2023-10-27T10:05:00Z' },
  { id: 3, agent: 'Reviewer', action: 'Reviewed PR #123', timestamp: '2023-10-27T10:15:00Z' },
  { id: 4, agent: 'Guardian', action: 'Triage issue #456', timestamp: '2023-10-27T10:20:00Z' },
];

const mockUtilityStats = {
  totalGenerated: 1500,
  todayGenerated: 5,
  classifiers: {
    'react-webpage': 10,
    'python-utils': 500,
    'rust-utils': 200,
    'bash-utils': 300,
    'github-actions': 150,
    'cli-apps': 100,
    'docker-tools': 50,
    'web-apis': 20,
    'js-utils': 70,
    'node-utils': 60,
    'typescript-utils': 40,
    'data-scripts': 30,
    'test-suite-tools': 25,
    'monitoring-scripts': 15,
    'infra-automation': 10,
    'go-utils': 5,
    'java-utils': 2,
    'cpp-utils': 1,
    'ansible-playbooks': 30,
    'terraform-modules': 10,
    'k8s-resources': 5,
    'ci-cd-pipelines': 20,
    'database-scripts': 10,
    'ml-notebooks': 5,
    'api-clients': 10,
  }
};

const mockWorkflowStatus = {
  totalWorkflows: 25,
  successful: 22,
  failed: 3,
  running: 0,
};

function App() {
  const [agentActivity, setAgentActivity] = useState([]);
  const [utilityStats, setUtilityStats] = useState({});
  const [workflowStatus, setWorkflowStatus] = useState({});

  useEffect(() => {
    // In a real app, fetch data from an API
    setAgentActivity(mockAgentActivity);
    setUtilityStats(mockUtilityStats);
    setWorkflowStatus(mockWorkflowStatus);
  }, []);

  // Helper to format timestamps
  const formatTimestamp = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleString();
  };

  // Function to get a whimsical color based on classifier name
  const getClassifierColor = (classifierName) => {
    const colors = [
      '#FF6B6B', '#4ECDC4', '#45B7D1', '#FED766', '#9B59B6',
      '#3498DB', '#1ABC9C', '#F39C12', '#E74C3C', '#2ECC71'
    ];
    let hash = 0;
    for (let i = 0; i < classifierName.length; i++) {
      hash = classifierName.charCodeAt(i) + ((hash << 5) - hash);
    }
    const index = Math.abs(hash) % colors.length;
    return colors[index];
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Command Center</h1>
        <p>Monitoring the pulse of our autonomous agents and their creations.</p>
      </header>
      <main>
        <section className="dashboard-section">
          <h2>Agent Activity Feed</h2>
          <ul className="activity-list">
            {agentActivity.map(item => (
              <li key={item.id} className="activity-item">
                <span className="agent-name">[{item.agent}]</span> {item.action} at {formatTimestamp(item.timestamp)}
              </li>
            ))}
          </ul>
        </section>

        <section className="dashboard-section">
          <h2>Utility Generation Stats</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Utilities</h3>
              <p className="stat-value">{utilityStats.totalGenerated}</p>
            </div>
            <div className="stat-card">
              <h3>Generated Today</h3>
              <p className="stat-value">{utilityStats.todayGenerated}</p>
            </div>
          </div>
          <div className="classifier-stats">
            <h3>Utilities by Classifier:</h3>
            <div className="classifier-list">
              {Object.entries(utilityStats.classifiers || {}).map(([classifier, count]) => (
                <div key={classifier} className="classifier-item" style={{ backgroundColor: getClassifierColor(classifier) }}>
                  <span className="classifier-name">{classifier}</span>
                  <span className="classifier-count">{count}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="dashboard-section">
          <h2>Workflow Status</h2>
          <div className="workflow-stats">
            <div className="stat-card">
              <h3>Total Workflows</h3>
              <p className="stat-value">{workflowStatus.totalWorkflows}</p>
            </div>
            <div className="stat-card success">
              <h3>Successful</h3>
              <p className="stat-value">{workflowStatus.successful}</p>
            </div>
            <div className="stat-card failed">
              <h3>Failed</h3>
              <p className="stat-value">{workflowStatus.failed}</p>
            </div>
            <div className="stat-card running">
              <h3>Running</h3>
              <p className="stat-value">{workflowStatus.running}</p>
            </div>
          </div>
        </section>
      </main>
      <footer className="App-footer">
        <p>&copy; 2023 ApocalypsAI Collective. Stay vigilant!</p>
      </footer>
    </div>
  );
}

export default App;
