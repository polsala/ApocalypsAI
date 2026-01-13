import '@testing-library/jest-dom';
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

test('renders initial forecast', () => {
  render(<App />);
  const heading = screen.getByText(/Apocalypse Weather Forecast/i);
  expect(heading).toBeInTheDocument();
  const button = screen.getByRole('button', { name: /Generate New Forecast/i });
  expect(button).toBeInTheDocument();
});

test('generates new forecast on button click', () => {
  // Mock Math.random to produce deterministic but different values for two renders
  const mockRandom = jest.spyOn(Math, 'random')
    .mockReturnValueOnce(0.1) // first location
    .mockReturnValueOnce(0.2) // first condition
    .mockReturnValueOnce(0.3) // second location
    .mockReturnValueOnce(0.4); // second condition

  render(<App />);
  const first = screen.getByText(/is experiencing/i).textContent;
  const button = screen.getByRole('button', { name: /Generate New Forecast/i });
  fireEvent.click(button);
  const second = screen.getByText(/is experiencing/i).textContent;
  expect(first).not.toBe(second);
  mockRandom.mockRestore();
});

