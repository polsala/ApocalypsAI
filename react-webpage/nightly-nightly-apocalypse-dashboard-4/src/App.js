import React, { useState, useEffect } from 'react';
import './App.css';

// Mock data for demonstration purposes
const mockData = {
  agents: [
    { name: 'Builder', status: 'active', color: '#4CAF50' },
    { name: 'Guardian', status: 'idle', color: '#FFC107' },
    { name: 'Integrator', status: 'active', color: '#4CAF50' },
    { name: 'Reviewer', status: 'error', color: '#F44336' },
  ],
  utilities: {
    total: 2000,
    classifiers: {
      'python-utils': 800,
      'react-webpage': 50,
      'bash-utils': 500,
      'rust-utils': 300,
      'github-actions': 100,
      'docker-tools': 150,
      'cli-apps': 100
    }
  },
  workflows: [
    { name: 'gen_openrouter', status: 'success', color: '#4CAF50' },
    { name: 'gen_groq', status: 'success', color: '#4CAF50' },
    { name: 'gen_gemini', status: 'warning', color: '#FFC107' },
    { name: 'nightly_self_heal', status: 'success', color: '#4CAF50' },
  ]
};

function AgentStatus({ agent }) {
  return (
    <div className="agent-card" style={{ borderColor: agent.color }}>
      <h3>{agent.name}</h3>
      <p>Status: <span className="status-indicator" style={{ backgroundColor: agent.color }}></span> {agent.status}</p>
    </div>
  );
}

function ClassifierDistribution({ classifiers }) {
  return (
    <div className="classifier-distribution">
      <h4>Utility Distribution by Classifier</h4>
      <ul>
        {Object.entries(classifiers).map(([classifier, count]) => (
          <li key={classifier}>
            {classifier}: {count}
          </li>
        ))}
      </ul>
    </div>
  );
}

function WorkflowStatus({ workflow }) {
  return (
    <div className="workflow-item">
      <span>{workflow.name}:</span>
      <span className="status-indicator" style={{ backgroundColor: workflow.color }}></span>
      {workflow.status}
    </div>
  );
}

function App() {
  const [data, setData] = useState(mockData);

  // In a real app, you'd fetch data here
  useEffect(() => {
    // Simulate fetching data
    // fetch('/api/status')
    //   .then(res => res.json())
    //   .then(data => setData(data));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Command Center</h1>
        <p>Monitoring the state of our glorious digital wasteland.</p>
      </header>
      <main>
        <section className="agents-section">
          <h2>Agent Status</h2>
          <div className="agent-grid">
            {data.agents.map(agent => (
              <AgentStatus key={agent.name} agent={agent} />
            ))}
          </div>
        </section>

        <section className="utilities-section">
          <h2>Utility Hub</h2>
          <p>Total Utilities Generated: <strong>{data.utilities.total}</strong></p>
          <ClassifierDistribution classifiers={data.utilities.classifiers} />
        </section>

        <section className="workflows-section">
          <h2>Workflow Health</h2>
          <div className="workflow-grid">
            {data.workflows.map(workflow => (
              <WorkflowStatus key={workflow.name} workflow={workflow} />
            ))}
          </div>
        </section>
      </main>
      <footer>
        <p>Stay vigilant. The future is automated.</p>
      </footer>
    </div>
  );
}

export default App;
