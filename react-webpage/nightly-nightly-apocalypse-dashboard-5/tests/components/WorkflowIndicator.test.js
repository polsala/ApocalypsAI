import React from 'react';
import { render, screen } from '@testing-library/react';
import WorkflowIndicator from '../../src/components/WorkflowIndicator';

describe('WorkflowIndicator Component', () => {
  test('renders workflow status correctly', () => {
    const workflowStatus = 'Success';
    render(<WorkflowIndicator status={workflowStatus} />);

    expect(screen.getByText(`Workflow Status: ${workflowStatus}`)).toBeInTheDocument();
  });

  test('applies correct CSS class for success status', () => {
    render(<WorkflowIndicator status="Success" />);
    const indicatorElement = screen.getByText('Workflow Status: Success').closest('.workflow-indicator');
    expect(indicatorElement).toHaveClass('indicator-success');
  });

  test('applies correct CSS class for failure status', () => {
    render(<WorkflowIndicator status="Failure" />);
    const indicatorElement = screen.getByText('Workflow Status: Failure').closest('.workflow-indicator');
    expect(indicatorElement).toHaveClass('indicator-failure');
  });

  test('applies correct CSS class for running status', () => {
    render(<WorkflowIndicator status="Running" />);
    const indicatorElement = screen.getByText('Workflow Status: Running').closest('.workflow-indicator');
    expect(indicatorElement).toHaveClass('indicator-running');
  });

  test('applies correct CSS class for unknown status', () => {
    render(<WorkflowIndicator status="Unknown" />);
    const indicatorElement = screen.getByText('Workflow Status: Unknown').closest('.workflow-indicator');
    expect(indicatorElement).toHaveClass('indicator-unknown');
  });
});
