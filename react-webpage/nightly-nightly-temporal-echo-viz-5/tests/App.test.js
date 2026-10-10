import { render, screen, act } from '@testing-library/react';
import App from '../src/App';

// Mock rationale: We use Jest's fake timers to control the setInterval calls
// that simulate temporal echo data. This ensures tests are deterministic and
// do not rely on real-time delays, making them fast and reliable.
jest.useFakeTimers();

describe('App', () => {
  test('renders Temporal Echo Visualizer header', () => {
    render(<App />);
    const headerElement = screen.getByText(/Temporal Echo Visualizer/i);
    expect(headerElement).toBeInTheDocument();
  });

  test('initial echo data is displayed', () => {
    render(<App />);
    // Advance timers by a small amount to allow initial useEffect to run
    act(() => {
      jest.advanceTimersByTime(0);
    });
    
    // Check for initial display of amplitude, frequency, and stability
    // Since values are random, we check for the labels and that they are numbers
    expect(screen.getByText(/Amplitude:/i)).toBeInTheDocument();
    expect(screen.getByText(/Frequency:/i)).toBeInTheDocument();
    expect(screen.getByText(/Timeline Stability/i)).toBeInTheDocument();
    
    // Check if a percentage value is displayed for stability
    const stabilityValue = screen.getByText(/%/, { exact: false });
    expect(stabilityValue).toBeInTheDocument();
    expect(stabilityValue.textContent).toMatch(/\d+%$/); // Ends with a number and %
  });

  test('echo data updates over time', () => {
    render(<App />);
    
    // Get initial stability value
    act(() => {
      jest.advanceTimersByTime(0);
    });
    const initialStabilityText = screen.getByText(/%/, { exact: false }).textContent;

    // Advance timers by 1 second to trigger data update
    act(() => {
      jest.advanceTimersByTime(1000);
    });

    // Get updated stability value
    const updatedStabilityText = screen.getByText(/%/, { exact: false }).textContent;

    // Expect the stability value to have potentially changed (it's random, so it's highly likely)
    // We can't assert it's *different* because random could theoretically produce the same, 
    // but we can assert it's still a valid percentage format.
    expect(updatedStabilityText).toMatch(/\d+%$/);
    
    // A more direct check for change (though still probabilistic): 
    // If the random numbers are truly random, it's highly unlikely they'll be the same.
    // For a deterministic test, we could mock Math.random, but for this level of utility,
    // checking for valid format after update is sufficient.
    expect(initialStabilityText).not.toBe(updatedStabilityText); // Highly likely to be different
  });

  test('stability status changes based on value', () => {
    // Mock Math.random to control generated values for deterministic stability status checks
    // Mock rationale: Controlling Math.random allows us to deterministically test the conditional
    // rendering of stability status messages and colors without relying on random chance.
    const mockMathRandom = jest.spyOn(Math, 'random');

    // Test Critical Anomaly (e.g., amplitude 90, frequency 40 -> very low stability)
    mockMathRandom.mockReturnValueOnce(0.9) // amplitude = 90
                  .mockReturnValueOnce(0.8); // frequency = 40
    render(<App />);
    act(() => { jest.advanceTimersByTime(0); });
    expect(screen.getByText(/Critical Anomaly/i)).toBeInTheDocument();
    expect(screen.getByText(/Critical Anomaly/i)).toHaveClass('status-red');

    // Clean up previous render and mock
    jest.clearAllTimers();
    mockMathRandom.mockRestore();

    // Test Stable (e.g., amplitude 10, frequency 5 -> high stability)
    mockMathRandom.mockReturnValueOnce(0.1) // amplitude = 10
                  .mockReturnValueOnce(0.1); // frequency = 5
    render(<App />);
    act(() => { jest.advanceTimersByTime(0); });
    expect(screen.getByText(/Stable/i)).toBeInTheDocument();
    expect(screen.getByText(/Stable/i)).toHaveClass('status-green');

    mockMathRandom.mockRestore();
  });
});
