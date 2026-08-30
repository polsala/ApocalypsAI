import { render, screen, fireEvent } from '@testing-library/react';
import InputForm from '../src/components/InputForm';

describe('InputForm Component', () => {
  it('renders with a textarea and a button', () => {
    render(<InputForm onLoadEvents={() => {}} />);
    expect(screen.getByLabelText(/Paste Event JSON Data:/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Load Events/i })).toBeInTheDocument();
  });

  it('updates textarea value on change', () => {
    render(<InputForm onLoadEvents={() => {}} />);
    const textarea = screen.getByLabelText(/Paste Event JSON Data:/i);
    fireEvent.change(textarea, { target: { value: 'test input' } });
    expect(textarea.value).toBe('test input');
  });

  it('calls onLoadEvents with textarea content on submit', () => {
    const mockOnLoadEvents = jest.fn();
    render(<InputForm onLoadEvents={mockOnLoadEvents} />);
    const textarea = screen.getByLabelText(/Paste Event JSON Data:/i);
    const submitButton = screen.getByRole('button', { name: /Load Events/i });

    const testJson = `[{ "id": "e1", "timestamp": "2024-01-01T00:00:00Z", "type": "Test" }]`;
    fireEvent.change(textarea, { target: { value: testJson } });
    fireEvent.click(submitButton);

    // Mock rationale: We are testing that the `onLoadEvents` prop is called with the correct data.
    // The mock function allows us to assert its call without needing to implement its actual logic.
    expect(mockOnLoadEvents).toHaveBeenCalledTimes(1);
    expect(mockOnLoadEvents).toHaveBeenCalledWith(testJson);
  });

  it('displays error message when provided', () => {
    const errorMessage = 'Invalid JSON format!';
    render(<InputForm onLoadEvents={() => {}} error={errorMessage} />);
    expect(screen.getByText(errorMessage)).toBeInTheDocument();
  });

  it('does not display error message when not provided', () => {
    render(<InputForm onLoadEvents={() => {}} />);
    expect(screen.queryByText(/Invalid JSON format!/i)).not.toBeInTheDocument();
  });
});
