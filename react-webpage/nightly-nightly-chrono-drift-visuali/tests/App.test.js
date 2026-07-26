import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import mockAnomalies from '../src/data/mockAnomalies'; // Mock rationale: Use predefined mock data for deterministic tests.

describe('App', () => {
  test('renders the main header', () => {
    render(<App />);
    const headerElement = screen.getByText(/Nightly Chrono-Drift Visualizer/i);
    expect(headerElement).toBeInTheDocument();
  });

  test('renders all anomaly markers from mock data', () => {
    render(<App />);
    // Expect a marker for each anomaly in mockAnomalies
    mockAnomalies.forEach(anomaly => {
      const marker = screen.getByTitle(anomaly.name);
      expect(marker).toBeInTheDocument();
      expect(marker).toHaveClass(`severity-${anomaly.severity}`);
    });
    expect(screen.getAllByText(/\d{3}/).length).toBe(mockAnomalies.length); // Check for ID parts like '001', '002'
  });

  test('displays "Select an anomaly to view details." initially', () => {
    render(<App />);
    const initialDetailsText = screen.getByText(/Select an anomaly to view details./i);
    expect(initialDetailsText).toBeInTheDocument();
  });

  test('displays anomaly details when a marker is clicked', () => {
    render(<App />);
    const firstAnomaly = mockAnomalies[0];
    const marker = screen.getByTitle(firstAnomaly.name);

    fireEvent.click(marker);

    // Check if details for the first anomaly are displayed
    expect(screen.getByText(`Anomaly: ${firstAnomaly.name}`)).toBeInTheDocument();
    expect(screen.getByText(`ID: ${firstAnomaly.id}`)).toBeInTheDocument();
    expect(screen.getByText(`Severity: ${firstAnomaly.severity.toUpperCase()}`)).toBeInTheDocument();
    expect(screen.getByText(`Resonance Frequency: ${firstAnomaly.resonanceFrequency}`)).toBeInTheDocument();
    expect(screen.getByText(`Drift Magnitude: ${firstAnomaly.driftMagnitude}`)).toBeInTheDocument();
    expect(screen.getByText(`Estimated Impact Radius: ${firstAnomaly.impactRadius}`)).toBeInTheDocument();
    expect(screen.getByText(`Description: ${firstAnomaly.description}`)).toBeInTheDocument();
  });

  test('clicking a different marker updates the displayed details', () => {
    render(<App />);
    const firstAnomaly = mockAnomalies[0];
    const secondAnomaly = mockAnomalies[1];

    // Click first anomaly
    fireEvent.click(screen.getByTitle(firstAnomaly.name));
    expect(screen.getByText(`Anomaly: ${firstAnomaly.name}`)).toBeInTheDocument();

    // Click second anomaly
    fireEvent.click(screen.getByTitle(secondAnomaly.name));
    expect(screen.queryByText(`Anomaly: ${firstAnomaly.name}`)).not.toBeInTheDocument(); // First anomaly details should be gone
    expect(screen.getByText(`Anomaly: ${secondAnomaly.name}`)).toBeInTheDocument(); // Second anomaly details should be present
  });
});
