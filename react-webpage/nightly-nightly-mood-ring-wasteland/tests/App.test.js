import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: The `analyzeSentiment` function is internal to App.js and
// uses a simple keyword-based approach. We are testing the component's
// reaction to input and how it displays the result of this internal logic,
// not the sophistication of the sentiment analysis itself.
// The tests directly interact with the DOM elements and verify their state
// changes based on user input, which implicitly tests the `analyzeSentiment`
// function's integration with the component.

describe('App Component', () => {
  test('renders Nightly Wasteland Mood Ring title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Wasteland Mood Ring/i)).toBeInTheDocument();
  });

  test('initial mood ring is Void Black for empty input', () => {
    render(<App />);
    const moodRing = screen.getByLabelText(/mood-ring/i); 
    expect(screen.getByText(/Void Black: Awaiting input/i)).toBeInTheDocument();
    expect(moodRing).toHaveStyle('background-color: #212121');
  });

  test('mood ring changes to Radiant Green for positive sentiment', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Type your message/i);
    fireEvent.change(textarea, { target: { value: 'Found a safe place, feeling hopeful!' } });

    const moodRing = screen.getByLabelText(/mood-ring/i);
    expect(screen.getByText(/Radiant Green: A beacon of hope/i)).toBeInTheDocument();
    expect(moodRing).toHaveStyle('background-color: #4CAF50');
  });

  test('mood ring changes to Scorched Red for negative sentiment', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Type your message/i);
    fireEvent.change(textarea, { target: { value: 'Raiders attacked, danger everywhere!' } });

    const moodRing = screen.getByLabelText(/mood-ring/i);
    expect(screen.getByText(/Scorched Red: Danger looms/i)).toBeInTheDocument();
    expect(moodRing).toHaveStyle('background-color: #F44336');
  });

  test('mood ring changes to Dusty Grey for neutral sentiment', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Type your message/i);
    fireEvent.change(textarea, { target: { value: 'Scavenge for water and food.' } });

    const moodRing = screen.getByLabelText(/mood-ring/i);
    expect(screen.getByText(/Dusty Grey: Calm, factual/i)).toBeInTheDocument();
    expect(moodRing).toHaveStyle('background-color: #9E9E9E');
  });

  test('mood ring changes to Flickering Amber for uncertain/mixed sentiment', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Type your message/i);
    fireEvent.change(textarea, { target: { value: 'Found some supplies but heard whispers of a new threat.' } });

    const moodRing = screen.getByLabelText(/mood-ring/i);
    expect(screen.getByText(/Flickering Amber: A mix of feelings/i)).toBeInTheDocument();
    expect(moodRing).toHaveStyle('background-color: #FFC107');
  });

  test('clearing input resets to Void Black', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Type your message/i);
    fireEvent.change(textarea, { target: { value: 'Feeling good!' } });
    expect(screen.getByText(/Radiant Green/i)).toBeInTheDocument();

    fireEvent.change(textarea, { target: { value: '' } });
    expect(screen.getByText(/Void Black: Awaiting input/i)).toBeInTheDocument();
    const moodRing = screen.getByLabelText(/mood-ring/i);
    expect(moodRing).toHaveStyle('background-color: #212121');
  });
});
