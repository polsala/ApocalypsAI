import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import MoodRing from '../src/MoodRing';
import { generateMood, resetMoodIndex } from '../src/utils';

// Mock rationale: Simulates external log analysis or sentiment API calls to ensure deterministic testing of UI rendering based on mood data.
jest.mock('../src/utils', () => {
  const originalModule = jest.requireActual('../src/utils');
  let mockMoodIndex = 0;
  const mockMoods = [
    { color: '#61dafb', description: 'Serene Blue: Calm, efficient operations.' },
    { color: '#4CAF50', description: 'Vibrant Green: Productive, growing integrations.' },
    { color: '#FF5722', description: 'Fiery Red: Intense activity, focused on critical tasks.' }
  ];

  return {
    __esModule: true,
    ...originalModule,
    generateMood: jest.fn(() => {
      const currentMood = mockMoods[mockMoodIndex];
      mockMoodIndex = (mockMoodIndex + 1) % mockMoods.length;
      return currentMood;
    }),
    resetMoodIndex: jest.fn(() => {
      mockMoodIndex = 0;
    })
  };
});

describe('MoodRing Component', () => {
  beforeEach(() => {
    // Reset the mock mood index before each test to ensure consistent starting state
    resetMoodIndex();
    // Clear any previous mock calls
    generateMood.mockClear();
  });

  test('renders with initial mood', () => {
    render(<App />);
    expect(screen.getByText(/Current Mood: Serene Blue/i)).toBeInTheDocument();
    expect(generateMood).toHaveBeenCalledTimes(1); // Called once for initial state
  });

  test('changes mood on button click', () => {
    render(<App />);
    const refreshButton = screen.getByText(/Simulate New Agent Activity/i);

    // Initial mood
    expect(screen.getByText(/Current Mood: Serene Blue/i)).toBeInTheDocument();

    // Click once, should go to next mood
    fireEvent.click(refreshButton);
    expect(screen.getByText(/Current Mood: Vibrant Green/i)).toBeInTheDocument();
    expect(generateMood).toHaveBeenCalledTimes(2); // Initial + 1 click

    // Click again, should go to next mood
    fireEvent.click(refreshButton);
    expect(screen.getByText(/Current Mood: Fiery Red/i)).toBeInTheDocument();
    expect(generateMood).toHaveBeenCalledTimes(3); // Initial + 2 clicks

    // Click again, should cycle back to first mood
    fireEvent.click(refreshButton);
    expect(screen.getByText(/Current Mood: Serene Blue/i)).toBeInTheDocument();
    expect(generateMood).toHaveBeenCalledTimes(4); // Initial + 3 clicks
  });

  test('MoodRing component displays correct mood description and color', () => {
    const testMood = { color: '#123456', description: 'Test Mood: Feeling good!' };
    render(<MoodRing mood={testMood} />);
    
    const moodDescription = screen.getByText('Current Mood: Test Mood: Feeling good!');
    expect(moodDescription).toBeInTheDocument();
    expect(moodDescription).toHaveStyle('color: #123456');

    const moodRingElement = screen.getByTestId('mood-ring-element');
    expect(moodRingElement).toBeInTheDocument();
    expect(moodRingElement).toHaveStyle('border-color: #123456');
  });

  test('App component auto-refreshes mood after interval', async () => {
    jest.useFakeTimers();
    render(<App />);

    // Initial mood
    expect(screen.getByText(/Current Mood: Serene Blue/i)).toBeInTheDocument();
    expect(generateMood).toHaveBeenCalledTimes(1);

    // Advance timers by 30 seconds
    jest.advanceTimersByTime(30000);
    expect(screen.getByText(/Current Mood: Vibrant Green/i)).toBeInTheDocument();
    expect(generateMood).toHaveBeenCalledTimes(2);

    // Advance timers again
    jest.advanceTimersByTime(30000);
    expect(screen.getByText(/Current Mood: Fiery Red/i)).toBeInTheDocument();
    expect(generateMood).toHaveBeenCalledTimes(3);

    jest.useRealTimers();
  });
});
