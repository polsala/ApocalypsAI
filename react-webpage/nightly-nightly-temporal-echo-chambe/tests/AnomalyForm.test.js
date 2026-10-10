import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import AnomalyForm from '../src/components/AnomalyForm';

describe('AnomalyForm', () => {
  it('renders all form fields', () => {
    render(<AnomalyForm onAddAnomaly={() => {}} />);

    expect(screen.getByLabelText(/Description:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Timestamp:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Anomaly Type:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Temporal Energy Level \(1-10\):/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Add Anomaly/i })).toBeInTheDocument();
  });

  it('calls onAddAnomaly with correct data on submit', () => {
    const mockAddAnomaly = jest.fn();
    render(<AnomalyForm onAddAnomaly={mockAddAnomaly} />);

    // Mock rationale: Date.now() is used to generate a unique ID. Mocking it ensures deterministic IDs for testing.
    const mockDateNow = jest.spyOn(Date, 'now').mockReturnValue(1234567890);

    fireEvent.change(screen.getByLabelText(/Description:/i), {
      target: { value: 'Test Anomaly' },
    });
    fireEvent.change(screen.getByLabelText(/Timestamp:/i), {
      target: { value: '2024-10-27T10:00' },
    });
    fireEvent.change(screen.getByLabelText(/Anomaly Type:/i), {
      target: { value: 'Visual Glitch' },
    });
    fireEvent.change(screen.getByLabelText(/Temporal Energy Level \(1-10\):/i), {
      target: { value: '7' },
    });

    fireEvent.click(screen.getByRole('button', { name: /Add Anomaly/i }));

    expect(mockAddAnomaly).toHaveBeenCalledTimes(1);
    expect(mockAddAnomaly).toHaveBeenCalledWith({
      id: 1234567890,
      description: 'Test Anomaly',
      timestamp: '2024-10-27T10:00',
      type: 'Visual Glitch',
      energyLevel: 7,
    });

    // Check if form fields are reset
    expect(screen.getByLabelText(/Description:/i)).toHaveValue('');
    expect(screen.getByLabelText(/Timestamp:/i)).toHaveValue('');
    expect(screen.getByLabelText(/Anomaly Type:/i)).toHaveValue('Auditory Echo');
    expect(screen.getByLabelText(/Temporal Energy Level \(1-10\):/i)).toHaveValue(5);

    mockDateNow.mockRestore();
  });

  it('shows alert if required fields are missing', () => {
    const mockAddAnomaly = jest.fn();
    const alertSpy = jest.spyOn(window, 'alert').mockImplementation(() => {}); // Mock rationale: Suppress alert for expected validation test.
    render(<AnomalyForm onAddAnomaly={mockAddAnomaly} />);

    fireEvent.click(screen.getByRole('button', { name: /Add Anomaly/i }));

    expect(alertSpy).toHaveBeenCalledWith('Description and Timestamp are required!');
    expect(mockAddAnomaly).not.toHaveBeenCalled();
    alertSpy.mockRestore();
  });
});
