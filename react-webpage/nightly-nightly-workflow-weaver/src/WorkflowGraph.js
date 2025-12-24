import React from 'react';
import WorkflowNode from './WorkflowNode';

const WorkflowGraph = ({ workflows }) => {
  return (
    <div className="workflow-graph">
      {workflows.map(workflow => (
        <WorkflowNode key={workflow.id} workflow={workflow} />
      ))}
    </div>
  );
};

export default WorkflowGraph;
