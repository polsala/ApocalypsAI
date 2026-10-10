import { render, screen, fireEvent } from '@testing-library/react';
import RippleDisplay from '../src/components/RippleDisplay';

describe('RippleDisplay Component', () => {
  const mockAnomalyActive = {
    id: 'TR-TEST-001',
    type: 'Test Drift',
    severity: 3,
    timestamp: '2024-07-21T10:00:00Z',
    status: 'active',
  };

  const mockAnomalyStabilized = {
    id: 'TR-TEST-002',
    type: 'Test Echo',
    severity: 1,
    timestamp: '2024-07-21T11:00:00Z',
    status: 'stabilized',
  };

  test('renders active anomaly details correctly', () => {
    render(<RippleDisplay anomaly={mockAnomalyActive} onStabilize={() => {}} />);
    expect(screen.getByText(/Test Drift Anomaly/i)).toBeInTheDocument();
    expect(screen.getByText(/ID: TR-TEST-001/i)).toBeInTheDocument();
    expect(screen.getByText(/Severity: 3 \/ 5/i)).toBeInTheDocument();
    expect(screen.getByText(/Status: active/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Stabilize Ripple/i })).toBeInTheDocument();
    expect(screen.queryByText(/Stabilized/i)).not.toBeInTheDocument();
  });

  test('renders stabilized anomaly details correctly', () => {
    render(<RippleDisplay anomaly={mockAnomalyStabilized} onStabilize={() => {}} />);
    expect(screen.getByText(/Test Echo Anomaly/i)).toBeInTheDocument();
    expect(screen.getByText(/ID: TR-TEST-002/i)).toBeInTheDocument();
    expect(screen.getByText(/Status: stabilized/i)).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /Stabilize Ripple/i })).not.toBeInTheDocument();
    expect(screen.getByText(/Stabilized/i)).toBeInTheDocument(); // Should show the indicator
  });

  test('calls onStabilize when button is clicked for active anomaly', () => {
    const mockOnStabilize = jest.fn(); // Mock rationale: Using Jest mock function to verify callback execution.
    render(<RippleDisplay anomaly={mockAnomalyActive} onStabilize={mockOnStabilize} />);
    const stabilizeButton = screen.getByRole('button', { name: /Stabilize Ripple/i });
    fireEvent.click(stabilizeButton);
    expect(mockOnStabilize).toHaveBeenCalledTimes(1);
    expect(mockOnStabilize).toHaveBeenCalledWith(mockAnomalyActive.id);
  });

  test('does not call onStabilize when button is clicked for stabilized anomaly', () => {
    const mockOnStabilize = jest.fn(); // Mock rationale: Using Jest mock function to verify callback execution.
    render(<RippleDisplay anomaly={mockAnomalyStabilized} onStabilize={mockOnStabilize} />);
    expect(screen.queryByRole('button', { name: /Stabilize Ripple/i })).not.toBeInTheDocument();
    expect(mockOnStabilize).not.toHaveBeenCalled();
  });

  test('does not show stabilize button when readOnly is true', () => {
    render(<RippleDisplay anomaly={mockAnomalyActive} onStabilize={() => {}} readOnly={true} />);
    expect(screen.queryByRole('button', { name: /Stabilize Ripple/i })).not.toBeInTheDocument();
  });
});
