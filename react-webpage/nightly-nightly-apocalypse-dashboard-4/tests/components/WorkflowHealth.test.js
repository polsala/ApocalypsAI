import React from 'react';
import { render, screen } from '@testing-library/react';
import WorkflowHealth from '../../src/components/WorkflowHealth';

// Mock rationale: Using mock data to ensure deterministic and offline tests.
// The mock data is directly passed as props to the component.

describe('WorkflowHealth Component', () => {
  test('renders workflow names and statuses correctly', () => {
    const mockWorkflows = [
      { name: 'Workflow A', status: 'Healthy' },
      { name: 'Workflow B', status: 'Warning' },
      { name: 'Workflow C', status: 'Unhealthy' }
    ];
    render(<WorkflowHealth workflowData={mockWorkflows} />);

    expect(screen.getByText(/Workflow Health/i)).toBeInTheDocument();
    expect(screen.getByText(/Workflow A/i)).toBeInTheDocument();
    expect(screen.getByText(/Healthy/i)).toBeInTheDocument();
    expect(screen.getByText(/Workflow B/i)).toBeInTheDocument();
    expect(screen.getByText(/Warning/i)).toBeInTheDocument();
    expect(screen.getByText(/Workflow C/i)).toBeInTheDocument();
    expect(screen.getByText(/Unhealthy/i)).toBeInTheDocument();
  });

  test('renders an empty list when no workflow data is provided', () => {
    render(<WorkflowHealth workflowData={[]} />);
    expect(screen.getByText(/Workflow Health/i)).toBeInTheDocument();
    // Check that no specific workflow names are rendered
    expect(screen.queryByText(/Workflow A/i)).not.toBeInTheDocument();
  });
});
