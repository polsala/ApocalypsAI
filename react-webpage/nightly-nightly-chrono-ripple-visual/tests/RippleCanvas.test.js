import { render, screen } from '@testing-library/react';
import RippleCanvas from '../src/RippleCanvas';

describe('RippleCanvas', () => {
  // Mock rationale: Canvas drawing operations are side effects and depend on a browser environment.
  // To make tests deterministic and offline, we mock the canvas context and its drawing methods.
  // This allows us to assert that the correct drawing commands would have been issued without a real browser.
  const mockContext = {
    clearRect: jest.fn(),
    beginPath: jest.fn(),
    arc: jest.fn(),
    stroke: jest.fn(),
    closePath: jest.fn(),
    // Mock properties
    set strokeStyle(value) { this._strokeStyle = value; },
    get strokeStyle() { return this._strokeStyle; },
    set lineWidth(value) { this._lineWidth = value; },
    get lineWidth() { return this._lineWidth; },
  };

  beforeAll(() => {
    jest.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(mockContext);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  afterAll(() => {
    jest.restoreAllMocks();
  });

  test('renders a canvas element', () => {
    const eventDetails = { date: '2023-01-01', description: 'Test', magnitude: 1 };
    render(<RippleCanvas eventDetails={eventDetails} />);
    expect(screen.getByRole('canvas', { name: /Chrono Ripple Visualization/i })).toBeInTheDocument();
  });

  test('draws correct number of ripples based on magnitude', () => {
    const eventDetails = { date: '2023-01-01', description: 'Test', magnitude: 5 };
    render(<RippleCanvas eventDetails={eventDetails} />);

    // Expect clearRect to be called once at the beginning of drawing
    expect(mockContext.clearRect).toHaveBeenCalledTimes(1);

    // Expect beginPath, arc, stroke, closePath to be called for each ripple
    const expectedCallsPerRipple = 4; // beginPath, arc, stroke, closePath
    expect(mockContext.beginPath).toHaveBeenCalledTimes(eventDetails.magnitude);
    expect(mockContext.arc).toHaveBeenCalledTimes(eventDetails.magnitude);
    expect(mockContext.stroke).toHaveBeenCalledTimes(eventDetails.magnitude);
    expect(mockContext.closePath).toHaveBeenCalledTimes(eventDetails.magnitude);

    // Verify arc calls for specific radii (approximate, based on canvas size 400x400)
    // Max radius is (400/2 - 10) = 190. For magnitude 5, ripples are at 190/5 * (1 to 5)
    expect(mockContext.arc).toHaveBeenCalledWith(200, 200, expect.closeTo(38), 0, 2 * Math.PI);
    expect(mockContext.arc).toHaveBeenCalledWith(200, 200, expect.closeTo(76), 0, 2 * Math.PI);
    expect(mockContext.arc).toHaveBeenCalledWith(200, 200, expect.closeTo(114), 0, 2 * Math.PI);
    expect(mockContext.arc).toHaveBeenCalledWith(200, 200, expect.closeTo(152), 0, 2 * Math.PI);
    expect(mockContext.arc).toHaveBeenCalledWith(200, 200, expect.closeTo(190), 0, 2 * Math.PI);
  });

  test('does not draw if magnitude is 0 (or less, though min is 1)', () => {
    const eventDetails = { date: '2023-01-01', description: 'Test', magnitude: 0 };
    render(<RippleCanvas eventDetails={eventDetails} />);

    expect(mockContext.clearRect).toHaveBeenCalledTimes(1); // Still clears
    expect(mockContext.beginPath).not.toHaveBeenCalled();
    expect(mockContext.arc).not.toHaveBeenCalled();
    expect(mockContext.stroke).not.toHaveBeenCalled();
  });

  test('updates drawing when eventDetails change', () => {
    const { rerender } = render(<RippleCanvas eventDetails={{ magnitude: 1 }} />);
    expect(mockContext.arc).toHaveBeenCalledTimes(1);
    jest.clearAllMocks();

    rerender(<RippleCanvas eventDetails={{ magnitude: 3 }} />);
    expect(mockContext.arc).toHaveBeenCalledTimes(3);
  });
});
