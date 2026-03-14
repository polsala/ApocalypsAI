import React from 'react';
import { render, screen } from '@testing-library/react';
import SafeZones from '../src/components/SafeZones';

describe('SafeZones Component', () => {
  const mockZones = [
    { id: 1, name: 'Haven', status: 'Stable' },
    { id: 2, name: 'Outpost', status: 'Caution' },
    { id: 3, name: 'Citadel', status: 'Compromised' },
  ];

  test('renders a list of safe zones with their statuses', () => {
    render(<SafeZones zones={mockZones} />);
    expect(screen.getByText(/Haven/i)).toBeInTheDocument();
    expect(screen.getByText(/Stable/i)).toBeInTheDocument();
    expect(screen.getByText(/Outpost/i)).toBeInTheDocument();
    expect(screen.getByText(/Caution/i)).toBeInTheDocument();
    expect(screen.getByText(/Citadel/i)).toBeInTheDocument();
    expect(screen.getByText(/Compromised/i)).toBeInTheDocument();
  });

  test('renders correct status colors', () => {
    render(<SafeZones zones={mockZones} />);
    expect(screen.getByText(/Stable/i)).toHaveClass('text-green-400');
    expect(screen.getByText(/Caution/i)).toHaveClass('text-yellow-400');
    expect(screen.getByText(/Compromised/i)).toHaveClass('text-red-400');
  });

  test('renders a message when there are no safe zones', () => {
    render(<SafeZones zones={[]} />);
    expect(screen.getByText(/No safe zones currently registered/i)).toBeInTheDocument();
  });

  test('renders correctly with a single safe zone', () => {
    const singleZone = [{ id: 1, name: 'Bunker', status: 'Stable' }];
    render(<SafeZones zones={singleZone} />);
    expect(screen.getByText(/Bunker/i)).toBeInTheDocument();
    expect(screen.getByText(/Stable/i)).toBeInTheDocument();
  });
});
