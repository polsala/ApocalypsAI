import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

// Mock rationale: Math.random is used for initial dust bunny positions and velocities.
// For deterministic tests, we need to mock it to ensure consistent rendering and behavior.
// We don't need to test the exact random positions, but rather that the components render
// and respond to interactions correctly, regardless of their initial random placement.
const mockMath = Object.create(global.Math);
mockMath.random = () => 0.5; // Always return 0.5 for deterministic positions/sizes
global.Math = mockMath;

describe('App', () => {
  test('renders header and initial counts', () => {
    render(<App />);
    expect(screen.getByText(/Cosmic Dust Bunny Collector/i)).toBeInTheDocument();
    expect(screen.getByText(/Collected Dust Bunnies: 0/i)).toBeInTheDocument();
    expect(screen.getByText(/Suggestions Completed: 0 \/ 5/i)).toBeInTheDocument();
  });

  test('renders initial dust bunnies', () => {
    render(<App />);
    // There are 10 initial dust bunnies, each with a title attribute
    const dustBunnies = screen.getAllByTitle(/Click to collect this digital dust bunny!/i);
    expect(dustBunnies).toHaveLength(10);
  });

  test('collecting a dust bunny increases the collected count', () => {
    render(<App />);
    const initialCountElement = screen.getByText(/Collected Dust Bunnies: 0/i);
    expect(initialCountElement).toBeInTheDocument();

    const dustBunny = screen.getAllByTitle(/Click to collect this digital dust bunny!/i)[0];
    fireEvent.click(dustBunny);

    expect(screen.getByText(/Collected Dust Bunnies: 1/i)).toBeInTheDocument();
    expect(initialCountElement).not.toBeInTheDocument(); // Old count should be gone
  });

  test('renders initial suggestions', () => {
    render(<App />);
    expect(screen.getByText(/Close 5 unused browser tabs that have been open for eons./i)).toBeInTheDocument();
    expect(screen.getByText(/Delete files older than 1 year from your Downloads folder./i)).toBeInTheDocument();
    expect(screen.getAllByRole('button', { name: /Complete/i })).toHaveLength(5);
  });

  test('completing a suggestion updates the completed count and marks it as done', () => {
    render(<App />);
    const initialSuggestionsCount = screen.getByText(/Suggestions Completed: 0 \/ 5/i);
    expect(initialSuggestionsCount).toBeInTheDocument();

    const completeButton = screen.getAllByRole('button', { name: /Complete/i })[0];
    fireEvent.click(completeButton);

    expect(screen.getByText(/Suggestions Completed: 1 \/ 5/i)).toBeInTheDocument();
    expect(initialSuggestionsCount).not.toBeInTheDocument(); // Old count should be gone

    // Check if the suggestion text is now line-through (visual indicator of completion)
    const completedSuggestionText = screen.getByText(/Close 5 unused browser tabs that have been open for eons./i);
    expect(completedSuggestionText).toHaveStyle('text-decoration: line-through');
    expect(completedSuggestionText.closest('.suggestion-card')).toHaveStyle('background-color: #4CAF50');

    // The 'Complete' button for this specific suggestion should no longer be present
    expect(completedSuggestionText.closest('.suggestion-card')).not.toHaveTextContent('Complete');
  });

  test('collecting a dust bunny removes it from the screen', () => {
    render(<App />);
    const dustBunniesBefore = screen.getAllByTitle(/Click to collect this digital dust bunny!/i);
    expect(dustBunniesBefore).toHaveLength(10);

    fireEvent.click(dustBunniesBefore[0]);

    const dustBunniesAfter = screen.getAllByTitle(/Click to collect this digital dust bunny!/i);
    expect(dustBunniesAfter).toHaveLength(9);
  });
});
