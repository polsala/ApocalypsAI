import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: Math.random is mocked to ensure deterministic test results
// when simulating new moods. Without this, tests would be flaky due to random selection.
const mockMathRandom = (returnValue) => {
  const mock = jest.spyOn(Math, 'random').mockReturnValue(returnValue);
  return mock;
};

const moods = [
  { name: 'Serene Void', color: '#2196F3', description: 'A state of calm acceptance, perhaps even peace amidst the desolation. The community is stable and reflective.' },
  { name: 'Whispering Hope', color: '#4CAF50', description: 'Signs of growth, optimism, and resilience. New ideas are budding, and spirits are lifting.' },
  { name: 'Anxious Static', color: '#FFEB3B', description: 'A sense of unease, caution, or low-level stress. The community is vigilant, perhaps anticipating change or minor threats.' },
  { name: 'Temporal Flux', color: '#FF9800', description: 'Unpredictability and rapid shifts. Things are in motion, and adaptability is key. Could indicate minor temporal anomalies or rapid environmental changes.' },
  { name: 'Despair\'s Embrace', color: '#D32F2F', description: 'Low morale, distress, or significant challenges. The community might be struggling with resource scarcity, illness, or existential dread.' },
  { name: 'Chaotic Spark', color: '#9C27B0', description: 'High energy, unpredictable, and potentially volatile. This could be a precursor to innovation or conflict, a period of intense activity.' }
];

describe('Apocalypse Mood Ring', () => {
  afterEach(() => {
    jest.restoreAllMocks(); // Clean up mocks after each test
  });

  test('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Apocalypse Mood Ring/i)).toBeInTheDocument();
  });

  test('renders an initial mood', () => {
    render(<App />);
    // By default, it should render the first mood in the array
    expect(screen.getByText(moods[0].name)).toBeInTheDocument();
    expect(screen.getByText(moods[0].description)).toBeInTheDocument();
  });

  test('changes mood when "Simulate New Mood" button is clicked', () => {
    // Mock Math.random to return a specific index (e.g., index 1 for Whispering Hope)
    const mock = mockMathRandom(0.2); // This will result in floor(0.2 * 6) = 1
    render(<App />);

    const button = screen.getByRole('button', { name: /Simulate New Mood/i });
    fireEvent.click(button);

    // Expect the mood to change to the one at index 1
    expect(screen.getByText(moods[1].name)).toBeInTheDocument();
    expect(screen.getByText(moods[1].description)).toBeInTheDocument();
    expect(mock).toHaveBeenCalled();
  });

  test('changes to a different mood on subsequent clicks', () => {
    // Mock Math.random to cycle through specific indices
    const mock = jest.spyOn(Math, 'random');
    mock.mockReturnValueOnce(0.2); // Index 1 (Whispering Hope)
    mock.mockReturnValueOnce(0.8); // Index 4 (Despair's Embrace)

    render(<App />);
    const button = screen.getByRole('button', { name: /Simulate New Mood/i });

    // First click
    fireEvent.click(button);
    expect(screen.getByText(moods[1].name)).toBeInTheDocument();
    expect(screen.getByText(moods[1].description)).toBeInTheDocument();

    // Second click
    fireEvent.click(button);
    expect(screen.getByText(moods[4].name)).toBeInTheDocument();
    expect(screen.getByText(moods[4].description)).toBeInTheDocument();
    expect(mock).toHaveBeenCalledTimes(2);
  });

  test('mood ring displays correct background color', () => {
    const mock = mockMathRandom(0.5); // Index 3 (Temporal Flux)
    render(<App />);
    const button = screen.getByRole('button', { name: /Simulate New Mood/i });
    fireEvent.click(button);

    const moodRing = screen.getByText(moods[3].name).closest('.mood-ring');
    expect(moodRing).toHaveStyle(`background-color: ${moods[3].color}`);
    expect(mock).toHaveBeenCalled();
  });
});
