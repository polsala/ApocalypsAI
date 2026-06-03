import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

// # Mock rationale: Simulates the global fetch API to provide deterministic
// and offline data for the React component tests, avoiding actual network requests.
const mockFetchData = {
  whimsyScore: 75,
  activity: {
    newUtilities: 3,
    openPRs: 7,
    openIssues: 12
  }
};

beforeAll(() => {
  jest.spyOn(global, 'fetch').mockImplementation(() =>
    Promise.resolve({
      json: () => Promise.resolve(mockFetchData),
    })
  );
});

afterAll(() => {
  global.fetch.mockRestore();
});

describe('App Component', () => {
  test('renders loading state initially', () => {
    render(<App />);
    expect(screen.getByText(/Calibrating Whimsy-Meter.../i)).toBeInTheDocument();
  });

  test('renders header and footer', async () => {
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText(/ApocalypsAI Whimsy-Meter/i)).toBeInTheDocument();
      expect(screen.getByText(/Gauging the collective spirit of the repository./i)).toBeInTheDocument();
      expect(screen.getByText(/\u00a9 ApocalypsAI Nightly Integrator/i)).toBeInTheDocument();
    });
  });

  test('displays Whimsy Score and Activity Data after fetching', async () => {
    render(<App />);

    await waitFor(() => {
      // Check WhimsyMeter content
      expect(screen.getByText('Whimsy Score')).toBeInTheDocument();
      expect(screen.getByText(mockFetchData.whimsyScore.toString())).toBeInTheDocument();
      expect(screen.getByText(/A delightful hum of creativity./i)).toBeInTheDocument(); // Based on score 75

      // Check ActivityPanel content
      expect(screen.getByText('Repository Pulse')).toBeInTheDocument();
      expect(screen.getByText(mockFetchData.activity.newUtilities.toString())).toBeInTheDocument();
      expect(screen.getByText('New Utilities')).toBeInTheDocument();
      expect(screen.getByText(mockFetchData.activity.openPRs.toString())).toBeInTheDocument();
      expect(screen.getByText('Open PRs')).toBeInTheDocument();
      expect(screen.getByText(mockFetchData.activity.openIssues.toString())).toBeInTheDocument();
      expect(screen.getByText('Active Issues')).toBeInTheDocument();
    }, { timeout: 2000 }); // Increased timeout for async operations
  });

  test('handles fetch error gracefully', async () => {
    // # Mock rationale: Simulates a failed API response to test error handling.
    global.fetch.mockImplementationOnce(() =>
      Promise.reject(new Error('Network error'))
    );

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(/Error: Failed to fetch repository data./i)).toBeInTheDocument();
    });
  });
});
