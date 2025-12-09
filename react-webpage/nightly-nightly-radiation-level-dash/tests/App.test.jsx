import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

test('renders slider and gauge with initial safe state', () => {
  render(<App />);
  const slider = screen.getByTestId('level-slider');
  expect(slider).toBeInTheDocument();

  const fill = screen.getByTestId('gauge-fill');
  expect(fill).toHaveStyle('width: 0%');

  const message = screen.getByTestId('gauge-message');
  expect(message).toHaveTextContent('Safe');
});

test('updates gauge color and message when slider changes', () => {
  render(<App />);
  const slider = screen.getByTestId('level-slider');
  fireEvent.change(slider, { target: { value: '80' } });

  const fill = screen.getByTestId('gauge-fill');
  expect(fill).toHaveStyle('width: 80%');
  expect(fill).toHaveStyle('background-color: red');

  const message = screen.getByTestId('gauge-message');
  expect(message).toHaveTextContent('Danger');
});
