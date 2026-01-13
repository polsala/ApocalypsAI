import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

test('gear list is not shown initially', () => {
  render(<App />);
  const gearList = screen.queryByTestId('gear-list');
  expect(gearList).not.toBeInTheDocument();
});

test('displays gear list after selecting an environment', () => {
  render(<App />);
  const select = screen.getByTestId('env-select');
  fireEvent.change(select, { target: { value: 'desert' } });
  const gearList = screen.getByTestId('gear-list');
  expect(gearList).toBeInTheDocument();
  expect(gearList).toHaveTextContent('Sunshade Cloak');
  expect(gearList).toHaveTextContent('Cactus Water Filter');
  expect(gearList).toHaveTextContent('Sandstorm Goggles');
});

// Mock rationale: tests are fully deterministic, no network calls, and use static data.
