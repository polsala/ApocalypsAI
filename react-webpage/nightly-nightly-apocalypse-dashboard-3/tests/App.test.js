import React from 'react';
import { render, screen, act } from '@testing-library/react';
import App from '../src/App';

// Mock the setInterval and clearInterval to control time in tests
jest.useFakeTimers();

describe('App Component', () => {
  test('renders without crashing', () => {
    render(<App />);
    expect(screen.getByText(/Apocalypse Dashboard/i)).toBeInTheDocument();
  });

  test('displays initial dashboard sections', () => {
    render(<App />);
    expect(screen.getByText(/Resource Status/i)).toBeInTheDocument();
    expect(screen.getByText(/Threat Level/i)).toBeInTheDocument();
    expect(screen.getByText(/Survivor Count/i)).toBeInTheDocument();
    expect(screen.getByText(/Temporal Stability/i)).toBeInTheDocument();
  });

  test('updates data periodically', () => {
    render(<App />);

    // Initial render should have 0s or default values before first update
    expect(screen.getByText(/Canned Beans: 0%/i)).toBeInTheDocument();
    expect(screen.getByText(/Clean Water: 0%/i)).toBeInTheDocument();
    expect(screen.getByText(/Current Threat: 0/5/i)).toBeInTheDocument();
    expect(screen.getByText(/Brave Souls Remaining: 0/i)).toBeInTheDocument();
    expect(screen.getByText(/Anomaly Gauge: 0/10/i)).toBeInTheDocument();

    // Advance timers by 5 seconds to trigger the first update
    act(() => {
      jest.advanceTimersByTime(5000);
    });

    // After the first update, the values should be non-zero (based on mock generation)
    // We can't assert exact values due to randomness, but we can check if they've changed
    // and are within reasonable ranges if we were to mock the generation functions more precisely.
    // For simplicity here, we'll just check that the text has updated from the initial 0s.
    // A more robust test would mock the random functions to return predictable values.

    // Mock rationale: We are advancing timers to simulate the useEffect hook's interval.
    // This allows us to test the periodic updates without waiting in real-time.

    // Example of checking if the text has changed from initial 0s (this is a weak check due to randomness)
    // A better approach would be to mock the random functions to return predictable values.
    // For now, we'll just ensure the component doesn't break after updates.
    expect(screen.getByText(/Canned Beans:/i)).not.toHaveTextContent('0%');
    expect(screen.getByText(/Clean Water:/i)).not.toHaveTextContent('0%');
    expect(screen.getByText(/Current Threat:/i)).not.toHaveTextContent('0/5');
    expect(screen.getByText(/Brave Souls Remaining:/i)).not.toHaveTextContent('0');
    expect(screen.getByText(/Anomaly Gauge:/i)).not.toHaveTextContent('0/10');
  });

  test('clears interval on unmount', () => {
    const clearIntervalSpy = jest.spyOn(window, 'clearInterval');
    const { unmount } = render(<App />);
    unmount();
    expect(clearIntervalSpy).toHaveBeenCalledTimes(1);
    jest.restoreAllMocks(); // Clean up the spy
  });
});
