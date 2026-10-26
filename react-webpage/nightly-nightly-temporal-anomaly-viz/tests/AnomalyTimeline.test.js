import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import AnomalyTimeline from '../src/components/AnomalyTimeline';

describe('AnomalyTimeline', () => {
  const mockAnomalies = [
    {
      id: 'at001',
      timestamp: '2024-07-20T10:00:00Z',
      type: 'Minor Glitch',
      severity: 'Mild Wobble',
      location: 'Lab',
      impact: 'Small hiccup',
      description: 'A tiny glitch'
    },
    {
      id: 'at002',
      timestamp: '2024-07-21T11:00:00Z',
      type: 'Major Shift',
      severity: 'Reality Shredder',
      location: 'Field',
      impact: 'Big change',
      description: 'A large shift'
    }
  ];

  // Mock rationale: We are testing the AnomalyTimeline component in isolation.
  // Providing a static array of mock anomalies allows for deterministic and offline testing
  // without needing to simulate data fetching or external dependencies.
  const mockOnSelectAnomaly = jest.fn();

  test('renders all anomalies provided', () => {
    render(<AnomalyTimeline anomalies={mockAnomalies} onSelectAnomaly={mockOnSelectAnomaly} />);

    expect(screen.getByText(/Minor Glitch/i)).toBeInTheDocument();
    expect(screen.getByText(/Major Shift/i)).toBeInTheDocument();
    expect(screen.getByText(/\(Mild Wobble\)/i)).toBeInTheDocument();
    expect(screen.getByText(/\(Reality Shredder\)/i)).toBeInTheDocument();
  });

  test('calls onSelectAnomaly with the correct anomaly when clicked', () => {
    render(<AnomalyTimeline anomalies={mockAnomalies} onSelectAnomaly={mockOnSelectAnomaly} />);

    userEvent.click(screen.getByText(/Minor Glitch/i));
    expect(mockOnSelectAnomaly).toHaveBeenCalledTimes(1);
    expect(mockOnSelectAnomaly).toHaveBeenCalledWith(mockAnomalies[0]);

    userEvent.click(screen.getByText(/Major Shift/i));
    expect(mockOnSelectAnomaly).toHaveBeenCalledTimes(2);
    expect(mockOnSelectAnomaly).toHaveBeenCalledWith(mockAnomalies[1]);
  });

  test('renders nothing if anomalies array is empty', () => {
    const { container } = render(<AnomalyTimeline anomalies={[]} onSelectAnomaly={mockOnSelectAnomaly} />);
    expect(container.firstChild).toBeEmptyDOMElement();
  });
});
