import React, { useState, useEffect } from 'react';
import './App.css';

const App = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshInterval, setRefreshInterval] = useState(30000); // 30 seconds

  // Mock data generator for demonstration
  const generateMockData = () => {
    const agents = [
      { name: 'Agent Builder', status: 'online', health: 95, lastSeen: new Date(Date.now() - Math.random() * 300000) },
      { name: 'Agent Reviewer', status: 'online', health: 88, lastSeen: new Date(Date.now() - Math.random() * 600000) },
      { name: 'Agent Guardian', status: 'offline', health: 0, lastSeen: new Date(Date.now() - Math.random() * 3600000) },
      { name: 'Agent Integrator', status: 'online', health: 92, lastSeen: new Date(Date.now() - Math.random() * 200000) },
    ];

    const metrics = {
      totalPRs: Math.floor(Math.random() * 50) + 100,
      openPRs: Math.floor(Math.random() * 20) + 5,
      mergedPRs: Math.floor(Math.random() * 30) + 40,
      failedPRs: Math.floor(Math.random() * 5) + 2,
      utilitiesCreated: Math.floor(Math.random() * 100) + 500,
      chaosExperiments: Math.floor(Math.random() * 20) + 10,
    };

    const timeline = [
      { time: new Date(Date.now() - 3600000), title: 'Chaos Experiment: Network Latency', description: 'Injected 200ms latency across all services', status: 'success' },
      { time: new Date(Date.now() - 7200000), title: 'Utility Integration: Backup Buddy', description: 'Successfully integrated new backup utility', status: 'success' },
      { time: new Date(Date.now() - 10800000), title: 'Agent Health Check', description: 'All agents reported healthy status', status: 'success' },
      { time: new Date(Date.now() - 14400000), title: 'Chaos Experiment: Disk Space', description: 'Simulated disk space exhaustion', status: 'warning' },
      { time: new Date(Date.now() - 18000000), title: 'PR Review: Security Patch', description: 'Automated security review completed', status: 'success' },
    ];

    const resources = {
      githubAPI: { usage: Math.random() * 80 + 10, limit: 5000 },
      diskSpace: { usage: Math.random() * 70 + 20, total: 100 },
      memoryUsage: { usage: Math.random() * 60 + 30, total: 100 },
      cpuLoad: { usage: Math.random() * 50 + 20, total: 100 },
    };

    return { agents, metrics, timeline, resources };
  };

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const mockData = generateMockData();
      setData(mockData);
    } catch (err) {
      setError('Failed to fetch data. Showing cached/mocked data.');
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    
    const interval = setInterval(fetchData, refreshInterval);
    return () => clearInterval(interval);
  }, [refreshInterval]);

  const getStatusColor = (status) => {
    switch (status) {
      case 'online': return 'success';
      case 'offline': return 'danger';
      case 'warning': return 'warning';
      default: return 'muted';
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString();
  };

  const formatRelativeTime = (date) => {
    const diff = Date.now() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    
    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return 'just now';
  };

  if (loading) {
    return (
      <div className="app-container">
        <div className="matrix-bg"></div>
        <div className="loading">
          <div className="glow" style={{fontSize: '1.5rem', marginBottom: '10px'}}>Initializing ApocalypsAI Dashboard...</div>
          <div>Scanning repository for agent activity...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <div className="matrix-bg"></div>
      {error && <div className="error">{error}</div>}
      
      <h1 className="header">ApocalypsAI Dashboard</h1>
      <p className="sub-header">Monitoring autonomous agent activity and repository health in real-time</p>
      
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px'}}>
        <div className="chip glow">Last Updated: {new Date().toLocaleTimeString()}</div>
        <div style={{display: 'flex', gap: '10px'}}>
          <select 
            value={refreshInterval} 
            onChange={(e) => setRefreshInterval(Number(e.target.value))}
            className="chip"
          >
            <option value={15000}>Auto-refresh: 15s</option>
            <option value={30000}>Auto-refresh: 30s</option>
            <option value={60000}>Auto-refresh: 1m</option>
            <option value={0}>Auto-refresh: Off</option>
          </select>
          <button 
            onClick={fetchData}
            className="chip success"
            style={{cursor: 'pointer'}}
          >
            Refresh Now
          </button>
        </div>
      </div>

      <div className="grid">
        {/* Agent Health Monitor */}
        <div className="card">
          <h3>🤖 Agent Health Monitor</h3>
          {data.agents.map((agent, index) => (
            <div key={index} className="metric">
              <div>
                <div style={{fontWeight: '600'}}>{agent.name}</div>
                <div className="metric-label" style={{marginTop: '5px'}}>
                  Last seen: {formatRelativeTime(agent.lastSeen)}
                </div>
              </div>
              <div style={{textAlign: 'right'}}>
                <div className={`status-indicator ${getStatusColor(agent.status)}`}></div>
                <div className="metric-value" style={{marginTop: '5px'}}>
                  {agent.status.toUpperCase()}
                </div>
              </div>
            </div>
          ))}
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{width: `${data.agents.filter(a => a.status === 'online').length / data.agents.length * 100}%`}}
            ></div>
          </div>
          <div className="metric-label" style={{marginTop: '10px'}}>
            {data.agents.filter(a => a.status === 'online').length} of {data.agents.length} agents online
          </div>
        </div>

        {/* Utility Metrics */}
        <div className="card">
          <h3>📊 Utility Metrics</h3>
          <div className="metric">
            <div className="metric-label">Total Utilities Created</div>
            <div className="metric-value glow">{data.metrics.utilitiesCreated}</div>
          </div>
          <div className="metric">
            <div className="metric-label">Chaos Experiments</div>
            <div className="metric-value glow">{data.metrics.chaosExperiments}</div>
          </div>
          <div className="metric">
            <div className="metric-label">Open PRs</div>
            <div className="metric-value">{data.metrics.openPRs}</div>
          </div>
          <div className="metric">
            <div className="metric-label">Merged PRs</div>
            <div className="metric-value">{data.metrics.mergedPRs}</div>
          </div>
          <div className="metric">
            <div className="metric-label">Failed PRs</div>
            <div className="metric-value">{data.metrics.failedPRs}</div>
          </div>
        </div>

        {/* Resource Tracker */}
        <div className="card">
          <h3>💾 Resource Tracker</h3>
          <div>
            <div className="metric">
              <div className="metric-label">GitHub API Usage</div>
              <div className="metric-value">{Math.floor(data.resources.githubAPI.usage)}/{data.resources.githubAPI.limit}</div>
            </div>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{width: `${(data.resources.githubAPI.usage / data.resources.githubAPI.limit) * 100}%`}}
              ></div>
            </div>
          </div>
          
          <div style={{marginTop: '15px'}}>
            <div className="metric">
              <div className="metric-label">Disk Space</div>
              <div className="metric-value">{Math.floor(data.resources.diskSpace.usage)}%</div>
            </div>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{width: `${data.resources.diskSpace.usage}%`}}
              ></div>
            </div>
          </div>
          
          <div style={{marginTop: '15px'}}>
            <div className="metric">
              <div className="metric-label">Memory Usage</div>
              <div className="metric-value">{Math.floor(data.resources.memoryUsage.usage)}%</div>
            </div>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{width: `${data.resources.memoryUsage.usage}%`}}
              ></div>
            </div>
          </div>
          
          <div style={{marginTop: '15px'}}>
            <div className="metric">
              <div className="metric-label">CPU Load</div>
              <div className="metric-value">{Math.floor(data.resources.cpuLoad.usage)}%</div>
            </div>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{width: `${data.resources.cpuLoad.usage}%`}}
              ></div>
            </div>
          </div>
        </div>

        {/* Chaos Event Timeline */}
        <div className="card" style={{gridColumn: '1 / -1'}}>
          <h3>🔥 Chaos Event Timeline</h3>
          <div className="timeline">
            {data.timeline.map((event, index) => (
              <div key={index} className="timeline-item">
                <div className="timeline-time">{formatTime(event.time)}</div>
                <div className="timeline-content">
                  <div className="timeline-title">
                    {event.title}
                    <span className={`chip ${event.status}`}>{event.status}</span>
                  </div>
                  <div className="timeline-desc">{event.description}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="footer">
        <div className="chip">ApocalypsAI Dashboard v1.0.0</div>
        <div style={{marginTop: '10px'}}>
          Built with React • Chart.js • CSS3 Animations
        </div>
      </div>
    </div>
  );
};

export default App;
