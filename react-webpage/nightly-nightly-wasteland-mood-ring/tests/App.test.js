import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: We are testing the component's rendering and state updates
// based on user interaction, not external API calls or complex side effects.
// The mood calculation logic is internal to the component and deterministic.

describe('App Component', () => {
  test('renders Wasteland Mood Ring title', () => {
    render(<App />);
    expect(screen.getByText(/Wasteland Mood Ring/i)).toBeInTheDocument();
  });

  test('initial mood is Cautious', () => {
    render(<App />);
    expect(screen.getByText(/A faint hum on the horizon/i)).toBeInTheDocument();
    const moodRing = screen.getByText(/A faint hum on the horizon/i).closest('.mood-ring');
    expect(moodRing).toHaveStyle('background-color: #FFEB3B'); // Yellow for Cautious
  });

  test('changes to Hopeful mood with optimal inputs', () => {
    render(<App />);

    fireEvent.change(screen.getByLabelText(/Scavenger Haul Quality:/i), { target: { value: 'bountiful' } });
    fireEvent.change(screen.getByLabelText(/Recent Mutant Encounters:/i), { target: { value: 'none' } });
    fireEvent.change(screen.getByLabelText(/Sky Condition:/i), { target: { value: 'clear' } });
    fireEvent.change(screen.getByLabelText(/Water Supply:/i), { target: { value: 'abundant' } });

    expect(screen.getByText(/The irradiated daisies are blooming!/i)).toBeInTheDocument();
    const moodRing = screen.getByText(/The irradiated daisies are blooming!/i).closest('.mood-ring');
    expect(moodRing).toHaveStyle('background-color: #8BC34A'); // Light Green for Hopeful
  });

  test('changes to Perilous mood with worst inputs', () => {
    render(<App />);

    fireEvent.change(screen.getByLabelText(/Scavenger Haul Quality:/i), { target: { value: 'poor' } });
    fireEvent.change(screen.getByLabelText(/Recent Mutant Encounters:/i), { target: { value: 'many' } });
    fireEvent.change(screen.getByLabelText(/Sky Condition:/i), { target: { value: 'ominous-green-glow' } });
    fireEvent.change(screen.getByLabelText(/Water Supply:/i), { target: { value: 'scarce' } });

    expect(screen.getByText(/The void whispers your name, and it sounds hungry./i)).toBeInTheDocument();
    const moodRing = screen.getByText(/The void whispers your name, and it sounds hungry./i).closest('.mood-ring');
    expect(moodRing).toHaveStyle('background-color: #F44336'); // Red for Perilous
  });

  test('changes to Cautious mood with mixed inputs', () => {
    render(<App />);

    // Set to a state that should result in Cautious (e.g., score 7-9)
    fireEvent.change(screen.getByLabelText(/Scavenger Haul Quality:/i), { target: { value: 'moderate' } }); // 2
    fireEvent.change(screen.getByLabelText(/Recent Mutant Encounters:/i), { target: { value: 'few' } });      // 2
    fireEvent.change(screen.getByLabelText(/Sky Condition:/i), { target: { value: 'cloudy' } });             // 2
    fireEvent.change(screen.getByLabelText(/Water Supply:/i), { target: { value: 'scarce' } });             // 1
    // Total score: 2+2+2+1 = 7 (Cautious range)

    expect(screen.getByText(/A faint hum on the horizon/i)).toBeInTheDocument();
    const moodRing = screen.getByText(/A faint hum on the horizon/i).closest('.mood-ring');
    expect(moodRing).toHaveStyle('background-color: #FFEB3B'); // Yellow for Cautious
  });
});
