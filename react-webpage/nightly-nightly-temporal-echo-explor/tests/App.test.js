import { render, screen } from '@testing-library/react';
import App from '../src/App';

test('renders Temporal Echo Explorer header', () => {
  render(<App />);
  const headerElement = screen.getByText(/Temporal Echo Explorer/i);
  expect(headerElement).toBeInTheDocument();
});

test('displays echo timeline events', () => {
  render(<App />);
  const timeElement = screen.getByText(/12:00:01/i);
  expect(timeElement).toBeInTheDocument();
});
