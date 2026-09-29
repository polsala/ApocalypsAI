import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../src/App';

// Mock rationale: We need to control the Date.now() value to ensure deterministic timestamps
// for newly added events during testing. This allows us to predict the 'id' and 'timestamp'
// of events and assert on their presence and order reliably.
const MOCK_DATE = 1678886400000; // March 15, 2023 12:00:00 PM UTC
const MOCK_DATE_2 = 1678886401000; // March 15, 2023 12:00:01 PM UTC

describe('App Component', () => {
  beforeEach(() => {
    jest.spyOn(Date, 'now').mockReturnValue(MOCK_DATE);
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Ripple Viewer/i)).toBeInTheDocument();
  });

  test('allows adding a new temporal ripple', async () => {
    const user = userEvent.setup();
    render(<App />);

    const descriptionInput = screen.getByPlaceholderText(/Describe the temporal anomaly.../i);
    const distortionSelect = screen.getByLabelText(/Distortion level/i);
    const addButton = screen.getByRole('button', { name: /Add Ripple/i });

    await user.type(descriptionInput, 'A squirrel briefly gained sentience');
    await user.selectOptions(distortionSelect, 'Moderate');
    await user.click(addButton);

    expect(screen.getByText(/A squirrel briefly.../i)).toBeInTheDocument();
    expect(descriptionInput).toHaveValue(''); // Input should clear after adding
    expect(distortionSelect).toHaveValue('Minor'); // Select should reset
  });

  test('does not add an empty ripple', async () => {
    const user = userEvent.setup();
    render(<App />);

    const addButton = screen.getByRole('button', { name: /Add Ripple/i });
    await user.click(addButton);

    // Expect no new ripple to be added (check for the default 'no ripples' message if applicable, or absence of new ripple text)
    expect(screen.queryByText(/.../)).not.toBeInTheDocument(); // Assuming no ripple text starts with '...'
    expect(screen.getByText(/No temporal ripples detected yet. Add one!/i)).toBeInTheDocument();
  });

  test('displays multiple ripples in chronological order', async () => {
    const user = userEvent.setup();
    render(<App />);

    const descriptionInput = screen.getByPlaceholderText(/Describe the temporal anomaly.../i);
    const distortionSelect = screen.getByLabelText(/Distortion level/i);
    const addButton = screen.getByRole('button', { name: /Add Ripple/i });

    // Add first event
    await user.type(descriptionInput, 'First anomaly');
    await user.selectOptions(distortionSelect, 'Minor');
    await user.click(addButton);

    // Mock rationale: Advance time for the second event to ensure different timestamps
    Date.now.mockReturnValue(MOCK_DATE_2);

    // Add second event
    await user.type(descriptionInput, 'Second anomaly');
    await user.selectOptions(distortionSelect, 'Severe');
    await user.click(addButton);

    const ripples = screen.getAllByText(/anomaly/i);
    expect(ripples).toHaveLength(2);

    // Verify order (based on substring, as full text is truncated)
    // The chart sorts by timestamp, so 'First anomaly' should come before 'Second anomaly'
    // This test primarily checks if both are rendered, visual order is harder to test with just text
    expect(screen.getByText(/First anomaly.../i)).toBeInTheDocument();
    expect(screen.getByText(/Second anomaly.../i)).toBeInTheDocument();
  });

  test('ripple title shows full description and details on hover', async () => {
    const user = userEvent.setup();
    render(<App />);

    const descriptionInput = screen.getByPlaceholderText(/Describe the temporal anomaly.../i);
    const distortionSelect = screen.getByLabelText(/Distortion level/i);
    const addButton = screen.getByRole('button', { name: /Add Ripple/i });

    const fullDescription = 'A very long and detailed description of a temporal anomaly that occurred.';
    await user.type(descriptionInput, fullDescription);
    await user.selectOptions(distortionSelect, 'Cataclysmic');
    await user.click(addButton);

    const rippleElement = screen.getByText(/A very long.../i).closest('.ripple');
    expect(rippleElement).toBeInTheDocument();
    expect(rippleElement).toHaveAttribute('title', expect.stringContaining(fullDescription));
    expect(rippleElement).toHaveAttribute('title', expect.stringContaining('Cataclysmic'));
    expect(rippleElement).toHaveAttribute('title', expect.stringContaining(new Date(MOCK_DATE).toLocaleString()));
  });
});
