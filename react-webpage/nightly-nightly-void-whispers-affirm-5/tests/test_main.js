import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: Simulate browser environment for React component testing without real DOM

const mockAffirmations = [
  "Even in the wasteland, your strength grows.",
  "The void whispers: you are not forgotten.",
  "Radiation cannot erode your spirit.",
  "Every step through ash is a victory.",
  "You are the last light in the dying world.",
  "Mutants fear those with unshakable will.",
  "Scarcity sharpens the mind, not dulls it.",
  "You are the author of your survival story.",
  "The silence speaks louder than the bombs ever did.",
  "Hope is your most powerful weapon."
];

test('renders initial affirmation', () => {
  render(<App />);
  const affirmationElement = screen.getByText(new RegExp(mockAffirmations[0].substring(0, 20), 'i'));
  expect(affirmationElement).toBeInTheDocument();
});

test('changes affirmation on button click', () => {
  render(<App />);
  const button = screen.getByText(/New Affirmation/i);
  fireEvent.click(button);
  const newAffirmationElement = screen.getByText(new RegExp(mockAffirmations[1].substring(0, 20), 'i'));
  expect(newAffirmationElement).toBeInTheDocument();
});
