import React from 'react';

function AgentFeed({ data }) {
  return (
    <section className="agent-feed">
      <h2>Agent Activity Feed</h2>
      {data && data.length > 0 ? (
        <ul>
          {data.map((item, index) => (
            <li key={index}>
              <span className="agent-name">{item.agent}</span> is performing <span className="action">{item.action}</span>.
            </li>
          ))}
        </ul>
      ) : (
        <p>No agent activity to display at the moment. The agents are probably on a coffee break.</p>
      )}
    </section>
  );
}

export default AgentFeed;
