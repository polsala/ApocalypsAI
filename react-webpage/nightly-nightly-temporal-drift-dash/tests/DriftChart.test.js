import React from 'react';
import { render, screen } from '@testing-library/react';
import DriftChart from '../src/components/DriftChart';

describe('DriftChart', () => {
  const mockDriftData = [
    { id: 'dc1', timestamp: '2024-07-21T10:00:00Z', severity: 'low', description: 'Chart test low.' },
    { id: 'dc2', timestamp: '2024-07-21T11:00:00Z', severity: 'medium', description: 'Chart test medium.' },
    { id: 'dc3', timestamp: '2024-07-21T12:00:00Z', severity: 'high', description: 'Chart test high.' }
  ];

  test('renders "No temporal drifts detected" when data is empty', () => {
    render(<DriftChart data={[]} />);
    expect(screen.getByText(/No temporal drifts detected. All clear... for now./i)).toBeInTheDocument();
  });

  test('renders drift items correctly with provided data', () => {
    render(<DriftChart data={mockDriftData} />);
    expect(screen.getByText(/Detected Temporal Anomalies/i)).toBeInTheDocument();
    expect(screen.getByText(/Chart test low./i)).toBeInTheDocument();
    expect(screen.getByText(/Chart test medium./i)).toBeInTheDocument();
    expect(screen.getByText(/Chart test high./i)).toBeInTheDocument();

    // Check for severity classes
    const lowSeverityItem = screen.getByText(/Chart test low./i).closest('.drift-item');
    expect(lowSeverityItem).toHaveClass('severity-low');

    const highSeverityItem = screen.getByText(/Chart test high./i).closest('.drift-item');
    expect(highSeverityItem).toHaveClass('severity-high');
  });

  test('formats timestamp correctly', () => {
    render(<DriftChart data={mockDriftData} />);
    // The toLocaleString() output depends on the locale, so we'll check for a part of it
    // or a more general pattern. For simplicity, let's check for the presence of the description.
    // A more robust test would mock Date or use a fixed locale.
    expect(screen.getByText(/Chart test low./i)).toBeInTheDocument();
    // We can check if the timestamp span exists and contains some date-like string
    const timestampElement = screen.getByText(/Chart test low./i).previousElementSibling;
    expect(timestampElement).toHaveTextContent(/2024/);
    expect(timestampElement).toHaveTextContent(/AM|PM|GMT|UTC/i); // Check for time indicator
  });
});
