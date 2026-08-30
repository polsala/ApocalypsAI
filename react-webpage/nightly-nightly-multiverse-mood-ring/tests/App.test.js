import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';
import * as MoodData from '../src/MoodData'; // Import MoodData to mock it

// Mock rationale: We want to ensure our React component behaves correctly
// based on the data it receives, without relying on the actual MoodData
// functions which might change or have complex logic. Mocking allows
// deterministic testing of the component's rendering and state updates.
jest.mock('../src/MoodData', () => ({
  getMoodData: jest.fn((mood) => {
    if (mood.toLowerCase() === 'hopeful') {
      return { keyword: 'Hopeful', color: '#87CEEB', message: 'A shimmering beacon.' };
    }
    if (mood.toLowerCase() === 'anxious') {
      return { keyword: 'Anxious', color: '#FFD700', message: 'The cosmic currents are turbulent.' };
    }
    return { keyword: 'Unclassified', color: '#000000', message: 'Intriguing!' };
  }),
  getRandomCommunityMood: jest.fn(() => ({
    keyword: 'Resilient',
    color: '#228B22',
    message: 'Like bedrock against the void\'s erosion.'
  })),
}));

describe('App', () => {
  beforeEach(() => {
    // Clear mocks before each test to ensure isolation
    MoodData.getMoodData.mockClear();
    MoodData.getRandomCommunityMood.mockClear();
    // Re-mock getRandomCommunityMood for the initial render
    MoodData.getRandomCommunityMood.mockReturnValueOnce({
      keyword: 'Resilient',
      color: '#228B22',
      message: 'Like bedrock against the void\'s erosion.'
    });
  });

  test('renders main heading', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Multiverse Mood Ring/i)).toBeInTheDocument();
  });

  test('renders user mood input and button', () => {
    render(<App />);
    expect(screen.getByLabelText(/What's your current apocalyptic vibe?/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Scan My Aura/i })).toBeInTheDocument();
  });

  test('displays user mood result after submission', async () => {
    render(<App />);
    const input = screen.getByLabelText(/What's your current apocalyptic vibe?/i);
    const button = screen.getByRole('button', { name: /Scan My Aura/i });

    fireEvent.change(input, { target: { value: 'Hopeful' } });
    fireEvent.click(button);

    await waitFor(() => {
      expect(screen.getByText(/Your Resonance: Hopeful/i)).toBeInTheDocument();
      expect(screen.getByText(/A shimmering beacon./i)).toBeInTheDocument();
      expect(MoodData.getMoodData).toHaveBeenCalledWith('Hopeful');
    });
  });

  test('displays unclassified mood for unknown input', async () => {
    render(<App />);
    const input = screen.getByLabelText(/What's your current apocalyptic vibe?/i);
    const button = screen.getByRole('button', { name: /Scan My Aura/i });

    fireEvent.change(input, { target: { value: 'Confused' } });
    fireEvent.click(button);

    await waitFor(() => {
      expect(screen.getByText(/Your Resonance: Unclassified/i)).toBeInTheDocument();
      expect(screen.getByText(/Intriguing!/i)).toBeInTheDocument();
      expect(MoodData.getMoodData).toHaveBeenCalledWith('Confused');
    });
  });

  test('displays community mood initially', () => {
    render(<App />);
    expect(screen.getByText(/Community's Collective Echo/i)).toBeInTheDocument();
    expect(screen.getByText(/Current Collective Vibe: Resilient/i)).toBeInTheDocument();
    expect(screen.getByText(/Like bedrock against the void's erosion./i)).toBeInTheDocument();
    expect(MoodData.getRandomCommunityMood).toHaveBeenCalledTimes(1); // Called once on initial render
  });

  test('community mood updates over time (mocked interval)', async () => {
    // Mock rationale: We need to control the passage of time in tests
    // to verify effects of setInterval without waiting real seconds.
    jest.useFakeTimers();

    render(<App />);

    // Initial render check
    expect(screen.getByText(/Current Collective Vibe: Resilient/i)).toBeInTheDocument();

    // Advance timers by 5 seconds to trigger the next community mood update
    // Mock getRandomCommunityMood to return a different value for the update
    MoodData.getRandomCommunityMood.mockReturnValueOnce({
      keyword: 'Anxious',
      color: '#FFD700',
      message: 'The cosmic currents are turbulent.'
    });
    jest.advanceTimersByTime(5000);

    await waitFor(() => {
      expect(screen.getByText(/Current Collective Vibe: Anxious/i)).toBeInTheDocument();
      expect(screen.getByText(/The cosmic currents are turbulent./i)).toBeInTheDocument();
      expect(MoodData.getRandomCommunityMood).toHaveBeenCalledTimes(2); // Called once initially, once after 5s
    });

    jest.useRealTimers(); // Restore real timers
  });
});
