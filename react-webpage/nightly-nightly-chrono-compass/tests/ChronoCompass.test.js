import { render, screen } from '@testing-library/react';
import ChronoCompass from '../src/components/ChronoCompass';
import mockAnomalies from '../src/data/mockAnomalies'; // # Mock rationale: Directly importing mock data for deterministic, offline testing.

describe('ChronoCompass', () => {
  it('renders the compass header', () => {
    render(<ChronoCompass anomalies={[]} />);
    expect(screen.getByText('Temporal Anomaly Log')).toBeInTheDocument();
    expect(screen.getByLabelText('compass')).toBeInTheDocument();
  });

  it('displays a message when no anomalies are detected', () => {
    render(<ChronoCompass anomalies={[]} />);
    expect(screen.getByText('No temporal anomalies detected. All clear... for now.')).toBeInTheDocument();
  });

  it('renders a list of anomalies when provided', () => {
    render(<ChronoCompass anomalies={mockAnomalies} />);

    expect(screen.getByText('Temporal Drift')).toBeInTheDocument();
    expect(screen.getByText('Slight desynchronization detected in local causality field.')).toBeInTheDocument();
    expect(screen.getByText('Minor')).toBeInTheDocument();

    expect(screen.getByText('Rift Fluctuation')).toBeInTheDocument();
    expect(screen.getByText('Localized spacetime rift showing signs of instability. Immediate attention required.')).toBeInTheDocument();
    expect(screen.getByText('Critical')).toBeInTheDocument();

    // Check that all mock anomalies are rendered
    expect(screen.getAllByText(/Temporal Drift|Echo Chamber Anomaly|Rift Fluctuation|Temporal Echo|Chronal Ripple/).length).toBe(mockAnomalies.length);
  });

  it('displays correct severity colors', () => {
    render(<ChronoCompass anomalies={mockAnomalies} />);

    const criticalAnomaly = screen.getByText('Critical').closest('div');
    expect(criticalAnomaly).toHaveStyle('border-color: #e94560');

    const moderateAnomaly = screen.getByText('Moderate').closest('div');
    expect(moderateAnomaly).toHaveStyle('border-color: #ff7b00');

    const minorAnomaly = screen.getByText('Minor').closest('div');
    expect(minorAnomaly).toHaveStyle('border-color: #ffd700');
  });
});
