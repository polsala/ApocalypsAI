import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import MoodCalendar from '../src/App.jsx';

test('renders correct emojis for known dates', () => {
  render(<MoodCalendar startDate="2023-01-01" days={3} />);
  const first = screen.getByText(/2023-01-01:/);
  const second = screen.getByText(/2023-01-02:/);
  const third = screen.getByText(/2023-01-03:/);
  expect(first).toHaveTextContent('ð');
  expect(second).toHaveTextContent('ð');
  expect(third).toHaveTextContent('ð');
});
