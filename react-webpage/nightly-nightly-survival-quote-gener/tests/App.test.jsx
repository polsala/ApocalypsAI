import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

describe('App', () => {
  const originalMath = Math;

  beforeAll(() => {
    // Mock Math.random to return a predictable sequence
    let callCount = 0;
    global.Math = {
      ...originalMath,
      random: () => {
        const sequence = [0.1, 0.6]; // will map to indices 0 and 3
        return sequence[callCount++] ?? 0.1;
      }
    };
  });

  afterAll(() => {
    global.Math = originalMath;
  });

  test('displays initial quote and changes on button click', () => {
    render(<App />);
    const quoteEl = screen.getByTestId('quote');
    expect(quoteEl.textContent).toBe('When the world ends, make sure your coffee is still hot.');
    const button = screen.getByText('New Quote');
    fireEvent.click(button);
    expect(quoteEl.textContent).toBe('Never trust a mutant with a smile.');
  });
});
