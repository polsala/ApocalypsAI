import React from 'react';
import { render, screen } from '@testing-library/react';
import EventDisplay from '../src/components/EventDisplay';

describe('EventDisplay Component', () => {
  test('renders "No current apocalyptic events" when no events are provided', () => {
    render(<EventDisplay events={[]} />);
    expect(screen.getByText(/No current apocalyptic events detected/i)).toBeInTheDocument();
  });

  test('renders a list of events when provided', () => {
    const mockEvents = [
      { id: 1, type: 'Meteor Shower', intensity: 'High', timestamp: 1678886400000 },
      { id: 2, type: 'Zombie Outbreak', location: 'Sector 7G', timestamp: 1678886500000 }
    ];
    render(<EventDisplay events={mockEvents} />);

    expect(screen.getByText(/Meteor Shower/i)).toBeInTheDocument();
    expect(screen.getByText(/Zombie Outbreak/i)).toBeInTheDocument();
    expect(screen.getByText(/High/i)).toBeInTheDocument();
    expect(screen.getByText(/Sector 7G/i)).toBeInTheDocument();
    expect(screen.getByText(/Occurred: 3/15/2023, 12:00:00 PM/i)).toBeInTheDocument(); // Assuming locale formatting
    expect(screen.getByText(/Occurred: 3/15/2023, 12:01:40 PM/i)).toBeInTheDocument(); // Assuming locale formatting
  });

  test('renders event details correctly', () => {
    const mockEvent = {
      id: 3,
      type: 'Alien Abduction',
      details: 'A small, green one.',
      timestamp: 1678886600000
    };
    render(<EventDisplay events={[mockEvent]} />);

    expect(screen.getByText(/Alien Abduction/i)).toBeInTheDocument();
    expect(screen.getByText(/A small, green one./i)).toBeInTheDocument();
    expect(screen.getByText(/Occurred: 3/15/2023, 12:03:20 PM/i)).toBeInTheDocument(); // Assuming locale formatting
  });
});
