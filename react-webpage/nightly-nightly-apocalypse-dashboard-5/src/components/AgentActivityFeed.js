import React from 'react';
import './AgentActivityFeed.css';

function AgentActivityFeed({ data }) {
  return (
    <div className="activity-feed">
      {data.length === 0 ? (
        <p>No activity yet...</p>
      ) : (
        <ul>
          {data.map(item => (
            <li key={item.id} className="activity-item">
              <span className="timestamp">[{item.timestamp}]</span>
              <span className="agent-name">{item.agent}</span>
              <span className="action">{item.action}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default AgentActivityFeed;
