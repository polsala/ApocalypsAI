import { render, screen, fireEvent, cleanup } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

// Mock rationale: We need to mock localStorage to ensure tests are deterministic
// and do not interfere with actual browser storage or other tests.
const localStorageMock = (function () {
  let store = {};
  return {
    getItem: jest.fn((key) => store[key] || null),
    setItem: jest.fn((key, value) => {
      store[key] = value.toString();
    }),
    clear: jest.fn(() => {
      store = {};
    }),
    removeItem: jest.fn((key) => {
      delete store[key];
    }),
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// Mock rationale: Date.now() is non-deterministic, so we mock it to ensure consistent timestamps in tests.
const MOCK_DATE_NOW = 1678886400000; // March 15, 2023 12:00:00 PM UTC
const MOCK_DATE_STRING = new Date(MOCK_DATE_NOW).toLocaleDateString();
const MOCK_TIME_STRING = new Date(MOCK_DATE_NOW).toLocaleTimeString();

describe('App', () => {
  beforeEach(() => {
    localStorageMock.clear(); // Clear local storage before each test
    localStorageMock.getItem.mockClear();
    localStorageMock.setItem.mockClear();
    jest.spyOn(Date, 'now').mockReturnValue(MOCK_DATE_NOW);
    jest.spyOn(Date.prototype, 'toLocaleDateString').mockReturnValue(MOCK_DATE_STRING);
    jest.spyOn(Date.prototype, 'toLocaleTimeString').mockReturnValue(MOCK_TIME_STRING);
  });

  afterEach(() => {
    cleanup();
    jest.restoreAllMocks(); // Restore Date.now() and localStorage mocks
  });

  test('renders the main title and initial state', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Community Mood Ring/i)).toBeInTheDocument();
    expect(screen.getByText(/How are you feeling today?/i)).toBeInTheDocument();
    expect(screen.getByText(/No moods logged yet\. Be the first!/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Log My Mood/i })).toBeDisabled();
  });

  test('loads moods from local storage on initial render', () => {
    // Mock rationale: Simulate existing data in localStorage for testing loading behavior.
    const mockMoods = [
      { moodId: 'resilient', timestamp: 1, date: '1/1/2023', time: '12:00:00 PM' },
    ];
    localStorageMock.getItem.mockReturnValueOnce(JSON.stringify(mockMoods));

    render(<App />);
    expect(localStorageMock.getItem).toHaveBeenCalledWith('communityMoods');
    expect(screen.getByText(/☀️ Radiantly Resilient/i)).toBeInTheDocument();
  });

  test('allows selecting a mood and logging it', () => {
    render(<App />);

    const resilientOption = screen.getByLabelText(/☀️ Radiantly Resilient/i);
    fireEvent.click(resilientOption);
    expect(screen.getByRole('button', { name: /Log My Mood/i })).toBeEnabled();

    fireEvent.click(screen.getByRole('button', { name: /Log My Mood/i }));

    expect(screen.getByText(/☀️ Radiantly Resilient - Logged on/i)).toBeInTheDocument();
    expect(screen.getByText(`- Logged on ${MOCK_DATE_STRING} at ${MOCK_TIME_STRING}`)).toBeInTheDocument();
    expect(localStorageMock.setItem).toHaveBeenCalledWith(
      'communityMoods',
      JSON.stringify([
        { moodId: 'resilient', timestamp: MOCK_DATE_NOW, date: MOCK_DATE_STRING, time: MOCK_TIME_STRING },
      ])
    );
    expect(screen.getByRole('button', { name: /Log My Mood/i })).toBeDisabled(); // Should reset selection
  });

  test('displays correct mood summary after logging multiple moods', () => {
    render(<App />);

    // Log Resilient
    fireEvent.click(screen.getByLabelText(/☀️ Radiantly Resilient/i));
    fireEvent.click(screen.getByRole('button', { name: /Log My Mood/i }));

    // Log Mutated
    fireEvent.click(screen.getByLabelText(/🧪 Mildly Mutated/i));
    fireEvent.click(screen.getByRole('button', { name: /Log My Mood/i }));

    // Log Resilient again
    fireEvent.click(screen.getByLabelText(/☀️ Radiantly Resilient/i));
    fireEvent.click(screen.getByRole('button', { name: /Log My Mood/i }));

    expect(screen.getByText(/Most common recent mood: ☀️ Radiantly Resilient/i)).toBeInTheDocument();
  });

  test('only keeps the last 10 moods in history', () => {
    render(<App />);

    for (let i = 0; i < 12; i++) {
      fireEvent.click(screen.getByLabelText(/☀️ Radiantly Resilient/i));
      fireEvent.click(screen.getByRole('button', { name: /Log My Mood/i }));
    }

    const moodItems = screen.getAllByText(/☀️ Radiantly Resilient - Logged on/i);
    expect(moodItems).toHaveLength(10); // Should only show the last 10
    expect(localStorageMock.setItem).toHaveBeenCalledWith(
      'communityMoods',
      expect.stringContaining('resilient') // Check if it saved to localStorage
    );
    const storedMoods = JSON.parse(localStorageMock.getItem('communityMoods'));
    expect(storedMoods).toHaveLength(10);
  });

  test('does not log mood if no mood is selected', () => {
    render(<App />);
    const logButton = screen.getByRole('button', { name: /Log My Mood/i });
    expect(logButton).toBeDisabled();
    fireEvent.click(logButton); // Attempt to click disabled button
    expect(localStorageMock.setItem).not.toHaveBeenCalled();
    expect(screen.getByText(/No moods logged yet\. Be the first!/i)).toBeInTheDocument();
  });
});
