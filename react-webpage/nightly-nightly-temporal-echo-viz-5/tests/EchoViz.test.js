import React from 'react';
import { render, screen } from '@testing-library/react';
import EchoViz from '../src/EchoViz';

// # Mock rationale: Mocking canvas context to test drawing operations deterministically
// without a real browser environment. This allows us to assert that drawing methods
// are called with expected parameters, ensuring the component attempts to render correctly.
const mockContext = {
  clearRect: jest.fn(),
  beginPath: jest.fn(),
  arc: jest.fn(),
  fill: jest.fn(),
  stroke: jest.fn(),
  moveTo: jest.fn(),
  lineTo: jest.fn(),
  // Mock properties that might be set
  set fillStyle(value) { this._fillStyle = value; },
  get fillStyle() { return this._fillStyle; },
  set shadowBlur(value) { this._shadowBlur = value; },
  get shadowBlur() { return this._shadowBlur; },
  set shadowColor(value) { this._shadowColor = value; },
  get shadowColor() { return this._shadowColor; },
  // Add any other methods/properties your drawing logic uses
};

// Mock getContext to return our mock context
HTMLCanvasElement.prototype.getContext = jest.fn(() => mockContext);

// Mock clientWidth/clientHeight for canvas sizing
Object.defineProperty(HTMLElement.prototype, 'clientWidth', {
  writable: true,
  value: 800,
});
Object.defineProperty(HTMLElement.prototype, 'clientHeight', {
  writable: true,
  value: 600,
});

describe('EchoViz', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  it('renders a canvas element', () => {
    render(<EchoViz echoData={[]} />);
    const canvasElement = screen.getByRole('img', { name: 'Temporal Echo Visualization' });
    expect(canvasElement).toBeInTheDocument();
    expect(canvasElement.tagName).toBe('CANVAS');
  });

  it('clears the canvas and draws visible echoes when echoData is provided', () => {
    const testEchoData = [
      { id: 'e1', x: 0.1, y: 0.2, intensity: 0.8, age: 0.1, vx: 0, vy: 0 }, // Visible
      { id: 'e2', x: 0.5, y: 0.7, intensity: 0.8, age: 0.1, vx: 0, vy: 0 }, // Visible
    ];

    render(<EchoViz echoData={testEchoData} />);

    // Expect clearRect to be called once at the beginning of drawing
    expect(mockContext.clearRect).toHaveBeenCalledTimes(1);
    expect(mockContext.clearRect).toHaveBeenCalledWith(0, 0, 800, 600);

    // Expect drawing operations for each visible echo
    expect(mockContext.beginPath).toHaveBeenCalledTimes(testEchoData.length);
    expect(mockContext.arc).toHaveBeenCalledTimes(testEchoData.length);
    expect(mockContext.fill).toHaveBeenCalledTimes(testEchoData.length);

    // Verify specific drawing calls for the first echo
    // x = 0.1 * 800 = 80
    // y = 0.2 * 600 = 120
    // radius = 5 + 0.8 * 10 = 13
    expect(mockContext.arc).toHaveBeenCalledWith(80, 120, 13, 0, Math.PI * 2);

    // Verify specific drawing calls for the second echo
    // x = 0.5 * 800 = 400
    // y = 0.7 * 600 = 420
    // radius = 5 + 0.8 * 10 = 13
    expect(mockContext.arc).toHaveBeenCalledWith(400, 420, 13, 0, Math.PI * 2);
  });

  it('does not draw echoes with alpha <= 0', () => {
    const fadedEchoData = [
      { id: 'f1', x: 0.1, y: 0.1, intensity: 0.1, age: 0.9, vx: 0, vy: 0 }, // alpha will be 0, not drawn
      { id: 'f2', x: 0.5, y: 0.5, intensity: 0.9, age: 0.1, vx: 0, vy: 0 }, // alpha will be 0.8, drawn
    ];

    render(<EchoViz echoData={fadedEchoData} />);

    expect(mockContext.beginPath).toHaveBeenCalledTimes(1); // Only one visible echo
    expect(mockContext.arc).toHaveBeenCalledTimes(1);
    expect(mockContext.fill).toHaveBeenCalledTimes(1);

    // Ensure the visible one was drawn
    expect(mockContext.arc).toHaveBeenCalledWith(400, 300, 14, 0, Math.PI * 2);
    // Ensure the faded one was NOT drawn (no call with its specific coords)
    expect(mockContext.arc).not.toHaveBeenCalledWith(80, 60, expect.any(Number), 0, Math.PI * 2);
  });
});
