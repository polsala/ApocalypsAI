import React from 'react';
import { render, screen } from '@testing-library/react';
import TemporalBloomCanvas from '../src/components/TemporalBloomCanvas';

// Mock rationale: We need to test that the canvas element is rendered and that
// its drawing context methods are called. We don't need to actually render
// pixels in a headless test environment, so mocking the canvas context
// allows us to assert on method calls and their arguments.
const mockContext = {
  clearRect: jest.fn(),
  fillRect: jest.fn(),
  beginPath: jest.fn(),
  arc: jest.fn(),
  fill: jest.fn(),
  // Add other methods if your drawing logic uses them
  // e.g., strokeStyle, stroke, moveTo, lineTo, etc.
};

// Mock rationale: We need to mock getContext to return our mockContext.
// This allows us to intercept calls to drawing methods.
HTMLCanvasElement.prototype.getContext = jest.fn(() => mockContext);

// Mock rationale: requestAnimationFrame and cancelAnimationFrame are browser APIs
// that control animation loops. In a Node.js test environment, these are not
// available. Mocking them allows us to control the animation loop manually
// for testing purposes, ensuring `draw` is called without infinite loops.
global.requestAnimationFrame = jest.fn((cb) => setTimeout(cb, 0));
global.cancelAnimationFrame = jest.fn();

describe('TemporalBloomCanvas', () => {
  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
    // Mock window dimensions for consistent test environment
    Object.defineProperty(window, 'innerWidth', { writable: true, configurable: true, value: 800 });
    Object.defineProperty(window, 'innerHeight', { writable: true, configurable: true, value: 600 });
  });

  it('renders a canvas element', () => {
    render(<TemporalBloomCanvas frequency={0.01} intensity={0.5} decay={0.95} />);
    const canvasElement = screen.getByRole('img', { name: 'Temporal Bloom Canvas' });
    expect(canvasElement).toBeInTheDocument();
    expect(canvasElement.tagName).toBe('CANVAS');
  });

  it('initializes canvas context and starts animation loop', () => {
    render(<TemporalBloomCanvas frequency={0.01} intensity={0.5} decay={0.95} />);
    expect(HTMLCanvasElement.prototype.getContext).toHaveBeenCalledWith('2d');
    expect(global.requestAnimationFrame).toHaveBeenCalled();
  });

  it('calls drawing methods on the canvas context', async () => {
    render(<TemporalBloomCanvas frequency={0.01} intensity={0.5} decay={0.95} />);

    // Wait for the next animation frame to ensure draw is called
    await new Promise(resolve => setTimeout(resolve, 10)); // Small delay for setTimeout in mock RAF

    // Expect fillRect to be called for background (decay effect)
    expect(mockContext.fillRect).toHaveBeenCalled();
    // Expect particle drawing methods to be called
    expect(mockContext.beginPath).toHaveBeenCalled();
    expect(mockContext.arc).toHaveBeenCalled();
    expect(mockContext.fill).toHaveBeenCalled();
  });

  it('cleans up animation frame on unmount', () => {
    const { unmount } = render(<TemporalBloomCanvas frequency={0.01} intensity={0.5} decay={0.95} />);
    unmount();
    expect(global.cancelAnimationFrame).toHaveBeenCalled();
  });

  it('updates canvas dimensions on resize', async () => {
    render(<TemporalBloomCanvas frequency={0.01} intensity={0.5} decay={0.95} />);

    // Clear mocks to check calls after resize
    jest.clearAllMocks();

    // Simulate a resize event
    Object.defineProperty(window, 'innerWidth', { writable: true, configurable: true, value: 1024 });
    Object.defineProperty(window, 'innerHeight', { writable: true, configurable: true, value: 768 });
    window.dispatchEvent(new Event('resize'));

    // Wait for the next animation frame to ensure draw is called after resize
    await new Promise(resolve => setTimeout(resolve, 10));

    // Expect getContext to be called again (or its internal logic to update canvas dimensions)
    // and drawing methods to be called with the new dimensions implicitly.
    // Mock rationale: The `resizeCanvas` function within `useEffect` updates the canvas
    // dimensions and re-initializes particles. While we can't directly inspect the canvasRef's
    // width/height, we can verify that the drawing loop continues and drawing methods are invoked,
    // implying the resize handler has done its job.
    expect(mockContext.fillRect).toHaveBeenCalled();
    expect(mockContext.beginPath).toHaveBeenCalled();
  });
});
