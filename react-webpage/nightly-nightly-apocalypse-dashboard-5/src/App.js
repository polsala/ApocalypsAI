import React, { useState, useEffect } from 'react';
import './App.css';

// Mock data for demonstration
const mockData = {
  agents: [
    { name: 'Builder', status: 'Operational', color: '#4CAF50' },
    { name: 'Guardian', status: 'Nominal', color: '#8BC34A' },
    { name: 'Integrator', status: 'Active', color: '#CDDC39' },
    { name: 'Reviewer', status: 'Standby', color: '#FFEB3B' },
  ],
  utilities: {
    total: 1942 + 1,
    classifiers: {
      'react-webpage': 1,
      'python-utils': 500,
      'rust-utils': 200,
      'bash-utils': 300,
      'github-actions': 100,
      'devops-tools': 150,
      'docker-tools': 120,
      'cli-apps': 250,
      'web-apis': 50,
      'js-utils': 100,
      'node-utils': 80,
      'typescript-utils': 70,
      'data-scripts': 100,
      'test-suite-tools': 90,
      'monitoring-scripts': 60,
      'infra-automation': 70,
      'go-utils': 50,
      'java-utils': 40,
      'cpp-utils': 30,
      'ansible-playbooks': 20,
      'terraform-modules': 15,
      'k8s-resources': 10,
      'ci-cd-pipelines': 5,
      'database-scripts': 10,
      'ml-notebooks': 5,
      'api-clients': 10,
    }
  },
  workflows: [
    { name: 'gen_openrouter', status: 'Success', lastRun: '2023-10-27T10:00:00Z', color: '#2196F3' },
    { name: 'gen_groq', status: 'Success', lastRun: '2023-10-27T10:20:00Z', color: '#2196F3' },
    { name: 'gen_gemini', status: 'Warning', lastRun: '2023-10-27T10:40:00Z', color: '#FF9800' },
    { name: 'nightly_self_heal', status: 'Success', lastRun: '2023-10-27T02:42:00Z', color: '#2196F3' },
  ]
};

function App() {
  const [data, setData] = useState(mockData);

  // In a real app, you'd fetch data here
  useEffect(() => {
    // Simulate fetching data
    // const fetchData = async () => {
    //   const response = await fetch('/api/apocalypse-status');
    //   const result = await response.json();
    //   setData(result);
    // };
    // fetchData();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Status Dashboard</h1>
        <p>Navigating the digital wasteland, one utility at a time.</p>
      </header>
      <main>
        <section className="agent-status">
          <h2>Agent Status</h2>
          <div className="agent-grid">
            {data.agents.map(agent => (
              <div key={agent.name} className="agent-card" style={{ borderColor: agent.color }}>
                <h3>{agent.name}</h3>
                <p>{agent.status}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="utility-tracker">
          <h2>Utility Generation</h2>
          <p>Total Utilities Generated: <strong>{data.utilities.total}</strong></p>
          <h3>Utilities by Classifier:</h3>
          <ul className="classifier-list">
            {Object.entries(data.utilities.classifiers).map(([classifier, count]) => (
              <li key={classifier}>{classifier}: {count}</li>
            ))}
          </ul>
        </section>

        <section className="workflow-monitor">
          <h2>Workflow Health</h2>
          <div className="workflow-grid">
            {data.workflows.map(workflow => (
              <div key={workflow.name} className="workflow-card" style={{ borderColor: workflow.color }}>
                <h3>{workflow.name}</h3>
                <p>Status: {workflow.status}</p>
                <p>Last Run: {new Date(workflow.lastRun).toLocaleString()}</p>
              </div>
            ))}
          </div>
        </section>
      </main>
      <footer>
        <p>&copy; 2023 ApocalypsAI Collective. All rights reserved (or not, depending on the timeline).</p>
      </footer>
    </div>
  );
}

export default App;
