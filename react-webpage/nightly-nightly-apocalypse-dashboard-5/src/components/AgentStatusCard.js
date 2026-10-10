import React from 'react';
import './AgentStatusCard.css';

function AgentStatusCard({ name, status }) {
  const getStatusClass = (status) => {
    switch (status.toLowerCase()) {
      case 'active':
        return 'status-active';
      case 'idle':
        return 'status-idle';
      case 'error':
        return 'status-error';
      default:
        return 'status-unknown';
    }
  };

  return (
    <div className={`agent-card ${getStatusClass(status)}`}>
      <h3>{name}</h3>
      <p>Status: <span className="status-text">{status}</span></p>
    </div>
  );
}

export default AgentStatusCard;
