import { render, screen, fireEvent } from '@testing-library/react';
import WhisperInput from '../src/components/WhisperInput';
import '@testing-library/jest-dom';

describe('WhisperInput', () => {
  test('renders input field and button', () => {
    render(<WhisperInput onAddWhisper={() => {}} />);
    expect(screen.getByLabelText(/Whisper input/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Weave Whisper/i })).toBeInTheDocument();
  });

  test('updates input value on change', () => {
    render(<WhisperInput onAddWhisper={() => {}} />);
    const inputElement = screen.getByLabelText(/Whisper input/i);
    fireEvent.change(inputElement, { target: { value: 'Hello' } });
    expect(inputElement).toHaveValue('Hello');
  });

  test('calls onAddWhisper with input value on submit', () => {
    const mockAddWhisper = jest.fn(); // # Mock rationale: Use a Jest mock function to track if onAddWhisper is called and with what arguments.
    render(<WhisperInput onAddWhisper={mockAddWhisper} />);
    const inputElement = screen.getByLabelText(/Whisper input/i);
    const buttonElement = screen.getByRole('button', { name: /Weave Whisper/i });

    fireEvent.change(inputElement, { target: { value: 'New whisper' } });
    fireEvent.click(buttonElement);

    expect(mockAddWhisper).toHaveBeenCalledTimes(1);
    expect(mockAddWhisper).toHaveBeenCalledWith('New whisper');
    expect(inputElement).toHaveValue(''); // Input should clear
  });

  test('submit button is disabled when input is empty', () => {
    render(<WhisperInput onAddWhisper={() => {}} />);
    const buttonElement = screen.getByRole('button', { name: /Weave Whisper/i });
    expect(buttonElement).toBeDisabled();

    const inputElement = screen.getByLabelText(/Whisper input/i);
    fireEvent.change(inputElement, { target: { value: ' ' } }); // Only whitespace
    expect(buttonElement).toBeDisabled();

    fireEvent.change(inputElement, { target: { value: 'Valid text' } });
    expect(buttonElement).not.toBeDisabled();
  });
});
