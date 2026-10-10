import React from 'react';
import './ActivityPanel.css';

function ActivityPanel({ data }) {
  if (!data) {
    return <div className="activity-panel-container"><p>No activity data available.</p></div>;
  }

  const { newUtilities, openPRs, openIssues } = data;

  return (
    <div className="activity-panel-container">
      <h2>Repository Pulse</h2>
      <div className="activity-stats">
        <div className="stat-item">
          <span className="stat-value">{newUtilities}</span>
          <span className="stat-label">New Utilities</span>
        </div>
        <div className="stat-item">
          <span className="stat-value">{openPRs}</span>
          <span className="stat-label">Open PRs</span>
        </div>
        <div className="stat-item">
          <span className="stat-value">{openIssues}</span>
          <span className="stat-label">Active Issues</span>
        </div>
      </div>
    </div>
  );
}

export default ActivityPanel;
