import { render, screen, fireEvent, act } from '@testing-library/react';
import EchoBloom from '../src/EchoBloom';

// Mock rationale: We need to control time-based functions (setInterval, requestAnimationFrame) and randomness
// to make tests deterministic and prevent them from running indefinitely or producing unpredictable results.
// - Math.random: Ensures echo properties (position, size, signature) are consistent across test runs.
// - setInterval: Allows us to manually advance time and trigger echo spawning logic.
// - requestAnimationFrame: Allows us to manually trigger animation frame updates for echo movement.

describe('EchoBloom', () => {
  let originalMathRandom;
  let originalSetInterval;
  let originalClearInterval;
  let originalRequestAnimationFrame;
  let originalCancelAnimationFrame;

  beforeAll(() => {
    originalMathRandom = Math.random;
    originalSetInterval = global.setInterval;
    originalClearInterval = global.clearInterval;
    originalRequestAnimationFrame = global.requestAnimationFrame;
    originalCancelAnimationFrame = global.cancelAnimationFrame;

    // Mock Math.random to return predictable values
    let randomCallCount = 0;
    Math.random = jest.fn(() => {
      randomCallCount++;
      // Provide a sequence of predictable random numbers for echo generation
      if (randomCallCount === 1) return 0.1; // size
      if (randomCallCount === 2) return 0.2; // x
      if (randomCallCount === 3) return 0.3; // y
      if (randomCallCount === 4) return 0.4; // velocityX
      if (randomCallCount === 5) return 0.5; // velocityY
      if (randomCallCount === 6) return 0.6; // temporalSignature
      // Reset for next echo or other random calls
      randomCallCount = 0;
      return 0.5;
    });

    // Mock setInterval and clearInterval
    jest.useFakeTimers();

    // Mock requestAnimationFrame and cancelAnimationFrame
    global.requestAnimationFrame = jest.fn(cb => setTimeout(() => cb(Date.now()), 0));
    global.cancelAnimationFrame = jest.fn(id => clearTimeout(id));
  });

  afterAll(() => {
    Math.random = originalMathRandom;
    global.setInterval = originalSetInterval;
    global.clearInterval = originalClearInterval;
    global.requestAnimationFrame = originalRequestAnimationFrame;
    global.cancelAnimationFrame = originalCancelAnimationFrame;
    jest.useRealTimers();
  });

  test('renders without crashing', () => {
    render(<EchoBloom />);
    expect(screen.getByTestId('echo-bloom-container')).toBeInTheDocument();
  });

  test('spawns initial echoes after interval', () => {
    render(<EchoBloom />);
    // No echoes initially, as they are spawned by setInterval
    expect(screen.queryAllByTitle(/Echo #/)).toHaveLength(0);

    act(() => {
      jest.advanceTimersByTime(500); // Advance time by one spawn interval
    });

    // Expect one echo to be spawned
    expect(screen.queryAllByTitle(/Echo #/)).toHaveLength(1);
    expect(screen.getByTitle('Echo #0')).toBeInTheDocument();

    act(() => {
      jest.advanceTimersByTime(500); // Advance time for another echo
    });
    expect(screen.queryAllByTitle(/Echo #/)).toHaveLength(2);
    expect(screen.getByTitle('Echo #1')).toBeInTheDocument();
  });

  test('harmonizes an echo when clicked', () => {
    render(<EchoBloom />);

    act(() => {
      jest.advanceTimersByTime(500); // Spawn one echo
    });

    const echoElement = screen.getByTitle('Echo #0');
    expect(echoElement).not.toHaveClass('harmonized');

    act(() => {
      fireEvent.click(echoElement);
    });

    expect(echoElement).toHaveClass('harmonized');
    expect(screen.getByTitle('Harmonized Echo #0')).toBeInTheDocument();

    // Click again to de-harmonize
    act(() => {
      fireEvent.click(echoElement);
    });
    expect(echoElement).not.toHaveClass('harmonized');
    expect(screen.getByTitle('Echo #0')).toBeInTheDocument();
  });

  test('echoes move over time', () => {
    render(<EchoBloom />);

    act(() => {
      jest.advanceTimersByTime(500); // Spawn one echo
    });

    const echoElement = screen.getByTitle('Echo #0');
    const initialLeft = parseFloat(echoElement.style.left);
    const initialTop = parseFloat(echoElement.style.top);

    act(() => {
      jest.advanceTimersByTime(16); // Simulate one animation frame (approx 60fps)
    });

    const newLeft = parseFloat(echoElement.style.left);
    const newTop = parseFloat(echoElement.style.top);

    // Due to velocityX and velocityY being non-zero, position should change
    expect(newLeft).not.toBeCloseTo(initialLeft);
    expect(newTop).not.toBeCloseTo(initialTop);
  });

  test('echoes are removed after their lifespan', () => {
    render(<EchoBloom />);

    act(() => {
      jest.advanceTimersByTime(500); // Spawn one echo
    });
    expect(screen.queryAllByTitle(/Echo #/)).toHaveLength(1);

    act(() => {
      jest.advanceTimersByTime(10000); // Advance past ECHO_LIFESPAN (10s)
    });

    expect(screen.queryAllByTitle(/Echo #/)).toHaveLength(0);
  });
});
