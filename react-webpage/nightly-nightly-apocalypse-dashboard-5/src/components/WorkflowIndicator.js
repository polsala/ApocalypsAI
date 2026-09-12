import React from 'react';
import './WorkflowIndicator.css';

function WorkflowIndicator({ status }) {
  const getIndicatorClass = (status) => {
    switch (status.toLowerCase()) {
      case 'success':
        return 'indicator-success';
      case 'failure':
        return 'indicator-failure';
      case 'running':
        return 'indicator-running';
      default:
        return 'indicator-unknown';
    }
  };

  return (
    <div className={`workflow-indicator ${getIndicatorClass(status)}`}>
      <div className="indicator-dot"></div>
      <p>Workflow Status: <span className="status-text">{status}</span></p>
    </div>
  );
}

export default WorkflowIndicator;
