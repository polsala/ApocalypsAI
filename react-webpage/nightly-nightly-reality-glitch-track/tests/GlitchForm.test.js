import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import GlitchForm from '../src/components/GlitchForm';

describe('GlitchForm Component', () => {
  test('renders form elements correctly', () => {
    render(<GlitchForm onAddGlitch={() => {}} />);

    expect(screen.getByText(/Report a New Glitch/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Description:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Type of Glitch:/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Report Glitch/i })).toBeInTheDocument();
  });

  test('calls onAddGlitch with correct data on submission', async () => {
    const mockOnAddGlitch = jest.fn(); // Mock rationale: Mocking a prop function to verify its calls.
    render(<GlitchForm onAddGlitch={mockOnAddGlitch} />);

    const descriptionInput = screen.getByLabelText(/Description:/i);
    const typeSelect = screen.getByLabelText(/Type of Glitch:/i);
    const reportButton = screen.getByRole('button', { name: /Report Glitch/i });

    userEvent.type(descriptionInput, 'My cat spoke Latin.');
    userEvent.selectOptions(typeSelect, 'Auditory Echo');
    fireEvent.click(reportButton);

    expect(mockOnAddGlitch).toHaveBeenCalledTimes(1);
    expect(mockOnAddGlitch).toHaveBeenCalledWith({
      description: 'My cat spoke Latin.',
      type: 'Auditory Echo',
    });

    // Ensure form fields are cleared after submission
    expect(descriptionInput).toHaveValue('');
    expect(typeSelect).toHaveValue('Object Displacement'); // Resets to default
  });

  test('does not call onAddGlitch if description is empty', () => {
    const mockOnAddGlitch = jest.fn(); // Mock rationale: Mocking a prop function to verify its calls.
    render(<GlitchForm onAddGlitch={mockOnAddGlitch} />);

    const reportButton = screen.getByRole('button', { name: /Report Glitch/i });
    fireEvent.click(reportButton); // Submit with empty description

    expect(mockOnAddGlitch).not.toHaveBeenCalled();
  });
});
