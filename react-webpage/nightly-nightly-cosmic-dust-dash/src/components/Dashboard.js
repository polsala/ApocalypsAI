import React, { useState, useEffect, useMemo } from 'react';
import { mockDailyDust } from '../data/mockData';

function Dashboard() {
  const [timeRange, setTimeRange] = useState(7); // Default to last 7 days

  // Mock rationale: All data is sourced from mockDailyDust, ensuring deterministic and offline operation.
  // Filtering and aggregation are performed on this static mock data.
  const filteredData = useMemo(() => {
    const today = new Date();
    const cutoffDate = new Date();
    cutoffDate.setDate(today.getDate() - timeRange);

    return mockDailyDust.filter(item => {
      const itemDate = new Date(item.date);
      return itemDate >= cutoffDate;
    });
  }, [timeRange]);

  const totalStars = useMemo(() => 
    filteredData.reduce((sum, item) => sum + item.stars, 0), 
    [filteredData]
  );
  const totalCommits = useMemo(() => 
    filteredData.reduce((sum, item) => sum + item.commits, 0), 
    [filteredData]
  );
  const totalIssues = useMemo(() => 
    filteredData.reduce((sum, item) => sum + item.issues, 0), 
    [filteredData]
  );

  const agentActivitySummary = useMemo(() => {
    const summary = {};
    filteredData.forEach(day => {
      day.agentActivity.forEach(activity => {
        summary[activity.agent] = (summary[activity.agent] || 0) + activity.count;
      });
    });
    return Object.entries(summary).sort(([, countA], [, countB]) => countB - countA);
  }, [filteredData]);

  const maxDustValue = useMemo(() => 
    Math.max(...filteredData.map(item => item.stars + item.commits + item.issues), 0),
    [filteredData]
  );

  return (
    <div className="dashboard-container">
      <div className="time-range-selector">
        <button 
          className={timeRange === 7 ? 'active' : ''} 
          onClick={() => setTimeRange(7)}
        >
          Last 7 Days
        </button>
        <button 
          className={timeRange === 30 ? 'active' : ''} 
          onClick={() => setTimeRange(30)}
        >
          Last 30 Days
        </button>
      </div>

      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Total Stars Collected ✨</h3>
          <p>{totalStars}</p>
        </div>
        <div className="metric-card">
          <h3>Total Commits Pushed 🚀</h3>
          <p>{totalCommits}</p>
        </div>
        <div className="metric-card">
          <h3>Total Issues Resolved ✅</h3>
          <p>{totalIssues}</p>
        </div>
      </div>

      <div className="chart-section">
        <h3>Daily Cosmic Dust Collection</h3>
        <div className="chart-bars">
          {filteredData.map((item, index) => {
            const totalDust = item.stars + item.commits + item.issues;
            const barHeight = maxDustValue > 0 ? (totalDust / maxDustValue) * 100 : 0;
            const shortDate = new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            return (
              <div 
                key={item.date} 
                className="chart-bar" 
                style={{ height: `${barHeight}%` }}
                title={`Date: ${item.date}\nStars: ${item.stars}\nCommits: ${item.commits}\nIssues: ${item.issues}\nTotal Dust: ${totalDust}`}
              >
                <span className="bar-label">{totalDust}</span>
                <span className="bar-date">{shortDate}</span>
              </div>
            );
          })}
        </div>
      </div>

      <div className="agent-activity-section">
        <h3>Top Dust Collectors (Agents)</h3>
        <ul className="agent-list">
          {agentActivitySummary.map(([agent, count]) => (
            <li key={agent}>
              <span>{agent}</span>
              <span>{count} activities</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;
