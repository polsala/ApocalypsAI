import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import App from '../src/App';
import React from 'react';

// Mock the fetchAnomalies function directly
// Mock rationale: The fetchAnomalies function is mocked to provide a consistent
// and predictable dataset for testing. This ensures tests are deterministic,
// run offline, and do not depend on external API availability or network latency.
jest.mock('../src/App', () => {
  const originalModule = jest.requireActual('../src/App');
  return {
    __esModule: true,
    ...originalModule,
    fetchAnomalies: jest.fn(() =>
      new Promise(resolve => {
        setTimeout(() => {
          resolve([
            { id: 'TEST-001', type: 'Test Drift', severity: 'Low', status: 'Unstable' },
            { id: 'TEST-002', type: 'Test Echo', severity: 'Medium', status: 'Stabilizing' },
          ]);
        }, 10); // Simulate minimal network delay
      })
    ),
  };
});

// Import the mocked function to reset it between tests
import { fetchAnomalies } from '../src/App';

describe('App Component', () => {
  beforeEach(() => {
    // Reset the mock before each test to ensure isolation
    fetchAnomalies.mockClear();
    fetchAnomalies.mockImplementation(() =>
      new Promise(resolve => {
        setTimeout(() => {
          resolve([
            { id: 'TEST-001', type: 'Test Drift', severity: 'Low', status: 'Unstable' },
            { id: 'TEST-002', type: 'Test Echo', severity: 'Medium', status: 'Stabilizing' },
          ]);
        }, 10);
      })
    );
  });

  test('renders Chrono-Compass title', async () => {
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText(/Nightly Chrono-Compass 🧭/i)).toBeInTheDocument();
    });
  });

  test('displays loading message initially', () => {
    // Temporarily override mock to never resolve to keep it in loading state
    fetchAnomalies.mockImplementationOnce(() => new Promise(() => {}));
    render(<App />);
    expect(screen.getByText(/Calibrating temporal sensors.../i)).toBeInTheDocument();
  });

  test('displays mock anomalies after loading', async () => {
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText(/TEST-001 - Test Drift/i)).toBeInTheDocument();
      expect(screen.getByText(/Severity: Low/i)).toBeInTheDocument();
      expect(screen.getByText(/Status: Unstable/i)).toBeInTheDocument();

      expect(screen.getByText(/TEST-002 - Test Echo/i)).toBeInTheDocument();
      expect(screen.getByText(/Severity: Medium/i)).toBeInTheDocument();
      expect(screen.getByText(/Status: Stabilizing/i)).toBeInTheDocument();
    });
  });

  test('stabilize all button changes status from Unstable to Stabilizing then Stabilized', async () => {
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(/TEST-001 - Test Drift/i)).toBeInTheDocument();
      expect(screen.getByText(/Status: Unstable/i)).toBeInTheDocument();
    });

    const stabilizeButton = screen.getByRole('button', { name: /Initiate Global Stabilization/i });
    fireEvent.click(stabilizeButton);

    await waitFor(() => {
      expect(screen.queryByText(/Status: Unstable/i)).not.toBeInTheDocument(); // TEST-001 should no longer be unstable
      expect(screen.getAllByText(/Status: Stabilizing/i).length).toBe(2); // Both should now be stabilizing
    });

    // Wait for the second phase of stabilization
    await waitFor(() => {
      expect(screen.queryByText(/Status: Stabilizing/i)).not.toBeInTheDocument(); // Should be gone
      expect(screen.getAllByText(/Status: Stabilized/i).length).toBe(2); // Both should be stabilized
    }, { timeout: 2000 }); // Increased timeout for the two-phase async update
  });

  test('stabilize all button is disabled when all anomalies are stabilized', async () => {
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(/Status: Unstable/i)).toBeInTheDocument();
    });

    const stabilizeButton = screen.getByRole('button', { name: /Initiate Global Stabilization/i });
    fireEvent.click(stabilizeButton); // First click to make them stabilizing

    await waitFor(() => {
      expect(screen.getAllByText(/Status: Stabilizing/i).length).toBe(2);
    });

    // Wait for the second phase to complete
    await waitFor(() => {
      expect(screen.getAllByText(/Status: Stabilized/i).length).toBe(2);
    }, { timeout: 2000 });

    expect(stabilizeButton).toBeDisabled();
  });
});
