import React from 'react';

function AgentStatus({ agentData }) {
  return (
    <section className="dashboard-section">
      <h2>Agent Status</h2>
      <ul>
        {agentData.map((agent, index) => (
          <li key={index}>
            <strong>{agent.name}</strong>: <span className={agent.status.toLowerCase()}>{agent.status}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default AgentStatus;
