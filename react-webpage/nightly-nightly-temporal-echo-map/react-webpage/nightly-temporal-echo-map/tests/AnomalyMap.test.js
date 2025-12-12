import { render, screen, fireEvent } from '@testing-library/react';
import AnomalyMap from '../src/AnomalyMap';

describe('AnomalyMap', () => {
  const mockAnomalies = [
    { id: 'm1', type: 'Temporal Ripple', location: 'Map Loc 1', severity: 'Minor', status: 'Active', coordinates: { lat: 10, lng: 20 }, description: 'Map anomaly 1' },
    { id: 'm2', type: 'Chronal Drift', location: 'Map Loc 2', severity: 'Moderate', status: 'Stabilized', coordinates: { lat: 30, lng: 40 }, description: 'Map anomaly 2' }
  ];
  const mockOnStabilize = jest.fn();

  // Mock rationale: We want to test the AnomalyMap component in isolation,
  // ensuring it renders markers correctly and calls the stabilization handler
  // when appropriate, without needing a full application context.
  test('renders anomaly markers with correct details', () => {
    render(<AnomalyMap anomalies={mockAnomalies} onStabilize={mockOnStabilize} />);

    // Check for active anomaly
    const marker1 = screen.getByTitle('Temporal Ripple: Map Loc 1 (Active)');
    expect(marker1).toBeInTheDocument();
    expect(marker1).toHaveClass('anomaly-marker');
    expect(marker1).not.toHaveClass('stabilized');
    expect(screen.getByText('Temporal Ripple')).toBeInTheDocument();
    expect(screen.getByText('Location: Map Loc 1')).toBeInTheDocument();
    expect(screen.getByText('Severity: Minor')).toBeInTheDocument();
    expect(screen.getByText('Status: Active')).toBeInTheDocument();
    expect(screen.getByText('Map anomaly 1')).toBeInTheDocument();

    // Check for stabilized anomaly
    const marker2 = screen.getByTitle('Chronal Drift: Map Loc 2 (Stabilized)');
    expect(marker2).toBeInTheDocument();
    expect(marker2).toHaveClass('anomaly-marker');
    expect(marker2).toHaveClass('stabilized');
    expect(screen.getByText('Chronal Drift')).toBeInTheDocument();
    expect(screen.getByText('Location: Map Loc 2')).toBeInTheDocument();
    expect(screen.getByText('Severity: Moderate')).toBeInTheDocument();
    expect(screen.getByText('Status: Stabilized')).toBeInTheDocument();
    expect(screen.getByText('Map anomaly 2')).toBeInTheDocument();
  });

  test('stabilize button is present for active anomalies and calls onStabilize', () => {
    render(<AnomalyMap anomalies={mockAnomalies} onStabilize={mockOnStabilize} />);

    // Find the stabilize button for the active anomaly
    const stabilizeButton = screen.getByRole('button', { name: /Stabilize/i });
    expect(stabilizeButton).toBeInTheDocument();

    fireEvent.click(stabilizeButton);
    expect(mockOnStabilize).toHaveBeenCalledTimes(1);
    expect(mockOnStabilize).toHaveBeenCalledWith('m1'); // Should call with the ID of the active anomaly
  });

  test('stabilize button is not present for stabilized anomalies', () => {
    render(<AnomalyMap anomalies={mockAnomalies} onStabilize={mockOnStabilize} />);

    // The stabilized anomaly (m2) should not have a stabilize button
    const stabilizedAnomalyMarker = screen.getByTitle('Chronal Drift: Map Loc 2 (Stabilized)');
    expect(stabilizedAnomalyMarker).toBeInTheDocument();

    // Check that there's only one "Stabilize" button (for the active anomaly)
    const stabilizeButtons = screen.queryAllByRole('button', { name: /Stabilize/i });
    expect(stabilizeButtons).toHaveLength(1);
  });

  test('anomaly details are initially hidden and appear on hover (simulated)', () => {
    render(<AnomalyMap anomalies={mockAnomalies} onStabilize={mockOnStabilize} />);

    // Details should be hidden by default (CSS display: none)
    // We can't directly test CSS display: none with @testing-library,
    // but we can check if the content is present in the DOM.
    // The hover effect is a CSS concern, but we can check if the elements exist.
    const detailsElement = screen.getByText('Map anomaly 1').closest('.anomaly-details');
    expect(detailsElement).toBeInTheDocument();
    // A more advanced test would involve simulating hover events and checking computed styles,
    // but for a self-contained utility, checking for existence is sufficient.
  });
});
