import { render, screen } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: Simulate static content rendering without external dependencies

test('renders header title', () => {
  render(<App />);
  const headerElement = screen.getByText(/Apocalypse Survival Dashboard/i);
  expect(headerElement).toBeInTheDocument();
});

test('renders resource tracker section', () => {
  render(<App />);
  const resourceElement = screen.getByText(/Resources/i);
  expect(resourceElement).toBeInTheDocument();
});

test('renders skill readiness section', () => {
  render(<App />);
  const skillElement = screen.getByText(/Survival Skills/i);
  expect(skillElement).toBeInTheDocument();
});

test('renders weather forecast section', () => {
  render(<App />);
  const weatherElement = screen.getByText(/Wasteland Weather/i);
  expect(weatherElement).toBeInTheDocument();
});

test('renders affirmation board section', () => {
  render(<App />);
  const affirmationElement = screen.getByText(/Daily Affirmation/i);
  expect(affirmationElement).toBeInTheDocument();
});
