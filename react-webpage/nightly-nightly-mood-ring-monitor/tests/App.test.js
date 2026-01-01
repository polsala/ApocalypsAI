import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import React from 'react';

// Mock rationale: We are testing the internal logic of the App component,
// specifically its sentiment analysis function. We don't need to mock
// external APIs or complex browser behaviors. We directly test the
// sentiment logic and verify UI updates based on state changes.
// React Testing Library provides a simulated DOM environment for component rendering.

describe('App Component', () => {
  test('renders Nightly Mood Ring Monitor title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Mood Ring Monitor/i)).toBeInTheDocument();
  });

  test('initial sentiment is neutral', () => {
    render(<App />);
    expect(screen.getByText(/Current Mood: NEUTRAL/i)).toBeInTheDocument();
    const moodRing = screen.getByTestId('mood-ring');
    expect(moodRing).toHaveStyle('background-color: #FFEB3B'); // Neutral yellow
  });

  test('sentiment changes to positive for positive input', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your daily logs/i);
    fireEvent.change(textarea, { target: { value: 'Today was a great day, full of success and hope!' } });
    expect(screen.getByText(/Current Mood: POSITIVE/i)).toBeInTheDocument();
    const moodRing = screen.getByTestId('mood-ring');
    expect(moodRing).toHaveStyle('background-color: #4CAF50'); // Positive green
  });

  test('sentiment changes to negative for negative input', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your daily logs/i);
    fireEvent.change(textarea, { target: { value: 'There was a threat of chaos and danger, a truly bad situation.' } });
    expect(screen.getByText(/Current Mood: NEGATIVE/i)).toBeInTheDocument();
    const moodRing = screen.getByTestId('mood-ring');
    expect(moodRing).toHaveStyle('background-color: #F44336'); // Negative red
  });

  test('sentiment remains neutral for balanced input', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your daily logs/i);
    fireEvent.change(textarea, { target: { value: 'Some good news, but also some bad news. It was a day of mixed feelings.' } });
    expect(screen.getByText(/Current Mood: NEUTRAL/i)).toBeInTheDocument();
    const moodRing = screen.getByTestId('mood-ring');
    expect(moodRing).toHaveStyle('background-color: #FFEB3B'); // Neutral yellow
  });

  test('sentiment remains neutral for empty input', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your daily logs/i);
    fireEvent.change(textarea, { target: { value: '' } });
    expect(screen.getByText(/Current Mood: NEUTRAL/i)).toBeInTheDocument();
    const moodRing = screen.getByTestId('mood-ring');
    expect(moodRing).toHaveStyle('background-color: #FFEB3B'); // Neutral yellow
  });

  test('sentiment handles case insensitivity', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your daily logs/i);
    fireEvent.change(textarea, { target: { value: 'GREAT success, but also some DANGER.' } });
    expect(screen.getByText(/Current Mood: NEUTRAL/i)).toBeInTheDocument(); // 1 positive, 1 negative
    const moodRing = screen.getByTestId('mood-ring');
    expect(moodRing).toHaveStyle('background-color: #FFEB3B'); // Neutral yellow
  });

  test('sentiment handles multiple occurrences of same keyword', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your daily logs/i);
    fireEvent.change(textarea, { target: { value: 'Great, great, great success!' } });
    expect(screen.getByText(/Current Mood: POSITIVE/i)).toBeInTheDocument();
    const moodRing = screen.getByTestId('mood-ring');
    expect(moodRing).toHaveStyle('background-color: #4CAF50'); // Positive green
  });

  test('sentiment handles multiple different positive keywords', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your daily logs/i);
    fireEvent.change(textarea, { target: { value: 'Hope and victory, truly a safe and calm day.' } });
    expect(screen.getByText(/Current Mood: POSITIVE/i)).toBeInTheDocument();
    const moodRing = screen.getByTestId('mood-ring');
    expect(moodRing).toHaveStyle('background-color: #4CAF50'); // Positive green
  });

  test('sentiment handles multiple different negative keywords', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your daily logs/i);
    fireEvent.change(textarea, { target: { value: 'Fear and threat, a broken and lost cause.' } });
    expect(screen.getByText(/Current Mood: NEGATIVE/i)).toBeInTheDocument();
    const moodRing = screen.getByTestId('mood-ring');
    expect(moodRing).toHaveStyle('background-color: #F44336'); // Negative red
  });
});
