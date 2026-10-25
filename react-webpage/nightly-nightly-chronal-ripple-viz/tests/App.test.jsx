import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';
import RippleCanvas from '../src/RippleCanvas';

// Mock rationale: requestAnimationFrame is a browser API for animation loops.
// Mocking it allows us to control the animation frame execution in tests,
// making them deterministic and preventing infinite loops or reliance on real browser timing.
const mockRequestAnimationFrame = jest.fn(cb => setTimeout(cb, 0));
const mockCancelAnimationFrame = jest.fn(id => clearTimeout(id));

// Mock rationale: HTMLCanvasElement.prototype.getContext is a browser API for getting
// the 2D rendering context of a canvas. Mocking it allows us to test that the
// React component correctly calls canvas drawing methods with expected parameters,
// without needing an actual browser or visual rendering. This makes tests deterministic
// and runnable in a Node.js environment.
const mockContext = {
  clearRect: jest.fn(),
  beginPath: jest.fn(),
  arc: jest.fn(),
  stroke: jest.fn(),
  strokeStyle: '',
  lineWidth: 0,
  globalAlpha: 0,
  scale: jest.fn(),
};

// Mock rationale: getBoundingClientRect is a DOM API that returns the size and position
// of an element. Mocking it provides consistent dimensions for the canvas in tests,
// ensuring deterministic behavior regardless of the test runner's environment.
const mockGetBoundingClientRect = jest.fn(() => ({
  width: 800,
  height: 600,
  x: 0, y: 0, top: 0, right: 800, bottom: 600, left: 0,
}));

describe('Chronal Ripple Visualizer App', () => {
  let originalRequestAnimationFrame;
  let originalCancelAnimationFrame;
  let originalGetContext;
  let originalDevicePixelRatio;

  beforeAll(() => {
    originalRequestAnimationFrame = window.requestAnimationFrame;
    originalCancelAnimationFrame = window.cancelAnimationFrame;
    originalGetContext = HTMLCanvasElement.prototype.getContext;
    originalDevicePixelRatio = window.devicePixelRatio;

    window.requestAnimationFrame = mockRequestAnimationFrame;
    window.cancelAnimationFrame = mockCancelAnimationFrame;
    HTMLCanvasElement.prototype.getContext = jest.fn(() => mockContext);
    Object.defineProperty(window, 'devicePixelRatio', { value: 1, writable: true }); // Set to 1 for consistent test results
  });

  beforeEach(() => {
    jest.clearAllMocks();
    // Reset mock context properties before each test
    mockContext.strokeStyle = '';
    mockContext.lineWidth = 0;
    mockContext.globalAlpha = 0;
    // Mock getBoundingClientRect on the canvas element itself
    Object.defineProperty(HTMLCanvasElement.prototype, 'getBoundingClientRect', {
      writable: true,
      value: mockGetBoundingClientRect,
    });
  });

  afterAll(() => {
    window.requestAnimationFrame = originalRequestAnimationFrame;
    window.cancelAnimationFrame = originalCancelAnimationFrame;
    HTMLCanvasElement.prototype.getContext = originalGetContext;
    Object.defineProperty(window, 'devicePixelRatio', { value: originalDevicePixelRatio, writable: true });
  });

  test('renders the main application title', () => {
    render(<App />);
    expect(screen.getByText(/Chronal Ripple Visualizer/i)).toBeInTheDocument();
  });

  test('renders control sliders with initial values', () => {
    render(<App />);
    expect(screen.getByLabelText(/Ripple Count: 5/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Ripple Speed: 0.50/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Ripple Decay: 0.010/i)).toBeInTheDocument();
  });

  test('updates ripple count when slider is changed', () => {
    render(<App />);
    const rippleCountSlider = screen.getByLabelText(/Ripple Count: 5/i);
    fireEvent.change(rippleCountSlider, { target: { value: '10' } });
    expect(screen.getByLabelText(/Ripple Count: 10/i)).toBeInTheDocument();
  });

  test('updates ripple speed when slider is changed', () => {
    render(<App />);
    const rippleSpeedSlider = screen.getByLabelText(/Ripple Speed: 0.50/i);
    fireEvent.change(rippleSpeedSlider, { target: { value: '1.5' } });
    expect(screen.getByLabelText(/Ripple Speed: 1.50/i)).toBeInTheDocument();
  });

  test('updates ripple decay when slider is changed', () => {
    render(<App />);
    const rippleDecaySlider = screen.getByLabelText(/Ripple Decay: 0.010/i);
    fireEvent.change(rippleDecaySlider, { target: { value: '0.025' } });
    expect(screen.getByLabelText(/Ripple Decay: 0.025/i)).toBeInTheDocument();
  });

  test('renders the RippleCanvas component', () => {
    render(<App />);
    const canvasElement = screen.getByRole('canvas');
    expect(canvasElement).toBeInTheDocument();
  });

  test('RippleCanvas initializes and calls canvas context methods', async () => {
    render(<App />);
    const canvasElement = screen.getByRole('canvas');

    // Ensure getContext was called on the canvas
    expect(canvasElement.getContext).toHaveBeenCalledWith('2d');

    // Advance timers to allow animation frame to run
    await waitFor(() => expect(mockRequestAnimationFrame).toHaveBeenCalled(), { timeout: 100 });
    mockRequestAnimationFrame.mock.calls[0][0](); // Manually call the callback

    // Expect drawing methods to be called
    expect(mockContext.clearRect).toHaveBeenCalled();
    expect(mockContext.beginPath).toHaveBeenCalled();
    expect(mockContext.arc).toHaveBeenCalled();
    expect(mockContext.stroke).toHaveBeenCalled();
    expect(mockContext.scale).toHaveBeenCalledWith(1, 1); // dpr is 1 in test
  });

  test('RippleCanvas cleans up animation frame on unmount', () => {
    const { unmount } = render(<App />);
    expect(mockRequestAnimationFrame).toHaveBeenCalled();
    unmount();
    expect(mockCancelAnimationFrame).toHaveBeenCalled();
  });

  test('Generate Ripple button logs a message (current implementation)', () => {
    const consoleSpy = jest.spyOn(console, 'log');
    render(<App />);
    const generateButton = screen.getByRole('button', { name: /Generate Ripple/i });
    fireEvent.click(generateButton);
    expect(consoleSpy).toHaveBeenCalledWith("Generating a new ripple (logic handled by RippleCanvas's continuous generation)");
    consoleSpy.mockRestore();
  });
});
