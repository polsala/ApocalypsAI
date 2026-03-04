import { render, screen, waitFor } from '@testing-library/react';
import App from '../src/App';
import mockEchoData from '../src/data/mockEchoData'; // Import mock data

// Mock rationale: We are testing the React component's rendering logic
// based on data it receives. Directly importing mockEchoData ensures
// deterministic test results without relying on actual network requests
// or complex mocking of the global fetch API. The setTimeout in App.js
// is also mocked implicitly by the test runner's fake timers if needed,
// but for this simple case, we just need to wait for the data to appear.

describe('App Component', () => {
  test('renders header and footer', async () => {
    render(<App />);
    expect(screen.getByText(/Temporal Echo Visualizer/i)).toBeInTheDocument();
    expect(screen.getByText(/Monitoring the fabric of spacetime for anomalies./i)).toBeInTheDocument();
    expect(screen.getByText(/ApocalypsAI Nightly Integrator/i)).toBeInTheDocument();
  });

  test('displays "Scanning for temporal echoes..." initially and then echoes', async () => {
    render(<App />);
    expect(screen.getByText(/Scanning for temporal echoes.../i)).toBeInTheDocument();

    // Wait for the mock data to be "fetched" and rendered
    await waitFor(() => {
      expect(screen.queryByText(/Scanning for temporal echoes.../i)).not.toBeInTheDocument();
      expect(screen.getByText(/Faint echo of a forgotten tea party./i)).toBeInTheDocument();
      expect(screen.getByText(/Minor temporal displacement detected near the old library./i)).toBeInTheDocument();
      expect(screen.getByText(/A chicken and egg situation, but with timelines. High priority!/i)).toBeInTheDocument();
    }, { timeout: 1000 }); // Increased timeout to account for the 500ms simulated delay
  });

  test('renders correct number of echo cards', async () => {
    render(<App />);
    await waitFor(() => {
      const echoCards = screen.getAllByText(/Echo at/i); // Find elements containing "Echo at"
      expect(echoCards.length).toBe(mockEchoData.length);
    }, { timeout: 1000 });
  });

  test('displays correct icons for echo types', async () => {
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText('👻')).toBeInTheDocument(); // Whisper
      expect(screen.getByText('🌊')).toBeInTheDocument(); // Ripple
      expect(screen.getByText('👾')).toBeInTheDocument(); // Glitch
      expect(screen.getByText('🌀')).toBeInTheDocument(); // Paradox
    }, { timeout: 1000 });
  });
});
