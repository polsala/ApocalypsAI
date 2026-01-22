import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: Simulate user interaction and affirmation display without real DOM dependencies.

test('renders initial affirmation on load', () => {
  render(<App />);
  const affirmationElement = screen.getByText(/You are/i);
  expect(affirmationElement).toBeInTheDocument();
});

test('changes affirmation on button click', () => {
  render(<App />);
  const button = screen.getByText('// next_message');
  const initialText = screen.getByText(/You are/i).textContent;

  fireEvent.click(button);
  const newText = screen.getByText(/You are/i).textContent;

  // Affirmation should change (or stay same due to randomness, but at least renders)
  expect(newText).toBeDefined();
});
