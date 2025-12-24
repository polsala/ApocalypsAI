import React from 'react';

const WorkflowNode = ({ workflow }) => {
  const { name, status, lastRun, mood } = workflow;

  const statusClass = `status-${status}`;

  return (
    <div className="workflow-node">
      <span className="mood-emoji" role="img" aria-label={mood.description}>{mood.emoji}</span>
      <h3>{name}</h3>
      <p>Last Run: {lastRun}</p>
      <p className={`status-indicator ${statusClass}`}>
        Status: {status.charAt(0).toUpperCase() + status.slice(1)}
      </p>
    </div>
  );
};

export default WorkflowNode;
