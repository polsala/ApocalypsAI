import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: No external API calls, but we want to ensure the App component
// correctly interacts with its sub-components and the TemporalProcessor logic.
// We'll test the integration by simulating user input and checking the rendered output.
// The TemporalProcessor functions are pure and tested separately for determinism.

describe('App', () => {
  test('renders header and input field', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Echo Visualizer/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Enter text to see its temporal echoes.../i)).toBeInTheDocument();
  });

  test('displays initial message when input is empty', () => {
    render(<App />);
    expect(screen.getByText(/Start typing to see echoes./i)).toBeInTheDocument();
  });

  test('generates and displays echoes after typing', async () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Enter text to see its temporal echoes.../i);
    fireEvent.change(textarea, { target: { value: 'Hello World' } });

    // Wait for the debounced input to process and echoes to appear
    await waitFor(() => {
      expect(screen.queryByText(/Start typing to see echoes./i)).not.toBeInTheDocument();
      // Expect at least one echo to be displayed. The exact text will vary due to transformations.
      // We check for the presence of the echo-item class or a general text presence.
      const echoItems = screen.getAllByText(/hello world/i, { exact: false }); // Case-insensitive check
      expect(echoItems.length).toBeGreaterThan(0);
      expect(screen.getByText(/Temporal Stability:/i)).toBeInTheDocument();
    }, { timeout: 1000 }); // Increased timeout for debounce
  });

  test('stability meter updates with input', async () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Enter text to see its temporal echoes.../i);

    fireEvent.change(textarea, { target: { value: 'Short' } });
    await waitFor(() => {
      expect(screen.getByText(/Stable/i)).toBeInTheDocument();
    }, { timeout: 1000 });

    fireEvent.change(textarea, { target: { value: 'This is a much longer and more complex sentence to test the stability calculation.' } });
    await waitFor(() => {
      expect(screen.getByText(/Unstable/i)).toBeInTheDocument();
    }, { timeout: 1000 });
  });

  test('clears echoes when input is cleared', async () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Enter text to see its temporal echoes.../i);
    fireEvent.change(textarea, { target: { value: 'Some text' } });

    await waitFor(() => {
      expect(screen.queryByText(/Start typing to see echoes./i)).not.toBeInTheDocument();
    }, { timeout: 1000 });

    fireEvent.change(textarea, { target: { value: '' } });

    await waitFor(() => {
      expect(screen.getByText(/Start typing to see echoes./i)).toBeInTheDocument();
      expect(screen.queryAllByText(/some text/i, { exact: false }).length).toBe(0);
    }, { timeout: 1000 });
  });
});
