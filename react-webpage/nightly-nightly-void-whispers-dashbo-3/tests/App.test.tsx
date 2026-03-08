import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

// Mock rationale: Simulate user interactions and DOM state without external dependencies

describe('Void Whispers Dashboard', () => {
  test('renders title correctly', () => {
    render(<App />);
    expect(screen.getByText(/_void whispers dashboard/i)).toBeInTheDocument();
  });

  test('allows adding a new affirmation', () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/whisper something/i);
    const button = screen.getByText(/send/i);

    fireEvent.change(input, { target: { value: 'Test affirmation' } });
    fireEvent.click(button);

    expect(screen.getByText('Test affirmation')).toBeInTheDocument();
  });

  test('toggles favorite status', () => {
    render(<App />);
    const starButton = screen.getAllByText('☆')[0];
    fireEvent.click(starButton);
    expect(starButton).toHaveTextContent('★');
  });
});
