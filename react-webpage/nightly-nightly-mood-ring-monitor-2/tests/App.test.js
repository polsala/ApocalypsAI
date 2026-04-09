import { render, screen, waitFor } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: Simulates the asynchronous data fetching for mood data
// to ensure tests are deterministic and do not rely on actual network calls
// or random values from the real fetchMoodData.
jest.mock('../src/App', () => {
  const ActualApp = jest.requireActual('../src/App').default;
  return function MockedApp(props) {
    const [mood, setMood] = jest.fn(() => [{
      value: 70,
      text: 'Mocked Balanced Glow'
    }, jest.fn()]);
    const [loading, setLoading] = jest.fn(() => [false, jest.fn()]);

    // Mock useEffect to prevent actual data fetching and interval setup
    jest.spyOn(require('react'), 'useEffect').mockImplementationOnce(f => f());

    return <ActualApp {...props} />;
  };
});

describe('App', () => {
  test('renders ApocalypsAI Mood Ring Monitor title', () => {
    render(<App />);
    const titleElement = screen.getByText(/ApocalypsAI Mood Ring Monitor/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('displays loading message initially', () => {
    // Temporarily unmock useEffect to test initial loading state
    jest.spyOn(require('react'), 'useEffect').mockRestore();
    render(<App />);
    const loadingElement = screen.getByText(/Analyzing cosmic vibrations.../i);
    expect(loadingElement).toBeInTheDocument();
  });

  test('renders MoodRing and MoodDisplay after loading', async () => {
    render(<App />);
    // Wait for the simulated data fetch to complete
    await waitFor(() => {
      expect(screen.getByText(/Current Vibe: Mocked Balanced Glow/i)).toBeInTheDocument();
    }, { timeout: 2000 }); // Adjust timeout if needed for mock delay

    const moodRingElement = screen.getByTestId('mood-ring'); // Add data-testid to MoodRing for easier selection
    expect(moodRingElement).toBeInTheDocument();
  });
});
