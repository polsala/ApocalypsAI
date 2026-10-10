import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import MoodOrb from '../src/MoodOrb';

describe('MoodOrb', () => {
  test('renders with neutral sentiment by default or explicitly', () => {
    const { rerender } = render(<MoodOrb sentiment="neutral" />);
    const orbNeutral = screen.getByRole('img', { name: /neutral mood/i }).closest('.mood-orb');
    expect(orbNeutral).toHaveStyle('background-color: #FFEB3B'); // Yellow
    expect(screen.getByRole('img', { name: /neutral mood/i })).toHaveTextContent('😐');

    // Test with no sentiment prop (should default to neutral)
    rerender(<MoodOrb />);
    const orbDefault = screen.getByRole('img', { name: /neutral mood/i }).closest('.mood-orb');
    expect(orbDefault).toHaveStyle('background-color: #FFEB3B');
    expect(screen.getByRole('img', { name: /neutral mood/i })).toHaveTextContent('😐');
  });

  test('renders with positive sentiment', () => {
    render(<MoodOrb sentiment="positive" />);
    const orbPositive = screen.getByRole('img', { name: /positive mood/i }).closest('.mood-orb');
    expect(orbPositive).toHaveStyle('background-color: #8BC34A'); // Green
    expect(screen.getByRole('img', { name: /positive mood/i })).toHaveTextContent('😊');
  });

  test('renders with negative sentiment', () => {
    render(<MoodOrb sentiment="negative" />);
    const orbNegative = screen.getByRole('img', { name: /negative mood/i }).closest('.mood-orb');
    expect(orbNegative).toHaveStyle('background-color: #F44336'); // Red
    expect(screen.getByRole('img', { name: /negative mood/i })).toHaveTextContent('😟');
  });
});
