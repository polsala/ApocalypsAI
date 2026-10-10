import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: Math.random is mocked to ensure deterministic mood generation for testing purposes,
// allowing specific mood states to be tested reliably without relying on true randomness.
const mockMath = Object.create(global.Math);
mockMath.random = () => 0.5; // Always return 0.5 for predictable mood selection
global.Math = mockMath;

describe('App Component', () => {
  beforeEach(() => {
    // Reset mock before each test to ensure consistent starting state
    mockMath.random = () => 0.5;
  });

  test('renders ApocalypsAI Mood Ring title', () => {
    render(<App />);
    const titleElement = screen.getByText(/ApocalypsAI Mood Ring/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('displays an initial mood on load', () => {
    render(<App />);
    // With Math.random() returning 0.5, and 6 moods, randomIndex will be floor(0.5 * 6) = 3
    // moods[3] is { color: '#87CEEB', description: 'Flowing smoothly, like a river of code.', emoji: '🌊' }
    const moodTextElement = screen.getByText(/Current Mood: Flowing smoothly, like a river of code! 🌊/i);
    expect(moodTextElement).toBeInTheDocument();
  });

  test('changes mood when refresh button is clicked', () => {
    render(<App />);
    // Initial mood (index 3)
    const initialMoodText = screen.getByText(/Current Mood: Flowing smoothly, like a river of code! 🌊/i);
    expect(initialMoodText).toBeInTheDocument();

    // Change Math.random to return a different value for the next call
    mockMath.random = () => 0.1; // This will result in moods[0]

    const refreshButton = screen.getByRole('button', { name: /Refresh Mood/i });
    fireEvent.click(refreshButton);

    // Expect the new mood to be displayed
    const newMoodText = screen.getByText(/Current Mood: Radiant with algorithmic joy! 🌈/i);
    expect(newMoodText).toBeInTheDocument();
    expect(initialMoodText).not.toBeInTheDocument(); // The old mood text should be gone
  });

  test('changes mood when mood ring is clicked', () => {
    render(<App />);
    // Initial mood (index 3)
    const initialMoodText = screen.getByText(/Current Mood: Flowing smoothly, like a river of code! 🌊/i);
    expect(initialMoodText).toBeInTheDocument();

    // Change Math.random to return a different value for the next call
    mockMath.random = () => 0.9; // This will result in moods[5]

    const moodRing = screen.getByTitle(/Click to refresh mood/i);
    fireEvent.click(moodRing);

    // Expect the new mood to be displayed
    const newMoodText = screen.getByText(/Current Mood: Too many unhandled exceptions today. 😠/i);
    expect(newMoodText).toBeInTheDocument();
    expect(initialMoodText).not.toBeInTheDocument(); // The old mood text should be gone
  });
});
