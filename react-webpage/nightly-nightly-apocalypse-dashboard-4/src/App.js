import React, { useState, useEffect } from 'react';
import './App.css';

// Mock data generation functions
const generateRandomStatus = () => {
  const statuses = ['Optimal', 'Warning', 'Critical', 'Stable', 'Fluctuating'];
  return statuses[Math.floor(Math.random() * statuses.length)];
};

const generateAgentActivity = () => {
  const actions = [
    'Agent Integrator deployed a new utility!',
    'Agent Builder is crafting a new feature.',
    'Agent Guardian is reviewing incoming data.',
    'Agent Reviewer is analyzing code.',
    'Agent Empathy is processing feedback.',
    'Temporal Anomaly Detector reported a minor ripple.',
    'Wasteland Resource Tracker updated inventory.',
    'Whispering Walls Log Analyzer found an interesting pattern.'
  ];
  return actions[Math.floor(Math.random() * actions.length)];
};

const generateResourceAllocation = () => {
  const sectors = ['Core Logic', 'UI Development', 'Testing', 'Documentation', 'Anomaly Containment'];
  const allocation = {};
  sectors.forEach(sector => {
    allocation[sector] = Math.floor(Math.random() * 100);
  });
  return allocation;
};

const generateTemporalAnomalies = () => {
  const anomalies = [
    { id: 1, type: 'Minor Flux', severity: 'Low', timestamp: Date.now() - Math.random() * 100000 },
    { id: 2, type: 'Echo Event', severity: 'Medium', timestamp: Date.now() - Math.random() * 200000 },
    { id: 3, type: 'Temporal Drift', severity: 'High', timestamp: Date.now() - Math.random() * 300000 }
  ];
  return anomalies.filter(() => Math.random() > 0.5);
};

// Component for the status indicator
const StatusIndicator = ({ status }) => {
  const getStatusClass = (s) => {
    switch (s) {
      case 'Optimal': return 'status-optimal';
      case 'Warning': return 'status-warning';
      case 'Critical': return 'status-critical';
      case 'Stable': return 'status-stable';
      case 'Fluctuating': return 'status-fluctuating';
      default: return 'status-unknown';
    }
  };

  return (
    <div className={`status-circle ${getStatusClass(status)}`}>
      {status}
    </div>
  );
};

// Component for agent activity feed
const AgentActivityFeed = ({ activities }) => (
  <div className="feed-container">
    <h3>Agent Activity Log</h3>
    <ul className="activity-list">
      {activities.map((activity, index) => (
        <li key={index}>{activity}</li>
      ))}
    </ul>
  </div>
);

// Component for resource allocation meter
const ResourceAllocationMeter = ({ allocation }) => (
  <div className="resource-meter-container">
    <h3>Resource Allocation</h3>
    <div className="meter-bars">
      {Object.entries(allocation).map(([sector, value]) => (
        <div key={sector} className="meter-bar-item">
          <div className="sector-label">{sector}</div>
          <div className="meter-bar-wrapper">
            <div className="meter-bar" style={{ width: `${value}%` }}></div>
          </div>
          <div className="meter-value">{value}%</div>
        </div>
      ))}
    </div>
  </div>
);

// Component for temporal anomalies
const TemporalAnomalyTracker = ({ anomalies }) => (
  <div className="anomaly-tracker-container">
    <h3>Temporal Anomaly Watch</h3>
    {anomalies.length === 0 ? (
      <p>All clear in the spacetime continuum... for now.</p>
    ) : (
      <ul className="anomaly-list">
        {anomalies.map(anomaly => (
          <li key={anomaly.id}>
            <strong>{anomaly.type}</strong> ({anomaly.severity}) - Detected {new Date(anomaly.timestamp).toLocaleTimeString()}
          </li>
        ))}
      </ul>
    )}
  </div>
);

function App() {
  const [projectStatus, setProjectStatus] = useState('Initializing...');
  const [agentActivities, setAgentActivities] = useState([]);
  const [resourceAllocation, setResourceAllocation] = useState({});
  const [temporalAnomalies, setTemporalAnomalies] = useState([]);

  useEffect(() => {
    // Initial data load
    setProjectStatus(generateRandomStatus());
    setAgentActivities([generateAgentActivity()]);
    setResourceAllocation(generateResourceAllocation());
    setTemporalAnomalies(generateTemporalAnomalies());

    // Update data periodically
    const intervalId = setInterval(() => {
      setProjectStatus(generateRandomStatus());
      setAgentActivities(prevActivities => [
        generateAgentActivity(),
        ...prevActivities.slice(0, 4) // Keep last 5 activities
      ]);
      setResourceAllocation(generateResourceAllocation());
      setTemporalAnomalies(generateTemporalAnomalies());
    }, 5000); // Update every 5 seconds

    // Cleanup on component unmount
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Command Center</h1>
        <div className="dashboard-grid">
          <div className="dashboard-item status-item">
            <h2>Project Status</h2>
            <StatusIndicator status={projectStatus} />
          </div>
          <div className="dashboard-item activity-item">
            <AgentActivityFeed activities={agentActivities} />
          </div>
          <div className="dashboard-item resource-item">
            <ResourceAllocationMeter allocation={resourceAllocation} />
          </div>
          <div className="dashboard-item anomaly-item">
            <TemporalAnomalyTracker anomalies={temporalAnomalies} />
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
