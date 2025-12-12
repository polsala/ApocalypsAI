import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import * as AnomalyData from '../src/AnomalyData'; // Import the module to mock it

// Mock rationale: We want to test the App component's rendering and interaction
// with anomaly data without relying on actual external data fetching or modifying
// global state. Mocking AnomalyData ensures deterministic tests.
jest.mock('../src/AnomalyData', () => ({
  getAnomalies: jest.fn(() => [
    { id: 'test1', type: 'Temporal Ripple', location: 'Test Loc 1', severity: 'Minor', status: 'Active', coordinates: { lat: 10, lng: 20 }, description: 'Test anomaly 1' },
    { id: 'test2', type: 'Echo Cascade', location: 'Test Loc 2', severity: 'Moderate', status: 'Active', coordinates: { lat: 30, lng: 40 }, description: 'Test anomaly 2' }
  ]),
  stabilizeAnomaly: jest.fn((id) => {
    const anomalies = [
      { id: 'test1', type: 'Temporal Ripple', location: 'Test Loc 1', severity: 'Minor', status: 'Active', coordinates: { lat: 10, lng: 20 }, description: 'Test anomaly 1' },
      { id: 'test2', type: 'Echo Cascade', location: 'Test Loc 2', severity: 'Moderate', status: 'Active', coordinates: { lat: 30, lng: 40 }, description: 'Test anomaly 2' }
    ];
    const anomaly = anomalies.find(a => a.id === id);
    if (anomaly) {
      anomaly.status = 'Stabilized';
      anomaly.severity = 'Minor';
    }
    // Return the updated list for the subsequent getAnomalies call
    AnomalyData.getAnomalies.mockReturnValueOnce(anomalies);
    return anomaly;
  })
}));

describe('App', () => {
  beforeEach(() => {
    // Reset mocks before each test to ensure isolation
    AnomalyData.getAnomalies.mockClear();
    AnomalyData.stabilizeAnomaly.mockClear();
    // Set initial mock return value for getAnomalies
    AnomalyData.getAnomalies.mockReturnValue([
      { id: 'test1', type: 'Temporal Ripple', location: 'Test Loc 1', severity: 'Minor', status: 'Active', coordinates: { lat: 10, lng: 20 }, description: 'Test anomaly 1' },
      { id: 'test2', type: 'Echo Cascade', location: 'Test Loc 2', severity: 'Moderate', status: 'Active', coordinates: { lat: 30, lng: 40 }, description: 'Test anomaly 2' }
    ]);
    // Mock window.alert for stabilization
    jest.spyOn(window, 'alert').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('renders header and anomaly map', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Echo Map/i)).toBeInTheDocument();
    expect(screen.getByText(/Visualizing Chronal Disturbances/i)).toBeInTheDocument();
    expect(screen.getByText(/Anomaly Log/i)).toBeInTheDocument();
    expect(screen.getByText(/Temporal Ripple/i)).toBeInTheDocument();
    expect(screen.getByText(/Echo Cascade/i)).toBeInTheDocument();
  });

  test('stabilizes an anomaly when button is clicked', () => {
    render(<App />);

    // Find the stabilize button for 'test1'
    const stabilizeButton = screen.getAllByText('Stabilize')[0]; // Assuming 'test1' is the first active anomaly
    fireEvent.click(stabilizeButton);

    // Expect stabilizeAnomaly to have been called
    expect(AnomalyData.stabilizeAnomaly).toHaveBeenCalledWith('test1');

    // Expect alert to have been called
    expect(window.alert).toHaveBeenCalledWith('Anomaly test1 has been stabilized!');

    // The current mock setup for `stabilizeAnomaly` directly updates the `getAnomalies` mock
    // for the *next* call, which is what happens in `handleStabilize`.
    // We need to ensure the UI reflects this.
    expect(screen.getByText(/Temporal Ripple at Test Loc 1 \(Severity: Minor, Status: Stabilized\)/i)).toBeInTheDocument();
  });

  test('displays "No anomalies detected" when there are no anomalies', () => {
    // Mock rationale: Test the empty state of the anomaly list.
    AnomalyData.getAnomalies.mockReturnValueOnce([]);
    render(<App />);
    expect(screen.getByText(/No anomalies detected\. All clear\.\.\. for now\./i)).toBeInTheDocument();
  });
});
