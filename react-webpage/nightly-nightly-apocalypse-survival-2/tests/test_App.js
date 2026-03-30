// Mock rationale: Simulate user interactions and verify state updates without external dependencies.
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

it('renders resource tracker', () => {
  render(<App />);
  expect(screen.getByText(/Resource Levels/i)).toBeInTheDocument();
});

it('logs activity correctly', () => {
  render(<App />);
  const input = screen.getByPlaceholderText(/Log today's activity.../i);
  const button = screen.getByText(/Add/i);
  
  fireEvent.change(input, { target: { value: 'Scavenged for supplies' } });
  fireEvent.click(button);
  
  expect(screen.getByText(/Scavenged for supplies/i)).toBeInTheDocument();
});
