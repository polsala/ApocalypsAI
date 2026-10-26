import React from 'react';
import { render, screen } from '@testing-library/react';
import WandererStatus from '../src/components/WandererStatus';

describe('WandererStatus Component', () => {
  test('renders "No wanderers currently being tracked" when no wanderers are provided', () => {
    render(<WandererStatus wanderers={[]} />);
    expect(screen.getByText(/No wanderers currently being tracked/i)).toBeInTheDocument();
  });

  test('renders a list of wanderers with their details', () => {
    const mockWanderers = [
      { id: 'W001', name: 'Ragnar', status: 'Scavenging', location: 'Ruined City' },
      { id: 'W002', name: 'Seraphina', status: 'Fortifying', location: 'Underground Bunker' }
    ];
    render(<WandererStatus wanderers={mockWanderers} />);

    expect(screen.getByText(/Ragnar/i)).toBeInTheDocument();
    expect(screen.getByText(/W001/i)).toBeInTheDocument();
    expect(screen.getByText(/Scavenging/i)).toBeInTheDocument();
    expect(screen.getByText(/Ruined City/i)).toBeInTheDocument();

    expect(screen.getByText(/Seraphina/i)).toBeInTheDocument();
    expect(screen.getByText(/W002/i)).toBeInTheDocument();
    expect(screen.getByText(/Fortifying/i)).toBeInTheDocument();
    expect(screen.getByText(/Underground Bunker/i)).toBeInTheDocument();
  });

  test('renders wanderer details correctly', () => {
    const mockWanderer = {
      id: 'W003',
      name: 'Gizmo',
      status: 'Observing',
      location: 'Radio Tower'
    };
    render(<WandererStatus wanderers={[mockWanderer]} />);

    expect(screen.getByText(/Gizmo/i)).toBeInTheDocument();
    expect(screen.getByText(/W003/i)).toBeInTheDocument();
    expect(screen.getByText(/Observing/i)).toBeInTheDocument();
    expect(screen.getByText(/Radio Tower/i)).toBeInTheDocument();
  });
});
