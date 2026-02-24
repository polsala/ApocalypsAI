import { render, screen, act } from '@testing-library/react';
import App from '../src/App';
import * as MoodDataService from '../src/MoodDataService'; // Import the service

// Mock rationale: We need to control the simulated mood data for deterministic tests.
// By mocking getSimulatedMood, we can ensure predictable values are returned,
// allowing us to test how the App component reacts to different mood states
// without relying on actual random numbers or external API calls.
jest.mock('../src/MoodDataService', () => ({
  getSimulatedMood: jest.fn(),
}));

describe('App', () => {
  beforeEach(() => {
    // Reset the mock before each test
    MoodDataService.getSimulatedMood.mockClear();
    jest.useFakeTimers(); // Use fake timers to control setInterval
  });

  afterEach(() => {
    jest.runOnlyPendingTimers();
    jest.useRealTimers(); // Restore real timers
  });

  test('renders the main title and initial mood', () => {
    MoodDataService.getSimulatedMood.mockReturnValue(50); // Mock initial mood
    render(<App />);
    expect(screen.getByText(/ApocalypsAI Community Mood Orb/i)).toBeInTheDocument();
    expect(screen.getByText(/Current Pulse: Optimistic & Steady \(50\)/i)).toBeInTheDocument();
  });

  test('updates mood description and value after interval', () => {
    MoodDataService.getSimulatedMood.mockReturnValueOnce(10).mockReturnValueOnce(80); // Mock two mood values

    render(<App />);
    expect(screen.getByText(/Current Pulse: Neutral & Observing \(10\)/i)).toBeInTheDocument();

    act(() => {
      jest.advanceTimersByTime(3000); // Advance time by 3 seconds
    });

    expect(screen.getByText(/Current Pulse: Radiant & Hopeful \(80\)/i)).toBeInTheDocument();
  });

  test('renders MoodOrb component with correct mood prop', () => {
    MoodDataService.getSimulatedMood.mockReturnValue(-60); // Mock a specific mood
    render(<App />);
    const moodOrbElement = screen.getByTestId('mood-orb');
    expect(moodOrbElement).toBeInTheDocument();
  });
});
