import React from 'react';
import { render, screen, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import EchoVisualizer from '../src/components/EchoVisualizer';

// Mock rationale: We need to control time for deterministic testing of useEffect with setInterval.
// By mocking `jest.useFakeTimers()` and `jest.advanceTimersByTime()`, we can simulate the passage
// of time without actual delays, making tests fast and predictable.
jest.useFakeTimers();

describe('EchoVisualizer', () => {
  beforeEach(() => {
    // Reset timers before each test to ensure isolation
    jest.clearAllTimers();
  });

  test('renders the SVG grid with initial circles', () => {
    render(<EchoVisualizer />);

    const svgElement = screen.getByTestId('echo-grid-svg');
    expect(svgElement).toBeInTheDocument();

    // Check if the correct number of circles are rendered initially
    // GRID_SIZE * GRID_SIZE = 10 * 10 = 100 circles
    const circles = svgElement.querySelectorAll('circle');
    expect(circles.length).toBe(100);

    // Check initial properties of a sample circle (e.g., first one)
    const firstCircle = circles[0];
    expect(firstCircle).toHaveAttribute('cx');
    expect(firstCircle).toHaveAttribute('cy');
    expect(parseFloat(firstCircle.getAttribute('r'))).toBeGreaterThanOrEqual(0);
    expect(firstCircle).toHaveAttribute('fill');
  });

  test('updates echo values over time', () => {
    render(<EchoVisualizer />);

    const svgElement = screen.getByTestId('echo-grid-svg');
    const initialCircles = svgElement.querySelectorAll('circle');

    // Store initial radii for comparison
    const initialRadii = Array.from(initialCircles).map(circle => parseFloat(circle.getAttribute('r')));

    // Advance timers by one interval
    act(() => {
      jest.advanceTimersByTime(200); // UPDATE_INTERVAL_MS from component
    });

    const updatedCircles = svgElement.querySelectorAll('circle');
    const updatedRadii = Array.from(updatedCircles).map(circle => parseFloat(circle.getAttribute('r')));

    // Expect radii to have changed (due to random fluctuation and decay)
    // It's highly unlikely all 100 values would remain exactly the same after an update
    // We can't assert specific values due to randomness, but we can assert they are different
    // or at least that the update function was called and had an effect.
    let changedCount = 0;
    for (let i = 0; i < initialRadii.length; i++) {
      if (initialRadii[i] !== updatedRadii[i]) {
        changedCount++;
      }
    }
    // Given the simulation logic (Math.random() - 0.5) * 0.2, it's very probable
    // that most, if not all, values will change. Assert at least some change.
    expect(changedCount).toBeGreaterThan(0);
    expect(changedCount).toBeLessThanOrEqual(initialRadii.length); // All could change

    // Advance timers again to ensure continuous updates
    act(() => {
      jest.advanceTimersByTime(200);
    });

    const furtherUpdatedCircles = svgElement.querySelectorAll('circle');
    const furtherUpdatedRadii = Array.from(furtherUpdatedCircles).map(circle => parseFloat(circle.getAttribute('r')));

    let furtherChangedCount = 0;
    for (let i = 0; i < updatedRadii.length; i++) {
      if (updatedRadii[i] !== furtherUpdatedRadii[i]) {
        furtherChangedCount++;
      }
    }
    expect(furtherChangedCount).toBeGreaterThan(0);
  });

  test('cleans up interval on unmount', () => {
    const clearIntervalSpy = jest.spyOn(global, 'clearInterval');
    const { unmount } = render(<EchoVisualizer />);

    expect(clearIntervalSpy).not.toHaveBeenCalled(); // Should not be called on mount

    unmount();

    // Expect clearInterval to be called when the component unmounts
    expect(clearIntervalSpy).toHaveBeenCalledTimes(1);

    clearIntervalSpy.mockRestore(); // Clean up the spy
  });
});
