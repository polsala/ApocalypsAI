import { render, screen } from '@testing-library/react';
import TemporalEchoDisplay from '../src/TemporalEchoDisplay';

describe('TemporalEchoDisplay', () => {
  const mockEchoes = [
    {
      id: 'test-echo-1',
      timestamp: '2024-07-20T12:00:00Z',
      magnitude: 0.8,
      type: 'Minor Ripple',
      description: 'A small test ripple.'
    },
    {
      id: 'test-echo-2',
      timestamp: '2024-07-20T13:30:00Z',
      magnitude: 1.5,
      type: 'Temporal Glitch',
      description: 'A significant test glitch.'
    }
  ];

  test('renders the list of echoes correctly', () => {
    // # Mock rationale: Provides sample temporal echo data to verify that the component correctly
    // # processes and displays the information it receives, without relying on external data sources.
    render(<TemporalEchoDisplay echoes={mockEchoes} />);

    // Check if the heading is present
    expect(screen.getByText(/Detected Echoes/i)).toBeInTheDocument();

    // Check if each echo item is rendered with its details
    expect(screen.getByText(/Minor Ripple/i)).toBeInTheDocument();
    expect(screen.getByText(/A small test ripple./i)).toBeInTheDocument();
    expect(screen.getByText(/Magnitude: 0.80/i)).toBeInTheDocument();

    expect(screen.getByText(/Temporal Glitch/i)).toBeInTheDocument();
    expect(screen.getByText(/A significant test glitch./i)).toBeInTheDocument();
    expect(screen.getByText(/Magnitude: 1.50/i)).toBeInTheDocument();

    // Check for correct timestamp formatting (using toLocaleString, which depends on locale, so partial match)
    const timestamp1 = screen.getByText(new RegExp(new Date('2024-07-20T12:00:00Z').getFullYear().toString()));
    expect(timestamp1).toBeInTheDocument();
  });

  test('renders no echoes message if array is empty', () => {
    render(<TemporalEchoDisplay echoes={[]} />);
    // The App.js handles the 'no echoes' message, this component just renders an empty list
    expect(screen.getByText(/Detected Echoes/i)).toBeInTheDocument();
    expect(screen.queryByRole('listitem')).not.toBeInTheDocument();
  });
});
