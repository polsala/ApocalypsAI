import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event'; // For more realistic user interactions
import App from '../src/App';

// Mock rationale: localStorage is a browser API. For testing, we can mock it
// to ensure tests are deterministic and don't interfere with actual browser storage.
const localStorageMock = (function() {
  let store = {};
  return {
    getItem: function(key) {
      return store[key] || null;
    },
    setItem: function(key, value) {
      store[key] = value.toString();
    },
    clear: function() {
      store = {};
    },
    removeItem: function(key) {
      delete store[key];
    }
  };
})();

Object.defineProperty(window, 'localStorage', { value: localStorageMock });

describe('App Component', () => {
  beforeEach(() => {
    localStorage.clear(); // Clear local storage before each test
    // Mock rationale: Date.now() and new Date().toLocaleString() are non-deterministic.
    // We mock them to ensure consistent output for timestamps in tests.
    jest.spyOn(Date, 'now').mockReturnValue(1678886400000); // Fixed timestamp
    jest.spyOn(Date.prototype, 'toLocaleString').mockReturnValue('3/15/2023, 12:00:00 AM');
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Reality Glitch Tracker/i)).toBeInTheDocument();
  });

  test('allows reporting a new glitch and displays it', async () => {
    render(<App />);

    const descriptionInput = screen.getByPlaceholderText(/e.g., My coffee mug vanished/i);
    const reportButton = screen.getByRole('button', { name: /Report Glitch/i });

    // Simulate user typing
    userEvent.type(descriptionInput, 'My socks disappeared from the dryer!');
    
    // Simulate selecting a glitch type
    const typeSelect = screen.getByLabelText(/Type of Glitch:/i);
    userEvent.selectOptions(typeSelect, 'Object Displacement');

    // Simulate form submission
    fireEvent.click(reportButton);

    // Check if the new glitch is displayed
    expect(await screen.findByText(/My socks disappeared from the dryer!/i)).toBeInTheDocument();
    expect(screen.getByText(/Object Displacement/i)).toBeInTheDocument();
    expect(screen.getByText(/Reported: 3\/15\/2023, 12:00:00 AM/i)).toBeInTheDocument();

    // Check if form inputs are cleared
    expect(descriptionInput).toHaveValue('');
    expect(typeSelect).toHaveValue('Object Displacement');
  });

  test('loads glitches from local storage on startup', () => {
    // Mock rationale: Pre-populating localStorage to test loading functionality.
    const initialGlitches = [
      { id: 1, description: 'Test Glitch 1', type: 'Time Skip', timestamp: '1/1/2023, 12:00:00 PM' }
    ];
    localStorage.setItem('glitches', JSON.stringify(initialGlitches));

    render(<App />);

    expect(screen.getByText(/Test Glitch 1/i)).toBeInTheDocument();
    expect(screen.getByText(/Time Skip/i)).toBeInTheDocument();
  });

  test('saves glitches to local storage when state changes', async () => {
    render(<App />);

    const descriptionInput = screen.getByPlaceholderText(/e.g., My coffee mug vanished/i);
    const reportButton = screen.getByRole('button', { name: /Report Glitch/i });

    userEvent.type(descriptionInput, 'A phantom smell of toast appeared.');
    fireEvent.click(reportButton);

    // Wait for the state update and useEffect to run
    await screen.findByText(/A phantom smell of toast appeared./i);

    // Check if localStorage was updated
    const savedGlitches = JSON.parse(localStorage.getItem('glitches'));
    expect(savedGlitches).toHaveLength(1);
    expect(savedGlitches[0].description).toBe('A phantom smell of toast appeared.');
  });
});
