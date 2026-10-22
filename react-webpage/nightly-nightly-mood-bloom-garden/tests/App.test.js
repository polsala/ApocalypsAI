import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: Math.random is used in App.js to generate bloom properties
// (rotation, delay, x, y coordinates). Mocking it ensures that bloom generation
// is deterministic for testing purposes, preventing flaky tests due to random values.
const mockMathRandom = jest.spyOn(Math, 'random').mockReturnValue(0.5);

describe('App Component', () => {
  beforeEach(() => {
    // Ensure consistent random value for each test
    mockMathRandom.mockClear();
    mockMathRandom.mockReturnValue(0.5);
  });

  afterAll(() => {
    mockMathRandom.mockRestore(); // Restore original Math.random after all tests
  });

  test('renders Nightly Mood Bloom Garden title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Mood Bloom Garden/i)).toBeInTheDocument();
  });

  test('renders MoodInput component with initial mood level', () => {
    render(<App />);
    expect(screen.getByLabelText(/Mood Level: 5/i)).toBeInTheDocument();
    expect(screen.getByRole('slider')).toHaveValue('5');
  });

  test('renders BloomGarden component with initial blooms', () => {
    render(<App />);
    expect(screen.getByTestId('bloom-garden-container')).toBeInTheDocument();
    // For initial mood 5, it's 3 + floor(5/3) = 3 + 1 = 4 blooms
    expect(screen.getAllByTestId('bloom-item')).toHaveLength(4);
  });

  test('changing mood level updates the displayed mood and garden blooms count', () => {
    render(<App />);
    const moodSlider = screen.getByRole('slider');

    // Change mood to 10
    fireEvent.change(moodSlider, { target: { value: '10' } });
    expect(screen.getByLabelText(/Mood Level: 10/i)).toBeInTheDocument();
    expect(moodSlider).toHaveValue('10');

    // For mood 10, it's 3 + floor(10/3) = 3 + 3 = 6 blooms
    expect(screen.getAllByTestId('bloom-item')).toHaveLength(6);

    // Change mood to 1
    fireEvent.change(moodSlider, { target: { value: '1' } });
    expect(screen.getByLabelText(/Mood Level: 1/i)).toBeInTheDocument();
    expect(moodSlider).toHaveValue('1');

    // For mood 1, it's 3 + floor(1/3) = 3 + 0 = 3 blooms
    expect(screen.getAllByTestId('bloom-item')).toHaveLength(3);
  });

  test('bloom properties change based on mood level', () => {
    render(<App />);
    const moodSlider = screen.getByRole('slider');

    // Set mood to 1
    fireEvent.change(moodSlider, { target: { value: '1' } });
    const bloomsLowMood = screen.getAllByTestId('bloom-item');
    // Check a bloom's style for mood 1 (size = 20 + 1*5 = 25)
    expect(bloomsLowMood[0]).toHaveStyle('width: 25px');
    expect(bloomsLowMood[0]).toHaveStyle('height: 25px');
    // Hue for mood 1: 120 - 1*10 = 110 (greenish)
    expect(bloomsLowMood[0]).toHaveStyle('background-color: hsl(110, 55%, 52%)');

    // Set mood to 10
    fireEvent.change(moodSlider, { target: { value: '10' } });
    const bloomsHighMood = screen.getAllByTestId('bloom-item');
    // Check a bloom's style for mood 10 (size = 20 + 10*5 = 70)
    expect(bloomsHighMood[0]).toHaveStyle('width: 70px');
    expect(bloomsHighMood[0]).toHaveStyle('height: 70px');
    // Hue for mood 10: 120 - 10*10 = 20 (reddish)
    expect(bloomsHighMood[0]).toHaveStyle('background-color: hsl(20, 100%, 70%)');
  });
});
