import React from 'react';
import './App.css';
import AgentStatus from './components/AgentStatus';
import UtilityCounter from './components/UtilityCounter';
import WorkflowHealth from './components/WorkflowHealth';
import ResourceMeter from './components/ResourceMeter';
import { getMockData } from './utils/mockData';

function App() {
  const mockData = getMockData();

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Dashboard</h1>
      </header>
      <main>
        <AgentStatus agentData={mockData.agentStatus} />
        <UtilityCounter utilityCounts={mockData.utilityCounts} />
        <WorkflowHealth workflowData={mockData.workflowHealth} />
        <ResourceMeter scarcityLevel={mockData.resourceScarcity} />
      </main>
    </div>
  );
}

export default App;
