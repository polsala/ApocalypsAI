import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

// Mock rationale: We want to test App's behavior in isolation,
// without needing to render or fully interact with its child components' internals.
// This ensures App's state management and prop passing are correct.
jest.mock('../src/components/EventInputForm', () => {
  return function MockEventInputForm({ onGenerate }) {
    const [inputValue, setInputValue] = React.useState('');
    return (
      <form data-testid="mock-event-input-form" onSubmit={(e) => {
        e.preventDefault();
        onGenerate(inputValue);
      }}>
        <input type="text" data-testid="event-input" value={inputValue} onChange={(e) => setInputValue(e.target.value)} />
        <button type="submit" data-testid="generate-button">Generate</button>
      </form>
    );
  };
});

jest.mock('../src/components/EchoDisplay', () => {
  return function MockEchoDisplay({ echoes }) {
    return (
      <div data-testid="mock-echo-display">
        {echoes.length > 0 ? `Displaying ${echoes.length} echoes` : 'No echoes'}
      </div>
    );
  };
});

describe('App Component', () => {
  test('renders header and initial state', () => {
    render(<App />);
    expect(screen.getByText(/Temporal Echo Visualizer/i)).toBeInTheDocument();
    expect(screen.getByText(/Unravel the ripples of events across the timelines./i)).toBeInTheDocument();
    expect(screen.getByTestId('mock-event-input-form')).toBeInTheDocument();
    expect(screen.getByTestId('mock-echo-display')).toHaveTextContent('No echoes');
  });

  test('generates echoes when EventInputForm triggers onGenerate with valid input', async () => {
    render(<App />);
    const input = screen.getByTestId('event-input');
    const generateButton = screen.getByTestId('generate-button');

    fireEvent.change(input, { target: { value: 'Test Event' } });
    fireEvent.click(generateButton);

    // Mock rationale: The generateEchoes function in App.js is deterministic.
    // We know 'Test Event' will always produce a specific number of echoes (e.g., 3-5).
    // We verify that the mock EchoDisplay receives a non-empty array.
    await waitFor(() => {
      expect(screen.getByTestId('mock-echo-display')).not.toHaveTextContent('No echoes');
      expect(screen.getByTestId('mock-echo-display')).toHaveTextContent(/Displaying \d+ echoes/);
    });
  });

  test('clears echoes when EventInputForm triggers onGenerate with empty input', async () => {
    render(<App />);
    const input = screen.getByTestId('event-input');
    const button = screen.getByTestId('generate-button');

    // First, input a value and generate echoes
    fireEvent.change(input, { target: { value: 'Another Event' } });
    fireEvent.click(button);
    await waitFor(() => {
      expect(screen.getByTestId('mock-echo-display')).not.toHaveTextContent('No echoes');
    });

    // Clear the input and generate again
    fireEvent.change(input, { target: { value: '' } });
    fireEvent.click(button);

    // Mock rationale: The `generateEchoes` function in App.js returns an empty array
    // if `eventName` is empty. This test verifies App's state update logic.
    await waitFor(() => {
      expect(screen.getByTestId('mock-echo-display')).toHaveTextContent('No echoes');
    });
  });
});
