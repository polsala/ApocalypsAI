import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App.jsx';

// Mock Date globally â deterministic tests
function mockDate(isoString) {
  const mock = new Date(isoString);
  const OriginalDate = global.Date;
  // eslint-disable-next-line no-global-assign
  global.Date = class extends OriginalDate {
    constructor(...args) {
      if (args.length) {
        return new OriginalDate(...args);
      }
      return mock;
    }
    static now() {
      return mock.getTime();
    }
  };
}

afterEach(() => {
  // Restore original Date after each test
  jest.restoreAllMocks();
  // eslint-disable-next-line no-global-assign
  global.Date = Date;
});

test('renders correct time format', () => {
  mockDate('2023-01-01T08:05:09Z'); // 08:05:09 UTC
  render(<App />);
  const timeElement = screen.getByText('08:05:09');
  expect(timeElement).toBeInTheDocument();
});

test('shows sun emoji during daytime (hour 9)', () => {
  mockDate('2023-01-01T09:15:00Z'); // hour 9
  render(<App />);
  const emoji = screen.getByLabelText('weather emoji');
  expect(emoji).toHaveTextContent('ð');
});

test('shows moon emoji during night (hour 22)', () => {
  mockDate('2023-01-01T22:45:00Z'); // hour 22
  render(<App />);
  const emoji = screen.getByLabelText('weather emoji');
  expect(emoji).toHaveTextContent('ð');
});

test('shows cloud emoji for the overcast hour (12 pm)', () => {
  mockDate('2023-01-01T12:00:00Z'); // hour 12
  render(<App />);
  const emoji = screen.getByLabelText('weather emoji');
  expect(emoji).toHaveTextContent('âï¸');
});

