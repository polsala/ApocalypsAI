import { render, screen } from '@testing-library/react';
import EchoVisualizer from '../src/components/EchoVisualizer';
import { parseISO } from 'date-fns';

// Mock rationale: The EchoVisualizer component uses `useRef` and `clientWidth` for responsive sizing.
// In a real browser environment, this works. For Jest/JSDOM, `clientWidth` is 0 by default.
// We mock `HTMLElement.prototype.clientWidth` to provide a non-zero value for testing rendering logic.
// date-fns functions are pure and deterministic, no need to mock them directly.

Object.defineProperty(HTMLElement.prototype, 'clientWidth', {
  configurable: true,
  value: 800, // Mock a fixed width for testing purposes
});

describe('EchoVisualizer Component', () => {
  const mockEvents = [
    { timestamp: '2024-01-01T10:00:00Z', event: 'Anomaly', date: parseISO('2024-01-01T10:00:00Z') },
    { timestamp: '2024-01-04T10:00:00Z', event: 'Anomaly', date: parseISO('2024-01-04T10:00:00Z') },
    { timestamp: '2024-01-02T14:30:00Z', event: 'Resource Drop', date: parseISO('2024-01-02T14:30:00Z') },
  ];

  const mockEchoes = {
    'Anomaly': { interval: 3, count: 2 } // 2 events, 1 interval. For 3 events, 2 intervals.
  };

  test('renders without crashing with empty events', () => {
    render(<EchoVisualizer events={[]} echoes={{}} />);
    expect(screen.getByText(/No events to display or container not ready./i)).toBeInTheDocument();
  });

  test('renders events as circles on the SVG', () => {
    const { container } = render(<EchoVisualizer events={mockEvents} echoes={{}} />);
    const circles = container.querySelectorAll('circle');
    expect(circles.length).toBe(mockEvents.length);

    // Check if event types are rendered as labels
    expect(screen.getByText(/Anomaly/i)).toBeInTheDocument();
    expect(screen.getByText(/Resource Drop/i)).toBeInTheDocument();
  });

  test('renders echo lines when echoes are present', () => {
    const eventsWithEcho = [
      { timestamp: '2024-01-01T10:00:00Z', event: 'Whispers', date: parseISO('2024-01-01T10:00:00Z') },
      { timestamp: '2024-01-03T10:00:00Z', event: 'Whispers', date: parseISO('2024-01-03T10:00:00Z') },
      { timestamp: '2024-01-05T10:00:00Z', event: 'Whispers', date: parseISO('2024-01-05T10:00:00Z') },
    ];
    const echoesForWhispers = {
      'Whispers': { interval: 2, count: 3 } // 3 events, 2 intervals of 2 days
    };

    const { container } = render(<EchoVisualizer events={eventsWithEcho} echoes={echoesForWhispers} />);
    const echoLines = container.querySelectorAll('line[stroke="#ffeb3b"]');
    expect(echoLines.length).toBe(2); // Two segments for a 3-event echo
    expect(echoLines[0]).toHaveAttribute('title', 'Echo: Whispers every 2 days');
  });

  test('renders x-axis labels', () => {
    render(<EchoVisualizer events={mockEvents} echoes={{}} />);
    expect(screen.getByText(/Jan 01/i)).toBeInTheDocument();
    expect(screen.getByText(/Jan 04/i)).toBeInTheDocument();
  });
});
