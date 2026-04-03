import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';
import * as SentimentAnalyzer from '../src/SentimentAnalyzer';

// Mock rationale: The SentimentAnalyzer is a simple utility, but for App.test.js,
// we want to ensure its behavior is predictable and isolated from the actual keyword logic.
// This allows us to test the App's state management and rendering based on known sentiment results.
jest.mock('../src/SentimentAnalyzer', () => ({
  analyzeSentiment: jest.fn((text) => {
    if (text.toLowerCase().includes('happy') || text.toLowerCase().includes('good')) {
      return { label: 'positive' };
    } else if (text.toLowerCase().includes('sad') || text.toLowerCase().includes('bad')) {
      return { label: 'negative' };
    } else {
      return { label: 'neutral' };
    }
  }),
}));

describe('App', () => {
  beforeEach(() => {
    // Reset the mock before each test
    SentimentAnalyzer.analyzeSentiment.mockClear();
  });

  test('renders the main title and initial neutral mood orb', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Mood Orb Calibrator/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Paste your message/i)).toBeInTheDocument();
    expect(screen.getByText(/Calibrate Mood/i)).toBeInTheDocument();
    // Initial mood orb should be neutral (yellow background, neutral emoji)
    const moodOrb = screen.getByRole('img', { name: /neutral mood/i }).closest('.mood-orb');
    expect(moodOrb).toHaveStyle('background-color: #FFEB3B');
    expect(screen.getByRole('img', { name: /neutral mood/i })).toHaveTextContent('😐');
  });

  test('updates mood orb to positive for positive text', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your message/i);
    const button = screen.getByText(/Calibrate Mood/i);

    fireEvent.change(textarea, { target: { value: 'This is a happy message.' } });
    fireEvent.click(button);

    // Assert that the mock was called
    expect(SentimentAnalyzer.analyzeSentiment).toHaveBeenCalledWith('This is a happy message.');

    // Mood orb should be positive (green background, positive emoji)
    const moodOrb = screen.getByRole('img', { name: /positive mood/i }).closest('.mood-orb');
    expect(moodOrb).toHaveStyle('background-color: #8BC34A');
    expect(screen.getByRole('img', { name: /positive mood/i })).toHaveTextContent('😊');
  });

  test('updates mood orb to negative for negative text', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your message/i);
    const button = screen.getByText(/Calibrate Mood/i);

    fireEvent.change(textarea, { target: { value: 'This is a sad message.' } });
    fireEvent.click(button);

    // Assert that the mock was called
    expect(SentimentAnalyzer.analyzeSentiment).toHaveBeenCalledWith('This is a sad message.');

    // Mood orb should be negative (red background, negative emoji)
    const moodOrb = screen.getByRole('img', { name: /negative mood/i }).closest('.mood-orb');
    expect(moodOrb).toHaveStyle('background-color: #F44336');
    expect(screen.getByRole('img', { name: /negative mood/i })).toHaveTextContent('😟');
  });

  test('updates mood orb to neutral for ambiguous text', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste your message/i);
    const button = screen.getByText(/Calibrate Mood/i);

    fireEvent.change(textarea, { target: { value: 'The weather is cloudy today.' } });
    fireEvent.click(button);

    // Assert that the mock was called
    expect(SentimentAnalyzer.analyzeSentiment).toHaveBeenCalledWith('The weather is cloudy today.');

    // Mood orb should be neutral (yellow background, neutral emoji)
    const moodOrb = screen.getByRole('img', { name: /neutral mood/i }).closest('.mood-orb');
    expect(moodOrb).toHaveStyle('background-color: #FFEB3B');
    expect(screen.getByRole('img', { name: /neutral mood/i })).toHaveTextContent('😐');
  });
});
