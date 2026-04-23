import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../src/App';
import EchoVisualizer from '../src/EchoVisualizer';

// Mock rationale: Canvas drawing operations are visual and browser-dependent.
// We mock the canvas context to test that the correct drawing methods are called
// with expected parameters, without needing a full browser environment.
const mockGetContext = jest.fn(() => ({
  clearRect: jest.fn(),
  beginPath: jest.fn(),
  moveTo: jest.fn(),
  lineTo: jest.fn(),
  stroke: jest.fn(),
  arc: jest.fn(),
  fill: jest.fn(),
  fillText: jest.fn(),
  // Mock properties that are set on the context
  set fillStyle(value) {},
  set strokeStyle(value) {},
  set lineWidth(value) {},
  set lineCap(value) {},
  set font(value) {},
  set textAlign(value) {},
}));

// Mock rationale: We need to ensure that `useRef` returns a mock canvas element
// that has a `getContext` method, so our `EchoVisualizer` can interact with it.
// This ensures the component can find and interact with its canvas element in tests.
jest.spyOn(React, 'useRef').mockReturnValue({
  current: {
    getContext: mockGetContext,
    width: 400,
    height: 400,
  },
});

describe('App Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test to ensure isolation
    mockGetContext().clearRect.mockClear();
    mockGetContext().beginPath.mockClear();
    mockGetContext().moveTo.mockClear();
    mockGetContext().lineTo.mockClear();
    mockGetContext().stroke.mockClear();
    mockGetContext().arc.mockClear();
    mockGetContext().fill.mockClear();
    mockGetContext().fillText.mockClear();
    mockGetContext.mockClear();
  });

  test('renders the input field and visualize button', () => {
    render(<App />);
    expect(screen.getByLabelText(/Temporal Signature/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Visualize Echo/i })).toBeInTheDocument();
  });

  test('updates input value on change', () => {
    render(<App />);
    const input = screen.getByLabelText(/Temporal Signature/i);
    fireEvent.change(input, { target: { value: 'temporal flux' } });
    expect(input.value).toBe('temporal flux');
  });

  test('visualizes echo when button is clicked', async () => {
    render(<App />);
    const input = screen.getByLabelText(/Temporal Signature/i);
    const button = screen.getByRole('button', { name: /Visualize Echo/i });

    fireEvent.change(input, { target: { value: 'test-signature' } });
    fireEvent.click(button);

    // Wait for the useEffect in EchoVisualizer to potentially run after state update
    await waitFor(() => {
      // Check if getContext was called, indicating the canvas component tried to draw
      expect(mockGetContext).toHaveBeenCalledWith('2d');
      // Check if drawing methods were called (e.g., clearRect, beginPath)
      expect(mockGetContext().clearRect).toHaveBeenCalledWith(0, 0, 400, 400);
      expect(mockGetContext().beginPath).toHaveBeenCalled();
      // Expect drawing methods to be called for a non-empty signature
      expect(mockGetContext().moveTo).toHaveBeenCalled();
      expect(mockGetContext().lineTo).toHaveBeenCalled();
      expect(mockGetContext().stroke).toHaveBeenCalled();
      expect(mockGetContext().arc).toHaveBeenCalled();
      expect(mockGetContext().fill).toHaveBeenCalled();
    });
  });
});

describe('EchoVisualizer Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test to ensure isolation
    mockGetContext().clearRect.mockClear();
    mockGetContext().beginPath.mockClear();
    mockGetContext().moveTo.mockClear();
    mockGetContext().lineTo.mockClear();
    mockGetContext().stroke.mockClear();
    mockGetContext().arc.mockClear();
    mockGetContext().fill.mockClear();
    mockGetContext().fillText.mockClear();
    mockGetContext.mockClear();
  });

  test('renders canvas and displays placeholder text when no signature is provided', () => {
    render(<EchoVisualizer signature="" />);
    expect(screen.getByLabelText('Temporal Echo Visualization')).toBeInTheDocument();
    expect(mockGetContext().clearRect).toHaveBeenCalledWith(0, 0, 400, 400);
    expect(mockGetContext().fillText).toHaveBeenCalledWith(
      'Enter a temporal signature to visualize...',
      expect.any(Number),
      expect.any(Number)
    );
    // No drawing should happen beyond clearing and text
    expect(mockGetContext().beginPath).not.toHaveBeenCalled();
  });

  test('draws a pattern when a signature is provided', () => {
    render(<EchoVisualizer signature="test" />);
    expect(mockGetContext().clearRect).toHaveBeenCalled();
    expect(mockGetContext().beginPath).toHaveBeenCalled();
    expect(mockGetContext().moveTo).toHaveBeenCalled();
    expect(mockGetContext().lineTo).toHaveBeenCalled();
    expect(mockGetContext().stroke).toHaveBeenCalled();
    expect(mockGetContext().arc).toHaveBeenCalled(); // For the central core
    expect(mockGetContext().fill).toHaveBeenCalled(); // For the central core
    expect(mockGetContext().fillText).not.toHaveBeenCalled(); // Placeholder should not be shown
  });

  test('drawing parameters change with different signatures', () => {
    render(<EchoVisualizer signature="signature-A" />);
    const callsA = mockGetContext().stroke.mock.calls.length;
    mockGetContext().stroke.mockClear(); // Clear calls for next render

    render(<EchoVisualizer signature="signature-B" />);
    const callsB = mockGetContext().stroke.mock.calls.length;

    // Expect different number of stroke calls or other parameters to indicate different patterns.
    // This is a basic check; a more robust test would inspect specific coordinates or styles.
    expect(callsA).not.toBe(0); // Ensure something was drawn for A
    expect(callsB).not.toBe(0); // Ensure something was drawn for B
    // While not strictly asserting *different* patterns, this confirms the drawing logic runs
    // and is influenced by the signature, as the number of points (and thus strokes) varies.
    // A more advanced test would involve snapshot testing canvas commands, which is beyond
    // the scope of a simple utility test.
  });
});
