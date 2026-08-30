import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../src/App';

describe('App Component', () => {
  it('renders header and input form initially', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Echo Visualizer/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Paste Event JSON Data:/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Load Events/i })).toBeInTheDocument();
  });

  it('loads and displays events from valid JSON input', async () => {
    render(<App />);
    const jsonInput = screen.getByLabelText(/Paste Event JSON Data:/i);
    const loadButton = screen.getByRole('button', { name: /Load Events/i });

    const validJson = `[
      { "id": "test1", "timestamp": "2024-01-01T10:00:00Z", "type": "SensorRead" },
      { "id": "test2", "timestamp": "2024-01-01T10:05:00Z", "type": "SystemAlert" }
    ]`;

    fireEvent.change(jsonInput, { target: { value: validJson } });
    fireEvent.click(loadButton);

    // Mock rationale: We are testing the App's ability to process and display data,
    // not the actual date parsing or rendering of sub-components in isolation.
    // The `waitFor` ensures React state updates are processed.
    await waitFor(() => {
      expect(screen.getByText(/Event Timeline/i)).toBeInTheDocument();
      expect(screen.getByText(/SensorRead/i)).toBeInTheDocument();
      expect(screen.getByText(/SystemAlert/i)).toBeInTheDocument();
    });
  });

  it('displays an error for invalid JSON input', async () => {
    render(<App />);
    const jsonInput = screen.getByLabelText(/Paste Event JSON Data:/i);
    const loadButton = screen.getByRole('button', { name: /Load Events/i });

    const invalidJson = `[{ "id": "test1", "timestamp": "2024-01-01T10:00:00Z", "type": "SensorRead" }`; // Missing closing bracket

    fireEvent.change(jsonInput, { target: { value: invalidJson } });
    fireEvent.click(loadButton);

    // Mock rationale: Testing error message display based on JSON parsing failure.
    // No external dependencies, purely UI reaction to bad input.
    await waitFor(() => {
      expect(screen.getByText(/Failed to parse events:/i)).toBeInTheDocument();
      expect(screen.queryByText(/Event Timeline/i)).not.toBeInTheDocument();
    });
  });

  it('displays an error for non-array JSON input', async () => {
    render(<App />);
    const jsonInput = screen.getByLabelText(/Paste Event JSON Data:/i);
    const loadButton = screen.getByRole('button', { name: /Load Events/i });

    const nonArrayJson = `{ "id": "test1", "timestamp": "2024-01-01T10:00:00Z", "type": "SensorRead" }`; // Not an array

    fireEvent.change(jsonInput, { target: { value: nonArrayJson } });
    fireEvent.click(loadButton);

    await waitFor(() => {
      expect(screen.getByText(/Input must be a JSON array of events./i)).toBeInTheDocument();
    });
  });

  it('displays an error for events missing required fields', async () => {
    render(<App />);
    const jsonInput = screen.getByLabelText(/Paste Event JSON Data:/i);
    const loadButton = screen.getByRole('button', { name: /Load Events/i });

    const missingFieldJson = `[
      { "id": "test1", "timestamp": "2024-01-01T10:00:00Z" },
      { "id": "test2", "type": "SystemAlert" }
    ]`; // Missing type in first, timestamp in second

    fireEvent.change(jsonInput, { target: { value: missingFieldJson } });
    fireEvent.click(loadButton);

    await waitFor(() => {
      expect(screen.getByText(/Event at index 0 is missing 'timestamp' or 'type'./i)).toBeInTheDocument();
    });
  });

  it('displays an error for events with invalid timestamp', async () => {
    render(<App />);
    const jsonInput = screen.getByLabelText(/Paste Event JSON Data:/i);
    const loadButton = screen.getByRole('button', { name: /Load Events/i });

    const invalidTimestampJson = `[
      { "id": "test1", "timestamp": "not-a-date", "type": "SensorRead" }
    ]`;

    fireEvent.change(jsonInput, { target: { value: invalidTimestampJson } });
    fireEvent.click(loadButton);

    await waitFor(() => {
      expect(screen.getByText(/Event at index 0 has an invalid 'timestamp'./i)).toBeInTheDocument();
    });
  });
});
