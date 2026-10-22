import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../src/App';

// # Mock rationale: localStorage is a browser-specific API.
// # Mocking it ensures tests are deterministic, offline, and don't interfere with actual browser storage.
const localStorageMock = (function() {
  let store = {};
  return {
    getItem(key) {
      return store[key] || null;
    },
    setItem(key, value) {
      store[key] = value.toString();
    },
    removeItem(key) {
      delete store[key];
    },
    clear() {
      store = {};
    }
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('App Component', () => {
  beforeEach(() => {
    localStorage.clear(); // Clear localStorage before each test
    jest.spyOn(Date, 'now').mockReturnValue(1234567890); // Mock Date.now for consistent IDs
  });

  afterEach(() => {
    jest.restoreAllMocks(); // Restore Date.now mock
  });

  test('renders the main title and input elements', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Mood Orb Monitor/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Log your sentiment \(1-10\)/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Log Sentiment/i })).toBeInTheDocument();
    expect(screen.getByText(/Collective Resonance: N\/A/i)).toBeInTheDocument();
    expect(screen.getByText(/Awaiting first resonance.../i)).toBeInTheDocument();
  });

  test('allows logging a sentiment and displays a new mood orb', async () => {
    render(<App />);
    const sentimentInput = screen.getByPlaceholderText(/Log your sentiment \(1-10\)/i);
    const logButton = screen.getByRole('button', { name: /Log Sentiment/i });

    await userEvent.type(sentimentInput, '7');
    fireEvent.click(logButton);

    expect(screen.getByText(/Stable \(7\)/i)).toBeInTheDocument();
    expect(sentimentInput).toHaveValue(null); // Input should clear after logging
    expect(screen.getByText(/Collective Resonance: 7.0/i)).toBeInTheDocument();
    expect(screen.getByText(/Steady Hum./i)).toBeInTheDocument();
  });

  test('does not log sentiment if input is invalid (out of range)', async () => {
    render(<App />);
    const sentimentInput = screen.getByPlaceholderText(/Log your sentiment \(1-10\)/i);
    const logButton = screen.getByRole('button', { name: /Log Sentiment/i });

    await userEvent.type(sentimentInput, '11');
    fireEvent.click(logButton);
    expect(screen.queryByText(/Radiant \(11\)/i)).not.toBeInTheDocument(); // Should not appear
    expect(screen.queryByText(/Stable \(11\)/i)).not.toBeInTheDocument(); // Should not appear
    expect(screen.getByText(/Collective Resonance: N\/A/i)).toBeInTheDocument(); // Still N/A

    await userEvent.clear(sentimentInput);
    await userEvent.type(sentimentInput, '0');
    fireEvent.click(logButton);
    expect(screen.queryByText(/Flickering \(0\)/i)).not.toBeInTheDocument(); // Should not appear
    expect(screen.getByText(/Collective Resonance: N\/A/i)).toBeInTheDocument(); // Still N/A
  });

  test('updates collective resonance with multiple entries', async () => {
    render(<App />);
    const sentimentInput = screen.getByPlaceholderText(/Log your sentiment \(1-10\)/i);
    const logButton = screen.getByRole('button', { name: /Log Sentiment/i });

    await userEvent.type(sentimentInput, '5');
    fireEvent.click(logButton);
    expect(screen.getByText(/Collective Resonance: 5.0/i)).toBeInTheDocument();
    expect(screen.getByText(/Steady Hum./i)).toBeInTheDocument();

    await userEvent.type(sentimentInput, '9');
    fireEvent.click(logButton);
    expect(screen.getByText(/Collective Resonance: 7.0/i)).toBeInTheDocument(); // (5+9)/2 = 7.0
    expect(screen.getByText(/Steady Hum./i)).toBeInTheDocument(); // Still steady hum

    await userEvent.type(sentimentInput, '2');
    fireEvent.click(logButton);
    expect(screen.getByText(/Collective Resonance: 5.3/i)).toBeInTheDocument(); // (5+9+2)/3 = 5.33
    expect(screen.getByText(/Steady Hum./i)).toBeInTheDocument();

    await userEvent.type(sentimentInput, '10');
    fireEvent.click(logButton);
    expect(screen.getByText(/Collective Resonance: 6.5/i)).toBeInTheDocument(); // (5+9+2+10)/4 = 6.5
    expect(screen.getByText(/Steady Hum./i)).toBeInTheDocument();

    await userEvent.type(sentimentInput, '8');
    fireEvent.click(logButton);
    expect(screen.getByText(/Collective Resonance: 6.8/i)).toBeInTheDocument(); // (5+9+2+10+8)/5 = 6.8
    expect(screen.getByText(/Steady Hum./i)).toBeInTheDocument();

    await userEvent.type(sentimentInput, '1');
    fireEvent.click(logButton);
    // Now it should consider (9+2+10+8+1)/5 = 6.0
    expect(screen.getByText(/Collective Resonance: 6.0/i)).toBeInTheDocument();
    expect(screen.getByText(/Steady Hum./i)).toBeInTheDocument();
  });

  test('loads mood entries from localStorage on initial render', () => {
    // # Mock rationale: localStorage is mocked to control initial state for testing.
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify([
      { id: 1, sentiment: 6 },
      { id: 2, sentiment: 9 }
    ]));

    render(<App />);
    expect(screen.getByText(/Stable \(6\)/i)).toBeInTheDocument();
    expect(screen.getByText(/Radiant \(9\)/i)).toBeInTheDocument();
    expect(screen.getByText(/Collective Resonance: 7.5/i)).toBeInTheDocument(); // (6+9)/2 = 7.5
  });

  test('button is disabled when input is empty', () => {
    render(<App />);
    const logButton = screen.getByRole('button', { name: /Log Sentiment/i });
    expect(logButton).toBeDisabled();

    const sentimentInput = screen.getByPlaceholderText(/Log your sentiment \(1-10\)/i);
    fireEvent.change(sentimentInput, { target: { value: '5' } });
    expect(logButton).not.toBeDisabled();

    fireEvent.change(sentimentInput, { target: { value: '' } });
    expect(logButton).toBeDisabled();
  });
});
