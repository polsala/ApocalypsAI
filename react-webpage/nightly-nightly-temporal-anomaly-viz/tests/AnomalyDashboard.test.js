import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import AnomalyDashboard from '../src/components/AnomalyDashboard';
import mockAnomalies from '../src/data/mockAnomalies'; // # Mock rationale: Directly importing mock data to ensure deterministic and offline testing without network requests.

// Mock the setTimeout used in AnomalyDashboard to simulate async data loading
jest.useFakeTimers();

describe('AnomalyDashboard', () => {
  test('renders loading state initially', () => {
    render(<AnomalyDashboard />);
    expect(screen.getByText(/Loading temporal anomalies.../i)).toBeInTheDocument();
  });

  test('renders anomalies after loading', async () => {
    render(<AnomalyDashboard />);
    jest.runAllTimers(); // Advance timers to resolve the simulated data fetch

    await waitFor(() => {
      expect(screen.getByText(/Anomaly ID: TA-001/i)).toBeInTheDocument();
      expect(screen.getByText(/Anomaly ID: TA-002/i)).toBeInTheDocument();
      expect(screen.getByText(/Anomaly ID: TA-003/i)).toBeInTheDocument();
      expect(screen.getByText(/Anomaly ID: TA-004/i)).toBeInTheDocument();
      expect(screen.getByText(/Anomaly ID: TA-005/i)).toBeInTheDocument();
    });
  });

  test('displays correct anomaly details', async () => {
    render(<AnomalyDashboard />);
    jest.runAllTimers();

    await waitFor(() => {
      const anomaly1 = mockAnomalies[0];
      expect(screen.getByText(`Type: ${anomaly1.type}`)).toBeInTheDocument();
      expect(screen.getByText(`Severity: ${anomaly1.severity}`)).toBeInTheDocument();
    });
  });

  test('stabilize button works and changes text', async () => {
    render(<AnomalyDashboard />);
    jest.runAllTimers();

    await waitFor(() => {
      const stabilizeButton = screen.getAllByText(/Stabilize Anomaly/i)[0];
      fireEvent.click(stabilizeButton);
      expect(stabilizeButton).toHaveTextContent('Stabilized');
      expect(stabilizeButton).toBeDisabled();
    });
  });

  test('renders "No temporal anomalies detected" when no data', async () => {
    // # Mock rationale: Overriding mockAnomalies to be empty for this specific test case.
    jest.spyOn(require('../src/data/mockAnomalies'), 'default', 'get').mockReturnValueOnce([]);

    render(<AnomalyDashboard />);
    jest.runAllTimers();

    await waitFor(() => {
      expect(screen.getByText(/No temporal anomalies detected. All clear!/i)).toBeInTheDocument();
    });
  });
});
