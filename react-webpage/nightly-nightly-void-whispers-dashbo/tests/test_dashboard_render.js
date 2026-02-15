// Mock rationale: Simulate DOM environment without browser
import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../src/App';

test('renders dashboard title', () => {
  render(<App />);
  const titleElement = screen.getByText(/\.Void Whispers Dashboard/i);
  expect(titleElement).toBeInTheDocument();
});

test('displays survival metrics', () => {
  render(<App />);
  const metricElement = screen.getByText(/Survival Rate: 92%/i);
  expect(metricElement).toBeInTheDocument();
});

test('shows void whispers', () => {
  render(<App />);
  const whisperElement = screen.getByText(/The void hums with forgotten echoes\./i);
  expect(whisperElement).toBeInTheDocument();
});
