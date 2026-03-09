import { render, screen } from '@testing-library/react';
import EchoDisplay from '../src/components/EchoDisplay'; // # Mock rationale: Testing the component in isolation with direct props.

describe('EchoDisplay Component', () => {
  const mockEcho = {
    id: 'test-echo-001',
    type: 'Test Anomaly',
    intensity: 5,
    timestamp: '2024-01-01T12:30:00Z',
    description: 'A simulated test echo for display.',
  };

  test('renders echo details correctly', () => {
    render(<EchoDisplay echo={mockEcho} />);

    expect(screen.getByText(/ID:/i)).toBeInTheDocument();
    expect(screen.getByText(mockEcho.id)).toBeInTheDocument();

    expect(screen.getByText(/Type:/i)).toBeInTheDocument();
    expect(screen.getByText(mockEcho.type)).toBeInTheDocument();

    expect(screen.getByText(/Intensity:/i)).toBeInTheDocument();
    expect(screen.getByText(mockEcho.intensity.toString())).toBeInTheDocument();

    expect(screen.getByText(/Timestamp:/i)).toBeInTheDocument();
    // Check for a part of the formatted timestamp, as toLocaleString can vary slightly
    expect(screen.getByText(/1\/1\/2024/i)).toBeInTheDocument();

    expect(screen.getByText(/Description:/i)).toBeInTheDocument();
    expect(screen.getByText(mockEcho.description)).toBeInTheDocument();
  });
});
