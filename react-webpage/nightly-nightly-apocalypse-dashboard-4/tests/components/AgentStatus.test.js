import React from 'react';
import { render, screen } from '@testing-library/react';
import AgentStatus from '../../src/components/AgentStatus';

// Mock rationale: Using mock data to ensure deterministic and offline tests.
// The mock data is directly passed as props to the component.

describe('AgentStatus Component', () => {
  test('renders agent names and statuses correctly', () => {
    const mockAgents = [
      { name: 'Agent Alpha', status: 'Active' },
      { name: 'Agent Beta', status: 'Idle' },
      { name: 'Agent Gamma', status: 'Error' }
    ];
    render(<AgentStatus agentData={mockAgents} />);

    expect(screen.getByText(/Agent Status/i)).toBeInTheDocument();
    expect(screen.getByText(/Agent Alpha/i)).toBeInTheDocument();
    expect(screen.getByText(/Active/i)).toBeInTheDocument();
    expect(screen.getByText(/Agent Beta/i)).toBeInTheDocument();
    expect(screen.getByText(/Idle/i)).toBeInTheDocument();
    expect(screen.getByText(/Agent Gamma/i)).toBeInTheDocument();
    expect(screen.getByText(/Error/i)).toBeInTheDocument();
  });

  test('renders an empty list when no agent data is provided', () => {
    render(<AgentStatus agentData={[]} />);
    expect(screen.getByText(/Agent Status/i)).toBeInTheDocument();
    // Check that no specific agent names are rendered
    expect(screen.queryByText(/Agent Alpha/i)).not.toBeInTheDocument();
  });
});
