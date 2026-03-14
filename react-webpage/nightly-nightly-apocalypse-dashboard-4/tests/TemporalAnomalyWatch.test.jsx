import React from 'react';
import { render, screen } from '@testing-library/react';
import TemporalAnomalyWatch from '../src/components/TemporalAnomalyWatch';

describe('TemporalAnomalyWatch Component', () => {
  test('renders the anomaly count', () => {
    render(<TemporalAnomalyWatch count={42} />);
    expect(screen.getByText(/42/i)).toBeInTheDocument();
  });

  test('renders 0 anomalies correctly', () => {
    render(<TemporalAnomalyWatch count={0} />);
    expect(screen.getByText(/0/i)).toBeInTheDocument();
    expect(screen.getByText(/Detected Anomalies/i)).toBeInTheDocument();
  });

  test('renders a large number of anomalies', () => {
    render(<TemporalAnomalyWatch count={999} />);
    expect(screen.getByText(/999/i)).toBeInTheDocument();
  });

  test('component has the animate-pulse class', () => {
    render(<TemporalAnomalyWatch count={10} />);
    const anomalyCountElement = screen.getByText(/10/i);
    expect(anomalyCountElement).toHaveClass('animate-pulse');
  });
});
