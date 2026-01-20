import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import { affirmations } from '../src/affirmations';

// Mock rationale: Simulate user interactions and verify UI updates without external dependencies.

test('renders initial affirmation', () => {
  render(<App />);
  expect(screen.getByText(affirmations[0])).toBeInTheDocument();
});

test('changes affirmation on button click', () => {
  render(<App />);
  const button = screen.getByText(/New Affirmation/i);
  fireEvent.click(button);
  const newAffirmation = screen.getByText(new RegExp(`^(?!${affirmations[0]}$).*`, 'i'));
  expect(newAffirmation).toBeInTheDocument();
});
