import React from 'react';
import { render, screen } from '@testing-library/react';
import AgentStatusCard from '../../src/components/AgentStatusCard';

describe('AgentStatusCard Component', () => {
  test('renders agent name and status correctly', () => {
    const agentName = 'Test Agent';
    const agentStatus = 'Active';
    render(<AgentStatusCard name={agentName} status={agentStatus} />);

    expect(screen.getByText(agentName)).toBeInTheDocument();
    expect(screen.getByText(`Status: ${agentStatus}`)).toBeInTheDocument();
  });

  test('applies correct CSS class for active status', () => {
    render(<AgentStatusCard name="Active Agent" status="Active" />);
    const cardElement = screen.getByText('Active Agent').closest('.agent-card');
    expect(cardElement).toHaveClass('status-active');
  });

  test('applies correct CSS class for idle status', () => {
    render(<AgentStatusCard name="Idle Agent" status="Idle" />);
    const cardElement = screen.getByText('Idle Agent').closest('.agent-card');
    expect(cardElement).toHaveClass('status-idle');
  });

  test('applies correct CSS class for error status', () => {
    render(<AgentStatusCard name="Error Agent" status="Error" />);
    const cardElement = screen.getByText('Error Agent').closest('.agent-card');
    expect(cardElement).toHaveClass('status-error');
  });

  test('applies correct CSS class for unknown status', () => {
    render(<AgentStatusCard name="Unknown Agent" status="Pending" />);
    const cardElement = screen.getByText('Unknown Agent').closest('.agent-card');
    expect(cardElement).toHaveClass('status-unknown');
  });
});
