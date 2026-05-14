import React from 'react';
import { render, screen } from '@testing-library/react';
import AgentActivityFeed from '../src/components/AgentActivityFeed';

describe('AgentActivityFeed Component', () => {
  test('renders message when no data is provided', () => {
    render(<AgentActivityFeed data={[]} />);
    expect(screen.getByText('No activity yet...')).toBeInTheDocument();
  });

  test('renders activity items correctly', () => {
    const mockData = [
      {
        id: 1,
        agent: 'Integrator',
        action: 'Generated Utility',
        timestamp: '10:00:00 AM'
      },
      {
        id: 2,
        agent: 'Builder',
        action: 'Reviewed PR',
        timestamp: '10:00:05 AM'
      }
    ];
    render(<AgentActivityFeed data={mockData} />);

    expect(screen.getByText('[10:00:00 AM]')).toBeInTheDocument();
    expect(screen.getByText('Integrator')).toBeInTheDocument();
    expect(screen.getByText('Generated Utility')).toBeInTheDocument();

    expect(screen.getByText('[10:00:05 AM]')).toBeInTheDocument();
    expect(screen.getByText('Builder')).toBeInTheDocument();
    expect(screen.getByText('Reviewed PR')).toBeInTheDocument();
  });

  test('renders multiple activity items', () => {
    const mockData = [
      { id: 1, agent: 'Agent A', action: 'Action 1', timestamp: '11:00:00 AM' },
      { id: 2, agent: 'Agent B', action: 'Action 2', timestamp: '11:00:01 AM' },
      { id: 3, agent: 'Agent C', action: 'Action 3', timestamp: '11:00:02 AM' }
    ];
    render(<AgentActivityFeed data={mockData} />);

    expect(screen.getAllByRole('listitem').length).toBe(3);
  });
});
