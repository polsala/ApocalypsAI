import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../src/App';

// Mock the SVG component or its rendering if it becomes complex
// For now, we'll assume it renders correctly based on props

describe('App Component', () => {
  test('renders without crashing', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Cosmic Compass/i)).toBeInTheDocument();
  });

  test('updates cosmic dust value on range change', () => {
    render(<App />);
    const slider = screen.getByLabelText(/Cosmic Dust:/i).querySelector('input[type="range"]');
    fireEvent.change(slider, { target: { value: '3' } });
    expect(slider).toHaveValue('3');
  });

  test('updates starlight intensity value on range change', () => {
    render(<App />);
    const slider = screen.getByLabelText(/Starlight Intensity:/i).querySelector('input[type="range"]');
    fireEvent.change(slider, { target: { value: '8' } });
    expect(slider).toHaveValue('8');
  });

  test('generates a path when button is clicked', async () => {
    render(<App />);
    const chartButton = screen.getByRole('button', { name: /Chart Course/i });
    
    // Mock Math.random to ensure deterministic path generation for testing
    // Mock rationale: To ensure tests are deterministic and repeatable, we mock Math.random
    // to return predictable sequences of values. This allows us to assert the exact
    // output of the path generation logic without relying on random chance.
    const mockMath = Object.create(global.Math);
    mockMath.random = jest.fn()
      .mockReturnValueOnce(0.1) // First random for dx
      .mockReturnValueOnce(0.9) // First random for dy
      .mockReturnValueOnce(0.5) // Second random for dx (starlight check)
      .mockReturnValueOnce(0.2) // Second random for dy (starlight check)
      .mockReturnValueOnce(0.3) // Third random for dx
      .mockReturnValueOnce(0.7) // Third random for dy
      .mockReturnValueOnce(0.6) // Fourth random for dx (starlight check)
      .mockReturnValueOnce(0.4) // Fourth random for dy (starlight check)
      // ... continue mocking for all expected calls within the loop
      // For simplicity in this example, we'll mock a few steps.
      // A real-world scenario might need more sophisticated mocking or a different approach
      // if the path generation is too complex to mock deterministically.
      // Let's assume a simplified path generation for this mock.
      .mockReturnValue(0.5); // Default for any other calls
    global.Math = mockMath;

    fireEvent.click(chartButton);

    // Wait for the state update and re-render
    await waitFor(() => {
      const svgElement = screen.getByRole('img', { name: /visualization/i }); // Assuming an aria-label or similar for the SVG
      expect(svgElement).toBeInTheDocument();
      // We can't easily assert the exact polyline points without more complex mocking or DOM inspection.
      // Instead, we check if the polyline element exists and has a stroke.
      const polyline = svgElement.querySelector('polyline');
      expect(polyline).toBeInTheDocument();
      expect(polyline).toHaveAttribute('stroke', '#00ff00');
    });

    // Restore original Math.random
    global.Math = Object.getPrototypeOf(global.Math);
  });

  // Add more tests for edge cases, different input combinations, etc.
});
