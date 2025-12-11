import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { vi } from 'vitest';
import RippleCanvas from '../src/components/RippleCanvas';

describe('RippleCanvas', () => {
  // Mock rationale:
  // 1. HTMLCanvasElement.prototype.getContext: Canvas drawing operations are visual and browser-specific.
  //    Mocking `getContext` allows us to assert that the correct drawing methods (e.g., `arc`, `stroke`, `clearRect`)
  //    are called with expected parameters, without needing a real browser environment. This makes tests fast and deterministic.
  // 2. window.requestAnimationFrame: The animation loop relies on this browser API.
  //    Mocking it allows us to control the passage of "animation frames" manually via `advanceAnimationFrames`,
  //    ensuring that animation logic (ripple expansion, decay, cleanup) can be tested step-by-step without waiting for real browser frames.
  //    This ensures deterministic testing of animation state changes.
  // 3. performance.now(): Used for calculating delta time. Mocked in `setupTests.js` to ensure deterministic time progression.
  // 4. HTMLElement.prototype.offsetWidth/Height: Mocked in `setupTests.js` to provide consistent canvas dimensions for testing.

  const mockContext = HTMLCanvasElement.prototype.getContext('2d');

  const defaultProps = {
    rippleSpeed: 0.05,
    rippleDecay: 0.005,
    maxRipples: 20,
    rippleColor: '#00ff00',
    isPaused: false,
    clearTrigger: 0,
  };

  it('renders a canvas element', () => {
    render(<RippleCanvas {...defaultProps} />);
    expect(screen.getByRole('canvas')).toBeInTheDocument();
  });

  it('calls requestAnimationFrame on mount', () => {
    render(<RippleCanvas {...defaultProps} />);
    expect(window.requestAnimationFrame).toHaveBeenCalled();
  });

  it('adds a ripple on canvas click', () => {
    render(<RippleCanvas {...defaultProps} />);
    const canvas = screen.getByRole('canvas');

    fireEvent.click(canvas, { clientX: 100, clientY: 100 });

    // Advance animation frame to allow ripple to be processed and drawn
    advanceAnimationFrames();

    // Expect clearRect and then drawing commands for the new ripple
    expect(mockContext.clearRect).toHaveBeenCalledWith(0, 0, 800, 600);
    expect(mockContext.beginPath).toHaveBeenCalled();
    expect(mockContext.arc).toHaveBeenCalledWith(100, 100, expect.any(Number), 0, Math.PI * 2);
    expect(mockContext.stroke).toHaveBeenCalled();
    expect(mockContext.strokeStyle).toBe(defaultProps.rippleColor);
  });

  it('ripples expand and fade over time', () => {
    render(<RippleCanvas {...defaultProps} />);
    const canvas = screen.getByRole('canvas');

    fireEvent.click(canvas, { clientX: 100, clientY: 100 });

    // Initial draw
    advanceAnimationFrames(1, 0); // First frame, delta time 0
    expect(mockContext.arc).toHaveBeenCalledWith(100, 100, 0, 0, Math.PI * 2);
    expect(mockContext.globalAlpha).toBeCloseTo(1);

    // Advance time, ripple should expand and fade
    mockContext.arc.mockClear();
    mockContext.clearRect.mockClear();
    advanceAnimationFrames(1, 100); // Simulate 100ms passing

    expect(mockContext.clearRect).toHaveBeenCalled();
    expect(mockContext.arc).toHaveBeenCalledWith(
      100, 100,
      expect.any(Number), // Radius should be > 0
      0, Math.PI * 2
    );
    expect(mockContext.arc.mock.calls[0][2]).toBeGreaterThan(0);
    expect(mockContext.globalAlpha).toBeLessThan(1);
  });

  it('clears all ripples when clearTrigger changes', () => {
    const { rerender } = render(<RippleCanvas {...defaultProps} />);
    const canvas = screen.getByRole('canvas');

    fireEvent.click(canvas, { clientX: 50, clientY: 50 });
    advanceAnimationFrames(); // Draw the ripple
    expect(mockContext.arc).toHaveBeenCalled();
    mockContext.arc.mockClear();

    // Trigger clear by changing clearTrigger prop
    rerender(<RippleCanvas {...defaultProps} clearTrigger={1} />);
    advanceAnimationFrames(); // Allow effect to run and animation loop to redraw

    // Expect clearRect but no arc calls, as ripples should be cleared
    expect(mockContext.clearRect).toHaveBeenCalled();
    expect(mockContext.arc).not.toHaveBeenCalled();
  });

  it('pauses and resumes animation', () => {
    const { rerender } = render(<RippleCanvas {...defaultProps} />);
    const canvas = screen.getByRole('canvas');

    fireEvent.click(canvas, { clientX: 100, clientY: 100 });
    advanceAnimationFrames(1, 100); // Draw and advance
    const initialRadius = mockContext.arc.mock.calls[0][2];
    mockContext.arc.mockClear();

    // Pause
    rerender(<RippleCanvas {...defaultProps} isPaused={true} />);
    advanceAnimationFrames(1, 100); // Advance while paused

    // Expect clearRect but arc should draw with same radius as before pause
    expect(mockContext.clearRect).toHaveBeenCalled();
    expect(mockContext.arc).toHaveBeenCalledWith(100, 100, initialRadius, 0, Math.PI * 2);
    mockContext.arc.mockClear();

    // Resume
    rerender(<RippleCanvas {...defaultProps} isPaused={false} />);
    advanceAnimationFrames(1, 100); // Advance while resumed

    // Expect radius to have increased again
    expect(mockContext.clearRect).toHaveBeenCalled();
    expect(mockContext.arc).toHaveBeenCalledWith(
      100, 100,
      expect.any(Number), // Radius should be > initialRadius
      0, Math.PI * 2
    );
    expect(mockContext.arc.mock.calls[0][2]).toBeGreaterThan(initialRadius);
  });

  it('limits the number of ripples to maxRipples', () => {
    const { rerender } = render(<RippleCanvas {...defaultProps} maxRipples={2} />);
    const canvas = screen.getByRole('canvas');

    fireEvent.click(canvas, { clientX: 10, clientY: 10 }); // Ripple 1
    fireEvent.click(canvas, { clientX: 20, clientY: 20 }); // Ripple 2
    fireEvent.click(canvas, { clientX: 30, clientY: 30 }); // Ripple 3 (should remove Ripple 1)

    advanceAnimationFrames(1, 100); // Process and draw

    // Expect only 2 arc calls (for ripple 2 and 3)
    expect(mockContext.arc).toHaveBeenCalledTimes(2);
    expect(mockContext.arc).not.toHaveBeenCalledWith(10, 10, expect.any(Number), 0, Math.PI * 2);
    expect(mockContext.arc).toHaveBeenCalledWith(20, 20, expect.any(Number), 0, Math.PI * 2);
    expect(mockContext.arc).toHaveBeenCalledWith(30, 30, expect.any(Number), 0, Math.PI * 2);
  });
});
