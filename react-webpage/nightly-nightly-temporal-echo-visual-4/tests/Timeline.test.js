import { render, screen } from '@testing-library/react';
import Timeline from '../src/components/Timeline';

describe('Timeline Component', () => {
  const mockEvents = [
    { id: 'e1', timestamp: '2024-01-01T10:00:00Z', type: 'SensorRead', value: 25.5 },
    { id: 'e3', timestamp: '2024-01-01T10:10:00Z', type: 'SensorRead', value: 26.1 },
    { id: 'e2', timestamp: '2024-01-01T10:05:00Z', type: 'SystemAlert', message: 'Temp high' }
  ];

  it('renders all provided events', () => {
    render(<Timeline events={mockEvents} />);
    // Mock rationale: Using static mock data to ensure component renders correctly.
    // No external dependencies or side effects are involved.
    expect(screen.getByText(/SensorRead/i)).toBeInTheDocument();
    expect(screen.getByText(/SystemAlert/i)).toBeInTheDocument();
    expect(screen.getAllByText(/SensorRead/i).length).toBe(2);
  });

  it('sorts events by timestamp correctly', () => {
    render(<Timeline events={mockEvents} />);
    // Mock rationale: Verifying the order of rendered elements based on timestamps.
    // The `getAllByText` returns elements in DOM order, allowing us to check sorting.
    const eventTypes = screen.getAllByText(/SensorRead|SystemAlert/i).map(el => el.textContent);

    // Expected order: e1 (10:00), e2 (10:05), e3 (10:10)
    expect(eventTypes[0]).toBe('SensorRead'); // from e1
    expect(eventTypes[1]).toBe('SystemAlert'); // from e2
    expect(eventTypes[2]).toBe('SensorRead'); // from e3
  });

  it('renders no events when an empty array is provided', () => {
    render(<Timeline events={[]} />);
    // Mock rationale: Testing edge case of empty input.
    expect(screen.queryByText(/SensorRead/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/SystemAlert/i)).not.toBeInTheDocument();
  });
});
