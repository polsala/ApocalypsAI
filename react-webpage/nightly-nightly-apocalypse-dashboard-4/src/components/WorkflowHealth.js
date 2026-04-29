import React from 'react';

function WorkflowHealth({ workflowData }) {
  const getHealthClass = (status) => {
    if (status === 'Healthy') return 'healthy';
    if (status === 'Warning') return 'warning';
    return 'unhealthy';
  };

  return (
    <section className="dashboard-section">
      <h2>Workflow Health</h2>
      <ul>
        {workflowData.map((workflow, index) => (
          <li key={index}>
            <strong>{workflow.name}</strong>: <span className={getHealthClass(workflow.status)}>{workflow.status}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default WorkflowHealth;
