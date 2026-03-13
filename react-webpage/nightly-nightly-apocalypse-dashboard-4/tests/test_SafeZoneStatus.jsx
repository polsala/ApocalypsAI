import React from 'react';
import { render, screen } from '@testing-library/react';
import SafeZoneStatus from '../src/components/SafeZoneStatus';

describe('SafeZoneStatus Component', () => {
  it('renders the title', () => {
    render(<SafeZoneStatus data={[]} />);
    expect(screen.getByText('Safe Zone Status')).toBeInTheDocument();
  });

  it('renders multiple safe zones correctly', () => {
    const mockData = [
      { name: 'Fortress Alpha', status: 'Secure', capacity: 200 },
      { name: 'Sanctuary City', status: 'Secure', capacity: 300 },
      { name: 'Underground Bunker 7', status: 'Compromised', capacity: 50 }
    ];
    render(<SafeZoneStatus data={mockData} />);

    expect(screen.getByText('Fortress Alpha')).toBeInTheDocument();
    expect(screen.getByText('Secure')).toBeInTheDocument();
    expect(screen.getByText('Capacity: 200')).toBeInTheDocument();

    expect(screen.getByText('Sanctuary City')).toBeInTheDocument();
    expect(screen.getByText('Secure')).toBeInTheDocument();
    expect(screen.getByText('Capacity: 300')).toBeInTheDocument();

    expect(screen.getByText('Underground Bunker 7')).toBeInTheDocument();
    expect(screen.getByText('Compromised')).toBeInTheDocument();
    expect(screen.getByText('Capacity: 50')).toBeInTheDocument();
  });

  it('renders a message when no data is provided', () => {
    render(<SafeZoneStatus data={[]} />);
    expect(screen.getByText('No safe zones identified. The world is a wasteland...')).toBeInTheDocument();
  });

  it('renders a message when data is null', () => {
    render(<SafeZoneStatus data={null} />);
    expect(screen.getByText('No safe zones identified. The world is a wasteland...')).toBeInTheDocument();
  });
});
