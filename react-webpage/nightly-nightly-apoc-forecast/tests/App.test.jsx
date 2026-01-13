import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

test('generates a forecast on button click', () => {
  render(<App />);
  const button = screen.getByText(/generate forecast/i);
  fireEvent.click(button);
  const forecast = screen.getByTestId('forecast');
  expect(forecast).toBeInTheDocument();
  expect(forecast.textContent).toMatch(/: /);
});
