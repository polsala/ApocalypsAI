import { render, screen, fireEvent } from '@testing-library/react';
import ChronoRippleForm from '../src/ChronoRippleForm';

describe('ChronoRippleForm', () => {
  const mockOnVisualize = jest.fn();
  const initialDetails = {
    date: '2023-01-01',
    description: 'Initial Event',
    magnitude: 3
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders all form elements with initial values', () => {
    render(<ChronoRippleForm onVisualize={mockOnVisualize} initialDetails={initialDetails} />);

    expect(screen.getByLabelText(/Event Date:/i)).toHaveValue('2023-01-01');
    expect(screen.getByLabelText(/Description:/i)).toHaveValue('Initial Event');
    expect(screen.getByLabelText(/Magnitude: 3/i)).toHaveValue('3');
    expect(screen.getByRole('button', { name: /Visualize Ripples/i })).toBeInTheDocument();
  });

  test('updates input values on change', () => {
    render(<ChronoRippleForm onVisualize={mockOnVisualize} initialDetails={initialDetails} />);

    const dateInput = screen.getByLabelText(/Event Date:/i);
    fireEvent.change(dateInput, { target: { value: '2024-02-15' } });
    expect(dateInput).toHaveValue('2024-02-15');

    const descriptionInput = screen.getByLabelText(/Description:/i);
    fireEvent.change(descriptionInput, { target: { value: 'New Event' } });
    expect(descriptionInput).toHaveValue('New Event');

    const magnitudeSlider = screen.getByLabelText(/Magnitude: \d+/i);
    fireEvent.change(magnitudeSlider, { target: { value: '7' } });
    expect(magnitudeSlider).toHaveValue('7');
  });

  test('calls onVisualize with correct data on submit', () => {
    render(<ChronoRippleForm onVisualize={mockOnVisualize} initialDetails={initialDetails} />);

    const dateInput = screen.getByLabelText(/Event Date:/i);
    const descriptionInput = screen.getByLabelText(/Description:/i);
    const magnitudeSlider = screen.getByLabelText(/Magnitude: \d+/i);
    const visualizeButton = screen.getByRole('button', { name: /Visualize Ripples/i });

    fireEvent.change(dateInput, { target: { value: '2025-03-20' } });
    fireEvent.change(descriptionInput, { target: { value: 'Future Echo' } });
    fireEvent.change(magnitudeSlider, { target: { value: '9' } });
    fireEvent.click(visualizeButton);

    expect(mockOnVisualize).toHaveBeenCalledTimes(1);
    expect(mockOnVisualize).toHaveBeenCalledWith({
      date: '2025-03-20',
      description: 'Future Echo',
      magnitude: 9
    });
  });
});
