import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: We need to mock Date to ensure deterministic shifted and echoed dates
// for consistent test results, as the App component calculates these based on the current time.
const MOCK_DATE = new Date('2024-07-20T10:00:00.000Z');
const MOCK_DATE_ISO = MOCK_DATE.toISOString().slice(0, 16); // YYYY-MM-DDTHH:MM format for input

const mockDate = jest.spyOn(global, 'Date');
mockDate.mockImplementation((dateString) => {
  if (dateString) {
    return new Date(dateString);
  }
  return MOCK_DATE;
});

describe('App Component', () => {
  test('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Chrono-Compass/i)).toBeInTheDocument();
  });

  test('allows adding an event and displays it', () => {
    render(<App />);

    const eventNameInput = screen.getByPlaceholderText(/e.g., Found the last can of beans/i);
    const dateTimeInput = screen.getByLabelText(/Original Date & Time:/i);
    const addButton = screen.getByRole('button', { name: /Add Event to Chrono-Compass/i });

    fireEvent.change(eventNameInput, { target: { value: 'Test Event' } });
    fireEvent.change(dateTimeInput, { target: { value: MOCK_DATE_ISO } });
    fireEvent.click(addButton);

    expect(screen.getByText('Test Event')).toBeInTheDocument();
    expect(screen.getByText(/Original: 7\/20\/2024, 10:00:00 AM/i)).toBeInTheDocument();
    // Verify shifted date (+3 hours from MOCK_DATE)
    expect(screen.getByText(/Shifted: 7\/20\/2024, 1:00:00 PM/i)).toBeInTheDocument();
    // Verify echo date (-7 days from MOCK_DATE)
    expect(screen.getByText(/Echo: 7\/13\/2024, 10:00:00 AM/i)).toBeInTheDocument();

    // Ensure inputs are cleared
    expect(eventNameInput.value).toBe('');
    expect(dateTimeInput.value).toBe('');
  });

  test('does not add an event if name or date is empty', () => {
    render(<App />);

    const addButton = screen.getByRole('button', { name: /Add Event to Chrono-Compass/i });
    const initialEventCount = screen.queryAllByRole('listitem').length;

    // Try to add with empty name
    fireEvent.click(addButton);
    expect(screen.queryAllByRole('listitem').length).toBe(initialEventCount);

    // Try to add with empty date
    const eventNameInput = screen.getByPlaceholderText(/e.g., Found the last can of beans/i);
    fireEvent.change(eventNameInput, { target: { value: 'Partial Event' } });
    fireEvent.click(addButton);
    expect(screen.queryAllByRole('listitem').length).toBe(initialEventCount);
  });
});
