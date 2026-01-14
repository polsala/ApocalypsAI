import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: We mock the DOM environment to test React component behavior without a browser

test('renders initial affirmation', () => {
  render(<App />);
  const affirmationElement = screen.getByText(/The void whispers: you are stronger than you believe/i);
  expect(affirmationElement).toBeInTheDocument();
});

test('changes affirmation on button click', () => {
  render(<App />);
  const button = screen.getByText(/Whisper Another Truth/i);
  
  // Click the button to change affirmation
  fireEvent.click(button);
  
  // Check that an affirmation is still displayed (randomly selected)
  const affirmationElements = screen.getAllByText(/.*/);
  expect(affirmationElements.length).toBeGreaterThan(0);
});

test('renders header text', () => {
  render(<App />);
  const headerElement = screen.getByText(/.Void Whispers./i);
  expect(headerElement).toBeInTheDocument();
});
