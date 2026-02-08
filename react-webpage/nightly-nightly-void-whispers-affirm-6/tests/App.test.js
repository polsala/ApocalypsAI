import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: Simulate user interaction and verify UI updates without external dependencies.

test('renders initial affirmation', () => {
  render(<App />);
  const affirmationElement = screen.getByText(/The stars align in your favor today\./i);
  expect(affirmationElement).toBeInTheDocument();
});

test('changes affirmation on button click', () => {
  render(<App />);
  const button = screen.getByText(/Receive Another Whisper/i);
  fireEvent.click(button);
  const newAffirmation = screen.getByText(/Your potential is as vast as the cosmos\./i);
  expect(newAffirmation).toBeInTheDocument();
});
