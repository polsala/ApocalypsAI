import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

// Mock rationale: The App component simulates an asynchronous data fetch.
// To make tests deterministic and offline, we mock the `setTimeout`
// and control its execution to immediately resolve the promise with test data.
jest.useFakeTimers();

describe('App', () => {
  test('renders loading state initially', () => {
    render(<App />);
    expect(screen.getByText(/Loading temporal echoes.../i)).toBeInTheDocument();
  });

  test('renders title after loading', async () => {
    render(<App />);
    jest.runAllTimers(); // Advance timers to resolve the simulated fetch

    await waitFor(() => {
      expect(screen.getByText(/Temporal Echo Visualizer/i)).toBeInTheDocument();
    });
  });

  test('renders timeline with echoes after loading', async () => {
    render(<App />);
    jest.runAllTimers(); // Advance timers

    await waitFor(() => {
      // Check for a known echo title from the mock data in App.jsx
      expect(screen.getByText(/Utility Genesis: Nightly-Silly-Commit-Message-Generat/i)).toBeInTheDocument();
      expect(screen.getByText(/Temporal Anomaly Detected/i)).toBeInTheDocument();
      expect(screen.getAllByText(/✨|⚠️|🏆|🤖|🔓|⚙️|🔮/)).toHaveLength(7); // Check for emojis, indicating events rendered
    });
  });
});
