import React from 'react';
import { render, screen } from '@testing-library/react';
import ResourceTracker from '../src/components/ResourceTracker';

describe('ResourceTracker Component', () => {
  it('renders the title', () => {
    render(<ResourceTracker data={[]} />);
    expect(screen.getByText('Resource Tracker')).toBeInTheDocument();
  });

  it('renders resource items correctly', () => {
    const mockData = [
      { name: 'Canned Beans', quantity: 500, unit: 'cans' },
      { name: 'Clean Water', quantity: 1000, unit: 'liters' }
    ];
    render(<ResourceTracker data={mockData} />);

    expect(screen.getByText('Canned Beans')).toBeInTheDocument();
    expect(screen.getByText('500 cans')).toBeInTheDocument();
    expect(screen.getByText('Clean Water')).toBeInTheDocument();
    expect(screen.getByText('1000 liters')).toBeInTheDocument();
  });

  it('renders a message when no data is provided', () => {
    render(<ResourceTracker data={[]} />);
    expect(screen.getByText('No resource data available. The pantry is bare...')).toBeInTheDocument();
  });

  it('renders a message when data is null', () => {
    render(<ResourceTracker data={null} />);
    expect(screen.getByText('No resource data available. The pantry is bare...')).toBeInTheDocument();
  });
});
