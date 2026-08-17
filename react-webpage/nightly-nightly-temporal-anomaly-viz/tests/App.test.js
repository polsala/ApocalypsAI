import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../src/App';

// Mock rationale: We are testing the App component's rendering and state management
// based on initial data, not actual API calls. Using a direct import of mock data
// ensures deterministic and offline testing.
jest.mock('../src/data/anomalies.json', () => ([
  {
    "id": "test-a001",
    "timestamp": "2024-07-20T10:30:00Z",
    "type": "Test Ripple",
    "location": "Test Sector",
    "severity": "Mild Wobble",
    "impact": "Test Deja Vu",
    "description": "A test ripple."
  },
  {
    "id": "test-a002",
    "timestamp": "2024-07-19T23:15:00Z",
    "type": "Test Bloom",
    "location": "Test Woods",
    "severity": "Significant Jiggle",
    "impact": "Test Lost Keys",
    "description": "A test bloom."
  }
]));

describe('App', () => {
  test('renders header and anomaly sections', async () => {
    render(<App />);
    expect(screen.getByText(/Nightly Temporal Anomaly Visualizer/i)).toBeInTheDocument();
    expect(screen.getByText(/Detected Anomalies/i)).toBeInTheDocument();
    expect(screen.getByText(/Anomaly Details/i)).toBeInTheDocument();

    // Wait for anomalies to load and render
    await waitFor(() => {
      expect(screen.getByText(/Test Ripple/i)).toBeInTheDocument();
      expect(screen.getByText(/Test Bloom/i)).toBeInTheDocument();
    });
  });

  test('displays "No anomaly selected" initially in details section', () => {
    render(<App />);
    expect(screen.getByText(/Select an anomaly from the timeline to view its intricate details./i)).toBeInTheDocument();
  });

  test('selects an anomaly and displays its details', async () => {
    render(<App />);

    // Wait for anomalies to load and render
    await waitFor(() => {
      expect(screen.getByText(/Test Ripple/i)).toBeInTheDocument();
    });

    // Click on the first anomaly
    userEvent.click(screen.getByText(/Test Ripple/i));

    // Check if details are displayed
    await waitFor(() => {
      expect(screen.getByText(/Test Ripple/i)).toBeInTheDocument(); // In card
      expect(screen.getByText(/Location: Test Sector/i)).toBeInTheDocument();
      expect(screen.getByText(/Severity: Mild Wobble/i)).toBeInTheDocument();
      expect(screen.getByText(/Potential Impact: Test Deja Vu/i)).toBeInTheDocument();
    });
  });
});
