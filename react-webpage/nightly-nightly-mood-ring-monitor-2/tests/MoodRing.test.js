import React from 'react';
import { render, screen } from '@testing-library/react';
import MoodRing from '../src/components/MoodRing';
import '@testing-library/jest-dom';

describe('MoodRing', () => {
  // Mock rationale: This component is purely presentational.
  // It receives props (score, color) and renders elements based on them.
  // We use @testing-library/react to render the component in a simulated DOM
  // and assert on its output, ensuring it correctly displays the mood and score.
  // No external dependencies or side effects are involved.

  test('renders with neutral mood and score 0', () => {
    render(<MoodRing score={0} color="#9E9E9E" />);
    expect(screen.getByText(/Current Mood: Neutral/i)).toBeInTheDocument();
    expect(screen.getByText(/Sentiment Score: 0/i)).toBeInTheDocument();
    const moodRingDiv = screen.getByRole('presentation', { name: /Mood Ring/i });
    expect(moodRingDiv).toHaveStyle('background-color: #9E9E9E');
  });

  test('renders with mild positive mood and score 1', () => {
    render(<MoodRing score={1} color="#CDDC39" />);
    expect(screen.getByText(/Current Mood: Mildly Positive/i)).toBeInTheDocument();
    expect(screen.getByText(/Sentiment Score: 1/i)).toBeInTheDocument();
    const moodRingDiv = screen.getByRole('presentation', { name: /Mood Ring/i });
    expect(moodRingDiv).toHaveStyle('background-color: #CDDC39');
  });

  test('renders with strong positive mood and score 6', () => {
    render(<MoodRing score={6} color="#4CAF50" />);
    expect(screen.getByText(/Current Mood: Strongly Positive/i)).toBeInTheDocument();
    expect(screen.getByText(/Sentiment Score: 6/i)).toBeInTheDocument();
    const moodRingDiv = screen.getByRole('presentation', { name: /Mood Ring/i });
    expect(moodRingDiv).toHaveStyle('background-color: #4CAF50');
  });

  test('renders with mild negative mood and score -1', () => {
    render(<MoodRing score={-1} color="#FFC107" />);
    expect(screen.getByText(/Current Mood: Mildly Negative/i)).toBeInTheDocument();
    expect(screen.getByText(/Sentiment Score: -1/i)).toBeInTheDocument();
    const moodRingDiv = screen.getByRole('presentation', { name: /Mood Ring/i });
    expect(moodRingDiv).toHaveStyle('background-color: #FFC107');
  });

  test('renders with strong negative mood and score -6', () => {
    render(<MoodRing score={-6} color="#F44336" />);
    expect(screen.getByText(/Current Mood: Strongly Negative/i)).toBeInTheDocument();
    expect(screen.getByText(/Sentiment Score: -6/i)).toBeInTheDocument();
    const moodRingDiv = screen.getByRole('presentation', { name: /Mood Ring/i });
    expect(moodRingDiv).toHaveStyle('background-color: #F44336');
  });
});
