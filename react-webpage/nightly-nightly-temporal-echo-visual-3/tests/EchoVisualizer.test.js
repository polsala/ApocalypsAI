import { render, screen } from '@testing-library/react';
import EchoVisualizer from '../src/EchoVisualizer';

describe('EchoVisualizer', () => {
  let requestAnimationFrameSpy;
  let cancelAnimationFrameSpy;
  let getContextSpy;
  let mockContext;

  beforeAll(() => {
    // Mock requestAnimationFrame and cancelAnimationFrame for deterministic tests
    // # Mock rationale: These are browser APIs that control animation loops. In a Node.js test environment,
    // # they don't exist and would cause errors. Mocking them with simple setTimeout/clearTimeout
    // # allows the useEffect hook to execute its setup and cleanup logic without actually running
    // # an infinite animation loop, making tests deterministic and preventing resource leaks.
    requestAnimationFrameSpy = jest.spyOn(window, 'requestAnimationFrame').mockImplementation(cb => setTimeout(cb, 0));
    cancelAnimationFrameSpy = jest.spyOn(window, 'cancelAnimationFrame').mockImplementation(id => clearTimeout(id));

    // Mock canvas context
    mockContext = {
      clearRect: jest.fn(),
      beginPath: jest.fn(),
      arc: jest.fn(),
      stroke: jest.fn(),
      // Mock properties that might be accessed on the context's canvas property
      canvas: {
        width: 600,
        height: 400,
      }
    };
    // # Mock rationale: Directly manipulating the canvas context in a test environment is complex
    // # and not the primary goal of this unit test. Mocking `getContext` allows us to verify
    // # that the drawing methods are invoked as expected by the component's logic, without needing
    // # an actual browser canvas. This ensures the component attempts to draw, making the test deterministic.
    getContextSpy = jest.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(mockContext);
  });

  afterAll(() => {
    requestAnimationFrameSpy.mockRestore();
    cancelAnimationFrameSpy.mockRestore();
    getContextSpy.mockRestore();
  });

  afterEach(() => {
    jest.clearAllTimers(); // Clear any pending timers after each test
    jest.clearAllMocks(); // Clear mock calls after each test
  });

  test('renders a canvas element', () => {
    render(<EchoVisualizer />);
    const canvasElement = screen.getByRole('img', { name: /Temporal Echo Visualization/i });
    expect(canvasElement).toBeInTheDocument();
    expect(canvasElement.tagName).toBe('CANVAS');
  });

  test('canvas has correct dimensions', () => {
    render(<EchoVisualizer />);
    const canvasElement = screen.getByRole('img');
    expect(canvasElement).toHaveAttribute('width', '600');
    expect(canvasElement).toHaveAttribute('height', '400');
  });

  test('animation frame functions are called on mount and unmount', () => {
    const { unmount } = render(<EchoVisualizer />);

    expect(requestAnimationFrameSpy).toHaveBeenCalled();

    unmount();

    expect(cancelAnimationFrameSpy).toHaveBeenCalled();
  });

  test('canvas context methods are called during animation', () => {
    jest.useFakeTimers(); // Use fake timers to control setTimeout/clearTimeout

    render(<EchoVisualizer />);

    // Expect getContext to be called
    expect(getContextSpy).toHaveBeenCalledWith('2d');

    // Advance timers to allow the animation loop (mocked by setTimeout) to run once
    jest.advanceTimersByTime(0); // Run initial animation frame

    expect(mockContext.clearRect).toHaveBeenCalled();
    expect(mockContext.beginPath).toHaveBeenCalled();
    expect(mockContext.arc).toHaveBeenCalled();
    expect(mockContext.stroke).toHaveBeenCalled();

    jest.useRealTimers(); // Restore real timers
  });
});
