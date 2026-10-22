// tests/App.test.js
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../src/App';
import { moods, getRandomMood } from '../src/moodData';

// Mock rationale: We need to control the random mood selection for deterministic tests.
// We'll mock getRandomMood to return specific moods in sequence.
jest.mock('../src/moodData', () => ({
  moods: [
    { name: "TestMood1", color: "#111", icon: "T1", insight: "Insight 1" },
    { name: "TestMood2", color: "#222", icon: "T2", insight: "Insight 2" }
  ],
  getRandomMood: jest.fn()
}));

describe('App', () => {
  beforeEach(() => {
    // Reset the mock before each test
    getRandomMood.mockClear();
  });

  test('renders loading state initially then displays a mood', async () => {
    getRandomMood.mockReturnValueOnce(moods[0]); // Mock initial mood

    render(<App />);

    // Check for loading state
    expect(screen.getByText(/Loading Mood.../i)).toBeInTheDocument();

    // Wait for the mood to be displayed
    await waitFor(() => {
      expect(screen.getByText('Apocalypse Mood Ring')).toBeInTheDocument();
      expect(screen.getByText('TestMood1')).toBeInTheDocument();
      expect(screen.getByText('Insight 1')).toBeInTheDocument();
      expect(screen.getByText('T1')).toBeInTheDocument();
    });
    expect(screen.queryByText(/Loading Mood.../i)).not.toBeInTheDocument();
  });

  test('changes mood when "Simulate New Mood" button is clicked', async () => {
    getRandomMood.mockReturnValueOnce(moods[0]) // Initial mood
                 .mockReturnValueOnce(moods[1]); // Next mood on button click

    render(<App />);

    // Wait for initial mood to load
    await waitFor(() => {
      expect(screen.getByText('TestMood1')).toBeInTheDocument();
    });

    const button = screen.getByRole('button', { name: /Simulate New Mood/i });
    fireEvent.click(button);

    // Wait for the new mood to be displayed
    await waitFor(() => {
      expect(screen.getByText('TestMood2')).toBeInTheDocument();
      expect(screen.getByText('Insight 2')).toBeInTheDocument();
      expect(screen.getByText('T2')).toBeInTheDocument();
    });
    expect(screen.queryByText('TestMood1')).not.toBeInTheDocument();
  });

  test('displays the disclaimer text', async () => {
    getRandomMood.mockReturnValueOnce(moods[0]); // Mock initial mood

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(/\*This is a simulated mood for whimsical purposes only\. Do not base critical survival decisions on it\./i)).toBeInTheDocument();
    });
  });

  test('App component background color updates with mood', async () => {
    getRandomMood.mockReturnValueOnce(moods[0]); // Mock initial mood

    const { container } = render(<App />);

    await waitFor(() => {
      const appDiv = container.querySelector('.App');
      expect(appDiv).toHaveStyle(`background-color: ${moods[0].color}`);
    });

    getRandomMood.mockReturnValueOnce(moods[1]); // Mock next mood
    fireEvent.click(screen.getByRole('button', { name: /Simulate New Mood/i }));

    await waitFor(() => {
      const appDiv = container.querySelector('.App');
      expect(appDiv).toHaveStyle(`background-color: ${moods[1].color}`);
    });
  });
});
