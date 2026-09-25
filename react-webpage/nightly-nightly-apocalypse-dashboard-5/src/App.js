import React, { useState, useEffect } from 'react';
import './App.css';
import AgentStatusCard from './components/AgentStatusCard';
import WorkflowIndicator from './components/WorkflowIndicator';
import { generateMockAgentData, generateMockWorkflowData } from './utils/mockData';

function App() {
  const [agents, setAgents] = useState([]);
  const [workflowStatus, setWorkflowStatus] = useState('unknown');

  useEffect(() => {
    // Simulate fetching data
    const mockAgents = generateMockAgentData(5);
    setAgents(mockAgents);

    const mockWorkflow = generateMockWorkflowData();
    setWorkflowStatus(mockWorkflow.status);

    // In a real app, you'd fetch this data from an API
    // const interval = setInterval(() => {
    //   fetch('/api/agents').then(res => res.json()).then(data => setAgents(data));
    //   fetch('/api/workflow').then(res => res.json()).then(data => setWorkflowStatus(data.status));
    // }, 5000);
    // return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Status Dashboard</h1>
        <p>Keeping the digital world... interesting.</p>
      </header>
      <main>
        <section className="agent-status-section">
          <h2>Agent Status</h2>
          <div className="agent-cards-container">
            {agents.map(agent => (
              <AgentStatusCard key={agent.id} name={agent.name} status={agent.status} />
            ))}
          </div>
        </section>
        <section className="workflow-section">
          <h2>Workflow Health</h2>
          <WorkflowIndicator status={workflowStatus} />
        </section>
      </main>
      <footer className="App-footer">
        <p>&copy; 2023 ApocalypsAI Collective. All rights reserved (mostly).</p>
      </footer>
    </div>
  );
}

export default App;
