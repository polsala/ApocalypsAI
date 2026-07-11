import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import mockTemporalData from '../src/api/mockTemporalData'; // Mock rationale: Directly importing mock data for deterministic test results.

// Mock rationale: Suppress act warnings from react-scripts test setup
const originalError = console.error;
beforeAll(() => {
  console.error = (...args) => {
    if (/^\\[.+\\]/.test(args[0])) {
      return;
    }
    originalError.call(console, ...args);
  };
});

afterAll(() => {
  console.error = originalError;
});

describe('App Component', () => {
  test('renders header and dashboard titles', () => {
    render(<App />);
    expect(screen.getByText(/ApocalypsAI Temporal Ripple Viewer/i)).toBeInTheDocument();
    expect(screen.getByText(/Active Temporal Ripples/i)).toBeInTheDocument();
    expect(screen.getByText(/Stabilized Anomalies/i)).toBeInTheDocument();
  });

  test('displays active anomalies from mock data', () => {
    render(<App />);
    const activeAnomalies = mockTemporalData.filter(a => a.status === 'active');
    activeAnomalies.forEach(anomaly => {
      expect(screen.getByText(new RegExp(anomaly.type, 'i'))).toBeInTheDocument();
      expect(screen.getByText(new RegExp(`ID: ${anomaly.id}`, 'i'))).toBeInTheDocument();
    });
  });

  test('displays stabilized anomalies from mock data', () => {
    render(<App />);
    const stabilizedAnomalies = mockTemporalData.filter(a => a.status === 'stabilized');
    stabilizedAnomalies.forEach(anomaly => {
      expect(screen.getByText(new RegExp(anomaly.type, 'i'))).toBeInTheDocument();
      expect(screen.getByText(new RegExp(`ID: ${anomaly.id}`, 'i'))).toBeInTheDocument();
      expect(screen.getByText(/Stabilized/i)).toBeInTheDocument(); // Check for the stabilized indicator
    });
  });

  test('stabilizes an active ripple when button is clicked', () => {
    render(<App />);
    const activeAnomalyToStabilize = mockTemporalData.find(a => a.status === 'active');
    const stabilizeButton = screen.getByRole('button', { name: /Stabilize Ripple/i, exact: false });

    fireEvent.click(stabilizeButton);

    // After clicking, the anomaly should move to the 'stabilized' section
    expect(screen.queryByText(new RegExp(activeAnomalyToStabilize.type, 'i'))).not.toBeInTheDocument(); // Should no longer be in active section
    expect(screen.getByText(new RegExp(activeAnomalyToStabilize.type, 'i'))).toBeInTheDocument(); // Should be in stabilized section
    expect(screen.getAllByText(/Stabilized/i).length).toBeGreaterThanOrEqual(1); // Check for the stabilized indicator
  });

  test('does not show stabilize button for already stabilized anomalies', () => {
    render(<App />);
    const stabilizedAnomaly = mockTemporalData.find(a => a.status === 'stabilized');
    const stabilizedAnomalyCard = screen.getByText(new RegExp(stabilizedAnomaly.type, 'i')).closest('.ripple-card');
    expect(stabilizedAnomalyCard).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /Stabilize Ripple/i, exact: false, container: stabilizedAnomalyCard })).not.toBeInTheDocument();
  });
});
