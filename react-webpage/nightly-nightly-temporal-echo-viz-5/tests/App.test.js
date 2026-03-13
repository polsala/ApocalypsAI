import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: date-fns functions are pure and deterministic, no need to mock them directly.
// We are testing the integration of these functions within the React component's logic.

describe('App Component', () => {
  test('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Temporal Echo Visualizer/i)).toBeInTheDocument();
  });

  test('handles valid JSON input and displays events', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your timestamped event JSON here/i);
    const button = screen.getByText(/Visualize Echoes/i);

    const validJson = `[\n      {"timestamp": "2024-01-01T10:00:00Z", "event": "Anomaly"},\n      {"timestamp": "2024-01-02T10:00:00Z", "event": "Resource Drop"}\n    ]`;
    fireEvent.change(textarea, { target: { value: validJson } });
    fireEvent.click(button);

    expect(screen.queryByText(/Failed to parse data/i)).not.toBeInTheDocument();
    expect(screen.getByText(/Event Timeline/i)).toBeInTheDocument();
    // Check if event types are rendered (EchoVisualizer will render them)
    expect(screen.getByText(/Anomaly/i)).toBeInTheDocument();
    expect(screen.getByText(/Resource Drop/i)).toBeInTheDocument();
  });

  test('handles invalid JSON input and displays error', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your timestamped event JSON here/i);
    const button = screen.getByText(/Visualize Echoes/i);

    const invalidJson = `[{ "timestamp": "invalid-date", "event": "Test" }]`;
    fireEvent.change(textarea, { target: { value: invalidJson } });
    fireEvent.click(button);

    expect(screen.getByText(/Failed to parse data: Invalid timestamp format for: invalid-date/i)).toBeInTheDocument();
    expect(screen.queryByText(/Event Timeline/i)).not.toBeInTheDocument();
  });

  test('detects and displays echoes correctly', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your timestamped event JSON here/i);
    const button = screen.getByText(/Visualize Echoes/i);

    const echoJson = `[\n      {"timestamp": "2024-01-01T00:00:00Z", "event": "Whispers"},\n      {"timestamp": "2024-01-03T00:00:00Z", "event": "Whispers"},\n      {"timestamp": "2024-01-05T00:00:00Z", "event": "Whispers"},\n      {"timestamp": "2024-01-02T00:00:00Z", "event": "Anomaly"}\n    ]`;
    fireEvent.change(textarea, { target: { value: echoJson } });
    fireEvent.click(button);

    expect(screen.getByText(/'Whispers' echoes every 2 days \(observed 3 times\)./i)).toBeInTheDocument();
    expect(screen.queryByText(/'Anomaly' echoes/i)).not.toBeInTheDocument(); // Anomaly only appears once, no echo
  });

  test('does not detect echo for single event type', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your timestamped event JSON here/i);
    const button = screen.getByText(/Visualize Echoes/i);

    const singleEventJson = `[\n      {"timestamp": "2024-01-01T00:00:00Z", "event": "Whispers"}\n    ]`;
    fireEvent.change(textarea, { target: { value: singleEventJson } });
    fireEvent.click(button);

    expect(screen.queryByText(/Detected Echoes:/i)).not.toBeInTheDocument();
  });

  test('does not detect echo if intervals are not consistent', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your timestamped event JSON here/i);
    const button = screen.getByText(/Visualize Echoes/i);

    const inconsistentEchoJson = `[\n      {"timestamp": "2024-01-01T00:00:00Z", "event": "Whispers"},\n      {"timestamp": "2024-01-03T00:00:00Z", "event": "Whispers"},\n      {"timestamp": "2024-01-07T00:00:00Z", "event": "Whispers"} // 2 days, then 4 days\n    ]`;
    fireEvent.change(textarea, { target: { value: inconsistentEchoJson } });
    fireEvent.click(button);

    expect(screen.queryByText(/Detected Echoes:/i)).not.toBeInTheDocument();
  });
});
