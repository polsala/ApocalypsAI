import React, { useState, useEffect } from 'react';
import './App.css';
import AgentFeed from './components/AgentFeed';
import UtilityTracker from './components/UtilityTracker';
import Visualizations from './components/Visualizations';
import { getMockData } from './data/mockData';

function App() {
  const [agentData, setAgentData] = useState([]);
  const [utilityData, setUtilityData] = useState({});

  useEffect(() => {
    const data = getMockData();
    setAgentData(data.agentActivity);
    setUtilityData(data.utilityStats);

    // Simulate real-time updates (optional)
    const interval = setInterval(() => {
      const newData = getMockData(); // Fetch new mock data
      setAgentData(newData.agentActivity);
      setUtilityData(newData.utilityStats);
    }, 15000); // Update every 15 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Command Center</h1>
        <p>Monitoring the pulse of our autonomous agents.</p>
      </header>
      <main>
        <AgentFeed data={agentData} />
        <UtilityTracker data={utilityData} />
        <Visualizations />
      </main>
      <footer>
        <p>&copy; 2023 ApocalypsAI Collective. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
