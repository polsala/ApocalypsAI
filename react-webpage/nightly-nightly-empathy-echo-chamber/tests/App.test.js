import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App'; // Adjust path as necessary
import '@testing-library/jest-dom';

// Mock rationale: We are testing the React component's behavior, not the actual sentiment analysis logic.
// The sentiment analysis is a simplified, internal function that we want to ensure is called
// and that its return value correctly updates the UI.
jest.mock('../src/EmpathyVisualizer', () => {
  return ({ mood, color }) => (
    <div data-testid="empathy-visualizer" style={{ backgroundColor: color }}>
      <p data-testid="visualizer-mood">{mood ? `Feeling: ${mood.charAt(0).toUpperCase() + mood.slice(1)}` : 'Awaiting input...'}</p>
    </div>
  );
});

describe('App Component', () => {
  test('renders the main title and input elements', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Empathy Echo Chamber/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Type your message, log entry, or thought here.../i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Echo Sentiment/i })).toBeInTheDocument();
    expect(screen.getByTestId('visualizer-mood')).toHaveTextContent('Awaiting input...');
  });

  test('updates input text on change', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Type your message, log entry, or thought here.../i);
    fireEvent.change(textarea, { target: { value: 'This is a test message.' } });
    expect(textarea.value).toBe('This is a test message.');
  });

  test('displays "Awaiting input..." when text is empty and button is clicked', () => {
    render(<App />);
    const button = screen.getByRole('button', { name: /Echo Sentiment/i });
    fireEvent.click(button);
    expect(screen.getByTestId('visualizer-mood')).toHaveTextContent('Awaiting input...');
    expect(screen.getByTestId('empathy-visualizer')).toHaveStyle('background-color: #333');
  });

  test('updates mood and color based on input containing "hope"', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Type your message, log entry, or thought here.../i);
    const button = screen.getByRole('button', { name: /Echo Sentiment/i });

    fireEvent.change(textarea, { target: { value: 'I have great hope for the future.' } });
    fireEvent.click(button);

    expect(screen.getByTestId('visualizer-mood')).toHaveTextContent('Feeling: Hopeful');
    expect(screen.getByTestId('empathy-visualizer')).toHaveStyle('background-color: #4CAF50'); // Green
  });

  test('updates mood and color based on input containing "danger"', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Type your message, log entry, or thought here.../i);
    const button = screen.getByRole('button', { name: /Echo Sentiment/i });

    fireEvent.change(textarea, { target: { value: 'There is danger ahead.' } });
    fireEvent.click(button);

    expect(screen.getByTestId('visualizer-mood')).toHaveTextContent('Feeling: Tense');
    expect(screen.getByTestId('empathy-visualizer')).toHaveStyle('background-color: #FF5722'); // Orange-Red
  });

  test('updates mood and color based on input containing "calm"', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Type your message, log entry, or thought here.../i);
    const button = screen.getByRole('button', { name: /Echo Sentiment/i });

    fireEvent.change(textarea, { target: { value: 'All is calm and peaceful.' } });
    fireEvent.click(button);

    expect(screen.getByTestId('visualizer-mood')).toHaveTextContent('Feeling: Calm');
    expect(screen.getByTestId('empathy-visualizer')).toHaveStyle('background-color: #2196F3'); // Blue
  });

  test('updates mood and color based on input containing "chaos"', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Type your message, log entry, or thought here.../i);
    const button = screen.getByRole('button', { name: /Echo Sentiment/i });

    fireEvent.change(textarea, { target: { value: 'The situation is pure chaos.' } });
    fireEvent.click(button);

    expect(screen.getByTestId('visualizer-mood')).toHaveTextContent('Feeling: Chaotic');
    expect(screen.getByTestId('empathy-visualizer')).toHaveStyle('background-color: #F44336'); // Red
  });

  // Test for default/random behavior (less deterministic, but ensures fallback)
  test('updates mood and color for unclassified input (random fallback)', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Type your message, log entry, or thought here.../i);
    const button = screen.getByRole('button', { name: /Echo Sentiment/i });

    fireEvent.change(textarea, { target: { value: 'A simple neutral statement.' } });
    fireEvent.click(button);

    const currentMoodText = screen.getByTestId('visualizer-mood').textContent;
    const currentColor = screen.getByTestId('empathy-visualizer').style.backgroundColor;

    // Check if the mood text starts with "Feeling: " and then one of the possible moods
    expect(currentMoodText).toMatch(/^Feeling: (Calm|Tense|Hopeful|Chaotic)$/);
    // Check if the color is not the default, implying it changed to one of the sentiment colors.
    expect(currentColor).not.toBe('rgb(51, 51, 51)'); // Not the default #333
  });
});
