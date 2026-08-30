import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import EventInputForm from '../src/components/EventInputForm';

describe('EventInputForm Component', () => {
  test('renders input field and button', () => {
    render(<EventInputForm onGenerate={() => {}} />);
    expect(screen.getByLabelText(/Describe a Temporal Event:/i)).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: /Temporal Event Name/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Generate Echoes/i })).toBeInTheDocument();
  });

  test('updates input value on change', () => {
    render(<EventInputForm onGenerate={() => {}} />);
    const input = screen.getByRole('textbox', { name: /Temporal Event Name/i });
    fireEvent.change(input, { target: { value: 'Test Event Description' } });
    expect(input).toHaveValue('Test Event Description');
  });

  test('calls onGenerate with input value on form submission', () => {
    // Mock rationale: We need to verify that the `onGenerate` prop is called
    // with the correct argument when the form is submitted. A Jest mock function
    // allows us to track calls and arguments deterministically.
    const mockOnGenerate = jest.fn();
    render(<EventInputForm onGenerate={mockOnGenerate} />);

    const input = screen.getByRole('textbox', { name: /Temporal Event Name/i });
    const button = screen.getByRole('button', { name: /Generate Echoes/i });

    fireEvent.change(input, { target: { value: 'The Grand Paradox' } });
    fireEvent.click(button);

    expect(mockOnGenerate).toHaveBeenCalledTimes(1);
    expect(mockOnGenerate).toHaveBeenCalledWith('The Grand Paradox');
  });

  test('calls onGenerate with empty string if input is empty', () => {
    // Mock rationale: Similar to the above, ensuring the callback handles empty input.
    const mockOnGenerate = jest.fn();
    render(<EventInputForm onGenerate={mockOnGenerate} />);

    const button = screen.getByRole('button', { name: /Generate Echoes/i });

    // Input is initially empty
    fireEvent.click(button);

    expect(mockOnGenerate).toHaveBeenCalledTimes(1);
    expect(mockOnGenerate).toHaveBeenCalledWith('');
  });
});
