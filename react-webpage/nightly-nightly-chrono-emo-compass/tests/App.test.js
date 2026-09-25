import { render, screen } from '@testing-library/react';
import App from '../src/App';
import mockMoodData from '../src/data/mockMoodData'; // # Mock rationale: Directly importing mock data ensures deterministic tests without network calls.

// Mock the MoodChart component to simplify testing App.js in isolation
jest.mock('../src/components/MoodChart', () => {
  return function MockMoodChart({ data }) {
    return (
      <div data-testid="mock-mood-chart">
        <p>Chart rendered with {data.length} data points.</p>
      </div>
    );
  };
});

describe('App Component', () => {
  test('renders the main title', () => {
    render(<App />);
    const titleElement = screen.getByText(/Nightly Chrono-Emotional Compass/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders the subtitle', () => {
    render(<App />);
    const subtitleElement = screen.getByText(/Visualizing the ApocalypsAI Community's Vibe/i);
    expect(subtitleElement).toBeInTheDocument();
  });

  test('renders the MoodChart component with data', async () => {
    render(<App />);
    // Wait for the mock data to be 'loaded' (i.e., useEffect to run)
    const chartElement = await screen.findByTestId('mock-mood-chart');
    expect(chartElement).toBeInTheDocument();
    expect(screen.getByText(`Chart rendered with ${mockMoodData.length} data points.`)).toBeInTheDocument();
  });

  test('renders the footer text', () => {
    render(<App />);
    const footerElement = screen.getByText(/Data is simulated for demonstration purposes./i);
    expect(footerElement).toBeInTheDocument();
  });
});
